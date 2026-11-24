/* לוח הניהול לדוגמה — כך יעבוד לוח הניהול שייבנה בוורדפרס. כאן הנתונים נשמרים רק בדפדפן. */
(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const store = {
    get(k, fb) { try { const v = JSON.parse(localStorage.getItem(k)); return v == null ? fb : v; } catch (e) { return fb; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { /* מצב פרטי */ } },
    del(k) { try { localStorage.removeItem(k); } catch (e) { /* */ } },
  };

  const BRANCHES = [
    { id: 'ramat-eshkol', name: 'רמת אשכול', city: 'ירושלים', venue: 'בתיאום עם צוות המקהלה', ages: '8–12', times: 'יעודכן' },
    { id: 'neve-yaakov', name: 'נווה יעקב', city: 'ירושלים', venue: 'מינהל קהילתי נווה יעקב', ages: '8–12', times: 'יעודכן' },
    { id: 'ramah-a', name: 'רמה א׳', city: 'בית שמש', venue: 'מתנ״ס גוונים', ages: '8–12', times: 'יעודכן' },
    { id: 'ramah-d', name: 'רמה ד׳', city: 'בית שמש', venue: 'מרכז קהילתי דורות', ages: '8–12', times: 'יעודכן' },
  ];
  const STATUSES = [['new', 'חדשה'], ['contacted', 'נוצר קשר'], ['audition', 'נקבע מבדק'], ['accepted', 'התקבל לחוג'], ['declined', 'לא התאים']];
  const statusLabel = Object.fromEntries(STATUSES);
  const daysAgo = (d, h = 10) => { const x = new Date(); x.setDate(x.getDate() - d); x.setHours(h, 15, 0, 0); return x.toISOString(); };
  // נתוני דוגמה בדויים בלבד
  const SEED = [
    { id: 's1', date: daysAgo(0, 9), branch: 'ramah-a', parent: 'ישראל כהן (דוגמה)', phone: '050-0000001', email: 'example1@example.com', child: 'יוסף', age: 9, cheder: 'תלמוד תורה לדוגמה', grade: 'ג׳', notes: 'אוהב לשיר בבית כל היום', status: 'new' },
    { id: 's2', date: daysAgo(1, 20), branch: 'ramat-eshkol', parent: 'משה לוי (דוגמה)', phone: '050-0000002', email: 'example2@example.com', child: 'אברהם', age: 11, cheder: 'חיידר לדוגמה', grade: 'ה׳', notes: '', status: 'new' },
    { id: 's3', date: daysAgo(3, 13), branch: 'neve-yaakov', parent: 'דוד פרידמן (דוגמה)', phone: '050-0000003', email: 'example3@example.com', child: 'שמואל', age: 8, cheder: 'תלמוד תורה לדוגמה', grade: 'ב׳', notes: '', status: 'contacted' },
    { id: 's4', date: daysAgo(5, 11), branch: 'ramah-d', parent: 'יעקב שטרן (דוגמה)', phone: '050-0000004', email: 'example4@example.com', child: 'מנחם', age: 10, cheder: 'חיידר לדוגמה', grade: 'ד׳', notes: 'שר כבר במקהלה בשנה שעברה', status: 'audition' },
    { id: 's5', date: daysAgo(9, 17), branch: 'ramat-eshkol', parent: 'אהרן גרין (דוגמה)', phone: '050-0000005', email: 'example5@example.com', child: 'נחמן', age: 12, cheder: 'תלמוד תורה לדוגמה', grade: 'ו׳', notes: '', status: 'accepted' },
    { id: 's6', date: daysAgo(12, 12), branch: 'ramah-a', parent: 'שלמה וייס (דוגמה)', phone: '050-0000006', email: 'example6@example.com', child: 'צבי', age: 9, cheder: 'חיידר לדוגמה', grade: 'ג׳', notes: '', status: 'accepted' },
  ];
  const SONGS = [
    ['-4sE-rfQI1k', 'אתה בחרתנו', 'לפני חודשיים'], ['rWHE6woblu4', 'אור חדש', 'לפני חודשיים'], ['aFhQjhm1if8', 'פתח ליבי', 'לפני 5 חודשים'],
    ['yjBQLelJDKw', 'מחרוזת שמחת תורה', 'לפני שנה'], ['sAeFaXlxv0E', 'מחרוזת שירי תשובה', 'לפני שנה'], ['n6tLDS_ioYk', 'מקהלולם: שמע קולינו', 'לפני שנה'],
  ];

  const state = store.get('ps-admin-state', {}) || {};
  state.status = state.status || {}; state.notes = state.notes || {};
  state.branches = state.branches || {}; state.shows = state.shows || []; state.behind = state.behind || [];
  state.featured = state.featured || '-4sE-rfQI1k'; state.hiddenSongs = state.hiddenSongs || [];
  const save = () => store.set('ps-admin-state', state);
  const branchById = (id) => ({ ...BRANCHES.find((b) => b.id === id), ...(state.branches[id] || {}) });

  const setInvalid = (el, on) => (on ? el.setAttribute('aria-invalid', 'true') : el.removeAttribute('aria-invalid'));
  const toastEl = $('.toast'); let toastT;
  const toast = (msg) => { toastEl.textContent = msg; toastEl.hidden = false; clearTimeout(toastT); toastT = setTimeout(() => { toastEl.hidden = true; }, 2600); };

  /* ---------- לשוניות ---------- */
  const tabs = $$('[role="tab"]');
  const select = (tab, focus) => {
    tabs.forEach((t) => {
      const on = t === tab;
      t.setAttribute('aria-selected', String(on));
      t.tabIndex = on ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
    });
    if (focus) tab.focus();
    try { history.replaceState(null, '', '#' + tab.dataset.tab); } catch (e) { /* */ }
  };
  tabs.forEach((t, i) => {
    t.addEventListener('click', () => select(t));
    t.addEventListener('keydown', (e) => {
      const rtl = document.documentElement.dir === 'rtl';
      const nextKeys = ['ArrowDown', rtl ? 'ArrowLeft' : 'ArrowRight'];
      const prevKeys = ['ArrowUp', rtl ? 'ArrowRight' : 'ArrowLeft'];
      let n = null;
      if (nextKeys.includes(e.key)) n = (i + 1) % tabs.length;
      else if (prevKeys.includes(e.key)) n = (i - 1 + tabs.length) % tabs.length;
      else if (e.key === 'Home') n = 0; else if (e.key === 'End') n = tabs.length - 1;
      if (n != null) { e.preventDefault(); select(tabs[n], true); }
    });
  });
  const fromHash = tabs.find((t) => '#' + t.dataset.tab === location.hash);
  if (fromHash) select(fromHash);

  /* ---------- פניות ---------- */
  const allInquiries = () => {
    const site = store.get('ps-inquiries', []);
    const fromSite = (Array.isArray(site) ? site : []).filter((x) => x && x.id && x.branch).map((x) => ({ ...x, fromSite: true }));
    return [...fromSite, ...SEED].map((x) => ({ ...x, status: state.status[x.id] || x.status || 'new', internal: state.notes[x.id] || '' }))
      .sort((a, b) => new Date(b.date) - new Date(a.date));
  };
  const fmtDate = (iso) => {
    try { return new Intl.DateTimeFormat('he-IL', { day: 'numeric', month: 'numeric', hour: '2-digit', minute: '2-digit' }).format(new Date(iso)); } catch (e) { return iso; }
  };
  const q = $('#q'); const fBranch = $('#f-branch'); const fStatus = $('#f-status');
  BRANCHES.forEach((b) => fBranch.insertAdjacentHTML('beforeend', `<option value="${b.id}">${esc(b.name)} · ${esc(b.city)}</option>`));
  STATUSES.forEach(([k, v]) => fStatus.insertAdjacentHTML('beforeend', `<option value="${k}">${esc(v)}</option>`));
  const rowsEl = $('[data-rows]'); const emptyEl = $('[data-empty]'); const resultLine = $('[data-result-line]');
  let current = [];
  const norm = (s) => String(s || '').toLowerCase().replace(/[\s\-()]/g, '');
  function render() {
    const all = allInquiries();
    const counts = { new: 0, contacted: 0, audition: 0, accepted: 0 };
    all.forEach((x) => { if (x.status in counts) counts[x.status]++; });
    Object.entries(counts).forEach(([k, v]) => { $(`[data-stat="${k}"]`).textContent = v; });
    $('[data-new-count]').textContent = counts.new || '';
    const term = norm(q.value);
    current = all.filter((x) => (!fBranch.value || x.branch === fBranch.value) && (!fStatus.value || x.status === fStatus.value)
      && (!term || [x.parent, x.child, x.phone, x.email].some((v) => norm(v).includes(term))));
    $$('[data-status-card]').forEach((c) => c.setAttribute('aria-pressed', String(fStatus.value === c.dataset.statusCard)));
    resultLine.textContent = `מוצגות ${current.length} פניות מתוך ${all.length}`;
    emptyEl.hidden = current.length > 0;
    rowsEl.innerHTML = current.map((x) => {
      const b = branchById(x.branch);
      return `<tr class="${x.status === 'new' ? 'is-new' : ''}" data-id="${esc(x.id)}">
        <td data-label="תאריך">${esc(fmtDate(x.date))}</td>
        <td data-label="הורה"><div class="cell-main">${esc(x.parent)}${x.status === 'new' ? '<span class="tag-new">חדש</span>' : ''}</div>
          <div class="cell-sub"><a href="tel:${esc(x.phone.replace(/[^\d+]/g, ''))}" dir="ltr"><svg class="ico" aria-hidden="true"><use href="#i-phone"/></svg>${esc(x.phone)}</a>
          <a href="mailto:${esc(x.email)}" dir="ltr"><svg class="ico" aria-hidden="true"><use href="#i-mail"/></svg>${esc(x.email)}</a></div></td>
        <td data-label="ילד"><div class="cell-main">${esc(x.child)}, ${esc(x.age)}</div><div class="cell-sub"><span>${esc(x.cheder)} · כיתה ${esc(x.grade)}</span></div>
          ${x.notes ? `<p class="parent-note">״${esc(x.notes)}״</p>` : ''}</td>
        <td data-label="חוג"><div class="cell-main">${esc(b.name)}</div><div class="cell-sub"><span>${esc(b.city)}</span></div></td>
        <td data-label="סטטוס"><label class="sr" for="st-${esc(x.id)}">סטטוס הפנייה של ${esc(x.parent)}</label>
          <select class="status-sel" id="st-${esc(x.id)}" data-status-for="${esc(x.id)}" data-s="${x.status}">${STATUSES.map(([k, v]) => `<option value="${k}"${k === x.status ? ' selected' : ''}>${esc(v)}</option>`).join('')}</select></td>
        <td data-label="הערה פנימית"><label class="sr" for="nt-${esc(x.id)}">הערה פנימית על ${esc(x.parent)}</label>
          <textarea class="note-in" id="nt-${esc(x.id)}" rows="1" data-note-for="${esc(x.id)}" placeholder="למשל: מבדק ביום ג׳">${esc(x.internal)}</textarea></td>
      </tr>`;
    }).join('');
  }
  rowsEl.addEventListener('change', (e) => {
    const s = e.target.closest('[data-status-for]');
    if (s) { state.status[s.dataset.statusFor] = s.value; save(); render(); toast('הסטטוס עודכן: ' + statusLabel[s.value]); }
  });
  rowsEl.addEventListener('input', (e) => {
    const n = e.target.closest('[data-note-for]');
    if (n) { state.notes[n.dataset.noteFor] = n.value; save(); }
  });
  [q, fBranch, fStatus].forEach((el) => el.addEventListener(el === q ? 'input' : 'change', render));
  $$('[data-status-card]').forEach((c) => c.addEventListener('click', () => {
    fStatus.value = fStatus.value === c.dataset.statusCard ? '' : c.dataset.statusCard; render();
  }));
  // ייצוא לאקסל (CSV עם BOM כדי שהעברית תוצג נכון), כולל הגנה מנוסחאות בתאים
  $('[data-export]').addEventListener('click', () => {
    const head = ['תאריך', 'שם ההורה', 'טלפון', 'מייל', 'שם הילד', 'גיל', 'חיידר', 'כיתה', 'חוג', 'סטטוס', 'הערת ההורה', 'הערה פנימית'];
    const cell = (v) => { let s = String(v == null ? '' : v); if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; return '"' + s.replace(/"/g, '""') + '"'; };
    const lines = [head.map(cell).join(',')].concat(current.map((x) => {
      const b = branchById(x.branch);
      return [fmtDate(x.date), x.parent, x.phone, x.email, x.child, x.age, x.cheder, x.grade, `${b.name} · ${b.city}`, statusLabel[x.status], x.notes, x.internal].map(cell).join(',');
    }));
    const blob = new Blob(['﻿' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    // שם באנגלית: חלק מהדפדפנים מתעלמים משם קובץ בעברית בהורדה מהדף
    a.download = `pirchei-shomayim-inquiries-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
    toast(`יוצאו ${current.length} פניות לקובץ אקסל`);
  });
  $('[data-reset]').addEventListener('click', () => {
    store.del('ps-admin-state'); store.del('ps-inquiries'); store.del('ps-subscribers');
    location.reload();
  });

  /* ---------- חוגים ---------- */
  const branchList = $('[data-branch-list]');
  function renderBranches() {
    branchList.innerHTML = BRANCHES.map((raw) => {
      const b = branchById(raw.id);
      return `<li class="card" data-branch="${b.id}">
        <span class="pill">${esc(b.city)}</span>
        <h2>${esc(b.name)}</h2>
        <p class="meta">${esc(b.venue)}</p>
        <p class="meta">גילאים: <bdi>${esc(b.ages)}</bdi> · ימים ושעות: ${esc(b.times)}</p>
        <div class="card-actions"><button type="button" class="btn btn-light" data-edit-branch="${b.id}" aria-expanded="false">עריכה</button></div>
      </li>`;
    }).join('');
  }
  branchList.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-edit-branch]');
    if (!btn) return;
    const card = btn.closest('.card'); const b = branchById(btn.dataset.editBranch);
    const open = card.querySelector('form');
    if (open) { open.remove(); btn.setAttribute('aria-expanded', 'false'); return; }
    btn.setAttribute('aria-expanded', 'true');
    card.insertAdjacentHTML('beforeend', `<form novalidate>
      <label>מקום החוג<input name="venue" value="${esc(b.venue)}" required></label>
      <label>גילאים<input name="ages" value="${esc(b.ages)}" required></label>
      <label>ימים ושעות<input name="times" value="${esc(b.times)}" placeholder="למשל: ימי ב׳, 17:00–18:30"></label>
      <button class="btn btn-primary" type="submit">שמירה</button></form>`);
    card.querySelector('input').focus();
  });
  branchList.addEventListener('submit', (e) => {
    e.preventDefault();
    const form = e.target; const id = form.closest('.card').dataset.branch;
    const v = Object.fromEntries(new FormData(form));
    const bad = ['venue', 'ages'].filter((k) => !String(v[k] || '').trim());
    $$('input', form).forEach((i) => setInvalid(i, bad.includes(i.name)));
    if (bad.length) { form.elements[bad[0]].focus(); return; }
    state.branches[id] = { venue: v.venue.trim(), ages: v.ages.trim(), times: (v.times || '').trim() || 'יעודכן' };
    save(); renderBranches(); render();
    toast('החוג עודכן באתר');
    const b = branchList.querySelector(`[data-edit-branch="${id}"]`); if (b) b.focus();
  });

  /* ---------- הופעות ומאחורי הקלעים ---------- */
  function renderList(kind) {
    const ul = $(`[data-list="${kind}"]`);
    const items = state[kind];
    if (!items.length) { ul.innerHTML = `<li class="card"><p class="meta">${kind === 'shows' ? 'עדיין לא נוספו הופעות. ההופעה הראשונה שתוסיפו תופיע באתר באזור ״ההופעה הבאה״.' : 'עדיין לא נוסף תיעוד. התיעוד הראשון יופיע בראש מדור מאחורי הקלעים.'}</p></li>`; return; }
    ul.innerHTML = items.map((x, i) => kind === 'shows'
      ? `<li class="card"><span class="pill pill-mint">${new Date(x.date) >= new Date(new Date().toDateString()) ? 'הופעה קרובה' : 'הופעה קודמת'}</span><h2>${esc(x.title)}</h2><p class="meta"><bdi>${esc(x.date.split('-').reverse().join('.'))}</bdi>${x.time ? ' · ' + esc(x.time) : ''} · ${esc(x.place)}</p>${x.pdf ? `<p class="meta">מודעה: ${esc(x.pdf)}</p>` : ''}<div class="card-actions"><button type="button" class="btn btn-light" data-remove="${kind}:${i}">הסרה</button></div></li>`
      : `<li class="card">${x.exclusive ? '<span class="pill pill-mint">בלעדי לאתר</span>' : ''}<h2>${esc(x.title)}</h2><p class="meta">${esc(x.text)}</p><div class="card-actions"><button type="button" class="btn btn-light" data-remove="${kind}:${i}">הסרה</button></div></li>`).join('');
  }
  $$('[data-add]').forEach((form) => form.addEventListener('submit', (e) => {
    e.preventDefault();
    const kind = form.dataset.add; const msg = $('.form-msg', form);
    const required = $$('[required]', form);
    const bad = required.filter((el) => !el.value.trim());
    required.forEach((el) => setInvalid(el, bad.includes(el)));
    const link = form.elements.link;
    if (link) setInvalid(link, false);
    if (link && link.value && !/^https?:\/\/\S+$/i.test(link.value.trim())) { bad.push(link); setInvalid(link, true); }
    if (bad.length) { msg.textContent = 'יש למלא את השדות המסומנים'; msg.classList.add('is-error'); bad[0].focus(); return; }
    msg.classList.remove('is-error');
    const v = Object.fromEntries(new FormData(form));
    const item = kind === 'shows'
      ? { title: v.title.trim(), date: v.date, time: v.time, place: v.place.trim(), link: (v.link || '').trim(), pdf: form.elements.pdf.files[0] ? form.elements.pdf.files[0].name : '' }
      : { title: v.title.trim(), text: v.text.trim(), link: (v.link || '').trim(), exclusive: !!form.elements.exclusive.checked };
    state[kind].unshift(item);
    if (kind === 'shows') state.shows.sort((a, b) => b.date.localeCompare(a.date));
    save(); renderList(kind); form.reset();
    if (kind === 'behind') form.elements.exclusive.checked = true;
    msg.textContent = kind === 'shows' ? 'ההופעה נוספה לאתר' : 'התיעוד פורסם באתר';
    toast(msg.textContent);
  }));
  document.addEventListener('click', (e) => {
    const r = e.target.closest('[data-remove]');
    if (!r) return;
    const [kind, i] = r.dataset.remove.split(':');
    state[kind].splice(Number(i), 1); save(); renderList(kind); toast('הפריט הוסר');
  });

  /* ---------- שירים ---------- */
  const songList = $('[data-song-list]');
  function renderSongs() {
    songList.innerHTML = SONGS.map(([id, title, when]) => `<li class="song-row">
      <img src="../../assets/img/covers/${id}-s.webp" alt="" width="360" height="203" loading="lazy">
      <div><b>${esc(title)}</b><small>עלה ליוטיוב ${esc(when)} · נוסף לאתר אוטומטית</small></div>
      <label class="check"><input type="radio" name="featured" value="${id}"${state.featured === id ? ' checked' : ''}> שיר מומלץ</label>
      <label class="check"><input type="checkbox" data-hide="${id}"${state.hiddenSongs.includes(id) ? '' : ' checked'}> מוצג באתר</label>
    </li>`).join('');
  }
  songList.addEventListener('change', (e) => {
    if (e.target.name === 'featured') { state.featured = e.target.value; toast('השיר המומלץ עודכן'); }
    if (e.target.dataset.hide) {
      const id = e.target.dataset.hide;
      state.hiddenSongs = e.target.checked ? state.hiddenSongs.filter((x) => x !== id) : [...state.hiddenSongs, id];
      toast(e.target.checked ? 'השיר מוצג באתר' : 'השיר הוסתר מהאתר');
    }
    save();
  });
  const sync = new Date(); sync.setMinutes(sync.getMinutes() - 12);
  $('[data-sync-time]').textContent = 'סונכרן מהפלייליסט היום ב־' + sync.toTimeString().slice(0, 5);

  render(); renderBranches(); renderList('shows'); renderList('behind'); renderSongs();
  window.addEventListener('storage', (e) => { if (e.key === 'ps-inquiries') render(); });

  /* ======================= מסלול 3: מנויים ודיוור ======================= */
  if (document.body.dataset.plan !== '3') return;
  const TOPICS = { songs: 'שירים חדשים', classes: 'חוגים חדשים', shows: 'הופעות' };
  const SUB_SEED = [
    { id: 'm1', date: daysAgo(1), name: 'משפחת כהן (דוגמה)', email: 'fan1@example.com', topics: ['songs', 'shows'], source: 'club', verified: true },
    { id: 'm2', date: daysAgo(2), name: 'ישראל כהן (דוגמה)', email: 'example1@example.com', topics: ['songs', 'classes', 'shows'], source: 'class', verified: true },
    { id: 'm3', date: daysAgo(4), name: '', email: 'fan3@example.com', topics: ['songs'], source: 'club', verified: true },
    { id: 'm4', date: daysAgo(6), name: 'דוד פרידמן (דוגמה)', email: 'example3@example.com', topics: ['classes'], source: 'class', verified: false },
    { id: 'm5', date: daysAgo(8), name: 'מתנ״ס לדוגמה', email: 'center@example.com', topics: ['shows'], source: 'club', verified: true },
    { id: 'm6', date: daysAgo(11), name: '', email: 'fan6@example.com', topics: ['songs', 'shows'], source: 'club', verified: true },
    { id: 'm7', date: daysAgo(15), name: 'אהרן גרין (דוגמה)', email: 'example5@example.com', topics: ['songs', 'classes'], source: 'class', verified: true },
  ];
  const allSubs = () => {
    const site = store.get('ps-subscribers', []);
    const fromSite = (Array.isArray(site) ? site : []).filter((x) => x && x.email && Array.isArray(x.topics));
    return [...fromSite, ...SUB_SEED].sort((a, b) => new Date(b.date) - new Date(a.date));
  };
  let topicFilter = '';
  let subsView = [];
  const subsBody = $('[data-subs]');
  function renderSubs() {
    const all = allSubs();
    Object.keys(TOPICS).forEach((k) => { $(`[data-topic-count="${k}"]`).textContent = all.filter((s) => s.topics.includes(k)).length; });
    $$('[data-topic-card]').forEach((c) => c.setAttribute('aria-pressed', String(c.dataset.topicCard === topicFilter)));
    subsView = all.filter((s) => !topicFilter || s.topics.includes(topicFilter));
    $('[data-subs-line]').textContent = `מוצגים ${subsView.length} מנויים מתוך ${all.length}`;
    subsBody.innerHTML = subsView.map((s) => `<tr>
      <td data-label="הצטרף">${esc(fmtDate(s.date))}</td>
      <td data-label="שם ומייל"><div class="cell-main">${esc(s.name || '—')}</div><div class="cell-sub"><a href="mailto:${esc(s.email)}" dir="ltr">${esc(s.email)}</a></div></td>
      <td data-label="נושאים"><div class="chips-row">${s.topics.map((k) => `<span class="mini-chip">${esc(TOPICS[k] || k)}</span>`).join('')}</div></td>
      <td data-label="מקור">${s.source === 'class' ? 'טופס החוג' : 'מועדון העדכונים'}</td>
      <td data-label="מצב"><span class="state ${s.verified ? 'ok' : 'wait'}">${s.verified ? 'מאושר' : 'ממתין לאישור המייל'}</span></td>
    </tr>`).join('');
  }
  $$('[data-topic-card]').forEach((c) => c.addEventListener('click', () => { topicFilter = topicFilter === c.dataset.topicCard ? '' : c.dataset.topicCard; renderSubs(); }));
  $('[data-export-subs]').addEventListener('click', () => {
    const cell = (v) => { let s = String(v == null ? '' : v); if (/^[=+\-@\t\r]/.test(s)) s = "'" + s; return '"' + s.replace(/"/g, '""') + '"'; };
    const lines = [['הצטרף', 'שם', 'מייל', 'נושאים', 'מקור', 'מצב'].map(cell).join(',')]
      .concat(subsView.map((s) => [fmtDate(s.date), s.name, s.email, s.topics.map((k) => TOPICS[k]).join(' / '), s.source === 'class' ? 'טופס החוג' : 'מועדון', s.verified ? 'מאושר' : 'ממתין'].map(cell).join(',')));
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob(['﻿' + lines.join('\r\n')], { type: 'text/csv;charset=utf-8' }));
    a.download = `pirchei-shomayim-subscribers-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a); a.click();
    setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1500);
    toast(`יוצאו ${subsView.length} מנויים לקובץ אקסל`);
  });

  /* ---------- דיוור: שלוש תבניות אחידות ---------- */
  const TPL = {
    songs: { tag: 'שיר חדש', cta: 'להאזנה ביוטיוב', fields: [['title', 'שם השיר', true], ['link', 'קישור ליוטיוב', true, 'url'], ['credits', 'קרדיטים (רשות)', false], ['lyrics', 'מילים (רשות)', false, 'textarea']] },
    classes: { tag: 'חוג חדש', cta: 'לפרטים ולהשארת פרטים', fields: [['title', 'שם החוג', true], ['place', 'עיר ומקום', true], ['ages', 'גילאים', true], ['times', 'ימים ושעות', false], ['link', 'קישור להרשמה', false, 'url']] },
    shows: { tag: 'הופעה', cta: 'לפרטים ולהרשמה', fields: [['title', 'שם ההופעה', true], ['date', 'תאריך', true, 'date'], ['time', 'שעה', false, 'time'], ['place', 'מקום', true], ['link', 'קישור להרשמה', false, 'url']] },
  };
  const mailForm = $('[data-mail-form]');
  const fieldsBox = $('[data-tpl-fields]');
  const preview = $('[data-mail-preview]');
  const tplNow = () => mailForm.elements.tpl.value;
  const recipients = (k) => allSubs().filter((s) => s.verified && s.topics.includes(k)).length;
  function buildFields() {
    const t = TPL[tplNow()];
    fieldsBox.innerHTML = t.fields.map(([name, label, req, type]) => `<label class="${type === 'textarea' ? 'wide' : ''}">${esc(label)}${type === 'textarea'
      ? `<textarea name="${name}" rows="3"${req ? ' required' : ''}></textarea>`
      : `<input name="${name}" type="${type || 'text'}"${type === 'url' ? ' dir="ltr" placeholder="https://"' : ''}${req ? ' required' : ''}>`}</label>`).join('');
    $('.form-msg', mailForm).textContent = '';
    updatePreview();
  }
  function updatePreview() {
    const k = tplNow(); const t = TPL[k]; const f = mailForm.elements;
    const v = (n) => (f[n] && f[n].value ? f[n].value.trim() : '');
    const date = v('date') ? v('date').split('-').reverse().join('.') : '';
    const lines = k === 'songs' ? [v('credits'), v('lyrics') ? 'המילים מצורפות במייל' : '']
      : k === 'classes' ? [v('place'), v('ages') ? 'גילאים: ' + v('ages') : '', v('times')]
      : [[date, v('time')].filter(Boolean).join(' · '), v('place')];
    const pdf = f.pdf && f.pdf.files[0] ? f.pdf.files[0].name : '';
    preview.innerHTML = `<div class="mc-head"><img src="../../assets/img/icon-64.png" alt="" width="36" height="36"><b>מקהלת פרחי שמיים</b></div>
      <div class="mc-body"><span class="mc-tag">${esc(t.tag)}</span>
        <h2>${esc(v('title') || 'הכותרת תופיע כאן')}</h2>
        ${lines.filter(Boolean).map((l) => `<p>${esc(l)}</p>`).join('')}
        ${v('lyrics') ? `<p class="mc-lyrics">${esc(v('lyrics'))}</p>` : ''}
        ${pdf ? `<p class="mc-pdf">מצורף: ${esc(pdf)}</p>` : ''}
        <span class="mc-btn">${esc(t.cta)}</span></div>
      <p class="mc-foot">קיבלתם את המייל כי בחרתם בעדכונים על ${esc(TOPICS[k])}. להסרה מהרשימה לחצו כאן.</p>`;
    $('[data-send-label]').textContent = `שליחה ל־${recipients(k)} מנויים`;
  }
  mailForm.addEventListener('change', (e) => { if (e.target.name === 'tpl') buildFields(); else updatePreview(); });
  mailForm.addEventListener('input', updatePreview);
  mailForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const msg = $('.form-msg', mailForm);
    const req = $$('[required]', fieldsBox);
    const bad = req.filter((el) => !el.value.trim());
    $$('input, textarea', fieldsBox).forEach((el) => setInvalid(el, bad.includes(el)));
    $$('input[type="url"]', fieldsBox).forEach((el) => { if (el.value && !/^https?:\/\/\S+$/i.test(el.value.trim())) { bad.push(el); setInvalid(el, true); } });
    if (bad.length) { msg.textContent = 'יש למלא את השדות המסומנים'; msg.classList.add('is-error'); bad[0].focus(); return; }
    msg.classList.remove('is-error');
    const n = recipients(tplNow());
    msg.textContent = `העדכון נשלח ל־${n} מנויים (בהדגמה לא נשלח מייל).`;
    toast(msg.textContent);
  });
  buildFields(); renderSubs();
  window.addEventListener('storage', (e) => { if (e.key === 'ps-subscribers') { renderSubs(); updatePreview(); } });
})();
