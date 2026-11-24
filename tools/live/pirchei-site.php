<?php
/**
 * Plugin Name: Pirchei Shomayim — האתר החדש
 * Description: מגיש את האתר החדש (עברית ואנגלית), מקבל פניות לחוגים והרשמות לעדכונים, שומר אותן בוורדפרס ושולח מייל לצוות המקהלה. כתובות ישנות מופנות לאתר החדש. לכיבוי: למחוק את הקובץ.
 * Version: 1.0
 */

if (!defined('ABSPATH')) {
	exit;
}

const PS_CHOIR_EMAIL = 'mordi.gordon@gmail.com';
const PS_BRANCHES = [
	'ramat-eshkol' => ['he' => 'רמת אשכול · ירושלים', 'en' => 'Ramat Eshkol · Jerusalem'],
	'neve-yaakov'  => ['he' => 'נווה יעקב · ירושלים', 'en' => 'Neve Yaakov · Jerusalem'],
	'ramah-a'      => ['he' => 'רמה א׳ · בית שמש', 'en' => 'Ramah A · Beit Shemesh'],
	'ramah-d'      => ['he' => 'רמה ד׳ · בית שמש', 'en' => 'Ramah D · Beit Shemesh'],
];
const PS_TOPICS = [
	'songs'   => ['he' => 'שירים וקליפים חדשים', 'en' => 'New songs and videos'],
	'classes' => ['he' => 'פתיחת רישום לחוגים', 'en' => 'Class registration opening'],
	'shows'   => ['he' => 'הופעות ומופעים', 'en' => 'Concerts and shows'],
];
define('PS_PAGES', ABSPATH . 'ps/pages/');

/* ------------------------------------------------------------------
 * 1. הדפים החדשים מוגשים מיד, עוד לפני שוורדפרס טוען תוספים ותבנית — מהיר
 * ------------------------------------------------------------------ */
function ps_serve_static() {
	$method = isset($_SERVER['REQUEST_METHOD']) ? $_SERVER['REQUEST_METHOD'] : 'GET';
	if (!in_array($method, ['GET', 'HEAD'], true) || is_admin() || wp_doing_ajax() || (defined('WP_CLI') && WP_CLI)) {
		return;
	}
	foreach (['p', 'page_id', 'preview', 'rest_route', 's', 'feed', 'attachment_id', 'post_type', 'cat', 'author', 'm'] as $k) {
		if (isset($_GET[$k])) {
			return;
		}
	}
	// כתובת אחת לאתר: www מופנה לכתובת בלעדיו, כדי שגוגל לא יראה שני אתרים
	$host = isset($_SERVER['HTTP_HOST']) ? strtolower($_SERVER['HTTP_HOST']) : '';
	if (strpos($host, 'www.') === 0) {
		header('Location: https://' . substr($host, 4) . (isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/'), true, 301);
		exit;
	}
	$path = parse_url(isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/', PHP_URL_PATH);
	$path = $path ? $path : '/';
	$map = [
		'/' => 'he.html', '/en/' => 'en.html',
		'/classes/' => 'classes-he.html', '/en/classes/' => 'classes-en.html',
		'/songs/' => 'songs-he.html', '/en/songs/' => 'songs-en.html',
		'/privacy/' => 'privacy-he.html', '/en/privacy/' => 'privacy-en.html',
	];
	// כתובת בלי לוכסן בסוף — הפניה קבועה לגרסה עם לוכסן
	if (substr($path, -1) !== '/' && isset($map[$path . '/'])) {
		$q = isset($_SERVER['QUERY_STRING']) && $_SERVER['QUERY_STRING'] !== '' ? '?' . $_SERVER['QUERY_STRING'] : '';
		header('Location: ' . $path . '/' . $q, true, 301);
		exit;
	}
	if (!isset($map[$path])) {
		return;
	}
	ps_send_file(PS_PAGES . $map[$path], 200, $method === 'HEAD');
}

function ps_send_file($file, $status = 200, $head_only = false) {
	if (!is_readable($file)) {
		return;
	}
	$etag = '"' . md5_file($file) . '"';
	http_response_code($status);
	header('Content-Type: text/html; charset=UTF-8');
	header('Cache-Control: public, max-age=300');
	header('X-Content-Type-Options: nosniff');
	header('Referrer-Policy: strict-origin-when-cross-origin');
	header('ETag: ' . $etag);
	if ($status === 200 && isset($_SERVER['HTTP_IF_NONE_MATCH']) && trim($_SERVER['HTTP_IF_NONE_MATCH']) === $etag) {
		http_response_code(304);
		exit;
	}
	header('Content-Length: ' . filesize($file));
	if (!$head_only) {
		readfile($file);
	}
	exit;
}
ps_serve_static();

/* ------------------------------------------------------------------
 * 2. כתובות ישנות שגוגל מכיר — הפניה קבועה למקום המתאים באתר החדש
 * ------------------------------------------------------------------ */
add_filter('wp_sitemaps_enabled', '__return_false');

/* האתר ציבורי למנועי חיפוש גם בהגדרות וורדפרס (״קריאה״ ← ״נראות במנועי חיפוש״). לפני ההשקה ההגדרה כובתה */
add_action('init', function () {
	if (get_option('blog_public') !== '1') {
		update_option('blog_public', '1');
	}
});
add_action('template_redirect', function () {
	if (is_robots() || is_favicon() || is_customize_preview()) {
		return;
	}
	$path = rawurldecode((string) parse_url(isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/', PHP_URL_PATH));
	$slug = trim($path, '/');
	$map = [
		'הופעות' => '/#stage', 'הופעות-2' => '/#stage',
		'השירים-שלנו' => '/songs/', 'שירים' => '/songs/',
		'חוגים' => '/classes/', 'צור-קשר' => '/#join',
		'אודות' => '/#about', 'דף-הבית' => '/',
	];
	if (isset($map[$slug])) {
		wp_redirect(home_url($map[$slug]), 301);
		exit;
	}
	if (is_404()) {
		$lang = strpos($path, '/en/') === 0 ? 'en' : 'he';
		nocache_headers();
		ps_send_file(PS_PAGES . '404-' . $lang . '.html', 404);
	}
	// כל שאר התוכן הישן (פוסטים, קבצים מצורפים, ארכיונים, פידים) — לדף הבית החדש
	wp_redirect(home_url('/'), 301);
	exit;
}, 0);

/* ------------------------------------------------------------------
 * 3. פניות והרשמות נשמרות בוורדפרס, בתפריט משלהן
 * ------------------------------------------------------------------ */
add_action('init', function () {
	$common = [
		'public' => false, 'show_ui' => true, 'show_in_menu' => true, 'show_in_rest' => false,
		'supports' => ['title'], 'capability_type' => 'post', 'map_meta_cap' => true,
		'capabilities' => ['create_posts' => 'do_not_allow'],
	];
	register_post_type('ps_inquiry', $common + [
		'menu_icon' => 'dashicons-groups', 'menu_position' => 3,
		'labels' => ['name' => 'פניות לחוגים', 'singular_name' => 'פנייה', 'menu_name' => 'פניות לחוגים', 'all_items' => 'כל הפניות', 'edit_item' => 'פרטי הפנייה', 'search_items' => 'חיפוש פניות', 'not_found' => 'אין עדיין פניות'],
	]);
	register_post_type('ps_subscriber', $common + [
		'menu_icon' => 'dashicons-email-alt', 'menu_position' => 4,
		'labels' => ['name' => 'מנויים לעדכונים', 'singular_name' => 'מנוי', 'menu_name' => 'מנויים לעדכונים', 'all_items' => 'כל המנויים', 'edit_item' => 'פרטי המנוי', 'search_items' => 'חיפוש מנויים', 'not_found' => 'אין עדיין מנויים'],
	]);
});

const PS_INQ_FIELDS = ['branch' => 'חוג', 'parent' => 'שם ההורה', 'phone' => 'טלפון', 'email' => 'מייל', 'child' => 'שם הילד', 'age' => 'גיל', 'cheder' => 'חיידר', 'grade' => 'כיתה', 'notes' => 'הערות', 'topics' => 'עדכונים שביקשו', 'lang' => 'שפת האתר', 'mailed' => 'מייל נשלח לצוות'];
const PS_SUB_FIELDS = ['email' => 'מייל', 'name' => 'שם', 'topics' => 'נושאים', 'source' => 'מקור', 'verified' => 'אושר במייל', 'lang' => 'שפת האתר'];

function ps_meta_value($post_id, $key) {
	$v = get_post_meta($post_id, '_ps_' . $key, true);
	if ($key === 'branch' && isset(PS_BRANCHES[$v])) {
		return PS_BRANCHES[$v]['he'];
	}
	if ($key === 'topics' && is_array($v)) {
		return implode(', ', array_map(function ($t) { return isset(PS_TOPICS[$t]) ? PS_TOPICS[$t]['he'] : $t; }, $v));
	}
	if (in_array($key, ['mailed', 'verified'], true)) {
		return $v ? 'כן' : 'לא';
	}
	if ($key === 'source') {
		return $v === 'class' ? 'טופס החוגים' : 'מועדון העדכונים';
	}
	return (string) $v;
}

add_action('add_meta_boxes', function () {
	foreach (['ps_inquiry' => PS_INQ_FIELDS, 'ps_subscriber' => PS_SUB_FIELDS] as $type => $fields) {
		add_meta_box('ps_details', 'הפרטים', function ($post) use ($fields) {
			echo '<table class="widefat striped" style="direction:rtl"><tbody>';
			foreach ($fields as $key => $label) {
				$val = ps_meta_value($post->ID, $key);
				if ($key === 'email' && $val) {
					$val = '<a href="mailto:' . esc_attr($val) . '">' . esc_html($val) . '</a>';
				} elseif ($key === 'phone' && $val) {
					$val = '<a href="tel:' . esc_attr(preg_replace('/[^\d+]/', '', $val)) . '" dir="ltr">' . esc_html($val) . '</a>';
				} else {
					$val = nl2br(esc_html($val));
				}
				echo '<tr><th style="width:150px">' . esc_html($label) . '</th><td>' . $val . '</td></tr>';
			}
			echo '<tr><th>התקבל</th><td>' . esc_html(get_the_date('j.n.Y H:i', $post)) . '</td></tr>';
			echo '</tbody></table>';
		}, $type, 'normal', 'high');
	}
});

foreach (['ps_inquiry' => ['branch', 'phone', 'email', 'age'], 'ps_subscriber' => ['email', 'topics', 'verified']] as $ps_type => $ps_cols) {
	add_filter("manage_{$ps_type}_posts_columns", function ($cols) use ($ps_cols, $ps_type) {
		$labels = $ps_type === 'ps_inquiry' ? PS_INQ_FIELDS : PS_SUB_FIELDS;
		$out = ['cb' => $cols['cb'], 'title' => 'שם'];
		foreach ($ps_cols as $c) {
			$out['ps_' . $c] = $labels[$c];
		}
		$out['date'] = 'התקבל';
		return $out;
	});
	add_action("manage_{$ps_type}_posts_custom_column", function ($col, $post_id) {
		if (strpos($col, 'ps_') === 0) {
			echo esc_html(ps_meta_value($post_id, substr($col, 3)));
		}
	}, 10, 2);
}

/* ------------------------------------------------------------------
 * 4. נקודות הקבלה: /wp-json/ps/v1/inquiry, ‏/subscribe, ‏/confirm
 * ------------------------------------------------------------------ */
add_action('rest_api_init', function () {
	register_rest_route('ps/v1', '/inquiry', ['methods' => 'POST', 'callback' => 'ps_rest_inquiry', 'permission_callback' => '__return_true']);
	register_rest_route('ps/v1', '/subscribe', ['methods' => 'POST', 'callback' => 'ps_rest_subscribe', 'permission_callback' => '__return_true']);
	register_rest_route('ps/v1', '/confirm', ['methods' => 'GET', 'callback' => 'ps_rest_confirm', 'permission_callback' => '__return_true']);
	// מצב ציבורי לבדיקה מבחוץ: האם האתר פתוח למנועי חיפוש בהגדרות וורדפרס
	register_rest_route('ps/v1', '/status', ['methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => function () {
		return new WP_REST_Response(['search_engines_allowed' => get_option('blog_public') === '1'], 200);
	}]);
});

function ps_fail($code, $status = 400, $errors = []) {
	return new WP_REST_Response(['ok' => false, 'code' => $code, 'errors' => $errors], $status);
}

/** רובוטים מקבלים ״הצלחה״ ריקה, כדי שלא ינסו שוב */
function ps_is_bot($p) {
	return !empty($p['website']) || (isset($p['t']) && (int) $p['t'] < 1500);
}

/** עד 5 שליחות בעשר דקות מאותה כתובת */
function ps_rate_limited($bucket) {
	$ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
	$key = 'ps_rl_' . $bucket . '_' . md5($ip . wp_salt('nonce'));
	$n = (int) get_transient($key);
	if ($n >= 5) {
		return true;
	}
	set_transient($key, $n + 1, 10 * MINUTE_IN_SECONDS);
	return false;
}

function ps_text($v, $max = 100) {
	return mb_substr(sanitize_text_field((string) $v), 0, $max);
}

function ps_topics($v) {
	return is_array($v) ? array_values(array_intersect(array_keys(PS_TOPICS), array_map('strval', $v))) : [];
}

function ps_mail($to, $subject, $lines, $reply_to = '') {
	$headers = ['Content-Type: text/plain; charset=UTF-8'];
	if ($reply_to && is_email($reply_to)) {
		$headers[] = 'Reply-To: ' . $reply_to;
	}
	$from_name = function () { return 'מקהלת פרחי שמיים'; };
	add_filter('wp_mail_from_name', $from_name);
	$ok = wp_mail($to, $subject, implode("\n", $lines), $headers);
	remove_filter('wp_mail_from_name', $from_name);
	return $ok;
}

/* מיילים יוצאים דרך תיבת המייל של המקהלה (SMTP). פרטי הכניסה בקובץ בשרת בלבד:
 * wp-content/ps-mail-config.php שמחזיר ['user' => ..., 'pass' => ...]. בלי הקובץ — שליחה רגילה של השרת */
add_action('phpmailer_init', function ($m) {
	$f = WP_CONTENT_DIR . '/ps-mail-config.php';
	if (!is_readable($f)) {
		return;
	}
	$c = include $f;
	if (!is_array($c) || empty($c['user']) || empty($c['pass'])) {
		return;
	}
	$m->isSMTP();
	$m->Host = isset($c['host']) ? $c['host'] : 'smtp.hostinger.com';
	$m->Port = isset($c['port']) ? (int) $c['port'] : 465;
	$m->SMTPSecure = $m->Port === 465 ? 'ssl' : 'tls';
	$m->SMTPAuth = true;
	$m->Username = $c['user'];
	$m->Password = $c['pass'];
	$m->setFrom($c['user'], 'מקהלת פרחי שמיים', false);
});

function ps_rest_inquiry(WP_REST_Request $req) {
	$p = (array) $req->get_json_params();
	if (ps_is_bot($p)) {
		return new WP_REST_Response(['ok' => true], 200);
	}
	$lang = (isset($p['lang']) && $p['lang'] === 'en') ? 'en' : 'he';
	$d = [
		'branch' => isset($p['branch']) ? (string) $p['branch'] : '',
		'parent' => ps_text(isset($p['parent']) ? $p['parent'] : ''),
		'phone'  => ps_text(isset($p['phone']) ? $p['phone'] : '', 30),
		'email'  => sanitize_email(isset($p['email']) ? $p['email'] : ''),
		'child'  => ps_text(isset($p['child']) ? $p['child'] : ''),
		'age'    => isset($p['age']) ? (int) $p['age'] : 0,
		'cheder' => ps_text(isset($p['cheder']) ? $p['cheder'] : ''),
		'grade'  => ps_text(isset($p['grade']) ? $p['grade'] : '', 20),
		'notes'  => mb_substr(sanitize_textarea_field(isset($p['notes']) ? (string) $p['notes'] : ''), 0, 1000),
		'topics' => ps_topics(isset($p['topics']) ? $p['topics'] : []),
		'lang'   => $lang,
	];
	$err = [];
	if (!isset(PS_BRANCHES[$d['branch']])) { $err['branch'] = 'required'; }
	foreach (['parent', 'child', 'cheder', 'grade'] as $k) {
		if ($d[$k] === '') { $err[$k] = 'required'; }
	}
	if (!preg_match('/^\d{9,12}$/', preg_replace('/[\s\-().+]/', '', $d['phone']))) { $err['phone'] = 'invalid'; }
	if (!is_email($d['email'])) { $err['email'] = 'invalid'; }
	if ($d['age'] < 5 || $d['age'] > 16) { $err['age'] = 'invalid'; }
	if (empty($p['consent'])) { $err['consent'] = 'required'; }
	if ($err) {
		return ps_fail('invalid', 400, $err);
	}
	if ($req->get_param('dry_run')) {
		return new WP_REST_Response(['ok' => true, 'dry_run' => true], 200);
	}
	if (ps_rate_limited('inq')) {
		return ps_fail('too_many', 429);
	}

	$branch_he = PS_BRANCHES[$d['branch']]['he'];
	$id = wp_insert_post([
		'post_type' => 'ps_inquiry', 'post_status' => 'private',
		'post_title' => $d['parent'] . ' · ' . $d['child'] . ' (' . $d['age'] . ') · ' . $branch_he,
	], true);
	if (is_wp_error($id)) {
		return ps_fail('store', 500);
	}
	foreach ($d as $k => $v) {
		update_post_meta($id, '_ps_' . $k, $v);
	}

	// מייל לצוות המקהלה — ״השב״ עונה ישר להורה
	$lines = ['פנייה חדשה מהאתר:', ''];
	foreach (PS_INQ_FIELDS as $k => $label) {
		if (in_array($k, ['mailed', 'lang'], true)) { continue; }
		$v = ps_meta_value($id, $k);
		if ($v !== '') { $lines[] = $label . ': ' . $v; }
	}
	$lines[] = '';
	$lines[] = 'כל הפניות: ' . admin_url('edit.php?post_type=ps_inquiry');
	$mailed = ps_mail(PS_CHOIR_EMAIL, 'פנייה חדשה לחוג ' . $branch_he . ': ' . $d['child'] . ' (' . $d['age'] . ')', $lines, $d['email']);
	update_post_meta($id, '_ps_mailed', $mailed ? 1 : 0);

	// עדכונים שביקשו בטופס (מסלול 3) — נשמרים כמנוי שממתין לאישור
	$confirm_url = '';
	if ($d['topics']) {
		$confirm_url = ps_upsert_subscriber($d['email'], $d['parent'], $d['topics'], 'class', $lang);
	}

	// מייל אישור להורה. בלי טקסט חופשי מהטופס, כדי שאי אפשר לנצל אותו לשליחת ספאם
	$b = PS_BRANCHES[$d['branch']][$lang];
	$home = home_url($lang === 'en' ? '/en/' : '/');
	$mail = $lang === 'en'
		? ['Hello,', '', 'Thank you — we received your inquiry for the ' . $b . ' class.', 'The choir team will get back to you soon to arrange a short audition.']
		: ['שלום,', '', 'תודה! קיבלנו את הפנייה לחוג ' . $b . '.', 'צוות המקהלה יחזור אליכם בימים הקרובים לתיאום מבדק התאמה קצר.'];
	if ($confirm_url) {
		$mail = array_merge($mail, ['', $lang === 'en' ? 'To confirm the updates you asked for:' : 'לאישור העדכונים שביקשתם:', $confirm_url]);
	}
	$mail = array_merge($mail, ['', $lang === 'en' ? 'Questions? Just reply to this email.' : 'שאלות? אפשר פשוט להשיב למייל הזה.', '', $lang === 'en' ? 'Pirchei Shomayim Boys’ Choir' : 'מקהלת פרחי שמיים', $home]);
	ps_mail($d['email'], $lang === 'en' ? 'We received your inquiry · Pirchei Shomayim' : 'קיבלנו את הפנייה · מקהלת פרחי שמיים', $mail, PS_CHOIR_EMAIL);

	return new WP_REST_Response(['ok' => true], 200);
}

/** יוצר או מעדכן מנוי, ומחזיר קישור אישור (אם עוד לא אושר) */
function ps_upsert_subscriber($email, $name, $topics, $source, $lang) {
	$found = get_posts(['post_type' => 'ps_subscriber', 'post_status' => 'private', 'numberposts' => 1, 'fields' => 'ids', 'meta_key' => '_ps_email', 'meta_value' => $email]);
	if ($found) {
		$id = $found[0];
		$old = get_post_meta($id, '_ps_topics', true);
		update_post_meta($id, '_ps_topics', array_values(array_unique(array_merge(is_array($old) ? $old : [], $topics))));
		if ($name && !get_post_meta($id, '_ps_name', true)) {
			update_post_meta($id, '_ps_name', $name);
		}
	} else {
		$id = wp_insert_post(['post_type' => 'ps_subscriber', 'post_status' => 'private', 'post_title' => $name ? $name . ' · ' . $email : $email]);
		if (!$id || is_wp_error($id)) {
			return '';
		}
		foreach (['email' => $email, 'name' => $name, 'topics' => $topics, 'source' => $source, 'lang' => $lang, 'verified' => 0] as $k => $v) {
			update_post_meta($id, '_ps_' . $k, $v);
		}
	}
	if (get_post_meta($id, '_ps_verified', true)) {
		return '';
	}
	$token = get_post_meta($id, '_ps_token', true);
	if (!$token) {
		$token = wp_generate_password(32, false, false);
		update_post_meta($id, '_ps_token', $token);
	}
	return add_query_arg(['id' => $id, 't' => $token], rest_url('ps/v1/confirm'));
}

function ps_rest_subscribe(WP_REST_Request $req) {
	$p = (array) $req->get_json_params();
	if (ps_is_bot($p)) {
		return new WP_REST_Response(['ok' => true], 200);
	}
	$lang = (isset($p['lang']) && $p['lang'] === 'en') ? 'en' : 'he';
	$email = sanitize_email(isset($p['email']) ? $p['email'] : '');
	$name = ps_text(isset($p['name']) ? $p['name'] : '');
	$topics = ps_topics(isset($p['topics']) ? $p['topics'] : []);
	$err = [];
	if (!is_email($email)) { $err['email'] = 'invalid'; }
	if (!$topics) { $err['topics'] = 'required'; }
	if (empty($p['consent'])) { $err['consent'] = 'required'; }
	if ($err) {
		return ps_fail('invalid', 400, $err);
	}
	if ($req->get_param('dry_run')) {
		return new WP_REST_Response(['ok' => true, 'dry_run' => true], 200);
	}
	if (ps_rate_limited('sub')) {
		return ps_fail('too_many', 429);
	}
	$url = ps_upsert_subscriber($email, $name, $topics, 'club', $lang);
	if ($url) {
		$names = implode(', ', array_map(function ($t) use ($lang) { return PS_TOPICS[$t][$lang]; }, $topics));
		$mail = $lang === 'en'
			? ['Hello,', '', 'Thank you for joining the Pirchei Shomayim Choir updates.', 'You chose: ' . $names . '.', '', 'To start receiving updates, please confirm your email:', $url, '', 'Didn’t ask for this? Just ignore this email.']
			: ['שלום,', '', 'תודה שהצטרפתם לעדכונים של מקהלת פרחי שמיים.', 'בחרתם לקבל: ' . $names . '.', '', 'כדי להתחיל לקבל עדכונים, אשרו את הכתובת:', $url, '', 'לא נרשמתם? אפשר פשוט להתעלם מהמייל הזה.'];
		ps_mail($email, $lang === 'en' ? 'Please confirm your updates · Pirchei Shomayim' : 'אישור ההרשמה לעדכונים · מקהלת פרחי שמיים', $mail, PS_CHOIR_EMAIL);
	}
	return new WP_REST_Response(['ok' => true], 200);
}

function ps_rest_confirm(WP_REST_Request $req) {
	$id = (int) $req->get_param('id');
	$token = (string) $req->get_param('t');
	$ok = false;
	if ($id && get_post_type($id) === 'ps_subscriber') {
		$saved = (string) get_post_meta($id, '_ps_token', true);
		if ($saved !== '' && hash_equals($saved, $token)) {
			update_post_meta($id, '_ps_verified', 1);
			update_post_meta($id, '_ps_verified_at', current_time('mysql'));
			$ok = true;
		}
	}
	$lang = $id ? get_post_meta($id, '_ps_lang', true) : 'he';
	$base = home_url($lang === 'en' ? '/en/' : '/');
	wp_redirect($ok ? add_query_arg('subscribed', '1', $base) . '#club' : $base, 302);
	exit;
}
