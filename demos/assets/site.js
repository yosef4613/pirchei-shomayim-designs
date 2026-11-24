/* פרחי שמיים · הדגמת מסלול 2 — התנהגות העמוד */
(() => {
  'use strict';
  const doc = document.documentElement;
  const data = JSON.parse(document.getElementById('page-data').textContent);
  const T = data.js;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const fill = (s, o) => s.replace(/\{(\w+)\}/g, (_, k) => (o[k] != null ? o[k] : ''));
  const motionOn = () => doc.dataset.motion !== 'reduce';
  const pageStart = Date.now(); // טופס שנשלח תוך שנייה מהטעינה הוא כמעט תמיד רובוט
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); return true; } catch (e) { return false; } },
  };
  const escapeHtml = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  /* ---------- הפחתת תנועה ---------- */
  const motionBtn = $('[data-motion-toggle]');
  const syncMotionBtn = () => {
    if (!motionBtn) return;
    const reduced = !motionOn();
    motionBtn.setAttribute('aria-pressed', String(reduced));
    const label = reduced ? data.motionOn : data.motionOff;
    motionBtn.setAttribute('aria-label', label);
    motionBtn.title = label;
  };
  syncMotionBtn();
  motionBtn && motionBtn.addEventListener('click', () => {
    doc.dataset.motion = motionOn() ? 'reduce' : 'full';
    store.set('ps-motion', doc.dataset.motion);
    syncMotionBtn();
    document.dispatchEvent(new CustomEvent('motionchange'));
  });

  /* ---------- כותרת ותפריט ---------- */
  const header = $('.site-header');
  const onScrollHeader = () => header.classList.toggle('is-solid', window.scrollY > 30 || header.classList.contains('menu-open'));
  onScrollHeader();
  window.addEventListener('scroll', onScrollHeader, { passive: true });
  const menuBtn = $('[data-menu-toggle]');
  const setMenu = (open) => {
    header.classList.toggle('menu-open', open);
    menuBtn.setAttribute('aria-expanded', String(open));
    document.body.classList.toggle('is-locked', open);
    onScrollHeader();
  };
  menuBtn.addEventListener('click', () => setMenu(!header.classList.contains('menu-open')));
  $$('.main-nav a').forEach((a) => a.addEventListener('click', () => setMenu(false)));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && header.classList.contains('menu-open')) { setMenu(false); menuBtn.focus(); } });
  window.matchMedia('(min-width: 1181px)').addEventListener('change', (e) => { if (e.matches) setMenu(false); });

  /* כלל המדגש: כפתור טורקיז אחד בכל מסך. כפתור הכותרת נדלק רק כשאין כפתור טורקיז אחר בתצוגה */
  const headCta = $('.header-cta');
  if (headCta && 'IntersectionObserver' in window) {
    const inView = new Set();
    const mio = new IntersectionObserver((entries) => {
      entries.forEach((en) => (en.isIntersecting ? inView.add(en.target) : inView.delete(en.target)));
      headCta.classList.toggle('is-quiet', inView.size > 0);
    });
    $$('.btn-mint').forEach((b) => { if (b !== headCta) mio.observe(b); });
  } else if (headCta) headCta.classList.remove('is-quiet');

  /* קישור השפה שומר על המקום בעמוד */
  $$('[data-lang-link]').forEach((a) => a.addEventListener('click', () => {
    if (location.hash) a.href = a.getAttribute('href').split('#')[0] + location.hash;
  }));

  /* ---------- פתיחה: גלריית במה מתחלפת בעדינות ---------- */
  const slides = $$('.hero-slide');
  let slideIdx = 0; let slideTimer = null;
  const loadSlides = () => slides.forEach((p) => {
    $$('[data-srcset]', p).forEach((s) => { s.srcset = s.dataset.srcset; s.removeAttribute('data-srcset'); });
    $$('img[data-src]', p).forEach((i) => { i.src = i.dataset.src; i.removeAttribute('data-src'); });
  });
  const runSlides = () => {
    clearInterval(slideTimer); slideTimer = null;
    if (!motionOn() || slides.length < 2) return;
    slideTimer = setInterval(() => {
      if (document.hidden) return;
      slides[slideIdx].classList.remove('is-active');
      slideIdx = (slideIdx + 1) % slides.length;
      slides[slideIdx].classList.add('is-active');
    }, 7000);
  };
  window.addEventListener('load', () => { loadSlides(); runSlides(); });
  document.addEventListener('motionchange', runSlides);

  /* ---------- מציאת חוג ---------- */
  const cards = $$('[data-branch-card]');
  const cityBtns = $$('.city-filter [data-city]');
  const branchSelect = $('#f-branch');
  const stepper = $$('.stepper li');
  const setStep = (n) => stepper.forEach((li, i) => { li.classList.toggle('is-current', i === n); li.classList.toggle('is-done', i < n); });
  cityBtns.forEach((b) => b.addEventListener('click', () => {
    cityBtns.forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    const c = b.dataset.city;
    cards.forEach((card) => { card.hidden = !(c === 'all' || card.dataset.city === c); });
  }));
  const markSelected = (id) => {
    cards.forEach((card) => {
      const on = card.dataset.branchCard === id;
      card.classList.toggle('is-selected', on);
      const btn = $('.branch-choose', card);
      btn.setAttribute('aria-pressed', String(on));
      $('.choose-label', btn).textContent = on ? data.chosen : data.choose;
    });
    setStep(id ? 1 : 0);
  };
  $$('[data-choose]').forEach((btn) => btn.addEventListener('click', () => {
    const id = btn.dataset.choose;
    branchSelect.value = id;
    clearError(branchSelect);
    markSelected(id);
    showForm();
    const area = $('#join-form-area');
    area.scrollIntoView({ behavior: motionOn() ? 'smooth' : 'auto', block: 'start' });
    setTimeout(() => $('#f-parent').focus({ preventScroll: true }), motionOn() ? 450 : 0);
  }));
  branchSelect.addEventListener('change', () => { markSelected(branchSelect.value); clearError(branchSelect); });
  // הגעה מעמוד החוגים (‎?branch=…) — החוג כבר נבחר בטופס
  const qBranch = new URLSearchParams(location.search).get('branch');
  if (qBranch && data.branches.some((x) => x.id === qBranch)) {
    branchSelect.value = qBranch; markSelected(qBranch);
    try { history.replaceState(null, '', location.pathname + location.hash); } catch (err) { /* לא קריטי */ }
  }

  /* ---------- בדיקת גיל מהירה: תשובה מיידית, עוד לפני שמשאירים פרטים ---------- */
  const fitBtns = $$('.fit-age');
  const fitOut = $('[data-fit-result]');
  const formFit = $('[data-form-fit]');
  fitBtns.forEach((b) => b.addEventListener('click', () => {
    const n = Number(b.dataset.age);
    const ok = n >= 8 && n <= 12;
    fitBtns.forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    const msg = ok ? fill(data.fit.ok, { n }) : (n < 8 ? data.fit.young : data.fit.old);
    // התשובה מופיעה גם כאן וגם בראש הטופס, ומשם ממשיכים ישר להרשמה
    [fitOut, formFit].forEach((el) => {
      if (!el) return;
      el.textContent = msg; el.hidden = false;
      el.classList.toggle('is-ok', ok); el.classList.toggle('is-out', !ok);
    });
    const age = $('#f-age');
    if (ok && age) { age.value = n; clearError(age); }
    showForm();
    $('#join-form-area').scrollIntoView({ behavior: motionOn() ? 'smooth' : 'auto', block: 'start' });
    setTimeout(() => (branchSelect.value ? $('#f-parent') : branchSelect).focus({ preventScroll: true }), motionOn() ? 450 : 0);
  }));

  /* ---------- הטופס ---------- */
  const form = $('#join-form');
  const success = $('#join-success');
  const summary = $('.form-error-summary', form);
  const fields = ['branch', 'parent', 'phone', 'email', 'child', 'age', 'cheder', 'grade', 'consent'].map((n) => form.elements[n]);
  const errorEl = (input) => document.getElementById('e-' + input.name);
  function setError(input, msg) { input.setAttribute('aria-invalid', 'true'); errorEl(input).textContent = msg; }
  function clearError(input) { input.removeAttribute('aria-invalid'); const e = errorEl(input); if (e) e.textContent = ''; }
  const validators = {
    branch: (v) => (v ? '' : T.branch),
    email: (v) => (!v ? T.required : /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? '' : T.email),
    phone: (v) => { const d = v.replace(/[\s\-().+]/g, ''); return !v ? T.required : /^\d{9,12}$/.test(d) ? '' : T.phone; },
    age: (v) => { const n = Number(v); return v === '' ? T.required : Number.isInteger(n) && n >= 5 && n <= 16 ? '' : T.age; },
    consent: (_, el) => (el.checked ? '' : T.consent),
  };
  const validate = (input) => {
    const v = (input.value || '').trim();
    const msg = validators[input.name] ? validators[input.name](v, input) : (v ? '' : T.required);
    if (msg) setError(input, msg); else clearError(input);
    return !msg;
  };
  fields.forEach((input) => {
    const ev = input.type === 'checkbox' || input.tagName === 'SELECT' ? 'change' : 'blur';
    input.addEventListener(ev, () => { if (input.getAttribute('aria-invalid') === 'true' || ev === 'change') validate(input); });
    input.addEventListener('input', () => { if (input.getAttribute('aria-invalid') === 'true') validate(input); });
  });
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    if (form.elements.website.value) return; // מלכודת לרובוטים
    const bad = fields.filter((f) => !validate(f));
    if (bad.length) {
      summary.hidden = false;
      summary.textContent = fill(T.summary, { n: bad.length });
      bad[0].focus();
      return;
    }
    summary.hidden = true;
    const val = (n) => form.elements[n].value.trim();
    const b = data.branches.find((x) => x.id === val('branch'));
    const entry = {
      id: 'w' + Date.now(), date: new Date().toISOString(), lang: data.lang,
      branch: b.id, parent: val('parent'), phone: val('phone'), email: val('email'),
      child: val('child'), age: Number(val('age')), cheder: val('cheder'), grade: val('grade'), notes: val('notes'), status: 'new',
    };
    const branchLabel = fill(T.branchFormat, { name: b.name, city: data.cities[b.city] });
    // מסלול 1: בלי שרת — פותחים את תוכנת המייל עם הודעה מוכנה למקהלה
    if (data.form === 'email') {
      const E = data.emailForm; const L = E.labels;
      const body = [E.intro, '', `${L.parent}: ${entry.parent}`, `${L.phone}: ${entry.phone}`, `${L.email}: ${entry.email}`, `${L.child}: ${entry.child}`, `${L.age}: ${entry.age}`, `${L.cheder}: ${entry.cheder}`, `${L.grade}: ${entry.grade}`]
        .concat(entry.notes ? [`${L.notes}: ${entry.notes}`] : []).join('\n');
      const href = `mailto:${data.choirEmail}?subject=${encodeURIComponent(fill(E.subject, { branch: branchLabel, child: entry.child }))}&body=${encodeURIComponent(body)}`;
      renderEmailSuccess(href);
      try { window.location.href = href; } catch (err) { /* הקישור בהודעה נשאר זמין */ }
      return;
    }
    // באתר החי: שליחה אמיתית לשרת. לא שומרים פרטים אישיים בדפדפן
    if (data.live) { sendLive(entry, branchLabel); return; }
    let list = [];
    try { list = JSON.parse(store.get('ps-inquiries') || '[]'); if (!Array.isArray(list)) list = []; } catch (err) { list = []; }
    list.unshift(entry);
    store.set('ps-inquiries', JSON.stringify(list.slice(0, 50)));
    // מסלול 3: אותו טופס פותח גם חשבון ועדכונים, רק אם ההורה בחר בכך
    let joined = false;
    const acc = form.elements.account;
    if (acc && acc.checked) {
      const topics = $$('[name="a-topic"]:checked', form).map((x) => x.value);
      if (topics.length) { addSubscriber({ name: entry.parent, email: entry.email, topics, source: 'class' }); joined = true; }
    }
    renderSuccess(entry, branchLabel, b, joined);
  });
  function renderSuccess(entry, branchLabel, b, joined) {
    const vars = { parent: escapeHtml(entry.parent), child: escapeHtml(entry.child), branch: escapeHtml(branchLabel), reg: escapeHtml(b.reg) };
    const lines = T.emailLines.map((l, i) => `<p${i === 0 ? ' style="font-weight:700"' : ''}>${fill(l, vars)}</p>`).join('');
    const extra = joined ? `<p class="email-extra">${escapeHtml(data.account.successExtra)}</p><span class="email-btn">${escapeHtml(data.account.confirm)}</span>` : '';
    success.innerHTML = `
      <div class="success-head"><span class="success-ico"><svg class="ico" aria-hidden="true"><use href="#i-check"/></svg></span>
        <div><h3>${fill(T.successTitle, vars)}</h3><p>${fill(T.successText, vars)}</p></div></div>
      <div><p class="email-label">${T.emailLabel}</p>
        <div class="email-preview">
          <div class="email-meta"><span><b>${T.emailFrom}</b></span><span>${T.emailSubject}</span></div>
          <div class="email-body"><div class="email-brand"><img src="${data.assetBase}img/icon-64.png" alt="" width="34" height="34">${T.emailFrom}</div>${lines}${extra}</div>
        </div></div>
      <div class="success-actions">
        <a class="btn btn-purple" href="${data.adminHref}">${T.toAdmin}</a>
        <button type="button" class="btn btn-outline" data-again>${T.again}</button>
      </div>`;
    showSuccess();
  }
  /* ---------- שליחה לשרת (האתר החי) ---------- */
  async function postJSON(path, body) {
    const res = await fetch(data.endpoint + path, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body), credentials: 'omit' });
    let json = null;
    try { json = await res.json(); } catch (err) { json = null; }
    if (!res.ok || !json || !json.ok) { const er = new Error('send'); er.status = res.status; throw er; }
    return json;
  }
  const busy = (btn, on) => { btn.disabled = on; btn.setAttribute('aria-busy', String(on)); };
  async function sendLive(entry, branchLabel) {
    const btn = $('button[type="submit"]', form);
    const acc = form.elements.account;
    const topics = acc && acc.checked ? $$('[name="a-topic"]:checked', form).map((x) => x.value) : [];
    busy(btn, true);
    try {
      await postJSON('inquiry', {
        branch: entry.branch, parent: entry.parent, phone: entry.phone, email: entry.email, child: entry.child,
        age: entry.age, cheder: entry.cheder, grade: entry.grade, notes: entry.notes, consent: true, topics,
        lang: data.lang, t: Date.now() - pageStart, website: form.elements.website.value,
      });
      renderLiveSuccess(entry, branchLabel, topics.length > 0);
    } catch (err) {
      summary.hidden = false;
      summary.textContent = err.status === 429 ? T.tooMany : fill(T.sendError, { email: data.choirEmail });
    } finally { busy(btn, false); }
  }
  function renderLiveSuccess(entry, branchLabel, joined) {
    const vars = { parent: escapeHtml(entry.parent), child: escapeHtml(entry.child), branch: escapeHtml(branchLabel), email: `<bdi>${escapeHtml(entry.email)}</bdi>` };
    success.innerHTML = `
      <div class="success-head"><span class="success-ico"><svg class="ico" aria-hidden="true"><use href="#i-check"/></svg></span>
        <div><h3>${fill(T.successTitle, vars)}</h3><p>${fill(T.successText, vars)}</p></div></div>
      <div class="live-note"><p>${fill(T.liveSent, vars)}</p>${joined ? `<p>${escapeHtml(data.account.successExtra)}</p>` : ''}<p class="live-hint">${escapeHtml(T.spamHint)}</p></div>
      <div class="success-actions"><button type="button" class="btn btn-outline" data-again>${T.again}</button></div>`;
    showSuccess();
  }
  function renderEmailSuccess(href) {
    const E = data.emailForm;
    success.innerHTML = `
      <div class="success-head"><span class="success-ico"><svg class="ico" aria-hidden="true"><use href="#i-mail"/></svg></span>
        <div><h3>${escapeHtml(E.successTitle)}</h3><p>${escapeHtml(E.successText)}</p></div></div>
      <div class="success-actions">
        <a class="btn btn-purple" data-mailto href="${escapeHtml(href)}">${escapeHtml(E.reopen)}</a>
        <button type="button" class="btn btn-outline" data-again>${T.again}</button>
      </div>`;
    showSuccess();
  }
  function addSubscriber(s) {
    let subs = [];
    try { subs = JSON.parse(store.get('ps-subscribers') || '[]'); if (!Array.isArray(subs)) subs = []; } catch (err) { subs = []; }
    subs = subs.filter((x) => x.email !== s.email);
    subs.unshift({ id: 'c' + Date.now(), date: new Date().toISOString(), verified: false, ...s });
    store.set('ps-subscribers', JSON.stringify(subs.slice(0, 100)));
  }
  function showSuccess() {
    form.hidden = true;
    success.hidden = false;
    setStep(2);
    success.focus({ preventScroll: true });
    success.scrollIntoView({ behavior: motionOn() ? 'smooth' : 'auto', block: 'start' });
    $('[data-again]', success).addEventListener('click', () => {
      form.reset(); fields.forEach(clearError); markSelected(''); if (formFit) formFit.hidden = true;
      if (accountTopicsBox()) accountTopicsBox().hidden = true;
      success.hidden = true; success.innerHTML = ''; form.hidden = false;
      $('#form-title').focus();
    });
  }
  function showForm() { if (!success.hidden) { success.hidden = true; form.hidden = false; } }
  function accountTopicsBox() { return document.querySelector('[data-account-topics]'); }

  /* ---------- הופעה הדרגתית ומספרים רצים ---------- */
  const io = 'IntersectionObserver' in window ? new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add('is-visible');
      const c = en.target.querySelector('[data-count]');
      if (c) countUp(c);
      io.unobserve(en.target);
    });
  }, { rootMargin: '0px 0px -18% 0px', threshold: 0.15 }) : null;
  $$('[data-reveal]').forEach((el) => (io ? io.observe(el) : el.classList.add('is-visible')));
  function countUp(el) {
    const end = Number(el.dataset.count); const suf = el.dataset.suffix || '';
    if (!motionOn()) { el.textContent = end + suf; return; }
    const t0 = performance.now(); const dur = 1400;
    const tick = (now) => {
      const p = Math.min(1, (now - t0) / dur); const e = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(end * e) + suf;
      if (p < 1) requestAnimationFrame(tick);
    };
    el.textContent = '0' + suf;
    requestAnimationFrame(tick);
  }

  /* ---------- המסע: קו הקול מצטייר לפי הגלילה ---------- */
  const journey = $('[data-journey]');
  const steps = $$('.journey-step');
  const updateJourney = () => {
    if (!journey) return;
    let p;
    if (!motionOn()) p = 1;
    else {
      const r = journey.getBoundingClientRect(); const vh = window.innerHeight;
      p = (vh * 0.7 - r.top) / (r.height + vh * 0.15);
      p = Math.max(0, Math.min(1, p));
    }
    journey.style.setProperty('--p', p.toFixed(4));
    const steps2 = $('.journey-steps');
    if (steps2) steps2.style.setProperty('--p', p.toFixed(4));
    steps.forEach((s, i) => s.classList.toggle('is-on', p >= (i + 0.35) / steps.length || p >= 0.999));
  };

  /* ---------- מאחורי הקלעים: רצועה אופקית במחשב ---------- */
  const strip = $('[data-strip]');
  const track = strip && $('.strip-track', strip);
  const stickyEl = strip && $('.strip-sticky', strip);
  const desktop = window.matchMedia('(min-width: 901px) and (hover: hover)');
  let overflow = 0;
  const setupStrip = () => {
    if (!strip) return;
    const pin = desktop.matches && motionOn();
    strip.classList.toggle('is-pinned', pin);
    if (!pin) { strip.style.height = ''; track.style.removeProperty('--tx'); return; }
    overflow = Math.max(0, track.scrollWidth - stickyEl.clientWidth);
    if (overflow < 40) { strip.classList.remove('is-pinned'); strip.style.height = ''; return; }
    strip.style.height = (window.innerHeight + overflow) + 'px';
    updateStrip();
  };
  const updateStrip = () => {
    if (!strip || !strip.classList.contains('is-pinned')) return;
    const r = strip.getBoundingClientRect();
    const total = strip.offsetHeight - window.innerHeight;
    const p = total > 0 ? Math.max(0, Math.min(1, -r.top / total)) : 0;
    const dir = doc.dir === 'rtl' ? 1 : -1;
    track.style.setProperty('--tx', (dir * p * overflow).toFixed(1) + 'px');
  };

  /* ---------- מקהלולם: קריאה ותשובה בזמן שהאזור נראה ---------- */
  const cr = $('.cr');
  if (cr) {
    $$('.cr-dots', cr).forEach((row) => $$('i', row).forEach((d, i) => d.style.setProperty('--i', i)));
    if ('IntersectionObserver' in window) {
      new IntersectionObserver((en) => en.forEach((x) => cr.classList.toggle('is-playing', x.isIntersecting)), { threshold: 0.3 }).observe(cr);
    }
  }

  /* מסלול 3: פעמוני העדכונים מצלצלים רק כשהאזור נראה */
  const clubSec = $('.club');
  if (clubSec && 'IntersectionObserver' in window) {
    new IntersectionObserver((en) => en.forEach((x) => clubSec.classList.toggle('is-in', x.isIntersecting)), { threshold: 0.25 }).observe(clubSec);
  }

  /* ---------- למטה בעמוד: וילון שנפתח, זרקורים שמתכנסים, עומק בתמונות הבמה ---------- */
  const curtain = $('[data-curtain]');
  const behindSec = curtain && curtain.closest('section');
  const finalSec = $('.final');
  const showImgs = $$('.show img');
  const clamp01 = (v) => Math.max(0, Math.min(1, v));
  const ease = (x) => x * x * (3 - 2 * x);
  // הזרקורים מכוונים בדיוק אל כפתור הסיום, בכל גודל מסך
  const aimBeams = () => {
    if (!finalSec) return;
    const cta = $('.btn', finalSec); if (!cta) return;
    const sr = finalSec.getBoundingClientRect(); const cr = cta.getBoundingClientRect();
    const tx = cr.left + cr.width / 2 - sr.left; const ty = cr.top + cr.height / 2 - sr.top;
    $$('.final-beam', finalSec).forEach((bm) => {
      const a1 = -Math.atan2(tx - (bm.offsetLeft + bm.offsetWidth / 2), ty - bm.offsetTop) * 180 / Math.PI;
      bm.style.setProperty('--a1', a1.toFixed(1) + 'deg');
      bm.style.setProperty('--a0', (a1 + (a1 < 0 ? 58 : -58)).toFixed(1) + 'deg');
    });
  };
  const updateLower = () => {
    const vh = window.innerHeight; const on = motionOn();
    // קודם קוראים את כל המידות, ורק אחר כך כותבים, כדי לא לאלץ חישוב פריסה חוזר
    const bTop = curtain ? behindSec.getBoundingClientRect().top : 0;
    const fTop = finalSec ? finalSec.getBoundingClientRect().top : 0;
    const shows = showImgs.map((img) => img.parentElement.getBoundingClientRect());
    if (curtain) {
      // הווילון נשאר סגור עד שהוא תופס חלק נכבד מהמסך, ונפתח לאט לאורך גלילה ארוכה — עד שהאזור מגיע לראש המסך
      const x = clamp01((vh * 0.72 - bTop) / (vh * 0.72));
      const open = on ? x * x * x * (x * (x * 6 - 15) + 10) : 1;
      curtain.style.setProperty('--open', open.toFixed(4));
      curtain.classList.toggle('is-open', open > 0.995);
    }
    if (finalSec) {
      if (on) finalSec.style.setProperty('--p', ease(clamp01((vh * 0.78 - fTop) / (vh * 0.4))).toFixed(4));
      else finalSec.style.removeProperty('--p');
    }
    showImgs.forEach((img, i) => {
      const r = shows[i];
      if (!on) { img.style.removeProperty('--py'); return; }
      if (r.bottom < -100 || r.top > vh + 100) return;
      img.style.setProperty('--py', (((r.top + r.height / 2) - vh / 2) / vh * -14).toFixed(2) + '%');
    });
  };

  /* ---------- גלילה אחת לכל האפקטים ---------- */
  let ticking = false;
  const onScroll = () => {
    if (ticking) return; ticking = true;
    requestAnimationFrame(() => { updateJourney(); updateStrip(); updateLower(); ticking = false; });
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  let rT;
  window.addEventListener('resize', () => { clearTimeout(rT); rT = setTimeout(() => { setupStrip(); updateJourney(); aimBeams(); updateLower(); }, 120); });
  window.addEventListener('load', () => { setupStrip(); updateJourney(); aimBeams(); updateLower(); });
  document.addEventListener('motionchange', () => { setupStrip(); updateJourney(); updateLower(); });
  updateJourney(); aimBeams(); updateLower();

  /* ---------- ספריית השירים: נפתחת בלחיצה, כדי שהדף יישאר קצר וקל ---------- */
  const library = $('#library');
  const libOpenBtn = $('[data-library-open]');
  const setLock = () => document.body.classList.toggle('is-locked',
    header.classList.contains('menu-open') || (library && !library.hidden) || !$('#player').hidden);
  let libReturn = null;
  if (library && libOpenBtn) {
    const songs = $$('.song', library);
    const countEl = $('[data-song-count]', library);
    const emptyEl = $('.songs-empty', library);
    const search = $('#song-search');
    let filter = 'all';
    const norm = (s) => s.toLowerCase().replace(/[֑-ׇ]/g, '').replace(/[׳'’"״.,:·\-–—()]/g, ' ').replace(/\s+/g, ' ').trim();
    const applySongs = () => {
      const q = norm(search.value || '');
      let n = 0;
      songs.forEach((li) => {
        const match = (filter === 'all' || li.dataset.cat === filter) && (!q || norm(li.dataset.title).includes(q));
        li.hidden = !match;
        if (match) n++;
      });
      countEl.textContent = fill(data.music.count, { n });
      emptyEl.hidden = n !== 0;
    };
    $$('[data-filter]', library).forEach((b) => b.addEventListener('click', () => {
      filter = b.dataset.filter;
      $$('[data-filter]', library).forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
      applySongs();
    }));
    search.addEventListener('input', applySongs);
    const openLibrary = () => {
      // התמונות נטענות רק עכשיו, בפתיחה הראשונה
      $$('img[data-src]', library).forEach((i) => { i.src = i.dataset.src; i.removeAttribute('data-src'); });
      libReturn = document.activeElement;
      library.hidden = false; setLock(); applySongs();
      library.scrollTop = 0; $('.library-in', library).scrollTop = 0;
      search.focus({ preventScroll: true });
    };
    const closeLibrary = () => {
      if (library.hidden) return;
      library.hidden = true; setLock();
      if (libReturn && document.contains(libReturn)) libReturn.focus();
    };
    libOpenBtn.addEventListener('click', openLibrary);
    $('[data-library-close]', library).addEventListener('click', closeLibrary);
    library.addEventListener('click', (e) => { if (e.target === library) closeLibrary(); });
    library.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && $('#player').hidden) { e.preventDefault(); closeLibrary(); return; }
      if (e.key !== 'Tab' || !$('#player').hidden) return;
      const f = $$('button:not([hidden]), input, a[href]', library).filter((el) => el.offsetParent !== null);
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    });
  }

  /* ---------- מסלול 3: חשבון ועדכונים בטופס החוג ---------- */
  const accountBox = form.elements.account;
  const accountTopics = $('[data-account-topics]');
  if (accountBox && accountTopics) {
    accountBox.addEventListener('change', () => { accountTopics.hidden = !accountBox.checked; });
  }

  /* ---------- מסלול 3: מועדון העדכונים ---------- */
  const clubForm = $('#club-form');
  const clubSuccess = $('#club-success');
  if (clubForm && clubSuccess) {
    const C = data.club;
    const cErr = (id, msg, el) => { $('#' + id).textContent = msg; if (el) { if (msg) el.setAttribute('aria-invalid', 'true'); else el.removeAttribute('aria-invalid'); } };
    clubForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const email = clubForm.elements.email; const consent = clubForm.elements.consent;
      const topics = $$('[name="c-topic"]:checked', clubForm).map((x) => x.value);
      const emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email.value.trim());
      cErr('ce-email', email.value.trim() ? (emailOk ? '' : T.email) : T.required, email);
      cErr('ce-topics', topics.length ? '' : C.errTopics);
      cErr('ce-consent', consent.checked ? '' : T.consent, consent);
      const firstBad = !emailOk ? email : !topics.length ? $('[name="c-topic"]', clubForm) : !consent.checked ? consent : null;
      if (firstBad) { firstBad.focus(); return; }
      const name = clubForm.elements.name.value.trim();
      if (data.live) { liveClub(name, email, topics); return; }
      addSubscriber({ name, email: email.value.trim(), topics, source: 'club' });
      const topicNames = topics.map((k) => data.topics[k]).join(data.lang === 'he' ? ', ' : ', ');
      const lines = C.emailLines.map((l, i) => `<p${i === 0 ? ' style="font-weight:700"' : ''}>${fill(l, { name: name ? ' ' + escapeHtml(name) : '', topics: escapeHtml(topicNames) })}</p>`).join('');
      clubSuccess.innerHTML = `
        <div class="success-head"><span class="success-ico"><svg class="ico" aria-hidden="true"><use href="#i-check"/></svg></span>
          <div><h3>${escapeHtml(C.successTitle)}</h3><p>${fill(escapeHtml(C.successText), { email: escapeHtml(email.value.trim()) })}</p></div></div>
        <div class="email-preview"><div class="email-meta"><span><b>${T.emailFrom}</b></span><span>${escapeHtml(C.emailSubject)}</span></div>
          <div class="email-body"><div class="email-brand"><img src="${data.assetBase}img/icon-64.png" alt="" width="34" height="34">${T.emailFrom}</div>${lines}<span class="email-btn">${escapeHtml(data.account.confirm)}</span></div></div>
        <div class="success-actions">${data.adminHref ? `<a class="btn btn-purple" href="${data.adminHref}#subscribers">${escapeHtml(data.lang === 'he' ? 'צפייה בלוח הניהול' : 'View in the admin area')}</a>` : ''}<button type="button" class="btn btn-outline" data-club-again>${escapeHtml(C.again)}</button></div>`;
      clubForm.hidden = true; clubSuccess.hidden = false; clubSuccess.focus({ preventScroll: true });
      $('[data-club-again]', clubSuccess).addEventListener('click', () => {
        clubForm.reset(); ['ce-email', 'ce-topics', 'ce-consent'].forEach((id) => cErr(id, ''));
        $$('[aria-invalid]', clubForm).forEach((x) => x.removeAttribute('aria-invalid'));
        clubSuccess.hidden = true; clubSuccess.innerHTML = ''; clubForm.hidden = false; email.focus();
      });
    });
    // באתר החי: הרשמה אמיתית, עם מייל לאישור הכתובת
    const showClubMessage = (title, text) => {
      clubSuccess.innerHTML = `
        <div class="success-head"><span class="success-ico"><svg class="ico" aria-hidden="true"><use href="#i-check"/></svg></span>
          <div><h3>${title}</h3><p>${text}</p></div></div>
        <div class="success-actions"><button type="button" class="btn btn-outline" data-club-again>${escapeHtml(C.again)}</button></div>`;
      clubForm.hidden = true; clubSuccess.hidden = false; clubSuccess.focus({ preventScroll: true });
      $('[data-club-again]', clubSuccess).addEventListener('click', () => {
        clubForm.reset(); ['ce-email', 'ce-topics', 'ce-consent'].forEach((id) => cErr(id, ''));
        clubSuccess.hidden = true; clubSuccess.innerHTML = ''; clubForm.hidden = false; clubForm.elements.email.focus();
      });
    };
    async function liveClub(name, email, topics) {
      const btn = $('button[type="submit"]', clubForm);
      busy(btn, true);
      try {
        await postJSON('subscribe', { name, email: email.value.trim(), topics, consent: true, lang: data.lang, t: Date.now() - pageStart, website: clubForm.elements.website.value });
        showClubMessage(escapeHtml(C.successTitle), `${fill(escapeHtml(C.successText), { email: `<bdi>${escapeHtml(email.value.trim())}</bdi>` })} ${escapeHtml(T.spamHint)}`);
      } catch (err) {
        cErr('ce-email', err.status === 429 ? T.tooMany : fill(T.sendError, { email: data.choirEmail }));
      } finally { busy(btn, false); }
    }
    // חזרה מקישור האישור שבמייל
    if (data.live && /[?&]subscribed=1\b/.test(location.search)) {
      showClubMessage(escapeHtml(T.confirmed), '');
      try { history.replaceState(null, '', location.pathname + '#club'); } catch (err) { /* לא קריטי */ }
      setTimeout(() => $('#club').scrollIntoView({ block: 'start' }), 300);
    }
  }

  /* הטיה עדינה של כרטיס השיר מול העכבר */
  if (window.matchMedia('(hover: hover)').matches) {
    $$('.song-btn').forEach((btn) => {
      const cover = $('.song-cover', btn);
      btn.addEventListener('pointermove', (e) => {
        if (!motionOn()) return;
        const r = cover.getBoundingClientRect();
        const x = (e.clientX - r.left) / r.width - 0.5; const y = (e.clientY - r.top) / r.height - 0.5;
        cover.style.setProperty('--ry', (x * 10).toFixed(2) + 'deg');
        cover.style.setProperty('--rx', (-y * 8).toFixed(2) + 'deg');
      });
      btn.addEventListener('pointerleave', () => { cover.style.removeProperty('--rx'); cover.style.removeProperty('--ry'); });
    });
  }

  /* ---------- נגן במסך מלא ---------- */
  const player = $('#player');
  const frame = $('[data-player-frame]', player);
  const titleEl = $('#player-title');
  const ytLink = $('[data-player-yt]', player);
  const bgImg = $('[data-player-bg]', player);
  const catEl = $('[data-player-cat]', player);
  const durEl = $('[data-player-dur]', player);
  const aboutEl = $('[data-player-about]', player);
  const countEl = $('[data-player-count]', player);
  const toastEl = $('[data-player-toast]', player);
  const queueEl = $('[data-player-queue]', player);
  const upNextBox = $('[data-player-upnext]', player);
  const shortIds = new Set(data.vertical || []);
  let queue = []; let qi = 0; let lastFocus = null;
  const coverFor = (id) => (shortIds.has(id) ? `img/shorts/${id}.webp` : `img/covers/${id}.webp`);
  const assetBase = data.assetBase;
  function load(id) {
    const vertical = shortIds.has(id);
    frame.classList.toggle('is-vertical', vertical);
    frame.innerHTML = '';
    const ifr = document.createElement('iframe');
    ifr.src = `https://www.youtube-nocookie.com/embed/${encodeURIComponent(id)}?autoplay=1&rel=0&modestbranding=1&playsinline=1&hl=${data.lang}`;
    ifr.title = data.videos[id] || data.player.label;
    ifr.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    ifr.allowFullscreen = true;
    ifr.referrerPolicy = 'strict-origin-when-cross-origin';
    frame.appendChild(ifr);
    titleEl.textContent = data.videos[id] || '';
    ytLink.href = vertical ? `https://www.youtube.com/shorts/${id}` : `https://www.youtube.com/watch?v=${id}`;
    bgImg.src = assetBase + coverFor(id);
    // פרטי השיר: סוג, משך, תיאור קצר ומיקום ברשימה
    const [cat, dur] = (data.meta && data.meta[id]) || ['', ''];
    const P = data.player;
    catEl.textContent = (cat && P.cats[cat]) || '';
    catEl.hidden = !catEl.textContent;
    $('bdi', durEl).textContent = dur;
    durEl.hidden = !dur;
    aboutEl.textContent = (cat && P.about[cat]) || '';
    const multi = queue.length > 1;
    $('[data-player-prev]', player).hidden = !multi;
    $('[data-player-next]', player).hidden = !multi;
    countEl.textContent = multi ? fill(P.count, { i: qi + 1, n: queue.length }) : '';
    toastEl.textContent = '';
    renderQueue();
    // קישור ישיר לשיר, כדי שאפשר לשלוח אותו הלאה
    try { history.replaceState(null, '', '#play=' + id); } catch (e) { /* לא קריטי */ }
  }
  function renderQueue() {
    const next = [];
    for (let k = 1; k < queue.length && next.length < 3; k++) next.push((qi + k) % queue.length);
    upNextBox.hidden = !next.length;
    queueEl.innerHTML = next.map((idx) => {
      const id = queue[idx]; const m = (data.meta && data.meta[id]) || ['', ''];
      const meta = [m[0] && data.player.cats[m[0]], m[1]].filter(Boolean).map(escapeHtml).join(' · ');
      return `<li><button type="button" class="q-item" data-q="${idx}"><span class="q-thumb"><img src="${assetBase}img/covers/${encodeURIComponent(id)}-s.webp" alt="" width="160" height="90" loading="lazy" decoding="async"></span><span class="q-copy"><span class="q-title">${escapeHtml(data.videos[id] || '')}</span><span class="q-meta">${meta}</span></span></button></li>`;
    }).join('');
  }
  function openPlayer(id, trigger) {
    // ״הבא בתור״ מגיע מאותו מקום שממנו לחצו: הספרייה, רצועת הערוץ או רשימת השירים בדף
    const scope = (trigger && (trigger.closest('#library') || trigger.closest('.channel-strip'))) || $('.music') || document;
    const list = $$(scope.classList && scope.classList.contains('channel-strip') ? '[data-play]' : '.song:not([hidden]) [data-play]', scope).map((b) => b.dataset.play);
    queue = list.includes(id) ? list : [id].concat(list.filter((x) => x !== id));
    qi = queue.indexOf(id);
    lastFocus = trigger || document.activeElement;
    player.hidden = false;
    setLock();
    load(id);
    $('.player-close', player).focus();
  }
  function closePlayer() {
    if (player.hidden) return;
    player.hidden = true;
    frame.innerHTML = '';
    setLock();
    try { history.replaceState(null, '', location.pathname + location.search); } catch (e) { /* לא קריטי */ }
    if (lastFocus && document.contains(lastFocus)) lastFocus.focus();
  }
  const step = (d) => { qi = (qi + d + queue.length) % queue.length; load(queue[qi]); };
  document.addEventListener('click', (e) => {
    const t = e.target.closest('[data-play]');
    if (t) { e.preventDefault(); openPlayer(t.dataset.play, t); return; }
    const q = e.target.closest('[data-q]');
    if (q) { qi = Number(q.dataset.q); load(queue[qi]); $('.player-close', player).focus(); return; }
    if (e.target.closest('[data-player-join]')) { closePlayer(); return; }
    if (e.target.closest('[data-player-close]')) closePlayer();
  });
  $('[data-player-prev]', player).addEventListener('click', () => step(-1));
  $('[data-player-next]', player).addEventListener('click', () => step(1));
  $('[data-player-share]', player).addEventListener('click', async () => {
    const id = queue[qi]; const title = data.videos[id] || '';
    const url = location.origin + location.pathname + '#play=' + id;
    if (navigator.share) {
      try { await navigator.share({ title, text: fill(data.player.shareText, { title }), url }); return; } catch (err) { if (err && err.name === 'AbortError') return; }
    }
    try { await navigator.clipboard.writeText(url); toastEl.textContent = data.player.copied; } catch (err) { toastEl.textContent = url; }
  });
  // פתיחה ישירה מקישור ששיתפו: ‎#play=מזהה
  const deep = /^#play=([\w-]{11})$/.exec(location.hash);
  if (deep && data.videos[deep[1]]) openPlayer(deep[1], null);
  player.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { e.preventDefault(); closePlayer(); return; }
    if ((e.key === 'ArrowLeft' || e.key === 'ArrowRight') && queue.length > 1 && !e.target.closest('input, textarea')) {
      e.preventDefault();
      const forward = (e.key === 'ArrowLeft') === (doc.dir === 'rtl');
      step(forward ? 1 : -1);
      return;
    }
    if (e.key !== 'Tab') return;
    const f = $$('button:not([hidden]), a[href], iframe', player).filter((el) => el.offsetParent !== null || el.tagName === 'IFRAME');
    if (!f.length) return;
    const first = f[0]; const last = f[f.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
})();
