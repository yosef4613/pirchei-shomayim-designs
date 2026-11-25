/* פרחי שמיים · מצב בדיקה למנהלים.
   נטען רק כשמנהל מחובר נכנס לאתר דרך ‎?ps_admin=1 (השרת מוסיף את window.PS_ADMIN).
   הכפתורים ממלאים את הטפסים בפרטי דוגמה עם המייל של המנהל — והשליחה אמיתית, מסומנת [בדיקה]. */
(() => {
  'use strict';
  const A = window.PS_ADMIN;
  if (!A) return;
  const he = (A.lang || document.documentElement.lang) !== 'en';
  const L = he ? {
    title: 'מצב בדיקה · רק מנהלים רואים את זה',
    fillClass: 'מילוי אוטומטי — טופס החוגים',
    fillClub: 'מילוי אוטומטי — עדכונים במייל',
    hide: 'הסתרה', show: 'מצב בדיקה',
    parent: 'בדיקה — ' + (A.name || 'מנהל'), child: 'ילד לבדיקה', cheder: 'תלמוד תורה לדוגמה', notes: 'פנייה לבדיקת האתר — אפשר למחוק',
    filled: 'מולא לחוג {branch}. לחצו ״שליחת הפרטים״ — זו שליחה אמיתית: הפנייה תישמר בוורדפרס עם הסימון [בדיקה], התראה תישלח אל {notify}, ומייל אישור אל {email}. כל לחיצה נוספת בוחרת את החוג הבא.',
    clubFilled: 'מולא עם {email} וכל הנושאים. לחצו ״הרשמה לעדכונים״ — יגיע אליכם מייל עם קישור לאישור.',
  } : {
    title: 'Test mode · only admins see this',
    fillClass: 'Auto-fill — class form',
    fillClub: 'Auto-fill — email updates',
    hide: 'Hide', show: 'Test mode',
    parent: 'Test — ' + (A.name || 'admin'), child: 'Test child', cheder: 'Sample Talmud Torah', notes: 'Website test inquiry — safe to delete',
    filled: 'Filled for {branch}. Press “Send my details” — this is a real submission: it is saved in WordPress marked [בדיקה], a notification goes to {notify}, and a confirmation email to {email}. Each further click picks the next class.',
    clubFilled: 'Filled with {email} and all topics. Press the sign-up button — you will get an email with a confirmation link.',
  };
  const $ = (s, r = document) => r.querySelector(s);
  const fill = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => (o[k] != null ? o[k] : ''));
  const set = (el, v) => { if (!el) return; el.value = v; el.dispatchEvent(new Event('input', { bubbles: true })); el.dispatchEvent(new Event('change', { bubbles: true })); };
  const check = (el) => { if (el && !el.checked) el.click(); };

  const style = document.createElement('style');
  style.textContent = `
    .ps-test { position: fixed; z-index: 85; inset-inline-start: 16px; bottom: 16px; width: min(360px, calc(100vw - 32px)); padding: 14px 16px 16px; border-radius: 16px;
      background: #15101f; color: #f3eefb; border: 1px solid rgba(203, 184, 255, .4); box-shadow: 0 20px 50px -20px rgba(0, 0, 0, .8); font: 15px/1.5 Heebo, Arial, sans-serif; display: grid; gap: 10px; }
    .ps-test b { color: #e6dcff; font-size: .95rem; }
    .ps-test button { min-height: 42px; border-radius: 12px; border: 1px solid rgba(203, 184, 255, .45); background: #4a19a0; color: #fff; font: inherit; font-weight: 700; cursor: pointer; padding: 8px 12px; }
    .ps-test button.ps-ghost { background: none; color: #cbb8ff; min-height: 32px; padding: 4px 10px; justify-self: start; }
    .ps-test p { margin: 0; font-size: .88rem; color: #d9cff0; }
    .ps-test p:empty { display: none; }
    .ps-test-tab { position: fixed; z-index: 85; inset-inline-start: 16px; bottom: 16px; border-radius: 999px; border: 1px solid rgba(203, 184, 255, .45); background: #4a19a0; color: #fff; font: 700 14px Heebo, Arial, sans-serif; padding: 8px 14px; cursor: pointer; }
    .ps-test[hidden], .ps-test-tab[hidden] { display: none; }`;
  document.head.appendChild(style);

  const box = document.createElement('div');
  box.className = 'ps-test';
  box.setAttribute('role', 'region');
  box.setAttribute('aria-label', L.title);
  box.innerHTML = `<b>${L.title}</b><button type="button" data-t="class">${L.fillClass}</button>${$('#club-form') ? `<button type="button" data-t="club">${L.fillClub}</button>` : ''}<p aria-live="polite"></p><button type="button" class="ps-ghost" data-t="hide">${L.hide}</button>`;
  const tab = document.createElement('button');
  tab.type = 'button'; tab.className = 'ps-test-tab'; tab.textContent = L.show; tab.hidden = true;
  document.body.append(box, tab);
  const note = $('p', box);

  let next = 0;
  const fillClass = () => {
    const form = $('#join-form'); if (!form) return;
    const again = $('#join-success:not([hidden]) [data-again]'); if (again) again.click();
    const sel = $('#f-branch');
    const opts = [...sel.options].filter((o) => o.value);
    const o = opts[next % opts.length]; next++;
    set(sel, o.value);
    set($('#f-parent'), L.parent); set($('#f-phone'), '050-0000000'); set($('#f-email'), A.email);
    set($('#f-child'), L.child); set($('#f-age'), '10'); set($('#f-cheder'), L.cheder);
    const g = $('#f-grade'); if (g) { g.selectedIndex = Math.min(4, g.options.length - 1); g.dispatchEvent(new Event('change', { bubbles: true })); }
    set($('#f-notes'), L.notes);
    check($('#f-consent'));
    form.dataset.test = '1';
    $('#join-form-area').scrollIntoView({ block: 'start', behavior: 'smooth' });
    setTimeout(() => { const b = $('button[type="submit"]', form); if (b) b.focus({ preventScroll: true }); }, 600);
    note.textContent = fill(L.filled, { branch: o.textContent.trim(), notify: A.notify, email: A.email });
  };
  const fillClub = () => {
    const f = $('#club-form'); if (!f) return;
    const again = $('#club-success:not([hidden]) [data-club-again]'); if (again) again.click();
    set(f.elements.name, L.parent); set(f.elements.email, A.email);
    f.querySelectorAll('[name="c-topic"]').forEach(check);
    check(f.elements.consent);
    f.dataset.test = '1';
    $('#club').scrollIntoView({ block: 'start', behavior: 'smooth' });
    setTimeout(() => { const b = $('button[type="submit"]', f); if (b) b.focus({ preventScroll: true }); }, 600);
    note.textContent = fill(L.clubFilled, { email: A.email });
  };
  box.addEventListener('click', (e) => {
    const t = e.target.closest('[data-t]'); if (!t) return;
    if (t.dataset.t === 'class') fillClass();
    else if (t.dataset.t === 'club') fillClub();
    else { box.hidden = true; tab.hidden = false; }
  });
  tab.addEventListener('click', () => { box.hidden = false; tab.hidden = true; });
})();
