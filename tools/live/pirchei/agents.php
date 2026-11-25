<?php
/**
 * שרת MCP של האתר — לקריאה בלבד: ‎/mcp
 * דרכו כלי בינה מלאכותית (ChatGPT, Claude ועוד) שואלים על המקהלה, על החוגים, על השירים ועל שאלות נפוצות.
 * המידע הוא אותו מידע שמופיע באתר (נבנה יחד עם הדפים: ps/pages/agent-data.json). אין כאן שליחת טפסים.
 * פרוטוקול: JSON-RPC 2.0 על HTTP (Streamable HTTP, בלי זרם אירועים).
 */
if (!defined('ABSPATH')) {
	exit;
}

const PS_MCP_VERSIONS = ['2025-06-18', '2025-03-26', '2024-11-05'];

add_action('template_redirect', function () {
	$path = parse_url(isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '/', PHP_URL_PATH);
	if ($path === '/mcp' || $path === '/mcp/') {
		ps_mcp_handle();
		exit;
	}
}, -3);

function ps_mcp_data($lang) {
	static $all = null;
	if ($all === null) {
		$f = PS_PAGES . 'agent-data.json';
		$all = is_readable($f) ? (array) json_decode((string) file_get_contents($f), true) : [];
	}
	$lang = $lang === 'en' ? 'en' : 'he';
	return isset($all[$lang]) ? $all[$lang] : [];
}

function ps_mcp_tools() {
	$f = PS_PAGES . 'mcp-tools.json';
	return is_readable($f) ? (array) json_decode((string) file_get_contents($f), true) : [];
}

function ps_mcp_send($status, $body = null) {
	status_header($status);
	if ($body !== null) {
		echo wp_json_encode($body, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
	}
}

function ps_mcp_error($id, $code, $message) {
	return ['jsonrpc' => '2.0', 'id' => $id, 'error' => ['code' => $code, 'message' => $message]];
}

function ps_mcp_handle() {
	nocache_headers();
	header('Content-Type: application/json; charset=UTF-8');
	header('Access-Control-Allow-Origin: *'); // מידע ציבורי בלבד
	header('Access-Control-Allow-Methods: POST, GET, OPTIONS');
	header('Access-Control-Allow-Headers: Content-Type, Accept, Mcp-Session-Id, Mcp-Protocol-Version');
	header('X-Robots-Tag: noindex');
	do_action('litespeed_control_set_nocache', 'ps mcp');
	$method = isset($_SERVER['REQUEST_METHOD']) ? $_SERVER['REQUEST_METHOD'] : 'GET';
	if ($method === 'OPTIONS') {
		ps_mcp_send(204);
		return;
	}
	if ($method !== 'POST') {
		// אין זרם אירועים מהשרת. GET מחזיר תיאור קצר, לפי המפרט: 405
		header('Allow: POST, OPTIONS');
		ps_mcp_send(405, ['error' => 'Use POST with JSON-RPC 2.0. Server card: ' . home_url('/.well-known/mcp/server-card.json')]);
		return;
	}
	$ip = isset($_SERVER['REMOTE_ADDR']) ? $_SERVER['REMOTE_ADDR'] : '';
	if (ps_rate_hit('mcp_' . $ip, 300, 10 * MINUTE_IN_SECONDS)) {
		ps_mcp_send(429, ps_mcp_error(null, -32000, 'Too many requests'));
		return;
	}
	$raw = (string) file_get_contents('php://input');
	if (strlen($raw) > 65536) {
		ps_mcp_send(413, ps_mcp_error(null, -32600, 'Request too large'));
		return;
	}
	$msg = json_decode($raw, true);
	if (!is_array($msg)) {
		ps_mcp_send(400, ps_mcp_error(null, -32700, 'Parse error'));
		return;
	}
	$batch = isset($msg[0]);
	$out = [];
	foreach ($batch ? $msg : [$msg] as $m) {
		$r = ps_mcp_dispatch(is_array($m) ? $m : []);
		if ($r !== null) {
			$out[] = $r;
		}
	}
	if (!$out) {
		ps_mcp_send(202); // רק הודעות (notifications) — אין תשובה
		return;
	}
	ps_mcp_send(200, $batch ? $out : $out[0]);
}

function ps_mcp_dispatch($m) {
	$id = array_key_exists('id', $m) ? $m['id'] : null;
	$method = isset($m['method']) ? (string) $m['method'] : '';
	$params = isset($m['params']) && is_array($m['params']) ? $m['params'] : [];
	if ($id === null && $method !== '') {
		return null; // הודעה, למשל notifications/initialized
	}
	if (!isset($m['jsonrpc']) || $m['jsonrpc'] !== '2.0' || $method === '') {
		return ps_mcp_error($id, -32600, 'Invalid request');
	}
	switch ($method) {
		case 'initialize':
			$want = isset($params['protocolVersion']) ? (string) $params['protocolVersion'] : '';
			return ['jsonrpc' => '2.0', 'id' => $id, 'result' => [
				'protocolVersion' => in_array($want, PS_MCP_VERSIONS, true) ? $want : PS_MCP_VERSIONS[0],
				'capabilities' => ['tools' => ['listChanged' => false]],
				'serverInfo' => ['name' => 'pirchei-shomayim', 'title' => 'Pirchei Shomayim Boys’ Choir', 'version' => '1.0.0'],
				'instructions' => 'Read-only information about the Pirchei Shomayim boys’ choir (Jerusalem & Beit Shemesh). Answers in Hebrew by default; pass lang=en for English. To join a class, send the parent to the "join" link returned by list_classes.',
			]];
		case 'ping':
			return ['jsonrpc' => '2.0', 'id' => $id, 'result' => new stdClass()];
		case 'tools/list':
			return ['jsonrpc' => '2.0', 'id' => $id, 'result' => ['tools' => ps_mcp_tools()]];
		case 'tools/call':
			$name = isset($params['name']) ? (string) $params['name'] : '';
			$args = isset($params['arguments']) && is_array($params['arguments']) ? $params['arguments'] : [];
			$data = ps_mcp_call($name, $args);
			if ($data === null) {
				return ps_mcp_error($id, -32602, 'Unknown tool: ' . $name);
			}
			return ['jsonrpc' => '2.0', 'id' => $id, 'result' => [
				'content' => [['type' => 'text', 'text' => wp_json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT)]],
				'structuredContent' => ['result' => $data],
				'isError' => false,
			]];
		default:
			return ps_mcp_error($id, -32601, 'Method not found');
	}
}

function ps_mcp_call($name, $args) {
	$lang = isset($args['lang']) && $args['lang'] === 'en' ? 'en' : 'he';
	$d = ps_mcp_data($lang);
	$has = function ($hay, $needle) { return $needle === '' || mb_stripos((string) $hay, $needle) !== false; };
	switch ($name) {
		case 'get_choir_info':
			return isset($d['choir']) ? $d['choir'] : [];
		case 'list_classes':
			$city = isset($args['city']) ? trim((string) $args['city']) : '';
			$aliases = ['jerusalem' => 'ירושלים', 'beit shemesh' => 'בית שמש', 'ירושלים' => 'Jerusalem', 'בית שמש' => 'Beit Shemesh'];
			$alt = isset($aliases[mb_strtolower($city)]) ? $aliases[mb_strtolower($city)] : $city;
			$list = array_values(array_filter(isset($d['classes']) ? $d['classes'] : [], function ($c) use ($city, $alt, $has) { return $city === '' || $has($c['city'], $city) || $has($c['city'], $alt); }));
			return ['classes' => $list, 'how_to_join' => isset($d['how_to_join']) ? $d['how_to_join'] : []];
		case 'search_songs':
			$q = isset($args['query']) ? trim((string) $args['query']) : '';
			$limit = isset($args['limit']) ? max(1, min(60, (int) $args['limit'])) : 20;
			$list = array_values(array_filter(isset($d['songs']) ? $d['songs'] : [], function ($s) use ($q, $has) { return $has($s['title'], $q) || $has($s['category'], $q); }));
			return ['total' => count($list), 'songs' => array_slice($list, 0, $limit)];
		case 'get_faq':
			return ['faq' => isset($d['faq']) ? $d['faq'] : []];
	}
	return null;
}
