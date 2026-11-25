<?php
/**
 * דיוור לרשימות התפוצה: שיר חדש, חוג חדש, הופעה ועדכון כללי — במייל מעוצב.
 * נשלח רק למי שאישר את הכתובת במייל ובחר בנושא, בקבוצות קטנות (כך גם שרת המייל לא חוסם),
 * עם קישור הסרה בכל מייל. כל דיוור נשמר בהיסטוריה.
 */
if (!defined('ABSPATH')) {
	exit;
}

const PS_MAIL_TPLS = [
	'songs'   => ['topic' => 'songs', 'label' => 'שיר חדש'],
	'classes' => ['topic' => 'classes', 'label' => 'חוג חדש'],
	'shows'   => ['topic' => 'shows', 'label' => 'הופעה'],
	'general' => ['topic' => '', 'label' => 'עדכון כללי'],
];
const PS_MAIL_BATCH = 8; // כמה מיילים בכל סבב

add_action('init', function () {
	register_post_type('ps_mailing', ['public' => false, 'show_ui' => false, 'show_in_rest' => false, 'supports' => ['title'], 'labels' => ['name' => 'דיוורים']]);
});

add_action('rest_api_init', function () {
	$can = function () { return ps_is_manager(); };
	register_rest_route('ps/v1', '/admin/mailing/preview', ['methods' => 'POST', 'callback' => 'ps_mailing_preview', 'permission_callback' => $can]);
	register_rest_route('ps/v1', '/admin/mailing/test', ['methods' => 'POST', 'callback' => 'ps_mailing_test', 'permission_callback' => $can]);
	register_rest_route('ps/v1', '/admin/mailing/send', ['methods' => 'POST', 'callback' => 'ps_mailing_start', 'permission_callback' => $can]);
	register_rest_route('ps/v1', '/admin/mailing/(?P<id>\d+)/batch', ['methods' => 'POST', 'callback' => 'ps_mailing_batch', 'permission_callback' => $can]);
	register_rest_route('ps/v1', '/admin/upload', ['methods' => 'POST', 'callback' => 'ps_admin_upload', 'permission_callback' => $can]);
	register_rest_route('ps/v1', '/admin/video-info', ['methods' => 'POST', 'callback' => 'ps_admin_video_info', 'permission_callback' => $can]);
	// הסרה מהרשימה: POST בלבד (לחיצה אחת בג׳ימייל, או אישור בחלון באתר). GET מעביר לאתר לאישור
	register_rest_route('ps/v1', '/unsubscribe', ['methods' => ['GET', 'POST'], 'callback' => 'ps_rest_unsubscribe', 'permission_callback' => '__return_true']);
});

/* ------------------------------------------------------------------
 * בניית המייל
 * ------------------------------------------------------------------ */
function ps_mailing_fields($p) {
	$f = isset($p['fields']) && is_array($p['fields']) ? $p['fields'] : [];
	$t = function ($k, $max = 140) use ($f) { return isset($f[$k]) ? mb_substr(sanitize_text_field((string) $f[$k]), 0, $max) : ''; };
	$url = function ($k) use ($f) { $u = isset($f[$k]) ? esc_url_raw(trim((string) $f[$k]), ['http', 'https']) : ''; return $u; };
	return [
		'title' => $t('title'), 'subject' => $t('subject', 160), 'place' => $t('place'), 'ages' => $t('ages', 40), 'times' => $t('times'),
		'date' => preg_match('/^\d{4}-\d{2}-\d{2}$/', isset($f['date']) ? (string) $f['date'] : '') ? $f['date'] : '',
		'time' => preg_match('/^\d{2}:\d{2}$/', isset($f['time']) ? (string) $f['time'] : '') ? $f['time'] : '',
		'credits' => $t('credits', 200), 'text' => isset($f['text']) ? mb_substr(sanitize_textarea_field((string) $f['text']), 0, 3000) : '',
		'video' => ps_video_id(isset($f['video']) ? $f['video'] : ''), 'link' => $url('link'), 'button' => $t('button', 40),
		'file' => $url('file'), 'file_kind' => (isset($f['file_kind']) && in_array($f['file_kind'], ['image', 'pdf'], true)) ? $f['file_kind'] : '',
	];
}

function ps_mailing_errors($tpl, $f) {
	$need = ['songs' => ['title', 'video'], 'classes' => ['title', 'place', 'ages'], 'shows' => ['title', 'date', 'place'], 'general' => ['subject', 'text']];
	$err = [];
	foreach ($need[$tpl] as $k) {
		if ($f[$k] === '') { $err[$k] = 'required'; }
	}
	return $err;
}

function ps_he_date($ymd) {
	$ts = strtotime($ymd . ' 12:00:00');
	if (!$ts) {
		return '';
	}
	$days = ['ראשון', 'שני', 'שלישי', 'רביעי', 'חמישי', 'שישי', 'שבת'];
	return 'יום ' . $days[(int) gmdate('w', $ts)] . ', ' . gmdate('j.n.Y', $ts);
}

/** תמונה גדולה של סרטון — באיכות הגבוהה שיש */
function ps_video_thumb($id) {
	$key = 'ps_thumb_' . $id;
	$cached = get_transient($key);
	if ($cached) {
		return $cached;
	}
	$hi = 'https://i.ytimg.com/vi/' . $id . '/maxresdefault.jpg';
	$r = wp_remote_head($hi, ['timeout' => 5]);
	$url = (!is_wp_error($r) && wp_remote_retrieve_response_code($r) === 200) ? $hi : 'https://i.ytimg.com/vi/' . $id . '/hqdefault.jpg';
	set_transient($key, $url, DAY_IN_SECONDS);
	return $url;
}

/** נושא ותוכן המייל. $sub = המנוי (לפנייה אישית ולקישור ההסרה) */
function ps_mailing_build($tpl, $f, $sub = null) {
	$site = home_url('/');
	$o = ['paras' => []];
	$name = $sub && !empty($sub['name']) ? ps_mail_safe($sub['name']) : '';
	$o['paras'][] = $name ? 'שלום ' . $name . ',' : 'שלום,';
	if ($tpl === 'songs') {
		$listen = home_url('/?song=' . rawurlencode($f['title'])) . '#play=' . $f['video'];
		$subject = 'שיר חדש מהמקהלה: ' . $f['title'];
		$o['kicker'] = 'שיר חדש · מקהלת פרחי שמיים';
		$o['title'] = $f['title'];
		$o['image'] = [ps_video_thumb($f['video']), $listen, $f['title']];
		$o['paras'][] = 'יצא שיר חדש של מקהלת פרחי שמיים — ואתם שומעים אותו ראשונים.';
		if ($f['text'] !== '') { $o['paras'][] = $f['text']; }
		if ($f['credits'] !== '') { $o['rows'] = [['קרדיטים', $f['credits']]]; }
		$o['button'] = ['להאזנה לשיר באתר', $listen];
	} elseif ($tpl === 'classes') {
		$subject = 'חוג חדש: ' . $f['title'] . ' · ' . $f['place'];
		$o['kicker'] = 'חוג חדש · מקהלת פרחי שמיים';
		$o['title'] = $f['title'];
		$o['paras'][] = 'נפתח חוג מקהלה חדש — ויש מקום להצטרף.';
		if ($f['text'] !== '') { $o['paras'][] = $f['text']; }
		$o['rows'] = array_values(array_filter([['מקום', $f['place']], ['גילאים', $f['ages']], $f['times'] !== '' ? ['ימים ושעות', $f['times']] : null]));
		$o['button'] = [$f['button'] !== '' ? $f['button'] : 'לפרטים ולהשארת פרטים', $f['link'] !== '' ? $f['link'] : $site . '#join'];
	} elseif ($tpl === 'shows') {
		$when = ps_he_date($f['date']);
		$subject = 'הופעה: ' . $f['title'] . ' · ' . gmdate('j.n', strtotime($f['date'] . ' 12:00:00'));
		$o['kicker'] = 'הופעה · מקהלת פרחי שמיים';
		$o['title'] = $f['title'];
		$o['paras'][] = 'מקהלת פרחי שמיים עולה לבמה — ונשמח לראות אתכם שם.';
		if ($f['text'] !== '') { $o['paras'][] = $f['text']; }
		$o['rows'] = array_values(array_filter([['תאריך', $when], $f['time'] !== '' ? ['שעה', $f['time']] : null, ['מקום', $f['place']]]));
		$o['button'] = [$f['button'] !== '' ? $f['button'] : ($f['link'] !== '' ? 'לפרטים ולהרשמה' : 'לאתר המקהלה'), $f['link'] !== '' ? $f['link'] : $site . '#stage'];
	} else {
		$subject = $f['subject'];
		$o['kicker'] = 'עדכון מהמקהלה';
		$o['title'] = $f['title'] !== '' ? $f['title'] : $f['subject'];
		foreach (preg_split('/\n\s*\n/', $f['text']) as $para) {
			if (trim($para) !== '') { $o['paras'][] = trim($para); }
		}
		if ($f['link'] !== '') { $o['button'] = [$f['button'] !== '' ? $f['button'] : 'לפרטים', $f['link']]; }
	}
	// מודעה או מסמך מצורפים
	if ($f['file'] !== '' && $f['file_kind'] === 'image' && empty($o['image'])) {
		$o['image'] = [$f['file'], $f['link'] !== '' ? $f['link'] : $f['file'], $o['title']];
	} elseif ($f['file'] !== '' && $f['file_kind'] === 'pdf') {
		$o['link'] = ['למודעה המלאה (PDF)', $f['file']];
	}
	$topic = PS_MAIL_TPLS[$tpl]['topic'];
	$why = $topic ? 'קיבלתם את המייל כי נרשמתם לעדכונים על ' . PS_TOPICS[$topic]['he'] . '.' : 'קיבלתם את המייל כי נרשמתם לעדכונים מהמקהלה.';
	$o['unsub'] = [$why, 'להסרה מהרשימה', $sub ? ps_unsub_page_url($sub['id'], $sub['token']) : home_url('/')];
	return [$subject, $o];
}

function ps_unsub_page_url($id, $token) {
	return home_url('/?unsub=' . (int) $id . '.' . $token);
}

/** מקבלי הדיוור: אישרו את הכתובת, בחרו בנושא, ולא פניות בדיקה */
function ps_mailing_recipients($tpl) {
	$topic = PS_MAIL_TPLS[$tpl]['topic'];
	$ids = [];
	foreach (get_posts(['post_type' => 'ps_subscriber', 'post_status' => 'private', 'numberposts' => 5000, 'fields' => 'ids', 'meta_key' => '_ps_verified', 'meta_value' => 1]) as $id) {
		if (ps_is_test_title(get_the_title($id))) {
			continue;
		}
		$topics = get_post_meta($id, '_ps_topics', true);
		if ($topic === '' || (is_array($topics) && in_array($topic, $topics, true))) {
			$ids[] = $id;
		}
	}
	return $ids;
}

function ps_mailing_sub($id) {
	$token = (string) get_post_meta($id, '_ps_token', true);
	if ($token === '') {
		$token = wp_generate_password(32, false, false);
		update_post_meta($id, '_ps_token', $token);
	}
	return ['id' => $id, 'email' => (string) get_post_meta($id, '_ps_email', true), 'name' => (string) get_post_meta($id, '_ps_name', true), 'token' => $token];
}

function ps_mailing_input(WP_REST_Request $req) {
	$p = (array) $req->get_json_params();
	$tpl = isset($p['tpl']) && isset(PS_MAIL_TPLS[$p['tpl']]) ? $p['tpl'] : '';
	return [$tpl, $tpl ? ps_mailing_fields($p) : []];
}

/* ------------------------------------------------------------------
 * תצוגה מקדימה, בדיקה ושליחה
 * ------------------------------------------------------------------ */
function ps_mailing_preview(WP_REST_Request $req) {
	list($tpl, $f) = ps_mailing_input($req);
	if (!$tpl) {
		return ps_private(ps_fail('invalid', 400));
	}
	$u = wp_get_current_user();
	list($subject, $o) = ps_mailing_build($tpl, $f, ['id' => 0, 'email' => $u->user_email, 'name' => $u->display_name, 'token' => 'preview']);
	return ps_admin_ok(['subject' => $subject, 'html' => ps_mail_html('he', $o), 'count' => count(ps_mailing_recipients($tpl)), 'errors' => (object) ps_mailing_errors($tpl, $f)]);
}

function ps_mailing_test(WP_REST_Request $req) {
	list($tpl, $f) = ps_mailing_input($req);
	if (!$tpl || ($err = ps_mailing_errors($tpl, $f))) {
		return ps_private(ps_fail('invalid', 400, $tpl ? $err : []));
	}
	$u = wp_get_current_user();
	list($subject, $o) = ps_mailing_build($tpl, $f, ['id' => 0, 'email' => $u->user_email, 'name' => $u->display_name, 'token' => 'test']);
	$ok = ps_send_mail($u->user_email, '[בדיקה] ' . $subject, 'he', $o, PS_PUBLIC_EMAIL);
	return $ok ? ps_admin_ok(['to' => $u->user_email]) : ps_private(ps_fail('mail', 500));
}

function ps_mailing_start(WP_REST_Request $req) {
	list($tpl, $f) = ps_mailing_input($req);
	if (!$tpl || ($err = ps_mailing_errors($tpl, $f))) {
		return ps_private(ps_fail('invalid', 400, $tpl ? $err : []));
	}
	$ids = ps_mailing_recipients($tpl);
	if (!$ids) {
		return ps_private(ps_fail('no_recipients', 400));
	}
	list($subject) = ps_mailing_build($tpl, $f);
	$id = wp_insert_post(['post_type' => 'ps_mailing', 'post_status' => 'private', 'post_title' => $subject], true);
	if (is_wp_error($id)) {
		return ps_private(ps_fail('store', 500));
	}
	foreach (['tpl' => $tpl, 'fields' => $f, 'recipients' => $ids, 'pos' => 0, 'ok' => 0, 'fail' => 0, 'status' => 'sending', 'by' => wp_get_current_user()->display_name] as $k => $v) {
		update_post_meta($id, '_ps_' . $k, $v);
	}
	return ps_admin_ok(['mailing' => ps_mailing_row(get_post($id))]);
}

function ps_mailing_batch(WP_REST_Request $req) {
	$id = (int) $req['id'];
	if (get_post_type($id) !== 'ps_mailing') {
		return ps_private(ps_fail('not_found', 404));
	}
	// שליחה אחת בכל פעם לכל דיוור (אם נפתחו שני חלונות)
	$lock = 'ps_mailing_lock_' . $id;
	if (get_transient($lock)) {
		return ps_admin_ok(['mailing' => ps_mailing_row(get_post($id)), 'busy' => true]);
	}
	set_transient($lock, 1, 60);
	@set_time_limit(90);
	$tpl = get_post_meta($id, '_ps_tpl', true);
	$f = (array) get_post_meta($id, '_ps_fields', true);
	$ids = (array) get_post_meta($id, '_ps_recipients', true);
	$pos = (int) get_post_meta($id, '_ps_pos', true);
	$ok = (int) get_post_meta($id, '_ps_ok', true);
	$fail = (int) get_post_meta($id, '_ps_fail', true);
	$streak = 0;
	$end = min(count($ids), $pos + PS_MAIL_BATCH);
	for (; $pos < $end; $pos++) {
		$sid = (int) $ids[$pos];
		if (get_post_type($sid) !== 'ps_subscriber') {
			continue; // הוסר בינתיים מהרשימה
		}
		$sub = ps_mailing_sub($sid);
		list($subject, $o) = ps_mailing_build($tpl, $f, $sub);
		$api = rest_url('ps/v1/unsubscribe?id=' . $sid . '&t=' . $sub['token']);
		$sent = is_email($sub['email']) && ps_send_mail($sub['email'], $subject, 'he', $o, PS_PUBLIC_EMAIL, [
			'List-Unsubscribe: <' . $api . '>',
			'List-Unsubscribe-Post: List-Unsubscribe=One-Click',
		]);
		if ($sent) { $ok++; $streak = 0; } else { $fail++; $streak++; }
		if ($streak >= 3) { $pos++; break; } // שרת המייל עוצר (למשל מגבלה יומית) — עוצרים ומחכים
	}
	$status = $pos >= count($ids) ? 'done' : ($streak >= 3 ? 'paused' : 'sending');
	foreach (['pos' => $pos, 'ok' => $ok, 'fail' => $fail, 'status' => $status] as $k => $v) {
		update_post_meta($id, '_ps_' . $k, $v);
	}
	if ($status === 'done') {
		update_post_meta($id, '_ps_done_at', current_time('mysql'));
	}
	delete_transient($lock);
	return ps_admin_ok(['mailing' => ps_mailing_row(get_post($id))]);
}

function ps_mailing_row($p) {
	$m = function ($k) use ($p) { return get_post_meta($p->ID, '_ps_' . $k, true); };
	return [
		'id' => $p->ID, 'subject' => $p->post_title, 'tpl' => (string) $m('tpl'), 'date' => get_post_time('c', true, $p),
		'total' => count((array) $m('recipients')), 'pos' => (int) $m('pos'), 'ok' => (int) $m('ok'), 'fail' => (int) $m('fail'),
		'status' => (string) $m('status'), 'by' => (string) $m('by'),
	];
}

function ps_mailing_list() {
	return array_map('ps_mailing_row', get_posts(['post_type' => 'ps_mailing', 'post_status' => 'private', 'numberposts' => 100, 'orderby' => 'date', 'order' => 'DESC']));
}

/* ------------------------------------------------------------------
 * שיר חדש: מדביקים קישור — שם השיר והתמונה נשלפים לבד (דרך הממשק הרשמי והפתוח של שירות הווידאו)
 * ------------------------------------------------------------------ */
/** שם נקי מתוך כותרת הסרטון: בלי שם המקהלה, בלי סוגריים ובלי האנגלית */
function ps_clean_video_title($t) {
	$t = html_entity_decode((string) $t, ENT_QUOTES, 'UTF-8');
	$t = preg_replace('/[\(\[][^\)\]]*[\)\]]/u', ' ', $t);
	$t = preg_replace('/(מקהלת\s+)?פרחי\s+שמי?ים/u', ' | ', $t);
	foreach (preg_split('/\s+-\s+|[|\/,&]|\s{2,}/u', $t) as $part) {
		if (!preg_match('/\p{Hebrew}/u', $part)) {
			continue;
		}
		$part = preg_replace('/[A-Za-z][A-Za-z0-9\'’.]*/u', '', $part);
		$part = preg_replace(['/\s+/u', '/^[\s\-–—:,.]+|[\s\-–—:,.]+$/u'], [' ', ''], $part); // לא trim — הוא חותך בתים של אותיות עבריות
		if (mb_strlen($part) >= 2) {
			return $part;
		}
	}
	return trim($t, " |");
}

function ps_admin_video_info(WP_REST_Request $req) {
	$p = (array) $req->get_json_params();
	$id = ps_video_id(isset($p['url']) ? $p['url'] : '');
	if (!$id) {
		return ps_private(ps_fail('invalid', 400));
	}
	$r = wp_remote_get('https://www.youtube.com/oembed?format=json&url=' . rawurlencode('https://www.youtube.com/watch?v=' . $id), ['timeout' => 8]);
	$j = (is_wp_error($r) || wp_remote_retrieve_response_code($r) !== 200) ? null : json_decode(wp_remote_retrieve_body($r), true);
	if (!is_array($j) || empty($j['title'])) {
		return ps_private(ps_fail('not_found', 404));
	}
	return ps_admin_ok([
		'id' => $id, 'title' => ps_clean_video_title($j['title']), 'raw' => (string) $j['title'], 'thumb' => ps_video_thumb($id),
		'vertical' => !empty($j['width']) && !empty($j['height']) && (int) $j['height'] > (int) $j['width'],
	]);
}

/* ------------------------------------------------------------------
 * העלאת מודעה (תמונה) או מסמך PDF לדיוור
 * ------------------------------------------------------------------ */
function ps_admin_upload(WP_REST_Request $req) {
	$p = (array) $req->get_json_params();
	$data = isset($p['data']) ? base64_decode(preg_replace('/^data:[^,]*,/', '', (string) $p['data']), true) : false;
	if ($data === false || strlen($data) < 8) {
		return ps_private(ps_fail('invalid', 400));
	}
	if (strlen($data) > 6 * 1024 * 1024) {
		return ps_private(ps_fail('too_big', 413));
	}
	$kinds = ["%PDF-" => ['pdf', 'pdf'], "\x89PNG" => ['png', 'image'], "\xFF\xD8\xFF" => ['jpg', 'image']];
	$ext = ''; $kind = '';
	foreach ($kinds as $magic => $k) {
		if (strncmp($data, $magic, strlen($magic)) === 0) { list($ext, $kind) = $k; break; }
	}
	if (!$ext) {
		return ps_private(ps_fail('type', 415));
	}
	$base = sanitize_file_name(pathinfo(isset($p['name']) ? (string) $p['name'] : 'file', PATHINFO_FILENAME));
	$base = $base !== '' ? mb_substr($base, 0, 60) : 'file';
	$up = wp_upload_bits('pirchei-' . $base . '-' . wp_generate_password(6, false, false) . '.' . $ext, null, $data);
	if (!empty($up['error'])) {
		return ps_private(ps_fail('store', 500));
	}
	return ps_admin_ok(['url' => $up['url'], 'kind' => $kind]);
}

/* ------------------------------------------------------------------
 * הסרה מרשימת התפוצה
 * ------------------------------------------------------------------ */
function ps_rest_unsubscribe(WP_REST_Request $req) {
	$p = (array) $req->get_json_params();
	$id = (int) (isset($p['id']) ? $p['id'] : $req->get_param('id'));
	$t = (string) (isset($p['t']) ? $p['t'] : $req->get_param('t'));
	if ($req->get_method() === 'GET') {
		// קישור שנפתח בדפדפן — לא מסירים מיד (סורקי מיילים פותחים קישורים); מבקשים אישור באתר
		wp_redirect(ps_unsub_page_url($id, preg_replace('/[^A-Za-z0-9]/', '', $t)), 302);
		exit;
	}
	$ok = false;
	if ($id && get_post_type($id) === 'ps_subscriber') {
		$saved = (string) get_post_meta($id, '_ps_token', true);
		if ($saved !== '' && hash_equals($saved, $t)) {
			wp_delete_post($id, true);
			$ok = true;
		}
	}
	return ps_private(new WP_REST_Response(['ok' => $ok], $ok ? 200 : 404));
}
