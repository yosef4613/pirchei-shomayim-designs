// בונה את שלוש הדגמות המסלולים (דף נחיתה, אתר חוגים, אתר ומועדון) בעברית ובאנגלית מאותו מקור,
// ואת עמוד הבחירה ואת לוחות הניהול לדוגמה.  הרצה מתיקיית המאגר: node tools/demos/build.mjs
import { writeFileSync, mkdirSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dict, branches, songs, shorts, CHOIR_EMAIL, CHANNEL_URL } from './content.mjs';
import { PLANS, planConfig, planText } from './plans.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..');
const OUT = join(ROOT, 'demos');
const VERSION = '2';
const SITE = 'https://yosef4613.github.io/pirchei-shomayim-designs/demos/';

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const catShort = {
  he: { clip: 'קליפ', live: 'מהבמה', medley: 'מחרוזת · מופע', makhalolam: 'מקהלולם' },
  en: { clip: 'Music video', live: 'Live', medley: 'Medley · concert', makhalolam: 'Makhalolam' },
};
const icon = (id, cls = '') => `<svg class="ico ${cls}" aria-hidden="true" focusable="false"><use href="#i-${id}"/></svg>`;

const sprite = `<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="i-arrow" viewBox="0 0 24 24"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-play" viewBox="0 0 24 24"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.4-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z" fill="currentColor"/></symbol>
  <symbol id="i-check" viewBox="0 0 24 24"><path d="M5 12.5l4.2 4.2L19 7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-motion" viewBox="0 0 24 24"><path d="M3 12c2.5-5 5.5-5 8 0s5.5 5 8 0" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="21" cy="12" r="1.3" fill="currentColor"/></symbol>
  <symbol id="i-mail" viewBox="0 0 24 24"><rect x="3" y="5" width="18" height="14" rx="3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M4 7l8 6 8-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
  <symbol id="i-youtube" viewBox="0 0 24 24"><rect x="2.5" y="5.5" width="19" height="13" rx="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M10.2 9.3v5.4l4.6-2.7z" fill="currentColor"/></symbol>
  <symbol id="i-search" viewBox="0 0 24 24"><circle cx="11" cy="11" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 16l4.5 4.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
  <symbol id="i-close" viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></symbol>
  <symbol id="i-menu" viewBox="0 0 24 24"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
  <symbol id="i-pin" viewBox="0 0 24 24"><path d="M12 21s-6.5-6-6.5-11a6.5 6.5 0 0 1 13 0c0 5-6.5 11-6.5 11z" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="10" r="2.3" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
  <symbol id="i-clock" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7.5V12l3 2" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
  <symbol id="i-star" viewBox="0 0 24 24"><path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.8l-5.2 2.8 1-5.8L3.5 9.7l5.9-.8z" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/></symbol>
  <symbol id="i-heart" viewBox="0 0 24 24"><path d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.2a4.3 4.3 0 0 1 7.5 2.6C19.5 15.4 12 20 12 20z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
  <symbol id="i-wave" viewBox="0 0 24 24"><path d="M3 12h2M7 8v8M11 5v14M15 8v8M19 10.5v3M21 12h0" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol>
  <symbol id="i-mic" viewBox="0 0 24 24"><rect x="9" y="3" width="6" height="11" rx="3" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M6 11a6 6 0 0 0 12 0M12 17v4M9 21h6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol>
  <symbol id="i-book" viewBox="0 0 24 24"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5zM4 20.5A2.5 2.5 0 0 0 6.5 21H20" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
  <symbol id="i-doc" viewBox="0 0 24 24"><path d="M7 3h7l5 5v13H7zM14 3v5h5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
  <symbol id="i-bell" viewBox="0 0 24 24"><path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15zM10 20a2 2 0 0 0 4 0" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
</svg>`;

function page(t, plan) {
  const cfg = planConfig[plan];
  const P = planText[t.lang];
  const lang = t.lang;
  const B = lang === 'he' ? '' : '../';          // שורש המסלול (demos/N/)
  const A = `${B}../assets/`;                     // נכסים משותפים (demos/assets/)
  const PDF = `${B}../../assets/`;                // מודעות החוג בשורש המאגר
  const langSuffix = lang === 'he' ? '' : 'en/';
  const branchName = (b) => `${b[lang].name} · ${t.join.cities[b.city]}`;
  const visible = cfg.songsLimit;
  const listSongs = cfg.tools ? songs : songs.filter((s) => !s.isNew).slice(0, visible);
  const featured = songs.find((s) => s.isNew);
  const pageData = {
    lang, dir: t.dir, plan, form: cfg.form, choirEmail: CHOIR_EMAIL, assetBase: A,
    js: t.js, player: t.player, music: { showAll: t.music.showAll, showLess: t.music.showLess, count: t.music.count },
    motionOn: t.motionOn, motionOff: t.motionOff, cities: t.join.cities, chosen: t.join.chosen, choose: t.join.choose,
    emailForm: P.emailForm, account: P.account, club: P.club, topics: P.topics,
    branches: branches.map((b) => ({ id: b.id, city: b.city, name: b[lang].name, reg: b[lang].reg })),
    videos: Object.fromEntries([...songs.map((s) => [s.id, s[lang]]), ...shorts.map((s) => [s.id, s[lang]])]),
    adminHref: cfg.admin ? `${B}admin/` : '',
  };
  const navItems = [['join', t.nav.classes], ['music', t.nav.music]]
    .concat(cfg.stage ? [['stage', t.nav.stage]] : [])
    .concat([['makhalolam', t.nav.makhalolam]])
    .concat(cfg.club ? [['club', P.club.nav]] : [])
    .concat([['about', t.nav.about]]);
  const navHtml = navItems.map(([id, label]) => `<li><a href="#${id}">${esc(label)}</a></li>`).join('\n        ');

  const songCard = (s, i) => `
          <li class="song${cfg.tools && i >= visible ? ' is-extra' : ''}" data-cat="${s.cat}" data-title="${esc(s.he + ' ' + s.en)}">
            <button class="song-btn" type="button" data-play="${s.id}" aria-label="${esc(t.music.play + ': ' + s[lang])}">
              <span class="song-cover"><img src="${A}img/covers/${s.id}-s.webp" alt="" width="360" height="203" loading="lazy" decoding="async"><span class="song-play">${icon('play')}</span><span class="eq" aria-hidden="true"><i></i><i></i><i></i><i></i></span>${s.isNew ? `<span class="badge-new">${t.music.newBadge}</span>` : ''}</span>
              <span class="song-info"><span class="song-title">${esc(s[lang])}</span><span class="song-meta">${catShort[lang][s.cat]} · <bdi>${s.dur}</bdi></span></span>
            </button>
          </li>`;

  const topicChecks = (prefix, checked) => Object.entries(P.topics).map(([k, v]) => `<label class="topic"><input type="checkbox" name="${prefix}topic" value="${k}"${checked ? ' checked' : ''}><span>${esc(v)}</span></label>`).join('');

  const nextList = cfg.form === 'email' ? P.emailForm.next : t.form.next;
  const demoBar = `<div class="demo-bar"><div class="wrap demo-bar-in">
    <span class="demo-label">${esc(P.demo)} · ${esc(P.plans[plan].short)}: ${esc(P.plans[plan].name)}</span>
    <nav class="plan-switch" aria-label="${esc(P.switchLabel)}">${PLANS.map((n) => `<a href="${B}../${n}/${langSuffix}"${n === plan ? ' aria-current="page"' : ''}>${n}</a>`).join('')}${cfg.admin ? `<a class="demo-admin" href="${B}admin/">${esc(P.adminLink)}</a>` : ''}</nav>
  </div></div>`;

  return `<!doctype html>
<html lang="${lang}" dir="${t.dir}" data-motion="full" data-plan="${plan}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>${esc(t.title)}</title>
  <meta name="description" content="${esc(t.description)}">
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#0b0812">
  <link rel="alternate" hreflang="he" href="${SITE}${plan}/">
  <link rel="alternate" hreflang="en" href="${SITE}${plan}/en/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="${esc(t.title)}">
  <meta property="og:description" content="${esc(t.description)}">
  <meta property="og:image" content="${SITE}assets/img/og.jpg">
  <meta property="og:locale" content="${lang === 'he' ? 'he_IL' : 'en_US'}">
  <link rel="icon" href="${A}img/icon-64.png" type="image/png">
  <link rel="apple-touch-icon" href="${A}img/icon-180.png">
  <link rel="preload" href="${A}fonts/${lang === 'he' ? 'heebo-hebrew' : 'heebo-latin'}.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="${A}img/stage/hero-1.webp" as="image" media="(min-width: 721px)" fetchpriority="high">
  <link rel="preload" href="${A}img/stage/hero-1-m.webp" as="image" media="(max-width: 720px)" fetchpriority="high">
  <link rel="stylesheet" href="${A}site.css?v=${VERSION}">
  <script>document.documentElement.classList.add('js');try{var m=localStorage.getItem('ps-motion');if(m==='reduce'||(!m&&matchMedia('(prefers-reduced-motion: reduce)').matches))document.documentElement.dataset.motion='reduce'}catch(e){if(matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.dataset.motion='reduce'}</script>
  <script defer src="${A}site.js?v=${VERSION}"></script>
</head>
<body>
${sprite}
<a class="skip" href="#main">${t.skip}</a>

<header class="site-header" id="top">
  ${demoBar}
  <div class="wrap header-in">
    <a class="brand" href="#main" aria-label="${esc(t.brand + ' · ' + t.brandSub)}">
      <img class="brand-icon" src="${A}img/icon-180.png" alt="" width="44" height="44">
      <span class="brand-text"><b>${t.brand}</b><small>${t.brandSub}</small></span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="${lang === 'he' ? 'ניווט ראשי' : 'Main navigation'}">
      <ul>
        ${navHtml}
      </ul>
    </nav>
    <div class="header-actions">
      <a class="lang-link" href="${t.otherHref}" hreflang="${t.other}" lang="${t.other}" aria-label="${esc(t.langAria)}" data-lang-link>${t.langShort}</a>
      <button class="icon-btn motion-btn" type="button" data-motion-toggle aria-pressed="false" aria-label="${esc(t.motionOff)}" title="${esc(t.motionOff)}">${icon('motion')}</button>
      <a class="btn btn-mint btn-sm header-cta" href="#join">${t.headerCta}</a>
      <button class="icon-btn menu-btn" type="button" aria-controls="main-nav" aria-expanded="false" data-menu-toggle><span class="sr">${t.menu}</span>${icon('menu', 'ico-menu')}${icon('close', 'ico-close')}</button>
    </div>
  </div>
</header>

<main id="main" tabindex="-1">

  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-media">
      <picture class="hero-slide is-active">
        <source media="(max-width: 720px)" srcset="${A}img/stage/hero-1-m.webp">
        <img src="${A}img/stage/hero-1.webp" alt="${esc(t.hero.alts[0])}" width="1280" height="720" fetchpriority="high" decoding="async">
      </picture>
      <picture class="hero-slide">
        <source media="(max-width: 720px)" data-srcset="${A}img/stage/hero-2-m.webp">
        <img data-src="${A}img/stage/hero-2.webp" alt="${esc(t.hero.alts[1])}" width="1280" height="922" decoding="async">
      </picture>
      <picture class="hero-slide">
        <source media="(max-width: 720px)" data-srcset="${A}img/stage/hero-3-m.webp">
        <img data-src="${A}img/stage/hero-3.webp" alt="${esc(t.hero.alts[2])}" width="1280" height="720" decoding="async">
      </picture>
      <span class="hero-scrim"></span>
      <span class="beam beam-a"></span>
      <span class="beam beam-b"></span>
    </div>
    <div class="wrap hero-in">
      <div class="hero-copy">
        <p class="eyebrow">${esc(t.hero.eyebrow)}</p>
        <h1 id="hero-title"><span>${esc(t.hero.h1a)}</span> <span class="h1-accent">${esc(t.hero.h1b)}</span></h1>
        <p class="hero-lead">${esc(t.hero.lead)}</p>
        <div class="hero-actions">
          <a class="btn btn-mint btn-lg" href="#join">${esc(t.hero.cta)}${icon('arrow', 'ico-dir')}</a>
          <button class="text-link listen-link" type="button" data-play="${featured.id}">${icon('play')}<span>${esc(t.hero.listen)}</span></button>
        </div>
        <ul class="trust">
          ${t.hero.trust.map((x) => `<li>${icon('check')}${esc(x)}</li>`).join('\n          ')}
        </ul>
      </div>
      <p class="motto" aria-hidden="true">${esc(t.hero.motto)}</p>
    </div>
  </section>

  <section class="join" id="join" aria-labelledby="join-title">
    <div class="wrap">
      <div class="join-panel">
        <div class="join-head">
          <div>
            <p class="kicker">${esc(t.join.kicker)}</p>
            <h2 id="join-title">${esc(t.join.title)}</h2>
            <p class="join-lead">${esc(t.join.lead)}</p>
          </div>
          <ol class="stepper" aria-label="${lang === 'he' ? 'שלבי ההצטרפות' : 'How to join'}">
            ${t.join.steps.map((s, i) => `<li${i === 0 ? ' class="is-current"' : ''}><span class="step-num">${i + 1}</span>${esc(s)}</li>`).join('\n            ')}
          </ol>
        </div>

        <div class="city-filter" role="group" aria-label="${esc(t.join.filterLabel)}">
          <button type="button" class="chip" data-city="all" aria-pressed="true">${esc(t.join.all)}</button>
          <button type="button" class="chip" data-city="jerusalem" aria-pressed="false">${esc(t.join.cities.jerusalem)}</button>
          <button type="button" class="chip" data-city="beit-shemesh" aria-pressed="false">${esc(t.join.cities['beit-shemesh'])}</button>
        </div>

        <ul class="branches">
          ${branches.map((b) => `<li class="branch" data-city="${b.city}" data-branch-card="${b.id}">
            <p class="branch-city">${icon('pin')}${esc(t.join.cities[b.city])}</p>
            <h3 class="branch-name">${esc(b[lang].name)}</h3>
            <ul class="branch-facts">
              <li>${icon('star')}${esc(t.join.ages)} · ${esc(t.join.audition)}</li>
              <li>${icon('clock')}${esc(t.join.times)}</li>
            </ul>
            <p class="branch-reg"><span>${esc(t.join.regLabel)}</span> ${esc(b[lang].venue)}</p>
            <button type="button" class="btn btn-purple branch-choose" data-choose="${b.id}" aria-pressed="false" aria-label="${esc(t.join.choose + ': ' + branchName(b))}"><span class="choose-label">${esc(t.join.choose)}</span>${icon('arrow', 'ico-dir')}</button>
          </li>`).join('\n          ')}
        </ul>
        <p class="flyers">${icon('doc')}<span>${esc(t.join.flyers)}</span> <a href="${PDF}jerusalem-hebrew.pdf" target="_blank" rel="noopener" lang="he">${t.join.flyerHe}</a> · <a href="${PDF}jerusalem-english.pdf" target="_blank" rel="noopener" lang="en">${t.join.flyerEn}</a></p>

        <div class="join-form-area" id="join-form-area">
          <form class="join-form" id="join-form" novalidate aria-labelledby="form-title">
            <h3 id="form-title" tabindex="-1">${esc(t.form.title)}</h3>
            <div class="form-error-summary" role="alert" hidden></div>
            <div class="field field-wide">
              <label for="f-branch">${esc(t.form.branch)} <span class="req" aria-hidden="true">*</span></label>
              <select id="f-branch" name="branch" required aria-describedby="e-branch">
                <option value="">${esc(t.form.branchPlaceholder)}</option>
                ${branches.map((b) => `<option value="${b.id}">${esc(branchName(b))}</option>`).join('\n                ')}
              </select>
              <p class="field-error" id="e-branch"></p>
            </div>
            <div class="field">
              <label for="f-parent">${esc(t.form.parent)} <span class="req" aria-hidden="true">*</span></label>
              <input id="f-parent" name="parent" type="text" autocomplete="name" required aria-describedby="e-parent">
              <p class="field-error" id="e-parent"></p>
            </div>
            <div class="field">
              <label for="f-phone">${esc(t.form.phone)} <span class="req" aria-hidden="true">*</span></label>
              <input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" dir="ltr" required aria-describedby="e-phone">
              <p class="field-error" id="e-phone"></p>
            </div>
            <div class="field field-wide">
              <label for="f-email">${esc(t.form.email)} <span class="req" aria-hidden="true">*</span></label>
              <input id="f-email" name="email" type="email" inputmode="email" autocomplete="email" dir="ltr" required aria-describedby="e-email">
              <p class="field-error" id="e-email"></p>
            </div>
            <div class="field">
              <label for="f-child">${esc(t.form.child)} <span class="req" aria-hidden="true">*</span></label>
              <input id="f-child" name="child" type="text" autocomplete="off" required aria-describedby="e-child">
              <p class="field-error" id="e-child"></p>
            </div>
            <div class="field field-third">
              <label for="f-age">${esc(t.form.age)} <span class="req" aria-hidden="true">*</span></label>
              <input id="f-age" name="age" type="number" inputmode="numeric" min="5" max="16" required aria-describedby="e-age">
              <p class="field-error" id="e-age"></p>
            </div>
            <div class="field">
              <label for="f-cheder">${esc(t.form.cheder)} <span class="req" aria-hidden="true">*</span></label>
              <input id="f-cheder" name="cheder" type="text" autocomplete="off" required aria-describedby="e-cheder">
              <p class="field-error" id="e-cheder"></p>
            </div>
            <div class="field field-third">
              <label for="f-grade">${esc(t.form.grade)} <span class="req" aria-hidden="true">*</span></label>
              <select id="f-grade" name="grade" required aria-describedby="e-grade">
                <option value="">${esc(t.form.gradePlaceholder)}</option>
                ${t.form.grades.map((g) => `<option>${esc(g)}</option>`).join('')}
              </select>
              <p class="field-error" id="e-grade"></p>
            </div>
            <div class="field field-wide">
              <label for="f-notes">${esc(t.form.notes)}</label>
              <textarea id="f-notes" name="notes" rows="2"></textarea>
            </div>${cfg.account ? `
            <fieldset class="field field-wide account-box">
              <legend>${icon('bell')}${esc(P.account.legend)}</legend>
              <label class="optin"><input id="f-account" name="account" type="checkbox"> <span>${esc(P.account.optIn)}</span></label>
              <div class="account-topics" data-account-topics hidden>
                <p class="hint">${esc(P.account.hint)}</p>
                <div class="topics">${topicChecks('a-', true)}</div>
              </div>
            </fieldset>` : ''}
            <div class="field field-wide field-check">
              <input id="f-consent" name="consent" type="checkbox" required aria-describedby="e-consent">
              <label for="f-consent">${esc(t.form.consent)}</label>
              <p class="field-error" id="e-consent"></p>
            </div>
            <div class="hp" aria-hidden="true"><label for="f-website">Website</label><input id="f-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
            <div class="form-submit">
              <button class="btn btn-mint btn-lg" type="submit">${esc(cfg.form === 'email' ? P.emailForm.submit : t.form.submit)}${icon(cfg.form === 'email' ? 'mail' : 'arrow', cfg.form === 'email' ? '' : 'ico-dir')}</button>
              <p class="form-privacy">${esc(cfg.form === 'email' ? P.emailForm.privacy : t.form.privacy)}</p>
            </div>
            <p class="demo-note">${esc(cfg.form === 'email' ? P.emailForm.demoNote : t.form.demoNote)}</p>
          </form>

          <div class="join-success" id="join-success" hidden tabindex="-1" aria-live="polite"></div>

          <aside class="join-next" aria-labelledby="next-title">
            <h3 id="next-title">${esc(t.form.nextTitle)}</h3>
            <ol>
              ${nextList.map((x, i) => `<li><span class="step-num">${i + 1}</span><span>${esc(x)}</span></li>`).join('\n              ')}
            </ol>
            <img class="join-next-img" src="${A}img/stage/PHbWcgVHTSQ-43.webp" alt="" width="720" height="540" loading="lazy" decoding="async">
          </aside>
        </div>
      </div>
    </div>
  </section>

  <section class="why" id="why" aria-labelledby="why-title">
    <div class="wrap">
      <p class="kicker" data-reveal>${esc(t.why.kicker)}</p>
      <h2 id="why-title" data-reveal>${esc(t.why.title)}</h2>
      <ul class="why-grid">
        ${t.why.items.map(([h, p], i) => `<li class="why-card" data-reveal style="--d:${i * 90}ms"><span class="why-ico">${icon(['heart', 'wave', 'mic', 'book'][i])}</span><h3>${esc(h)}</h3><p>${esc(p)}</p></li>`).join('\n        ')}
      </ul>
      <dl class="stats">
        ${t.stats.map((s) => `<div class="stat" data-reveal><dt>${esc(s.label)}</dt><dd>${s.text ? `<bdi>${esc(s.text)}</bdi>` : `<bdi data-count="${s.value}" data-suffix="${esc(s.suffix)}">${s.value}${esc(s.suffix)}</bdi>`}</dd></div>`).join('\n        ')}
      </dl>
    </div>
  </section>

  <section class="program" id="program" aria-labelledby="program-title">
    <div class="wrap">
      <div class="section-head">
        <p class="kicker" data-reveal>${esc(t.program.kicker)}</p>
        <h2 id="program-title" data-reveal>${esc(t.program.title)}</h2>
        <p class="section-lead" data-reveal>${esc(t.program.lead)}</p>
      </div>
      <div class="journey" data-journey>
        <svg class="journey-wave" viewBox="0 0 1000 120" preserveAspectRatio="none" aria-hidden="true">
          <path class="wave-base" d="M0 60 C 50 10, 100 10, 150 60 S 250 110, 300 60 S 400 10, 450 60 S 550 110, 600 60 S 700 10, 750 60 S 850 110, 900 60 S 975 30, 1000 60"/>
          <path class="wave-live" pathLength="1" d="M0 60 C 50 10, 100 10, 150 60 S 250 110, 300 60 S 400 10, 450 60 S 550 110, 600 60 S 700 10, 750 60 S 850 110, 900 60 S 975 30, 1000 60"/>
        </svg>
        <ol class="journey-steps">
          ${t.program.steps.map(([h, p, img, alt], i) => `<li class="journey-step" data-step="${i}">
            <span class="journey-dot" aria-hidden="true">${i + 1}</span>
            <figure><img src="${A}img/stage/${img}-43.webp" alt="${esc(alt)}" width="720" height="540" loading="lazy" decoding="async"></figure>
            <h3>${esc(h)}</h3>
            <p>${esc(p)}</p>
          </li>`).join('\n          ')}
        </ol>
      </div>
    </div>
  </section>

  <section class="music" id="music" aria-labelledby="music-title">
    <div class="wrap">
      <div class="section-head section-head-row">
        <div>
          <p class="kicker" data-reveal>${esc(t.music.kicker)}</p>
          <h2 id="music-title" data-reveal>${esc(t.music.title)}</h2>
          <p class="section-lead" data-reveal>${esc(cfg.tools ? t.music.lead : t.music.lead.split('.')[0] + '.')}</p>
        </div>
        <a class="text-link" href="${CHANNEL_URL}" target="_blank" rel="noopener">${icon('youtube')}<span>${esc(t.music.channel)}</span></a>
      </div>

      <article class="featured" data-reveal>
        <button class="featured-media" type="button" data-play="${featured.id}" aria-label="${esc(t.music.play + ': ' + featured[lang])}">
          <img src="${A}img/covers/${featured.id}.webp" alt="" width="640" height="360" loading="lazy" decoding="async">
          <span class="featured-play">${icon('play')}</span>
        </button>
        <div class="featured-copy">
          <p class="badge-new">${esc(t.music.featuredLabel)}</p>
          <h3>${esc(featured[lang])}</h3>
          <p>${esc(t.music.featuredText)}</p>
          <button class="btn btn-ghost" type="button" data-play="${featured.id}">${icon('play')}${esc(t.music.play)} · <bdi>${featured.dur}</bdi></button>
        </div>
      </article>
${cfg.tools ? `
      <div class="music-tools">
        <div class="chips" role="group" aria-label="${lang === 'he' ? 'סינון שירים' : 'Filter songs'}">
          ${Object.entries(t.music.filters).map(([k, v], i) => `<button type="button" class="chip chip-dark" data-filter="${k}" aria-pressed="${i === 0}">${esc(v)}</button>`).join('\n          ')}
        </div>
        <div class="search">
          <label class="sr" for="song-search">${esc(t.music.searchLabel)}</label>
          ${icon('search')}
          <input id="song-search" type="search" placeholder="${esc(t.music.searchPlaceholder)}" autocomplete="off">
        </div>
      </div>
      <p class="song-count" aria-live="polite" data-song-count></p>` : ''}
      <ul class="songs" data-songs>${listSongs.map(songCard).join('')}
      </ul>${cfg.tools ? `
      <p class="songs-empty" hidden>${esc(t.music.empty)}</p>
      <div class="songs-more"><button type="button" class="btn btn-ghost" data-songs-more aria-expanded="false">${esc(t.music.showAll)}</button></div>` : ''}
    </div>
  </section>
${cfg.stage ? `
  <section class="stage" id="stage" aria-labelledby="stage-title">
    <div class="wrap">
      <div class="section-head">
        <p class="kicker" data-reveal>${esc(t.stage.kicker)}</p>
        <h2 id="stage-title" data-reveal>${esc(t.stage.title)}</h2>
      </div>
      <div class="stage-grid">
        <article class="upcoming" data-reveal>
          <p class="kicker">${esc(t.stage.upcomingTitle)}</p>
          <span class="upcoming-ico">${icon('star')}</span>
          <p>${esc(t.stage.upcomingText)}</p>
        </article>
        <div class="shows">
          <h3 class="shows-title">${esc(t.stage.pastTitle)}</h3>
          <ul>
            ${t.stage.shows.map((s) => `<li data-reveal><button class="show" type="button" data-play="${s.video}"><img src="${A}img/stage/${s.img}-43.webp" alt="" width="720" height="540" loading="lazy" decoding="async"><span class="show-copy"><b>${esc(s.title)}</b><small>${esc(s.sub)}</small></span><span class="show-play">${icon('play')}</span></button></li>`).join('\n            ')}
          </ul>
        </div>
      </div>
      <div class="booking" data-reveal>
        <div><h3>${esc(t.stage.bookingTitle)}</h3><p>${esc(t.stage.bookingText)}</p></div>
        <a class="btn btn-outline" href="mailto:${CHOIR_EMAIL}?subject=${encodeURIComponent(t.stage.bookingSubject)}">${icon('mail')}${esc(t.stage.bookingCta)}</a>
      </div>
    </div>
  </section>` : ''}

  <section class="makhalolam" id="makhalolam" aria-labelledby="mk-title">
    <div class="wrap mk-grid">
      <div class="mk-visual">
        <div class="mk-logo"><img src="${A}img/makhalolam.webp" alt="${esc(t.makhalolam.logoAlt)}" width="560" height="560" loading="lazy" decoding="async"></div>
        <div class="cr" aria-hidden="true">
          <div class="cr-row cr-choir"><span class="cr-label">${esc(t.makhalolam.choir)}</span><span class="cr-dots">${'<i></i>'.repeat(9)}</span></div>
          <div class="cr-row cr-aud"><span class="cr-label">${esc(t.makhalolam.audience)}</span><span class="cr-dots">${'<i></i>'.repeat(13)}</span></div>
          <p class="cr-together">${esc(t.makhalolam.together)}</p>
        </div>
      </div>
      <div class="mk-copy">
        <p class="kicker" data-reveal>${esc(t.makhalolam.kicker)}</p>
        <h2 id="mk-title" data-reveal>${esc(t.makhalolam.title)} <span class="h2-sub">${esc(t.makhalolam.subtitle)}</span></h2>
        <p data-reveal>${esc(t.makhalolam.text)}</p>
        <ul class="ticks" data-reveal>${t.makhalolam.points.map((p) => `<li>${icon('check')}${esc(p)}</li>`).join('')}</ul>
        <div class="mk-videos" data-reveal>
          <button class="mk-video" type="button" data-play="n6tLDS_ioYk"><img src="${A}img/covers/n6tLDS_ioYk-s.webp" alt="" width="360" height="203" loading="lazy" decoding="async"><span>${icon('play')}${esc(t.makhalolam.videoMain)}</span></button>
          <button class="mk-video" type="button" data-play="eSJg_mli2y8"><img src="${A}img/covers/eSJg_mli2y8-s.webp" alt="" width="360" height="203" loading="lazy" decoding="async"><span>${icon('play')}${esc(t.makhalolam.videoPromo)}</span></button>
        </div>
        <a class="btn btn-outline" data-reveal href="mailto:${CHOIR_EMAIL}?subject=${encodeURIComponent(t.makhalolam.subject)}">${icon('mail')}${esc(t.makhalolam.cta)}</a>
      </div>
    </div>
  </section>
${cfg.behind ? `
  <section class="behind" id="behind" aria-labelledby="behind-title">
    <div class="strip-outer" data-strip>
      <div class="strip-sticky">
        <div class="wrap"><div class="section-head">
          <p class="kicker">${esc(t.behind.kicker)}</p>
          <h2 id="behind-title">${esc(t.behind.title)}</h2>
          <p class="section-lead">${esc(t.behind.lead)}</p>
        </div></div>
        <div class="strip-viewport">
          <ul class="strip-track">
            <li class="strip-item strip-exclusive"><span class="tag">${esc(t.behind.exclusiveTag)}</span><span class="excl-ico">${icon('mic')}</span><h3>${esc(t.behind.exclusiveTitle)}</h3><p>${esc(t.behind.exclusiveText)}</p></li>
            ${shorts.map((s) => `<li class="strip-item strip-short"><button type="button" data-play="${s.id}"><img src="${A}img/shorts/${s.id}.webp" alt="" width="360" height="640" loading="lazy" decoding="async"><span class="short-cap">${icon('play')}${esc(s[lang])}</span></button></li>`).join('\n            ')}
            ${t.behind.stories.map((s) => `<li class="strip-item strip-story"><img src="${A}img/covers/${s.img}.webp" alt="" width="640" height="360" loading="lazy" decoding="async"><div class="story-copy"><h3>${esc(s.title)}</h3><p>${esc(s.text)}</p><button type="button" class="text-link" data-play="${s.img}">${icon('play')}<span>${esc(t.behind.watch)}</span></button></div></li>`).join('\n            ')}
          </ul>
        </div>
      </div>
    </div>
  </section>` : ''}
${cfg.club ? `
  <section class="club" id="club" aria-labelledby="club-title">
    <div class="wrap club-grid">
      <div class="club-copy">
        <p class="kicker" data-reveal>${esc(P.club.kicker)}</p>
        <h2 id="club-title" data-reveal>${esc(P.club.title)}</h2>
        <p class="section-lead" data-reveal>${esc(P.club.lead)}</p>
        <div class="club-bells" aria-hidden="true">${Object.values(P.topics).map((v, i) => `<span class="bell" style="--i:${i}">${icon('bell')}${esc(v)}</span>`).join('')}</div>
      </div>
      <div class="club-card">
        <form class="club-form" id="club-form" novalidate>
          <div class="field">
            <label for="c-name">${esc(P.club.name)}</label>
            <input id="c-name" name="name" type="text" autocomplete="name">
          </div>
          <div class="field">
            <label for="c-email">${esc(P.club.email)} <span class="req" aria-hidden="true">*</span></label>
            <input id="c-email" name="email" type="email" dir="ltr" autocomplete="email" required aria-describedby="ce-email">
            <p class="field-error" id="ce-email"></p>
          </div>
          <fieldset class="field field-wide" aria-describedby="ce-topics">
            <legend>${esc(P.club.topicsLabel)}</legend>
            <div class="topics">${topicChecks('c-', true)}</div>
            <p class="field-error" id="ce-topics"></p>
          </fieldset>
          <div class="field field-wide field-check">
            <input id="c-consent" name="consent" type="checkbox" required aria-describedby="ce-consent">
            <label for="c-consent">${esc(P.club.consent)}</label>
            <p class="field-error" id="ce-consent"></p>
          </div>
          <button class="btn btn-purple btn-lg" type="submit">${icon('bell')}${esc(P.club.submit)}</button>
          <p class="demo-note">${esc(P.club.demoNote)}</p>
        </form>
        <div class="club-success" id="club-success" hidden tabindex="-1" aria-live="polite"></div>
      </div>
    </div>
  </section>` : ''}

  <section class="about" id="about" aria-labelledby="about-title">
    <div class="wrap about-grid">
      <div class="about-logo" data-reveal><img src="${A}img/logo-full.webp" alt="${esc(t.about.logoAlt)}" width="720" height="508" loading="lazy" decoding="async"></div>
      <div class="about-copy">
        <p class="kicker" data-reveal>${esc(t.about.kicker)}</p>
        <h2 id="about-title" data-reveal>${esc(t.about.title)}</h2>
        ${t.about.paras.map((p) => `<p data-reveal>${esc(p)}</p>`).join('\n        ')}
        <p class="conductor" data-reveal><b>${esc(t.about.conductor)}</b><span>${esc(t.about.conductorRole)}</span></p>
      </div>
    </div>
    <div class="wrap">
      <ul class="about-cards">
        ${t.about.cards.map(([h, p]) => `<li data-reveal><h3>${esc(h)}</h3><p>${esc(p)}</p><span class="soon">${esc(t.about.soon)}</span></li>`).join('\n        ')}
        <li class="testimonials" data-reveal><span class="quote-mark" aria-hidden="true">”</span><h3>${esc(t.about.testimonialsTitle)}</h3><p>${esc(t.about.testimonialsText)}</p><span class="soon">${esc(t.about.soon)}</span></li>
      </ul>
    </div>
  </section>

  <section class="final" aria-labelledby="final-title">
    <div class="wrap final-in" data-reveal>
      <h2 id="final-title">${esc(t.final.title)}</h2>
      <p>${esc(t.final.text)}</p>
      <a class="btn btn-mint btn-lg" href="#join">${esc(t.final.cta)}${icon('arrow', 'ico-dir')}</a>
    </div>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap footer-in">
    <div class="footer-brand">
      <img src="${A}img/icon-180.png" alt="" width="48" height="48" loading="lazy">
      <p><b>${t.brand}</b><small>${t.brandSub} · ${esc(t.hero.motto)}</small></p>
    </div>
    <nav aria-label="${lang === 'he' ? 'ניווט תחתון' : 'Footer navigation'}">
      <ul>
        ${navHtml}
      </ul>
    </nav>
    <div class="footer-contact">
      <a href="mailto:${CHOIR_EMAIL}">${icon('mail')}<span>${esc(t.footer.contact)}</span></a>
      <a href="${CHANNEL_URL}" target="_blank" rel="noopener">${icon('youtube')}<span>${esc(t.footer.youtube)}</span></a>
      <a href="${t.otherHref}" hreflang="${t.other}" lang="${t.other}" data-lang-link>${t.langLabel}</a>
    </div>
  </div>
  <div class="wrap footer-legal">
    <span>${esc(t.footer.rights)}</span>
    <a href="#top">${esc(t.footer.access)}</a>
    <a href="#top">${esc(t.footer.privacy)}</a>
    <span class="footer-demo">${esc(t.footer.demo)}</span>
  </div>
</footer>

<div class="player" id="player" role="dialog" aria-modal="true" aria-labelledby="player-title" hidden>
  <div class="player-backdrop" data-player-close></div>
  <div class="player-bg" aria-hidden="true"><img alt="" data-player-bg></div>
  <div class="player-box">
    <div class="player-top">
      <span class="eq eq-live" aria-hidden="true"><i></i><i></i><i></i><i></i></span>
      <h2 id="player-title" class="player-title"></h2>
      <button type="button" class="icon-btn player-close" data-player-close aria-label="${esc(t.player.close)}">${icon('close')}</button>
    </div>
    <div class="player-frame" data-player-frame></div>
    <div class="player-bottom">
      <button type="button" class="icon-btn" data-player-prev aria-label="${esc(t.player.prev)}">${icon('arrow', 'ico-prev')}</button>
      <a class="text-link" data-player-yt href="#" target="_blank" rel="noopener">${icon('youtube')}<span>${esc(t.player.youtube)}</span></a>
      <button type="button" class="icon-btn" data-player-next aria-label="${esc(t.player.next)}">${icon('arrow', 'ico-dir')}</button>
    </div>
    <p class="player-note">${esc(t.player.note)}</p>
  </div>
</div>

<script type="application/json" id="page-data">${JSON.stringify(pageData).replace(/</g, '\\u003c')}</script>
</body>
</html>
`;
}

// עמוד הבחירה בין שלושת המסלולים
function hub() {
  const P = planText.he; const H = P.hub; const A = 'assets/';
  return `<!doctype html>
<html lang="he" dir="rtl" data-motion="full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(H.title)}</title>
  <meta name="robots" content="noindex, nofollow">
  <meta name="theme-color" content="#0b0812">
  <link rel="icon" href="${A}img/icon-64.png" type="image/png">
  <link rel="stylesheet" href="${A}site.css?v=${VERSION}">
</head>
<body class="hub">
${sprite}
<main class="wrap hub-in">
  <header class="hub-head">
    <img src="${A}img/icon-180.png" alt="" width="64" height="64">
    <p class="kicker">פרחי שמיים · מקהלת הילדים</p>
    <h1>${esc(H.title)}</h1>
    <p class="section-lead">${esc(H.lead)}</p>
  </header>
  <ul class="hub-grid">
    ${PLANS.map((n) => {
      const p = P.plans[n]; const cfg = planConfig[n];
      return `<li class="hub-card${n === 2 ? ' is-chosen' : ''}">
      ${n === 2 ? `<span class="hub-tag">${esc(H.recommended)}</span>` : ''}
      <img src="${A}img/stage/${['FzzkmO2WIhg', '9--ZpQoS3AQ', 'n6tLDS_ioYk'][n - 1]}-43.webp" alt="" width="720" height="540" loading="lazy">
      <div class="hub-body">
        <p class="kicker">${esc(p.short)}</p>
        <h2>${esc(p.name)}</h2>
        <p>${esc(p.desc)}</p>
        <ul class="ticks">${p.bullets.map((b) => `<li>${icon('check')}${esc(b)}</li>`).join('')}</ul>
        <div class="hub-actions">
          <a class="btn ${n === 2 ? 'btn-mint' : 'btn-purple'}" href="${n}/">${esc(H.view)}${icon('arrow', 'ico-dir')}</a>
          <a class="btn btn-ghost" href="${n}/en/" lang="en">${H.english}</a>
          ${cfg.admin ? `<a class="btn btn-ghost" href="${n}/admin/">${esc(H.admin)}</a>` : ''}
        </div>
      </div>
    </li>`;
    }).join('\n    ')}
  </ul>
  <p class="hub-note">${esc(H.note)} <a href="../proposal/">${esc(H.proposal)}</a></p>
</main>
</body>
</html>
`;
}

const bidi = (html) => html.replace(/(\d+)–(\d+)/g, '\u2066$1–$2\u2069'); // טווח מספרים לא יתהפך בעברית
const write = (file, html) => { mkdirSync(dirname(file), { recursive: true }); writeFileSync(file, html); console.log('wrote', file.replace(ROOT + '/', '')); };

for (const plan of PLANS) {
  for (const key of ['he', 'en']) {
    const html = page(dict[key], plan);
    write(join(OUT, String(plan), key === 'he' ? '' : 'en', 'index.html'), key === 'he' ? bidi(html) : html);
  }
  if (planConfig[plan].admin) {
    let admin = readFileSync(join(HERE, 'admin.html'), 'utf8').replace(/\{\{PLAN\}\}/g, String(plan)).replace(/\{\{V\}\}/g, VERSION);
    admin = plan === 3 ? admin.replace(/<!--P3-->|<!--\/P3-->/g, '') : admin.replace(/<!--P3-->[\s\S]*?<!--\/P3-->/g, '');
    write(join(OUT, String(plan), 'admin', 'index.html'), bidi(admin));
  }
}
write(join(OUT, 'index.html'), bidi(hub()));
