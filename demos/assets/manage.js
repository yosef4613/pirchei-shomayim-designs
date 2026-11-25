/* אזור הניהול של מקהלת פרחי שמיים — מחובר לנתונים האמיתיים בוורדפרס.
   השרת מוסיף את window.PS_MANAGE: מצב הכניסה, כתובת הנתונים ומפתח אבטחה (nonce). */
(() => {
  'use strict';
  const boot = window.PS_MANAGE || { state: 'login', rest: '/wp-json/ps/v1/' };
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const icon = (id) => `<svg class="ico" aria-hidden="true"><use href="#i-${id}"/></svg>`;

  const BRANCHES = { 'ramat-eshkol': ['רמת אשכול', 'ירושלים'], 'neve-yaakov': ['נווה יעקב', 'ירושלים'], 'ramah-a': ['רמה א׳', 'בית שמש'], 'ramah-d': ['רמה ד׳', 'בית שמש'] };
  const STATUSES = [['new', 'חדשה'], ['contacted', 'נוצר קשר'], ['audition', 'נקבע מבדק'], ['accepted', 'התקבל לחוג'], ['declined', 'לא התאים']];
  const statusLabel = Object.fromEntries(STATUSES);
  const TOPICS = { songs: 'שירים חדשים', classes: 'פתיחת רישום', shows: 'הופעות' };
  const SOURCES = { class: 'טופס החוגים', club: 'הרשמה לעדכונים' };

  const toastEl = $('.toast'); let toastT;
  const toast = (msg) => { toastEl.textContent = msg; toastEl.hidden = false; clearTimeout(toastT); toastT = setTimeout(() => { toastEl.hidden = true; }, 2800); };

  async function api(path, body, method) {
    const opts = { credentials: 'same-origin', cache: 'no-store', headers: {} };
    if (boot.nonce) opts.headers['X-WP-Nonce'] = boot.nonce;
    if (body !== undefined) { opts.method = method || 'POST'; opts.headers['Content-Type'] = 'application/json'; opts.body = JSON.stringify(body); }
    const res = await fetch(boot.rest + path, opts);
    let json = null;
    try { json = await res.json(); } catch (e) { json = null; }
    if (!res.ok || !json || json.ok === false) { const er = new Error((json && (json.code || json.message)) || 'error'); er.status = res.status; er.data = json; throw er; }
    return json;
  }

  /* ---------- מסך כניסה / אין הרשאה ---------- */
  const gate = $('[data-gate]'); const app = $('[data-app]');
  const gateText = $('[data-gate-text]'); const gateForm = $('[data-gate-form]'); const gateErr = $('[data-gate-err]');
  const logout = async () => {
    try { await api('logout', {}); } catch (e) { /* ממשיכים */ }
    document.cookie = 'ps_m=; Max-Age=0; path=/; SameSite=Lax' + (location.protocol === 'https:' ? '; Secure' : '');
    location.reload();
  };
  if (boot.state !== 'ok') {
    gate.hidden = false;
    if (boot.state === 'denied') {
      gateText.textContent = `המשתמש ${boot.user ? boot.user.email : ''} אינו מוגדר כמנהל. אם זו טעות — פנו למי שבנה את האתר.`;
      $('[data-gate-logout]').hidden = false;
      $('[data-gate-logout]').addEventListener('click', logout);
    } else {
      gateText.textContent = 'כניסה בלי סיסמה: מזינים את המייל, ומקבלים קישור כניסה. הכניסה פתוחה רק למנהלי המקהלה.';
      gateForm.hidden = false;
      const started = Date.now();
      gateForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const email = gateForm.elements.email.value.trim();
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) { gateErr.textContent = 'נא לכתוב כתובת מייל תקינה.'; gateForm.elements.email.focus(); return; }
        gateErr.textContent = '';
        const btn = $('button', gateForm); btn.disabled = true;
        try {
          await api('login', { email, lang: 'he', to: 'manage', t: Date.now() - started, website: gateForm.elements.website.value });
          gateForm.hidden = true;
          gateText.innerHTML = `שלחנו קישור כניסה אל <bdi>${esc(email)}</bdi>. הקישור תקף לחצי שעה. לא הגיע? כדאי להציץ בספאם.`;
        } catch (err) {
          gateErr.textContent = err.status === 429 ? 'יותר מדי ניסיונות. נסו שוב בעוד כמה דקות.' : 'משהו השתבש. נסו שוב בעוד רגע.';
        } finally { btn.disabled = false; }
      });
      setTimeout(() => gateForm.elements.email.focus(), 50);
    }
    return;
  }
  gate.hidden = true; app.hidden = false;
  const u = boot.user || {};
  $('[data-user-name]').textContent = u.name || '';
  $('[data-user-email]').textContent = u.email || '';
  $('[data-avatar]').textContent = (u.name || u.email || '?').trim().charAt(0).toUpperCase();
  $('[data-logout]').addEventListener('click', logout);
  if (boot.wpadmin) { const w = $('[data-wpadmin]'); w.href = boot.wpadmin; w.hidden = false; }

  /* ---------- לשוניות ---------- */
  const tabs = $$('[role="tab"]');
  const select = (tab, focus) => {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute('aria-selected', String(on)); t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tab.focus();
    try { history.replaceState(null, '', '#' + tab.dataset.tab); } catch (e) { /* */ }
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => select(t));
    t.addEventListener('keydown', (e) => {
      const keys = { ArrowDown: 1, ArrowLeft: 1, ArrowUp: -1, ArrowRight: -1 };
      let n = null;
      if (e.key in keys) n = (i + keys[e.key] + tabs.length) % tabs.length;
      else if (e.key === 'Home') n = 0; else if (e.key === 'End') n = tabs.length - 1;
      if (n != null) { e.preventDefault(); select(tabs[n], true); }
    });
  });
  const fromHash = tabs.find((t) => '#' + t.dataset.tab === location.hash);
  if (fromHash) select(fromHash);

  const fmtDate = (iso, withTime = true) => {
    if (!iso) return '';
    try { return new Intl.DateTimeFormat('he-IL', withTime ? { day: 'numeric', month: 'numeric', year: '2-digit', hour: '2-digit', minute: '2-digit' } : { day: 'numeric', month: 'numeric', year: 'numeric' }).format(new Date(iso)); } catch (e) { return iso; }
  };
  const norm = (s) => String(s || '').toLowerCase().replace(/[\s\-()]/g, '');
  const csv = (rows) => '﻿' + rows.map((r) => r.map((v) => `"${String(v == null ? '' : v).replace(/"/g, '""')}"`).join(',')).join('\r\n');
  const download = (name, text) => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([text], { type: 'text/csv;charset=utf-8' }));
    a.download = name; document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  };
  const today = () => new Date().toISOString().slice(0, 10);

  let D = { inquiries: [], subscribers: [], members: [], exclusive: [] };
  const loadErr = $('[data-load-error]');
  async function load() {
    try {
      D = await api('admin/data');
      loadErr.hidden = true;
      $$('[data-notify]').forEach((el) => { el.textContent = D.notify || ''; });
      renderInquiries(); renderSubs(); renderMembers(); renderExcl();
    } catch (err) {
      loadErr.hidden = false;
      loadErr.textContent = err.status === 403 || err.status === 401 ? 'פג תוקף הכניסה. רעננו את הדף (ואם צריך — היכנסו שוב).' : 'לא הצלחנו לטעון את הנתונים. בדקו את החיבור ורעננו את הדף.';
    }
  }

  /* ---------- פניות ---------- */
  const q = $('#q'); const fBranch = $('#f-branch'); const fStatus = $('#f-status'); const fHideTest = $('#f-hide-test');
  Object.entries(BRANCHES).forEach(([id, [n, c]]) => fBranch.insertAdjacentHTML('beforeend', `<option value="${id}">${esc(n)} · ${esc(c)}</option>`));
  STATUSES.forEach(([k, v]) => fStatus.insertAdjacentHTML('beforeend', `<option value="${k}">${esc(v)}</option>`));
  const rowsEl = $('[data-rows]');
  let current = [];
  function renderInquiries() {
    const all = D.inquiries;
    const counts = { new: 0, contacted: 0, audition: 0, accepted: 0 };
    all.forEach((x) => { if (!x.test && x.status in counts) counts[x.status]++; });
    Object.entries(counts).forEach(([k, v]) => { $(`[data-stat="${k}"]`).textContent = v; });
    $('[data-new-count]').textContent = counts.new || '';
    const term = norm(q.value);
    current = all.filter((x) => (!fBranch.value || x.branch === fBranch.value) && (!fStatus.value || x.status === fStatus.value)
      && (!fHideTest.checked || !x.test)
      && (!term || [x.parent, x.child, x.phone, x.email].some((v) => norm(v).includes(term))));
    $$('[data-status-card]').forEach((c) => c.setAttribute('aria-pressed', String(fStatus.value === c.dataset.statusCard)));
    $('[data-result-line]').textContent = `מוצגות ${current.length} פניות מתוך ${all.length}`;
    $('[data-empty]').hidden = current.length > 0;
    $('[data-trash-tests]').hidden = !all.some((x) => x.test);
    rowsEl.innerHTML = current.map((x) => {
      const [bn, bc] = BRANCHES[x.branch] || [x.branch, ''];
      const tel = String(x.phone || '').replace(/[^\d+]/g, '');
      return `<tr class="${x.status === 'new' ? 'is-new' : ''}" data-id="${x.id}">
        <td data-label="תאריך">${esc(fmtDate(x.date))}${x.mailed ? '' : '<div class="mail-flag">המייל לא נשלח</div>'}</td>
        <td data-label="הורה"><div class="cell-main">${esc(x.parent)}${x.status === 'new' ? '<span class="tag-new">חדש</span>' : ''}${x.test ? '<span class="tag-test">בדיקה</span>' : ''}${x.lang === 'en' ? '<span class="tag-en">EN</span>' : ''}</div>
          <div class="cell-sub"><a href="tel:${esc(tel)}" dir="ltr">${icon('phone')}${esc(x.phone)}</a><a href="mailto:${esc(x.email)}" dir="ltr">${icon('mail')}${esc(x.email)}</a></div></td>
        <td data-label="ילד"><div class="cell-main">${esc(x.child)}, ${esc(x.age)}</div><div class="cell-sub"><span>${esc(x.cheder)} · כיתה ${esc(x.grade)}</span></div>
          ${x.notes ? `<p class="parent-note">״${esc(x.notes)}״</p>` : ''}</td>
        <td data-label="חוג"><div class="cell-main">${esc(bn)}</div><div class="cell-sub"><span>${esc(bc)}</span></div></td>
        <td data-label="סטטוס"><label class="sr" for="st-${x.id}">סטטוס הפנייה של ${esc(x.parent)}</label>
          <select class="status-sel" id="st-${x.id}" data-status-for="${x.id}" data-s="${x.status}">${STATUSES.map(([k, v]) => `<option value="${k}"${k === x.status ? ' selected' : ''}>${esc(v)}</option>`).join('')}</select></td>
        <td data-label="הערה פנימית"><label class="sr" for="nt-${x.id}">הערה פנימית על ${esc(x.parent)}</label>
          <textarea class="note-in" id="nt-${x.id}" rows="1" data-note-for="${x.id}" placeholder="למשל: מבדק ביום ג׳">${esc(x.note)}</textarea></td>
        <td class="cell-act"><button type="button" class="row-del" data-del-inq="${x.id}" aria-label="העברת הפנייה של ${esc(x.parent)} לפח" title="העברה לפח">${icon('trash')}</button></td>
      </tr>`;
    }).join('');
  }
  const findInq = (id) => D.inquiries.find((x) => String(x.id) === String(id));
  rowsEl.addEventListener('change', async (e) => {
    const sel = e.target.closest('[data-status-for]');
    if (sel) {
      const x = findInq(sel.dataset.statusFor); const prev = x.status;
      x.status = sel.value; sel.dataset.s = sel.value;
      try { await api('admin/inquiry/' + x.id, { status: sel.value }); toast(`הסטטוס עודכן: ${statusLabel[sel.value]}`); renderInquiries(); }
      catch (err) { x.status = prev; sel.value = prev; sel.dataset.s = prev; toast('השמירה לא הצליחה. נסו שוב.'); }
      return;
    }
    const note = e.target.closest('[data-note-for]');
    if (note) {
      const x = findInq(note.dataset.noteFor);
      note.classList.add('is-saving');
      try { await api('admin/inquiry/' + x.id, { note: note.value }); x.note = note.value; note.classList.remove('is-saving'); note.classList.add('is-saved'); setTimeout(() => note.classList.remove('is-saved'), 1500); toast('ההערה נשמרה'); }
      catch (err) { note.classList.remove('is-saving'); toast('ההערה לא נשמרה. נסו שוב.'); }
    }
  });
  rowsEl.addEventListener('click', async (e) => {
    const b = e.target.closest('[data-del-inq]'); if (!b) return;
    const x = findInq(b.dataset.delInq);
    if (!confirm(`להעביר לפח את הפנייה של ${x.parent} (${x.child})?\nאפשר לשחזר אותה מהפח בוורדפרס.`)) return;
    try { await api('admin/inquiry/' + x.id, { delete: true }); D.inquiries = D.inquiries.filter((y) => y !== x); renderInquiries(); toast('הפנייה הועברה לפח'); }
    catch (err) { toast('המחיקה לא הצליחה. נסו שוב.'); }
  });
  $('[data-trash-tests]').addEventListener('click', async () => {
    const tests = D.inquiries.filter((x) => x.test);
    if (!tests.length || !confirm(`להעביר לפח את כל ${tests.length} פניות הבדיקה?`)) return;
    for (const x of tests) { try { await api('admin/inquiry/' + x.id, { delete: true }); D.inquiries = D.inquiries.filter((y) => y !== x); } catch (err) { /* ממשיכים */ } }
    renderInquiries(); toast('פניות הבדיקה הועברו לפח');
  });
  [q, fBranch, fStatus, fHideTest].forEach((el) => el.addEventListener(el.type === 'search' ? 'input' : 'change', renderInquiries));
  $$('[data-status-card]').forEach((c) => c.addEventListener('click', () => { fStatus.value = fStatus.value === c.dataset.statusCard ? '' : c.dataset.statusCard; renderInquiries(); }));
  $('[data-export]').addEventListener('click', () => {
    const head = ['תאריך', 'שם ההורה', 'טלפון', 'מייל', 'שם הילד', 'גיל', 'תלמוד תורה', 'כיתה', 'חוג', 'סטטוס', 'הערה פנימית', 'הערות ההורה', 'בדיקה'];
    download(`פניות-לחוגים-${today()}.csv`, csv([head, ...current.map((x) => [fmtDate(x.date), x.parent, x.phone, x.email, x.child, x.age, x.cheder, x.grade, (BRANCHES[x.branch] || [x.branch]).join(' · '), statusLabel[x.status], x.note, x.notes, x.test ? 'כן' : ''])]));
  });

  /* ---------- עדכונים במייל ---------- */
  const qSubs = $('#q-subs'); const fVerified = $('#f-verified');
  let topicFilter = ''; let subsCurrent = [];
  function renderSubs() {
    const all = D.subscribers;
    Object.keys(TOPICS).forEach((k) => { $(`[data-topic-count="${k}"]`).textContent = all.filter((s) => s.verified && s.topics.includes(k)).length; });
    $$('[data-topic-card]').forEach((c) => c.setAttribute('aria-pressed', String(topicFilter === c.dataset.topicCard)));
    const term = norm(qSubs.value);
    subsCurrent = all.filter((s) => (!topicFilter || s.topics.includes(topicFilter)) && (!fVerified.checked || s.verified) && (!term || norm(s.name).includes(term) || norm(s.email).includes(term)));
    const ok = all.filter((s) => s.verified).length;
    $('[data-subs-line]').textContent = `מוצגים ${subsCurrent.length} מתוך ${all.length} · ${ok} אישרו את הכתובת`;
    $('[data-subs-empty]').hidden = all.length > 0;
    $('[data-subs]').innerHTML = subsCurrent.map((s) => `<tr data-id="${s.id}">
      <td data-label="נרשם">${esc(fmtDate(s.date))}</td>
      <td data-label="שם ומייל"><div class="cell-main">${esc(s.name || '—')}${s.test ? '<span class="tag-test">בדיקה</span>' : ''}${s.lang === 'en' ? '<span class="tag-en">EN</span>' : ''}</div><div class="cell-sub"><a href="mailto:${esc(s.email)}" dir="ltr">${icon('mail')}${esc(s.email)}</a></div></td>
      <td data-label="נושאים"><div class="chips-row">${s.topics.map((t) => `<span class="mini-chip">${esc(TOPICS[t] || t)}</span>`).join('')}</div></td>
      <td data-label="מקור">${esc(SOURCES[s.source] || s.source)}</td>
      <td data-label="מצב">${s.verified ? '<span class="state ok">אישר במייל</span>' : '<span class="state wait">ממתין לאישור</span>'}</td>
      <td class="cell-act"><button type="button" class="row-del" data-del-sub="${s.id}" aria-label="הסרת ${esc(s.email)} מהעדכונים" title="הסרה מהעדכונים">${icon('trash')}</button></td>
    </tr>`).join('');
  }
  [qSubs, fVerified].forEach((el) => el.addEventListener(el.type === 'search' ? 'input' : 'change', renderSubs));
  $$('[data-topic-card]').forEach((c) => c.addEventListener('click', () => { topicFilter = topicFilter === c.dataset.topicCard ? '' : c.dataset.topicCard; renderSubs(); }));
  $('[data-subs]').addEventListener('click', async (e) => {
    const b = e.target.closest('[data-del-sub]'); if (!b) return;
    const s = D.subscribers.find((x) => String(x.id) === b.dataset.delSub);
    if (!confirm(`להסיר את ${s.email} מהעדכונים? (למשל, אם ביקש להפסיק לקבל)`)) return;
    try { await api('admin/subscriber/' + s.id, { delete: true }); D.subscribers = D.subscribers.filter((x) => x !== s); renderSubs(); toast('הכתובת הוסרה מהעדכונים'); }
    catch (err) { toast('ההסרה לא הצליחה. נסו שוב.'); }
  });
  $('[data-copy-emails]').addEventListener('click', async () => {
    const list = subsCurrent.filter((s) => s.verified && !s.test).map((s) => s.email);
    if (!list.length) { toast('אין כתובות מאושרות בתצוגה הנוכחית'); return; }
    try { await navigator.clipboard.writeText(list.join(', ')); toast(`הועתקו ${list.length} כתובות — הדביקו בשדה ״עותק מוסתר״`); }
    catch (err) { prompt('העתיקו את הכתובות:', list.join(', ')); }
  });
  $('[data-export-subs]').addEventListener('click', () => {
    download(`עדכונים-במייל-${today()}.csv`, csv([['נרשם', 'שם', 'מייל', 'נושאים', 'מקור', 'אישר במייל'], ...subsCurrent.map((s) => [fmtDate(s.date), s.name, s.email, s.topics.map((t) => TOPICS[t] || t).join(', '), SOURCES[s.source] || s.source, s.verified ? 'כן' : 'לא'])]));
  });

  /* ---------- רשומים לאתר ---------- */
  function renderMembers() {
    const all = D.members;
    $('[data-members-line]').textContent = `${all.length} משתמשים · ${all.filter((m) => m.manager).length} מנהלים`;
    $('[data-members]').innerHTML = all.map((m) => `<tr>
      <td data-label="שם ומייל"><div class="cell-main">${esc(m.name)}</div><div class="cell-sub"><a href="mailto:${esc(m.email)}" dir="ltr">${icon('mail')}${esc(m.email)}</a></div></td>
      <td data-label="נרשם">${esc(fmtDate(m.joined, false))}</td>
      <td data-label="כניסה אחרונה">${m.last ? esc(fmtDate(m.last.replace(' ', 'T'))) : '—'}</td>
      <td data-label="תפקיד"><span class="role${m.manager ? ' is-manager' : ''}">${m.manager ? 'מנהל' : m.wp ? 'וורדפרס' : 'רשום'}</span></td>
      <td class="cell-act">${m.manager || m.wp ? '' : `<button type="button" class="row-del" data-del-member="${m.id}" aria-label="מחיקת המשתמש ${esc(m.email)}" title="מחיקת המשתמש">${icon('trash')}</button>`}</td>
    </tr>`).join('');
  }
  $('[data-members]').addEventListener('click', async (e) => {
    const b = e.target.closest('[data-del-member]'); if (!b) return;
    const m = D.members.find((x) => String(x.id) === b.dataset.delMember);
    if (!confirm(`למחוק את המשתמש ${m.email}? הוא יוכל להירשם שוב בעתיד.`)) return;
    try { await api('admin/member/' + m.id, { delete: true }); D.members = D.members.filter((x) => x !== m); renderMembers(); toast('המשתמש נמחק'); }
    catch (err) { toast('המחיקה לא הצליחה.'); }
  });

  /* ---------- מאחורי הקלעים ---------- */
  const ef = $('[data-excl-form]'); const eMsg = $('[data-excl-msg]');
  let editing = null;
  const ytId = (v) => { const s = String(v || '').trim(); if (/^[\w-]{11}$/.test(s)) return s; const m = /(?:v=|youtu\.be\/|\/shorts\/|\/embed\/|\/live\/)([\w-]{11})/.exec(s); return m ? m[1] : ''; };
  function renderExcl() {
    const all = D.exclusive;
    $('[data-excl-empty]').hidden = all.length > 0;
    $('[data-excl-list]').innerHTML = all.map((x) => `<li class="card excl-item${x.status === 'draft' ? ' is-draft' : ''}">
      <div class="thumb"${x.video ? ` style="background-image:url('https://i.ytimg.com/vi/${esc(x.video)}/mqdefault.jpg')"` : ''}>${x.video ? icon('play') : icon('star')}</div>
      <div class="body">
        <span class="pill${x.status === 'draft' ? ' pill-draft' : ' pill-mint'}">${x.status === 'draft' ? 'טיוטה — לא מוצג' : 'מוצג לרשומים'}</span>
        <h2>${esc(x.title)}</h2>
        ${x.text ? `<p class="text">${esc(x.text)}</p>` : ''}
        <p class="meta">${esc(fmtDate(x.date, false))}${x.video ? ' · סרטון' : ''}${x.title_en ? ' · יש גם באנגלית' : ''}</p>
        <div class="card-actions">
          <button type="button" class="btn btn-light" data-excl-edit="${x.id}">${icon('edit')}עריכה</button>
          <button type="button" class="btn btn-light" data-excl-toggle="${x.id}">${x.status === 'draft' ? 'פרסום' : 'הסתרה'}</button>
          <button type="button" class="btn btn-danger-light" data-excl-del="${x.id}">${icon('trash')}מחיקה</button>
        </div>
      </div></li>`).join('');
  }
  const formData = () => ({
    title: ef.elements.title.value.trim(), text: ef.elements.text.value.trim(), video: ef.elements.video.value.trim(),
    vertical: ef.elements.vertical.checked, status: ef.elements.draft.checked ? 'draft' : 'publish',
    title_en: ef.elements.title_en.value.trim(), text_en: ef.elements.text_en.value.trim(),
  });
  const resetForm = () => {
    ef.reset(); editing = null; eMsg.textContent = ''; eMsg.classList.remove('is-error');
    $('[data-excl-form-title]').textContent = 'הוספת תוכן'; $('[data-excl-submit]').textContent = 'פרסום באתר'; $('[data-excl-cancel]').hidden = true;
    $$('[aria-invalid]', ef).forEach((el) => el.removeAttribute('aria-invalid'));
  };
  ef.addEventListener('submit', async (e) => {
    e.preventDefault();
    const d = formData();
    $$('[aria-invalid]', ef).forEach((el) => el.removeAttribute('aria-invalid'));
    eMsg.classList.add('is-error');
    if (!d.title) { eMsg.textContent = 'חסרה כותרת.'; ef.elements.title.setAttribute('aria-invalid', 'true'); ef.elements.title.focus(); return; }
    if (d.video && !ytId(d.video)) { eMsg.textContent = 'הקישור לסרטון לא מזוהה. הדביקו קישור מיוטיוב (רגיל, קצר או שורטס).'; ef.elements.video.setAttribute('aria-invalid', 'true'); ef.elements.video.focus(); return; }
    eMsg.classList.remove('is-error'); eMsg.textContent = 'שומר…';
    const btn = $('button[type="submit"]', ef); btn.disabled = true;
    try {
      const res = await api('admin/exclusive' + (editing ? '/' + editing : ''), d);
      if (editing) D.exclusive = D.exclusive.map((x) => (x.id === res.item.id ? res.item : x));
      else D.exclusive.unshift(res.item);
      const was = editing; resetForm(); renderExcl();
      toast(was ? 'השינויים נשמרו' : (d.status === 'draft' ? 'נשמר כטיוטה' : 'פורסם באתר לכל הרשומים'));
    } catch (err) {
      eMsg.classList.add('is-error'); eMsg.textContent = 'השמירה לא הצליחה. בדקו את הפרטים ונסו שוב.';
    } finally { btn.disabled = false; }
  });
  $('[data-excl-cancel]').addEventListener('click', resetForm);
  $('[data-excl-list]').addEventListener('click', async (e) => {
    const ed = e.target.closest('[data-excl-edit]');
    const tg = e.target.closest('[data-excl-toggle]');
    const dl = e.target.closest('[data-excl-del]');
    const t = ed || tg || dl; if (!t) return;
    const id = Number(t.dataset.exclEdit || t.dataset.exclToggle || t.dataset.exclDel);
    const x = D.exclusive.find((y) => y.id === id); if (!x) return;
    if (ed) {
      editing = x.id;
      ef.elements.title.value = x.title; ef.elements.text.value = x.text; ef.elements.video.value = x.video ? `https://youtu.be/${x.video}` : '';
      ef.elements.vertical.checked = !!x.vertical; ef.elements.draft.checked = x.status === 'draft';
      ef.elements.title_en.value = x.title_en || ''; ef.elements.text_en.value = x.text_en || '';
      $('[data-excl-form-title]').textContent = 'עריכת תוכן'; $('[data-excl-submit]').textContent = 'שמירת השינויים'; $('[data-excl-cancel]').hidden = false;
      ef.scrollIntoView({ behavior: 'smooth', block: 'start' }); ef.elements.title.focus({ preventScroll: true });
      return;
    }
    if (tg) {
      try {
        const res = await api('admin/exclusive/' + x.id, { title: x.title, text: x.text, video: x.video, vertical: x.vertical, title_en: x.title_en, text_en: x.text_en, status: x.status === 'draft' ? 'publish' : 'draft' });
        D.exclusive = D.exclusive.map((y) => (y.id === x.id ? res.item : y)); renderExcl();
        toast(res.item.status === 'draft' ? 'הוסתר מהאתר' : 'פורסם באתר');
      } catch (err) { toast('השמירה לא הצליחה.'); }
      return;
    }
    if (dl) {
      if (!confirm(`למחוק את ״${x.title}״? אי אפשר לשחזר.`)) return;
      try { await api('admin/exclusive/' + x.id, { delete: true }); D.exclusive = D.exclusive.filter((y) => y !== x); if (editing === x.id) resetForm(); renderExcl(); toast('נמחק'); }
      catch (err) { toast('המחיקה לא הצליחה.'); }
    }
  });

  load();
})();
