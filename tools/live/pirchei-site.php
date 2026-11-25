<?php
/**
 * Plugin Name: Pirchei Shomayim — האתר החדש
 * Description: מגיש את האתר החדש (עברית ואנגלית), מקבל פניות לחוגים והרשמות לעדכונים, שומר אותן בוורדפרס ושולח מייל לצוות המקהלה. כתובות ישנות מופנות לאתר החדש. לכיבוי: למחוק את הקובץ.
 * Version: 1.0
 */

if (!defined('ABSPATH')) {
	exit;
}

const PS_CHOIR_EMAIL = 'mordi.gordon@gmail.com'; // לכאן מגיעות ההודעות על פניות חדשות (לא מוצג לציבור)
const PS_PUBLIC_EMAIL = 'info@xn--cebeaqd7a2ak.com'; // הכתובת שההורים רואים ועונים אליה
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
	$map = ps_page_map();
	// כתובת בלי לוכסן בסוף — הפניה קבועה לגרסה עם לוכסן
	if (substr($path, -1) !== '/' && isset($map[$path . '/'])) {
		$q = isset($_SERVER['QUERY_STRING']) && $_SERVER['QUERY_STRING'] !== '' ? '?' . $_SERVER['QUERY_STRING'] : '';
		header('Location: ' . $path . '/' . $q, true, 301);
		exit;
	}
	// גרסת Markdown של עמוד (לסוכני בינה מלאכותית): ‎/index.md, ‏/classes/index.md וכו׳
	if (substr($path, -8) === 'index.md' && isset($map[substr($path, 0, -8)])) {
		ps_send_file(PS_PAGES . ps_md_name($map[substr($path, 0, -8)]), 200, $method === 'HEAD', 'text/markdown; charset=UTF-8');
	}
	if (!isset($map[$path])) {
		return;
	}
	// מצב בדיקה למנהלים — וורדפרס צריך להיטען כדי לדעת מי מחובר (סעיף 5 למטה)
	if (isset($_GET['ps_admin'])) {
		return;
	}
	// סוכן שמבקש Markdown מקבל את גרסת ה־Markdown של העמוד, באותה כתובת
	$accept = isset($_SERVER['HTTP_ACCEPT']) ? strtolower((string) $_SERVER['HTTP_ACCEPT']) : '';
	if (strpos($accept, 'text/markdown') !== false && is_readable(PS_PAGES . ps_md_name($map[$path]))) {
		header('Cache-Control: private, no-store'); // לא נשמר במטמון — כדי שדפדפנים תמיד יקבלו את העמוד הרגיל
		header('Vary: Accept');
		ps_send_file(PS_PAGES . ps_md_name($map[$path]), 200, $method === 'HEAD', 'text/markdown; charset=UTF-8', false);
	}
	// קישורים למשאבים לסוכנים: הסיכום לבינה מלאכותית וגרסת ה־Markdown של העמוד
	header('Link: </llms.txt>; rel="describedby"; type="text/plain", <' . $path . 'index.md>; rel="alternate"; type="text/markdown"');
	header('Vary: Accept');
	ps_send_file(PS_PAGES . $map[$path], 200, $method === 'HEAD');
}

function ps_md_name($html_name) {
	return preg_replace('/\.html$/', '.md', $html_name);
}

function ps_page_map() {
	return [
		'/' => 'he.html', '/en/' => 'en.html',
		'/classes/' => 'classes-he.html', '/en/classes/' => 'classes-en.html',
		'/songs/' => 'songs-he.html', '/en/songs/' => 'songs-en.html',
		'/privacy/' => 'privacy-he.html', '/en/privacy/' => 'privacy-en.html',
		'/about/' => 'about-he.html', '/en/about/' => 'about-en.html',
		'/contact/' => 'contact-he.html', '/en/contact/' => 'contact-en.html',
	];
}

/** הגדרות שנשמרות רק בשרת (לא במאגר הקוד): wp-content/ps-site-config.php שמחזיר ['notify' => מייל] */
function ps_site_config() {
	static $c = null;
	if ($c === null) {
		$f = WP_CONTENT_DIR . '/ps-site-config.php';
		$c = is_readable($f) ? (array) include $f : [];
	}
	return $c;
}

/** לאן נשלחת ההתראה על פנייה חדשה */
function ps_notify_email() {
	$c = ps_site_config();
	return (!empty($c['notify']) && is_email($c['notify'])) ? $c['notify'] : PS_CHOIR_EMAIL;
}

function ps_send_file($file, $status = 200, $head_only = false, $type = 'text/html; charset=UTF-8', $cache = true) {
	if (!is_readable($file)) {
		return;
	}
	$etag = '"' . md5_file($file) . '"';
	http_response_code($status);
	header('Content-Type: ' . $type);
	if ($cache) {
		header('Cache-Control: public, max-age=300');
	}
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

// מכאן — רק כשוורדפרס ממשיך לטעון (טפסים, כניסה, אזור הניהול). הדפים הקבועים כבר הוגשו למעלה
foreach (['mail', 'auth', 'manage', 'mailing', 'agents'] as $ps_mod) {
	require_once __DIR__ . '/pirchei/' . $ps_mod . '.php';
}

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
		'חוגים' => '/classes/', 'צור-קשר' => '/contact/',
		'אודות' => '/about/', 'דף-הבית' => '/',
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
		return $v === 'class' ? 'טופס החוגים' : 'הרשמה לעדכונים';
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

/** מונה פעולות: true אם עברו את המכסה */
function ps_rate_hit($key, $max, $ttl) {
	$key = 'ps_rl_' . md5($key . wp_salt('nonce'));
	$n = (int) get_transient($key);
	if ($n >= $max) {
		return true;
	}
	set_transient($key, $n + 1, $ttl);
	return false;
}

/** עד 5 שליחות בעשר דקות מאותה כתובת */
function ps_rate_limited($bucket) {
	$ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
	return ps_rate_hit($bucket . '_' . $ip, 5, 10 * MINUTE_IN_SECONDS);
}

/** טקסט מהטופס שנכנס למייל להורה: קצר, ובלי שום דבר שנראה כמו קישור או כתובת */
function ps_mail_safe($s, $max = 40) {
	$s = trim((string) $s);
	if ($s === '' || preg_match('~https?:|www\.|\.[a-z]{2,}\b|@|[<>{}]~i', $s)) {
		return '';
	}
	return mb_substr($s, 0, $max);
}

function ps_text($v, $max = 100) {
	return mb_substr(sanitize_text_field((string) $v), 0, $max);
}

function ps_topics($v) {
	return is_array($v) ? array_values(array_intersect(array_keys(PS_TOPICS), array_map('strval', $v))) : [];
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
	if ($d['parent'] === '') { $err['parent'] = 'required'; } // שם הילד, החיידר והכיתה — רשות
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
	$test = !empty($p['test']) ? '[בדיקה] ' : '';
	$id = wp_insert_post([
		'post_type' => 'ps_inquiry', 'post_status' => 'private',
		'post_title' => $test . $d['parent'] . ' · ' . ($d['child'] !== '' ? $d['child'] : 'בן') . ' (' . $d['age'] . ') · ' . $branch_he,
	], true);
	if (is_wp_error($id)) {
		return ps_fail('store', 500);
	}
	foreach ($d as $k => $v) {
		update_post_meta($id, '_ps_' . $k, $v);
	}

	// מייל לצוות המקהלה — ״השב״ עונה ישר להורה
	$kid = $d['child'] !== '' ? $d['child'] : 'בן';
	$rows = [['חוג', $branch_he], ['הורה', $d['parent']], ['טלפון', $d['phone'], 'tel:' . preg_replace('/[^\d+]/', '', $d['phone'])], ['מייל', $d['email'], 'mailto:' . $d['email']],
		['ילד', $d['child'] !== '' ? $d['child'] . ', בן ' . $d['age'] : 'בן ' . $d['age']]];
	$school = trim($d['cheder'] . ($d['grade'] !== '' ? ' · כיתה ' . $d['grade'] : ''), ' ·');
	if ($school !== '') { $rows[] = ['תלמוד תורה', $school]; }
	if ($d['notes'] !== '') { $rows[] = ['הערות', $d['notes']]; }
	if ($d['topics']) { $rows[] = ['עדכונים שביקשו', ps_meta_value($id, 'topics')]; }
	if ($lang === 'en') { $rows[] = ['שפת האתר', 'אנגלית']; }
	$mailed = ps_send_mail(ps_notify_email(), $test . 'פנייה חדשה לחוג ' . $branch_he . ': ' . $kid . ' (' . $d['age'] . ')', 'he', [
		'kicker' => 'פנייה חדשה מהאתר' . ($test ? ' · בדיקה' : ''),
		'title' => $kid . ' (' . $d['age'] . ') · ' . $branch_he,
		'paras' => ['״השב״ במייל הזה עונה ישר להורה.'],
		'rows' => $rows,
		'button' => ['לכל הפניות באזור הניהול', home_url('/manage/')],
	], $d['email']);
	update_post_meta($id, '_ps_mailed', $mailed ? 1 : 0);

	// עדכונים שביקשו בטופס (מסלול 3) — נשמרים כמנוי שממתין לאישור
	$confirm_url = '';
	if ($d['topics']) {
		$confirm_url = ps_upsert_subscriber($d['email'], $d['parent'], $d['topics'], 'class', $lang, $test);
	}

	// מייל אישור אישי להורה, עם הפרטים שהשאיר. שמות שנראים כמו קישור או כתובת לא נכנסים למייל —
	// כדי שאי אפשר לנצל את הטופס לשליחת ספאם לאחרים (ויש גם הגבלה של 5 שליחות בעשר דקות)
	$he = $lang !== 'en';
	$b = PS_BRANCHES[$d['branch']][$lang];
	$parent = ps_mail_safe($d['parent']);
	$child = ps_mail_safe($d['child']);
	$cheder = ps_mail_safe($d['cheder']);
	$grade = ps_mail_safe($d['grade'], 12);
	$phone = mb_substr(preg_replace('/[^\d\-+ ]/', '', $d['phone']), 0, 20);
	$rows = $he
		? array_values(array_filter([['חוג', $b], $child ? ['הילד', $child . ', בן ' . $d['age']] : ['גיל', $d['age']], $cheder ? ['תלמוד תורה', $cheder . ($grade ? ' · כיתה ' . $grade : '')] : null, ['טלפון לחזרה', $phone], ['מייל', $d['email']]]))
		: array_values(array_filter([['Class', $b], $child ? ['Child', $child . ', age ' . $d['age']] : ['Age', $d['age']], $cheder ? ['Cheder', $cheder . ($grade ? ' · grade ' . $grade : '')] : null, ['Phone', $phone], ['Email', $d['email']]]));
	if ($d['topics']) {
		$rows[] = [$he ? 'עדכונים שביקשתם' : 'Updates you asked for', implode(', ', array_map(function ($t) use ($lang) { return PS_TOPICS[$t][$lang]; }, $d['topics']))];
	}
	$o = [
		'kicker' => $he ? 'מקהלת פרחי שמיים · ' . $b : 'Pirchei Shomayim · ' . $b,
		'title' => $child ? ($he ? 'הפרטים של ' . $child . ' אצלנו' : 'We have ' . $child . '’s details') : ($he ? 'קיבלנו את הפנייה לחוג ' . $b : 'We received your inquiry for ' . $b),
		'paras' => $he
			? [$parent ? 'שלום ' . $parent . ',' : 'שלום,', 'תודה שפניתם אלינו! קיבלנו את הפנייה לחוג ' . $b . '.', 'צוות המקהלה יחזור אליכם בטלפון בימים הקרובים, כדי לתאם מבדק התאמה קצר ונעים.', 'אלה הפרטים שהשארתם:']
			: [$parent ? 'Hello ' . $parent . ',' : 'Hello,', 'Thank you for reaching out! We received your inquiry for the ' . $b . ' class.', 'The choir team will call you in the coming days to arrange a short, friendly audition.', 'These are the details you left:'],
		'rows' => $rows,
		'note' => $he ? 'טעות בפרטים או שאלה? השיבו למייל הזה ונחזור אליכם.' : 'A mistake or a question? Reply to this email and we’ll get back to you.',
	];
	if ($confirm_url) {
		$o['note'] = ($he ? 'ביקשתם גם עדכונים במייל — הכפתור למעלה מאשר אותם. ' : 'You also asked for email updates — the button above confirms them. ') . $o['note'];
		$o['button'] = [$he ? 'אישור העדכונים' : 'Confirm my updates', $confirm_url];
		$o['link'] = [$he ? 'ובינתיים — לשירים של המקהלה' : 'Meanwhile — listen to the choir', home_url($he ? '/songs/' : '/en/songs/')];
	} else {
		$o['button'] = [$he ? 'ובינתיים — לשירים של המקהלה' : 'Meanwhile — listen to the choir', home_url($he ? '/songs/' : '/en/songs/')];
	}
	$subject = $he ? 'קיבלנו את הפנייה' . ($child ? ' של ' . $child : '') . ' לחוג ' . $b : 'We received your inquiry' . ($child ? ' for ' . $child : '') . ' · Pirchei Shomayim';
	ps_send_mail($d['email'], $test . $subject, $lang, $o, PS_PUBLIC_EMAIL);

	return new WP_REST_Response(['ok' => true], 200);
}

/** יוצר או מעדכן מנוי, ומחזיר קישור אישור (אם עוד לא אושר) */
function ps_upsert_subscriber($email, $name, $topics, $source, $lang, $test = '') {
	$found = get_posts(['post_type' => 'ps_subscriber', 'post_status' => 'private', 'numberposts' => 1, 'fields' => 'ids', 'meta_key' => '_ps_email', 'meta_value' => $email]);
	if ($found) {
		$id = $found[0];
		$old = get_post_meta($id, '_ps_topics', true);
		update_post_meta($id, '_ps_topics', array_values(array_unique(array_merge(is_array($old) ? $old : [], $topics))));
		if ($name && !get_post_meta($id, '_ps_name', true)) {
			update_post_meta($id, '_ps_name', $name);
		}
	} else {
		$id = wp_insert_post(['post_type' => 'ps_subscriber', 'post_status' => 'private', 'post_title' => $test . ($name ? $name . ' · ' . $email : $email)]);
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
	return add_query_arg(['id' => $id, 't' => $token], home_url('/confirm/'));
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
	$test = !empty($p['test']) ? '[בדיקה] ' : '';
	$url = ps_upsert_subscriber($email, $name, $topics, 'club', $lang, $test);
	if ($url) {
		$he = $lang !== 'en';
		$names = implode(', ', array_map(function ($t) use ($lang) { return PS_TOPICS[$t][$lang]; }, $topics));
		ps_send_mail($email, $test . ($he ? 'אישור ההרשמה לעדכונים · מקהלת פרחי שמיים' : 'Please confirm your updates · Pirchei Shomayim'), $lang, [
			'title' => $he ? 'עוד לחיצה אחת ואתם רשומים' : 'One more click and you’re in',
			'paras' => $he
				? ['תודה שנרשמתם לעדכונים של מקהלת פרחי שמיים.', 'כדי להתחיל לקבל עדכונים, אשרו את הכתובת. אחרי האישור תיכנסו גם לתכנים מאחורי הקלעים שיש רק באתר.']
				: ['Thank you for signing up for Pirchei Shomayim Choir updates.', 'Please confirm your email to start receiving them. Once confirmed you’ll also be signed in to the behind-the-scenes content that’s only on the site.'],
			'rows' => [[$he ? 'בחרתם לקבל' : 'You chose', $names]],
			'button' => [$he ? 'אישור ההרשמה' : 'Confirm my email', $url],
			'note' => $he ? 'לא נרשמתם? אפשר פשוט להתעלם מהמייל הזה.' : 'Didn’t sign up? Just ignore this email.',
		], PS_PUBLIC_EMAIL);
	}
	return new WP_REST_Response(['ok' => true], 200);
}

/** אישור ההרשמה לעדכונים מהקישור שבמייל. באישור הראשון — גם נכנסים לאתר (המייל הוכח) */
function ps_do_confirm($id, $token) {
	$ok = false;
	if ($id && get_post_type($id) === 'ps_subscriber') {
		$saved = (string) get_post_meta($id, '_ps_token', true);
		if ($saved !== '' && hash_equals($saved, (string) $token)) {
			$ok = true;
			if (!get_post_meta($id, '_ps_verified', true)) {
				update_post_meta($id, '_ps_verified', 1);
				update_post_meta($id, '_ps_verified_at', current_time('mysql'));
				$uid = ps_member_for_email((string) get_post_meta($id, '_ps_email', true), (string) get_post_meta($id, '_ps_name', true));
				if ($uid && !user_can($uid, 'edit_posts')) {
					ps_login_session($uid);
				}
			}
		}
	}
	$lang = $id ? get_post_meta($id, '_ps_lang', true) : 'he';
	$base = home_url($lang === 'en' ? '/en/' : '/');
	nocache_headers();
	wp_redirect($ok ? add_query_arg('subscribed', '1', $base) . '#club' : $base, 302);
	exit;
}

// קישורים ישנים שכבר נשלחו (‎/wp-json/ps/v1/confirm)
function ps_rest_confirm(WP_REST_Request $req) {
	ps_do_confirm((int) $req->get_param('id'), (string) $req->get_param('t'));
}

// הכתובת החדשה והנקייה: ‎/confirm/?id=…&t=…
add_action('template_redirect', function () {
	if (parse_url(isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/', PHP_URL_PATH) === '/confirm/') {
		ps_do_confirm(isset($_GET['id']) ? (int) $_GET['id'] : 0, isset($_GET['t']) ? (string) wp_unslash($_GET['t']) : '');
	}
}, -2);

/* ------------------------------------------------------------------
 * 5. מצב בדיקה למנהלים: ‎/?ps_admin=1 — מנהל מחובר רואה כפתור ״מילוי אוטומטי לבדיקה״.
 *    השליחה אמיתית (נשמרת ונשלחת במייל), ומסומנת [בדיקה] כדי שיהיה קל למחוק.
 * ------------------------------------------------------------------ */
add_action('template_redirect', function () {
	if (!isset($_GET['ps_admin'])) {
		return;
	}
	$path = parse_url(isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/', PHP_URL_PATH);
	$path = $path ? $path : '/';
	$map = ps_page_map();
	if (!isset($map[$path]) || !is_readable(PS_PAGES . $map[$path])) {
		return;
	}
	if (!ps_is_manager()) {
		wp_safe_redirect(home_url('/manage/'));
		exit;
	}
	$u = wp_get_current_user();
	$cfg = ['email' => $u->user_email, 'name' => $u->display_name, 'notify' => ps_notify_email(), 'lang' => strpos($path, '/en/') === 0 ? 'en' : 'he'];
	$inject = '<script>window.PS_ADMIN=' . wp_json_encode($cfg) . ';</script><script src="/ps/assets/admin-test.js?v=2" defer></script>';
	$html = str_replace('</body>', $inject . '</body>', (string) file_get_contents(PS_PAGES . $map[$path]));
	nocache_headers();
	header('Cache-Control: private, no-store, max-age=0');
	header('Content-Type: text/html; charset=UTF-8');
	header('X-Robots-Tag: noindex, nofollow');
	echo $html;
	exit;
}, -1);

// קישור למצב הבדיקה בסרגל העליון של וורדפרס ובמסכי הפניות והמנויים
add_action('admin_bar_menu', function ($bar) {
	if (!ps_is_manager()) {
		return;
	}
	$bar->add_node(['id' => 'ps-manage', 'title' => 'אזור הניהול של המקהלה', 'href' => home_url('/manage/')]);
	$bar->add_node(['id' => 'ps-test', 'title' => 'בדיקת הטפסים באתר', 'href' => home_url('/?ps_admin=1#join'), 'meta' => ['target' => '_blank']]);
}, 90);
add_action('admin_notices', function () {
	$screen = function_exists('get_current_screen') ? get_current_screen() : null;
	if (!$screen || !in_array($screen->post_type, ['ps_inquiry', 'ps_subscriber'], true) || !current_user_can('edit_posts')) {
		return;
	}
	echo '<div class="notice notice-info"><p><b>אזור הניהול הנוח:</b> <a href="' . esc_url(home_url('/manage/')) . '">' . esc_html(home_url('/manage/')) . '</a> — פניות עם סטטוסים, מנויים, משתמשים ותכנים מאחורי הקלעים.</p><p><b>בדיקת הטפסים:</b> <a href="' . esc_url(home_url('/?ps_admin=1#join')) . '" target="_blank">פתיחת האתר במצב בדיקה</a> · <a href="' . esc_url(home_url('/en/?ps_admin=1#join')) . '" target="_blank">English</a> — שם מופיע כפתור ״מילוי אוטומטי לבדיקה״. פניות בדיקה מסומנות [בדיקה], ואפשר להעביר אותן לפח. התראות על פניות נשלחות אל: <b>' . esc_html(ps_notify_email()) . '</b></p></div>';
});
