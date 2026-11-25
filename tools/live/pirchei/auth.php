<?php
/**
 * כניסה לאתר בלי סיסמה: מזינים מייל ומקבלים קישור כניסה (תקף לחצי שעה, לכניסה אחת).
 * אותו קישור משמש גם להרשמה — אם אין עדיין משתמש עם המייל, הוא נוצר כמשתמש רגיל (subscriber).
 * מנהלים: מנהל בוורדפרס, או מייל שמופיע ב-'admins' בקובץ ההגדרות שבשרת (wp-content/ps-site-config.php).
 *
 * העמודים של האתר הם קבצים קבועים, ולכן האתר שואל את /ps/v1/me אם יש מחובר.
 * הבדיקה נעשית מול עוגיית הכניסה של וורדפרס, ורק לבקשות שמגיעות מהאתר עצמו.
 */
if (!defined('ABSPATH')) {
	exit;
}

const PS_HINT_COOKIE = 'ps_m'; // רמז לדפדפן שיש מחובר (בלי שום מידע) — כדי לא לפנות לשרת סתם בכל כניסה לאתר

function ps_admin_emails() {
	$c = ps_site_config();
	$list = isset($c['admins']) ? (array) $c['admins'] : [];
	return array_values(array_filter(array_map(function ($e) { return strtolower(trim((string) $e)); }, $list)));
}

function ps_is_manager($user = null) {
	$u = $user instanceof WP_User ? $user : ($user ? get_userdata((int) $user) : wp_get_current_user());
	if (!$u || !$u->exists()) {
		return false;
	}
	return user_can($u, 'manage_options') || in_array(strtolower($u->user_email), ps_admin_emails(), true);
}

/** האם המייל שייך למנהל (לפי קובץ ההגדרות, או משתמש וורדפרס עם הרשאות ניהול) */
function ps_email_is_manager($email) {
	if (in_array(strtolower($email), ps_admin_emails(), true)) {
		return true;
	}
	$u = get_user_by('email', $email);
	return $u ? ps_is_manager($u) : false;
}

/** בקשה שמגיעה מהאתר עצמו (ולא מאתר זר שמנסה לקרוא את פרטי המחובר) */
function ps_same_origin() {
	$host = strtolower((string) parse_url(home_url(), PHP_URL_HOST));
	$origin = isset($_SERVER['HTTP_ORIGIN']) ? (string) $_SERVER['HTTP_ORIGIN'] : '';
	if ($origin !== '') {
		return strtolower((string) parse_url($origin, PHP_URL_HOST)) === $host;
	}
	$site = isset($_SERVER['HTTP_SEC_FETCH_SITE']) ? (string) $_SERVER['HTTP_SEC_FETCH_SITE'] : '';
	return $site === '' || $site === 'same-origin' || $site === 'none';
}

/** מי מחובר לפי עוגיית הכניסה (0 = אף אחד) */
function ps_cookie_user() {
	if (!ps_same_origin() || empty($_COOKIE[LOGGED_IN_COOKIE])) {
		return 0;
	}
	$uid = wp_validate_auth_cookie((string) $_COOKIE[LOGGED_IN_COOKIE], 'logged_in');
	return $uid ? (int) $uid : 0;
}

/** תשובה אישית — אסור לשמור אותה במטמון של השרת או של הדפדפן */
function ps_private($r) {
	$r->header('Cache-Control', 'no-store, private, max-age=0');
	$r->header('X-LiteSpeed-Cache-Control', 'no-cache');
	$r->header('Vary', 'Cookie');
	do_action('litespeed_control_set_nocache', 'ps private');
	return $r;
}

function ps_me_payload($uid) {
	$u = get_userdata($uid);
	$manager = ps_is_manager($u);
	return [
		'logged' => true,
		'name' => $u->display_name,
		'email' => $u->user_email,
		'manager' => $manager,
		'manage' => $manager ? '/manage/' : '',
		'test' => $manager ? '/?ps_admin=1#join' : '',
	];
}

/** המשתמש של המייל הזה — ואם אין, יוצרים אותו */
function ps_member_for_email($email, $name = '') {
	$u = get_user_by('email', $email);
	if ($u) {
		return (int) $u->ID;
	}
	if ($name === '') {
		$s = get_posts(['post_type' => 'ps_subscriber', 'post_status' => 'private', 'numberposts' => 1, 'fields' => 'ids', 'meta_key' => '_ps_email', 'meta_value' => $email]);
		if ($s) {
			$name = (string) get_post_meta($s[0], '_ps_name', true);
		}
	}
	$base = sanitize_user(strstr($email, '@', true), true);
	$base = $base !== '' ? substr($base, 0, 40) : 'member';
	$login = $base;
	for ($i = 2; username_exists($login); $i++) {
		$login = $base . '-' . $i;
	}
	$uid = wp_insert_user([
		'user_login' => $login, 'user_email' => $email, 'user_pass' => wp_generate_password(32, true, true),
		'display_name' => $name !== '' ? $name : $base, 'first_name' => $name, 'role' => 'subscriber',
	]);
	if (is_wp_error($uid)) {
		return 0;
	}
	update_user_meta($uid, 'ps_member', current_time('mysql'));
	update_user_meta($uid, 'show_admin_bar_front', 'false');
	return (int) $uid;
}

function ps_login_session($uid) {
	wp_set_auth_cookie($uid, true, is_ssl());
	setcookie(PS_HINT_COOKIE, '1', ['expires' => time() + 14 * DAY_IN_SECONDS, 'path' => '/', 'secure' => is_ssl(), 'httponly' => false, 'samesite' => 'Lax']);
	update_user_meta($uid, 'ps_last_login', current_time('mysql'));
}

/** מי שהוכיח שהמייל שלו (בקישור כניסה) — גם ההרשמה שלו לעדכונים מאושרת */
function ps_verify_subscriber_email($email) {
	$s = get_posts(['post_type' => 'ps_subscriber', 'post_status' => 'private', 'numberposts' => 1, 'fields' => 'ids', 'meta_key' => '_ps_email', 'meta_value' => $email]);
	if ($s && !get_post_meta($s[0], '_ps_verified', true)) {
		update_post_meta($s[0], '_ps_verified', 1);
		update_post_meta($s[0], '_ps_verified_at', current_time('mysql'));
	}
}

/* ------------------------------------------------------------------
 * תכנים מאחורי הקלעים — רק למשתמשים רשומים. מנוהלים מאזור הניהול.
 * ------------------------------------------------------------------ */
add_action('init', function () {
	register_post_type('ps_exclusive', [
		'public' => false, 'show_ui' => false, 'show_in_rest' => false, 'supports' => ['title', 'editor'],
		'labels' => ['name' => 'מאחורי הקלעים', 'singular_name' => 'תוכן מאחורי הקלעים'],
	]);
});

function ps_exclusive_item($p) {
	$m = function ($k) use ($p) { return (string) get_post_meta($p->ID, '_ps_' . $k, true); };
	return [
		'id' => $p->ID, 'title' => $p->post_title, 'text' => $p->post_content, 'title_en' => $m('title_en'), 'text_en' => $m('text_en'),
		'video' => $m('video'), 'vertical' => (bool) $m('vertical'), 'date' => get_post_time('c', true, $p), 'status' => $p->post_status,
	];
}

/* ------------------------------------------------------------------
 * נקודות הכניסה
 * ------------------------------------------------------------------ */
add_action('rest_api_init', function () {
	foreach ([['/login', 'POST', 'ps_rest_login'], ['/verify', 'POST', 'ps_rest_verify'], ['/me', 'GET', 'ps_rest_me'], ['/logout', 'POST', 'ps_rest_logout'], ['/members', 'GET', 'ps_rest_members']] as $r) {
		register_rest_route('ps/v1', $r[0], ['methods' => $r[1], 'callback' => $r[2], 'permission_callback' => '__return_true']);
	}
});

function ps_login_mail($email, $url, $lang, $to) {
	$he = $lang !== 'en';
	$manage = $to === 'manage';
	return ps_send_mail($email, $he ? 'קישור הכניסה שלכם · מקהלת פרחי שמיים' : 'Your sign-in link · Pirchei Shomayim', $lang, [
		'title' => $manage ? ($he ? 'כניסה לאזור הניהול' : 'Sign in to the admin area') : ($he ? 'כניסה לאתר המקהלה' : 'Sign in to the choir site'),
		'paras' => $he
			? ['לחצו על הכפתור כדי להיכנס — בלי סיסמה.', $manage ? 'אחרי הכניסה תגיעו ישר לאזור הניהול.' : 'אחרי הכניסה תוכלו לצפות בתכנים מאחורי הקלעים שיש רק באתר.']
			: ['Click the button to sign in — no password needed.', $manage ? 'You’ll go straight to the admin area.' : 'Once signed in you can watch the behind-the-scenes content that’s only on the site.'],
		'button' => [$manage ? ($he ? 'כניסה לאזור הניהול' : 'Open the admin area') : ($he ? 'כניסה לאתר' : 'Sign in'), $url],
		'note' => $he ? 'הקישור תקף לחצי שעה ולכניסה אחת. לא ביקשתם להיכנס? אפשר פשוט להתעלם מהמייל הזה.' : 'The link works once, for 30 minutes. Didn’t ask to sign in? Just ignore this email.',
	]);
}

function ps_rest_login(WP_REST_Request $req) {
	$p = (array) $req->get_json_params();
	if (ps_is_bot($p)) {
		return new WP_REST_Response(['ok' => true], 200);
	}
	$lang = (isset($p['lang']) && $p['lang'] === 'en') ? 'en' : 'he';
	$email = strtolower(sanitize_email(isset($p['email']) ? $p['email'] : ''));
	if (!is_email($email)) {
		return ps_fail('invalid', 400, ['email' => 'invalid']);
	}
	$to = isset($p['to']) && in_array($p['to'], ['manage', 'behind'], true) ? $p['to'] : '';
	// מנהל שנכנס — הקישור מוביל תמיד לאזור הניהול (ומשם יש קישור לאתר)
	if ($to === '' && ps_email_is_manager($email)) {
		$to = 'manage';
	}
	if ($req->get_param('dry_run')) {
		return new WP_REST_Response(['ok' => true, 'dry_run' => true], 200);
	}
	if (ps_rate_limited('login') || ps_rate_hit('login_' . md5($email), 4, 30 * MINUTE_IN_SECONDS)) {
		return ps_fail('too_many', 429);
	}
	$token = wp_generate_password(40, false, false);
	set_transient('ps_ml_' . hash('sha256', $token), ['email' => $email, 'to' => $to, 'name' => ps_text(isset($p['name']) ? $p['name'] : '')], 30 * MINUTE_IN_SECONDS);
	$url = home_url($lang === 'en' ? '/en/' : '/') . '?login=' . $token . ($to ? '&to=' . $to : '');
	ps_login_mail($email, $url, $lang, $to);
	return new WP_REST_Response(['ok' => true], 200);
}

function ps_rest_verify(WP_REST_Request $req) {
	if (!ps_same_origin()) {
		return ps_private(ps_fail('origin', 403));
	}
	$p = (array) $req->get_json_params();
	$token = isset($p['token']) ? preg_replace('/[^A-Za-z0-9]/', '', (string) $p['token']) : '';
	$key = 'ps_ml_' . hash('sha256', $token);
	$d = strlen($token) >= 30 ? get_transient($key) : false;
	if (!is_array($d) || empty($d['email'])) {
		return ps_private(ps_fail('expired', 410));
	}
	delete_transient($key);
	$uid = ps_member_for_email($d['email'], isset($d['name']) ? $d['name'] : '');
	if (!$uid) {
		return ps_private(ps_fail('store', 500));
	}
	ps_login_session($uid);
	ps_verify_subscriber_email($d['email']);
	$out = ps_me_payload($uid);
	$out['ok'] = true;
	$out['to'] = $d['to'];
	return ps_private(new WP_REST_Response($out, 200));
}

function ps_rest_me() {
	$uid = ps_cookie_user();
	return ps_private(new WP_REST_Response($uid ? ps_me_payload($uid) : ['logged' => false], 200));
}

function ps_rest_logout() {
	if (!ps_same_origin()) {
		return ps_private(ps_fail('origin', 403));
	}
	$uid = ps_cookie_user();
	if ($uid) {
		$t = wp_get_session_token();
		if ($t) {
			WP_Session_Tokens::get_instance($uid)->destroy($t);
		}
	}
	wp_clear_auth_cookie();
	setcookie(PS_HINT_COOKIE, '', ['expires' => time() - HOUR_IN_SECONDS, 'path' => '/', 'secure' => is_ssl(), 'samesite' => 'Lax']);
	return ps_private(new WP_REST_Response(['ok' => true], 200));
}

function ps_rest_members() {
	$uid = ps_cookie_user();
	$posts = get_posts(['post_type' => 'ps_exclusive', 'post_status' => 'publish', 'numberposts' => 60, 'orderby' => 'date', 'order' => 'DESC']);
	if (!$uid) {
		return ps_private(new WP_REST_Response(['ok' => true, 'member' => false, 'count' => count($posts)], 200));
	}
	return ps_private(new WP_REST_Response(['ok' => true, 'member' => true, 'items' => array_map('ps_exclusive_item', $posts)], 200));
}

/* משתמשים רגילים לא צריכים את מסכי הניהול של וורדפרס — חוזרים לאתר */
add_action('admin_init', function () {
	if (wp_doing_ajax() || !is_user_logged_in() || current_user_can('edit_posts')) {
		return;
	}
	wp_safe_redirect(ps_is_manager() ? home_url('/manage/') : home_url('/'));
	exit;
});
add_filter('show_admin_bar', function ($show) {
	return current_user_can('edit_posts') ? $show : false;
});
