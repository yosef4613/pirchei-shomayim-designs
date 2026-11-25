<?php
/**
 * מיילים של האתר: תבנית HTML אחת מעוצבת, עם גרסת טקסט רגיל לצידה.
 * מיילים בעיצוב מסודר (ולא טקסט עם כתובות ארוכות) מגיעים לתיבה הראשית ולא לספאם.
 */
if (!defined('ABSPATH')) {
	exit;
}

/**
 * $o: title, paras[], rows[[label, value, href?]], button[text, url], link[text, url], note, kicker,
 *     image[src, href, alt] (תמונה גדולה בראש המייל), unsub[text, linkText, url] (הסרה מרשימת התפוצה, בתחתית)
 */
function ps_mail_html($lang, $o) {
	$he = $lang !== 'en';
	$dir = $he ? 'rtl' : 'ltr';
	$align = $he ? 'right' : 'left';
	$e = function ($s) { return esc_html((string) $s); };
	$site = home_url('/');
	$brand = $he ? 'מקהלת פרחי שמיים' : 'Pirchei Shomayim Boys’ Choir';
	$h = '<!doctype html><html lang="' . ($he ? 'he' : 'en') . '" dir="' . $dir . '"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>' . $e($o['title']) . '</title></head>';
	$h .= '<body style="margin:0;padding:0;background:#f3f0f8;">';
	$h .= '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f3f0f8;"><tr><td align="center" style="padding:24px 12px;">';
	$h .= '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" dir="' . $dir . '" style="max-width:600px;background:#ffffff;border-radius:18px;overflow:hidden;font-family:Arial,Helvetica,sans-serif;color:#1d1530;text-align:' . $align . ';direction:' . $dir . ';">';
	// כותרת כהה עם הסמל
	$h .= '<tr><td style="background:#0b0812;padding:24px 26px;">';
	$h .= '<table role="presentation" cellspacing="0" cellpadding="0"><tr>';
	$h .= '<td style="padding-' . ($he ? 'left' : 'right') . ':14px;"><img src="' . esc_url(home_url('/ps/assets/img/icon-180.png')) . '" width="48" height="48" alt="" style="display:block;border-radius:12px;background:#ffffff;"></td>';
	$h .= '<td><div style="font-size:13px;color:#a6fcef;font-weight:bold;">' . $e(!empty($o['kicker']) ? $o['kicker'] : $brand) . '</div>';
	$h .= '<div style="font-size:22px;line-height:1.3;color:#ffffff;font-weight:bold;margin-top:4px;">' . $e($o['title']) . '</div></td>';
	$h .= '</tr></table></td></tr>';
	// תמונה גדולה (שיר חדש, מודעת הופעה)
	if (!empty($o['image'][0])) {
		$img = '<img src="' . esc_url($o['image'][0]) . '" width="600" alt="' . esc_attr(isset($o['image'][2]) ? $o['image'][2] : '') . '" style="display:block;width:100%;max-width:600px;height:auto;border:0;">';
		$h .= '<tr><td style="padding:0;background:#0b0812;">' . (!empty($o['image'][1]) ? '<a href="' . esc_url($o['image'][1]) . '">' . $img . '</a>' : $img) . '</td></tr>';
	}
	// גוף
	$h .= '<tr><td style="padding:24px 26px 8px;font-size:16px;line-height:1.7;color:#3b3350;">';
	foreach ((array) (isset($o['paras']) ? $o['paras'] : []) as $p) {
		$h .= '<p style="margin:0 0 12px;">' . $e($p) . '</p>';
	}
	if (!empty($o['rows'])) {
		$h .= '<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin:6px 0 14px;border-collapse:separate;border-spacing:0 6px;">';
		foreach ($o['rows'] as $r) {
			$val = $e($r[1]);
			if (!empty($r[2])) {
				$val = '<a href="' . esc_url($r[2], ['http', 'https', 'mailto', 'tel']) . '" style="color:#4a19a0;font-weight:bold;text-decoration:none;" dir="ltr">' . $val . '</a>';
			}
			$h .= '<tr><td style="width:34%;padding:9px 12px;background:#f6f2ff;border-radius:' . ($he ? '0 10px 10px 0' : '10px 0 0 10px') . ';font-size:14px;color:#6b6380;">' . $e($r[0]) . '</td>';
			$h .= '<td style="padding:9px 12px;background:#f6f2ff;border-radius:' . ($he ? '10px 0 0 10px' : '0 10px 10px 0') . ';font-size:15px;color:#1d1530;font-weight:bold;">' . nl2br($val) . '</td></tr>';
		}
		$h .= '</table>';
	}
	if (!empty($o['button'])) {
		$h .= '<table role="presentation" cellspacing="0" cellpadding="0" style="margin:8px 0 16px;"><tr><td style="background:#a6fcef;border-radius:12px;">';
		$h .= '<a href="' . esc_url($o['button'][1]) . '" style="display:inline-block;padding:13px 24px;font-size:16px;font-weight:bold;color:#08332e;text-decoration:none;">' . $e($o['button'][0]) . '</a>';
		$h .= '</td></tr></table>';
	}
	if (!empty($o['link'])) {
		$h .= '<p style="margin:0 0 12px;font-size:15px;"><a href="' . esc_url($o['link'][1]) . '" style="color:#4a19a0;font-weight:bold;">' . $e($o['link'][0]) . '</a></p>';
	}
	if (!empty($o['note'])) {
		$h .= '<p style="margin:6px 0 12px;font-size:14px;color:#6b6380;">' . $e($o['note']) . '</p>';
	}
	$h .= '</td></tr>';
	// תחתית
	$h .= '<tr><td style="padding:14px 26px 20px;border-top:1px solid #ece6f7;font-size:13px;color:#7b7290;line-height:1.7;">';
	$h .= '<a href="' . esc_url($site) . '" style="color:#4a19a0;">' . $e($brand) . '</a>' . ($he ? ' · מקהלת ילדים בירושלים ובבית שמש' : ' · Boys’ choir in Jerusalem & Beit Shemesh');
	if (!empty($o['unsub'])) {
		$h .= '<br>' . $e($o['unsub'][0]) . ' <a href="' . esc_url($o['unsub'][2]) . '" style="color:#7b7290;">' . $e($o['unsub'][1]) . '</a>';
	}
	$h .= '</td></tr></table></td></tr></table></body></html>';
	return $h;
}

/** אותו תוכן כטקסט רגיל — לתוכנות מייל שלא מציגות עיצוב */
function ps_mail_text($lang, $o) {
	$t = [$o['title'], ''];
	foreach ((array) (isset($o['paras']) ? $o['paras'] : []) as $p) {
		$t[] = $p;
	}
	if (!empty($o['rows'])) {
		$t[] = '';
		foreach ($o['rows'] as $r) {
			$t[] = $r[0] . ': ' . $r[1];
		}
	}
	foreach (['button', 'link'] as $k) {
		if (!empty($o[$k])) {
			$t[] = '';
			$t[] = $o[$k][0] . ': ' . $o[$k][1];
		}
	}
	if (!empty($o['note'])) {
		$t[] = '';
		$t[] = $o['note'];
	}
	$t[] = '';
	$t[] = ($lang === 'en' ? 'Pirchei Shomayim Boys’ Choir' : 'מקהלת פרחי שמיים') . ' · ' . home_url('/');
	if (!empty($o['unsub'])) {
		$t[] = $o['unsub'][0] . ' ' . $o['unsub'][1] . ': ' . $o['unsub'][2];
	}
	return implode("\n", $t);
}

/** שליחת מייל מעוצב. מחזיר true אם שרת המייל קיבל אותו */
function ps_send_mail($to, $subject, $lang, $o, $reply_to = '', $extra_headers = []) {
	$headers = array_merge(['Content-Type: text/html; charset=UTF-8'], $extra_headers);
	if ($reply_to && is_email($reply_to)) {
		$headers[] = 'Reply-To: ' . $reply_to;
	}
	$alt = ps_mail_text($lang, $o);
	$set_alt = function ($m) use ($alt) { $m->AltBody = $alt; };
	$from_name = function () use ($lang) { return $lang === 'en' ? 'Pirchei Shomayim Choir' : 'מקהלת פרחי שמיים'; };
	add_action('phpmailer_init', $set_alt, 20);
	add_filter('wp_mail_from_name', $from_name);
	$ok = wp_mail($to, $subject, ps_mail_html($lang, $o), $headers);
	remove_filter('wp_mail_from_name', $from_name);
	remove_action('phpmailer_init', $set_alt, 20);
	return $ok;
}
