<?php
/**
 * אזור הניהול של המקהלה: ‎/manage/
 * פניות לחוגים (סטטוס והערה פנימית), מנויים לעדכונים, משתמשים רשומים, ותכנים מאחורי הקלעים.
 * נכנסים בקישור למייל (בלי סיסמה). רק מנהלים — ראו ps_is_manager.
 */
if (!defined('ABSPATH')) {
	exit;
}

const PS_STATUSES = ['new', 'contacted', 'audition', 'accepted', 'declined'];

/* העמוד עצמו */
add_action('template_redirect', function () {
	$path = parse_url(isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/', PHP_URL_PATH);
	if ($path === '/manage') {
		wp_safe_redirect(home_url('/manage/'), 301);
		exit;
	}
	if ($path !== '/manage/') {
		return;
	}
	$file = PS_PAGES . 'manage.html';
	if (!is_readable($file)) {
		return;
	}
	$u = wp_get_current_user();
	$state = !$u->exists() ? 'login' : (ps_is_manager($u) ? 'ok' : 'denied');
	$boot = [
		'state' => $state,
		'rest' => esc_url_raw(rest_url('ps/v1/')),
		'nonce' => $state === 'ok' ? wp_create_nonce('wp_rest') : '',
		'user' => $u->exists() ? ['name' => $u->display_name, 'email' => $u->user_email] : null,
		'notify' => $state === 'ok' ? ps_notify_email() : '',
		'wpadmin' => current_user_can('manage_options') ? admin_url() : '',
	];
	status_header(200);
	nocache_headers();
	do_action('litespeed_control_set_nocache', 'ps manage');
	header('Cache-Control: private, no-store, max-age=0');
	header('Content-Type: text/html; charset=UTF-8');
	header('X-Robots-Tag: noindex, nofollow');
	header('X-Frame-Options: DENY');
	header('Referrer-Policy: same-origin');
	echo str_replace('<!--PS_BOOT-->', '<script>window.PS_MANAGE=' . wp_json_encode($boot) . ';</script>', (string) file_get_contents($file));
	exit;
}, -2);

/* ------------------------------------------------------------------
 * הנתונים — רק למנהלים, עם אימות וורדפרס (עוגייה + nonce)
 * ------------------------------------------------------------------ */
add_action('rest_api_init', function () {
	$can = function () { return ps_is_manager(); };
	register_rest_route('ps/v1', '/admin/data', ['methods' => 'GET', 'callback' => 'ps_admin_data', 'permission_callback' => $can]);
	register_rest_route('ps/v1', '/admin/inquiry/(?P<id>\d+)', ['methods' => 'POST', 'callback' => 'ps_admin_inquiry', 'permission_callback' => $can]);
	register_rest_route('ps/v1', '/admin/subscriber/(?P<id>\d+)', ['methods' => 'POST', 'callback' => 'ps_admin_subscriber', 'permission_callback' => $can]);
	register_rest_route('ps/v1', '/admin/member/(?P<id>\d+)', ['methods' => 'POST', 'callback' => 'ps_admin_member', 'permission_callback' => $can]);
	register_rest_route('ps/v1', '/admin/exclusive', ['methods' => 'POST', 'callback' => 'ps_admin_exclusive', 'permission_callback' => $can]);
	register_rest_route('ps/v1', '/admin/exclusive/(?P<id>\d+)', ['methods' => 'POST', 'callback' => 'ps_admin_exclusive', 'permission_callback' => $can]);
});

function ps_admin_ok($data = []) {
	return ps_private(new WP_REST_Response(['ok' => true] + $data, 200));
}

function ps_is_test_title($t) {
	return strpos((string) $t, '[בדיקה]') === 0;
}

function ps_admin_inquiry_row($p) {
	$m = function ($k) use ($p) { return get_post_meta($p->ID, '_ps_' . $k, true); };
	$topics = $m('topics');
	return [
		'id' => $p->ID, 'date' => get_post_time('c', true, $p), 'test' => ps_is_test_title($p->post_title),
		'branch' => (string) $m('branch'), 'parent' => (string) $m('parent'), 'phone' => (string) $m('phone'), 'email' => (string) $m('email'),
		'child' => (string) $m('child'), 'age' => (int) $m('age'), 'cheder' => (string) $m('cheder'), 'grade' => (string) $m('grade'),
		'notes' => (string) $m('notes'), 'topics' => is_array($topics) ? $topics : [], 'lang' => (string) $m('lang'), 'mailed' => (bool) $m('mailed'),
		'status' => in_array($m('status'), PS_STATUSES, true) ? $m('status') : 'new', 'note' => (string) $m('note'),
	];
}

function ps_admin_data() {
	$inq = get_posts(['post_type' => 'ps_inquiry', 'post_status' => 'private', 'numberposts' => 1000, 'orderby' => 'date', 'order' => 'DESC']);
	$subs = get_posts(['post_type' => 'ps_subscriber', 'post_status' => 'private', 'numberposts' => 3000, 'orderby' => 'date', 'order' => 'DESC']);
	$excl = get_posts(['post_type' => 'ps_exclusive', 'post_status' => ['publish', 'draft'], 'numberposts' => 200, 'orderby' => 'date', 'order' => 'DESC']);
	$users = get_users(['number' => 3000, 'orderby' => 'registered', 'order' => 'DESC']);
	return ps_admin_ok([
		'inquiries' => array_map('ps_admin_inquiry_row', $inq),
		'subscribers' => array_map(function ($p) {
			$m = function ($k) use ($p) { return get_post_meta($p->ID, '_ps_' . $k, true); };
			$topics = $m('topics');
			return ['id' => $p->ID, 'date' => get_post_time('c', true, $p), 'test' => ps_is_test_title($p->post_title), 'email' => (string) $m('email'), 'name' => (string) $m('name'),
				'topics' => is_array($topics) ? $topics : [], 'source' => (string) $m('source'), 'verified' => (bool) $m('verified'), 'lang' => (string) $m('lang')];
		}, $subs),
		'members' => array_map(function ($u) {
			return ['id' => $u->ID, 'name' => $u->display_name, 'email' => $u->user_email, 'joined' => mysql2date('c', $u->user_registered, false),
				'last' => (string) get_user_meta($u->ID, 'ps_last_login', true), 'manager' => ps_is_manager($u), 'wp' => user_can($u, 'edit_posts')];
		}, $users),
		'exclusive' => array_map('ps_exclusive_item', $excl),
		'notify' => ps_notify_email(),
	]);
}

function ps_admin_inquiry(WP_REST_Request $req) {
	$id = (int) $req['id'];
	if (get_post_type($id) !== 'ps_inquiry') {
		return ps_private(ps_fail('not_found', 404));
	}
	$p = (array) $req->get_json_params();
	if (!empty($p['delete'])) {
		wp_trash_post($id);
		return ps_admin_ok();
	}
	if (isset($p['status']) && in_array($p['status'], PS_STATUSES, true)) {
		update_post_meta($id, '_ps_status', $p['status']);
	}
	if (isset($p['note'])) {
		update_post_meta($id, '_ps_note', mb_substr(sanitize_textarea_field((string) $p['note']), 0, 1000));
	}
	return ps_admin_ok(['item' => ps_admin_inquiry_row(get_post($id))]);
}

function ps_admin_subscriber(WP_REST_Request $req) {
	$id = (int) $req['id'];
	if (get_post_type($id) !== 'ps_subscriber') {
		return ps_private(ps_fail('not_found', 404));
	}
	$p = (array) $req->get_json_params();
	if (!empty($p['delete'])) {
		wp_delete_post($id, true); // הסרה מלאה — מי שביקש להסיר את עצמו
	}
	return ps_admin_ok();
}

function ps_admin_member(WP_REST_Request $req) {
	$id = (int) $req['id'];
	$u = get_userdata($id);
	$p = (array) $req->get_json_params();
	// רק משתמשים רגילים שנרשמו באתר. מנהלים ומשתמשי וורדפרס לא נמחקים מכאן
	if (!$u || ps_is_manager($u) || user_can($u, 'edit_posts') || $id === get_current_user_id()) {
		return ps_private(ps_fail('forbidden', 403));
	}
	if (!empty($p['delete'])) {
		require_once ABSPATH . 'wp-admin/includes/user.php';
		wp_delete_user($id);
	}
	return ps_admin_ok();
}

/** מזהה סרטון מתוך קישור (רגיל, קצר, שורטס או הטמעה) או מזהה בלבד */
function ps_video_id($v) {
	$v = trim((string) $v);
	if (preg_match('~^[\w-]{11}$~', $v)) {
		return $v;
	}
	if (preg_match('~(?:v=|youtu\.be/|/shorts/|/embed/|/live/)([\w-]{11})~', $v, $m)) {
		return $m[1];
	}
	return '';
}

function ps_admin_exclusive(WP_REST_Request $req) {
	$id = isset($req['id']) ? (int) $req['id'] : 0;
	if ($id && get_post_type($id) !== 'ps_exclusive') {
		return ps_private(ps_fail('not_found', 404));
	}
	$p = (array) $req->get_json_params();
	if ($id && !empty($p['delete'])) {
		wp_delete_post($id, true);
		return ps_admin_ok();
	}
	$title = ps_text(isset($p['title']) ? $p['title'] : '', 140);
	$video = ps_video_id(isset($p['video']) ? $p['video'] : '');
	$err = [];
	if ($title === '') { $err['title'] = 'required'; }
	if (isset($p['video']) && trim((string) $p['video']) !== '' && $video === '') { $err['video'] = 'invalid'; }
	if ($err) {
		return ps_private(ps_fail('invalid', 400, $err));
	}
	$post = [
		'post_type' => 'ps_exclusive', 'post_title' => $title,
		'post_content' => mb_substr(sanitize_textarea_field(isset($p['text']) ? (string) $p['text'] : ''), 0, 2000),
		'post_status' => (isset($p['status']) && $p['status'] === 'draft') ? 'draft' : 'publish',
	];
	if ($id) {
		$post['ID'] = $id;
		$id = wp_update_post($post, true);
	} else {
		$id = wp_insert_post($post, true);
	}
	if (is_wp_error($id)) {
		return ps_private(ps_fail('store', 500));
	}
	update_post_meta($id, '_ps_video', $video);
	update_post_meta($id, '_ps_vertical', !empty($p['vertical']) || (isset($p['video']) && strpos((string) $p['video'], '/shorts/') !== false) ? 1 : 0);
	update_post_meta($id, '_ps_title_en', ps_text(isset($p['title_en']) ? $p['title_en'] : '', 140));
	update_post_meta($id, '_ps_text_en', mb_substr(sanitize_textarea_field(isset($p['text_en']) ? (string) $p['text_en'] : ''), 0, 2000));
	return ps_admin_ok(['item' => ps_exclusive_item(get_post($id))]);
}
