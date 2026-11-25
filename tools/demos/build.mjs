// בונה את שלוש הדגמות המסלולים (דף נחיתה, אתר חוגים, אתר ומועדון) בעברית ובאנגלית מאותו מקור,
// ואת עמוד הבחירה ואת לוחות הניהול לדוגמה.  הרצה מתיקיית המאגר: node tools/demos/build.mjs
import { writeFileSync, mkdirSync, readFileSync, cpSync, rmSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { dict, branches, songs, shorts, CHOIR_EMAIL, CHOIR_EMAIL_HREF, CHANNEL_URL } from './content.mjs';
import { PLANS, planConfig, planText, exclusiveText } from './plans.mjs';
import { seoText } from './seo.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..', '..');
const OUT = join(ROOT, 'demos');
const VERSION = '16';
const SITE = 'https://yosef4613.github.io/pirchei-shomayim-designs/demos/';
// האתר החי (הדומיין העברי בקידוד הבינלאומי). לכאן מפנות הכתובות הקנוניות בגרסה החיה
const LIVE = 'https://xn--cebeaqd7a2ak.com/';
const LIVE_PLAN = 3;
// מי בנה את האתר — מופיע בתחתית כל עמוד ובנתונים לגוגל
const BUILDER = { name: 'YYG', url: 'https://yosef4613.github.io/yyg-site/' };
const credit = (t) => `<span class="footer-credit">${esc(t.footer.builtBy)} <a href="${BUILDER.url}" target="_blank" rel="noopener">${BUILDER.name}</a></span>`;

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const catShort = {
  he: { clip: 'קליפ', live: 'מהבמה', medley: 'מחרוזת · מופע', makhalolam: 'מקהלולם', short: 'קטע קצר' },
  en: { clip: 'Music video', live: 'Live', medley: 'Medley · concert', makhalolam: 'Makhalolam', short: 'Short clip' },
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
  <symbol id="i-music" viewBox="0 0 24 24"><path d="M9 18V6l11-2v12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><circle cx="6.5" cy="18" r="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="17.5" cy="16" r="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/></symbol>
  <symbol id="i-share" viewBox="0 0 24 24"><path d="M12 3v12M7.5 7.5 12 3l4.5 4.5M5 13v5a3 3 0 0 0 3 3h8a3 3 0 0 0 3-3v-5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-external" viewBox="0 0 24 24"><path d="M14 4h6v6M20 4l-9 9M18 14v4a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>
  <symbol id="i-bell" viewBox="0 0 24 24"><path d="M6 16V11a6 6 0 0 1 12 0v5l1.5 2h-15zM10 20a2 2 0 0 0 4 0" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol>
</svg>`;

function page(t, plan, live = false) {
  const cfg = planConfig[plan];
  const P = planText[t.lang];
  const lang = t.lang;
  const B = lang === 'he' ? '' : '../';          // שורש המסלול (demos/N/)
  const A = live ? '/ps/assets/' : `${B}../assets/`;          // נכסים משותפים
  const PDF = live ? '/ps/flyers/' : `${B}../../assets/`;      // מודעות החוג
  const langSuffix = lang === 'he' ? '' : 'en/';
  const ROOTURL = live ? LIVE : `${SITE}${plan}/`;
  const PAGEURL = ROOTURL + langSuffix;
  const IMGURL = live ? `${LIVE}ps/assets/img/` : `${SITE}assets/img/`;
  const legal = live ? `/${langSuffix}privacy/` : '#top';
  const S = seoText[lang];
  const branchName = (b) => `${b[lang].name} · ${t.join.cities[b.city]}`;
  // בדף הבית: מבחר קצר. כל השירים נפתחים בלחיצה בספרייה נפרדת (במסלולים 2 ו־3)
  const homeSongs = songs.filter((s) => !s.isNew && !s.vertical).slice(0, cfg.tools ? 4 : 8);
  const L = lang === 'he'
    ? { libOpen: `לכל ${songs.length} השירים והקליפים`, libTitle: 'כל השירים והקליפים', libClose: 'סגירת ספריית השירים' }
    : { libOpen: `All ${songs.length} songs & videos`, libTitle: 'All songs & videos', libClose: 'Close the song library' };
  const featured = songs.find((s) => s.isNew);
  const pageData = {
    lang, dir: t.dir, plan, form: cfg.form, choirEmail: CHOIR_EMAIL, choirEmailHref: CHOIR_EMAIL_HREF, assetBase: A, live, endpoint: live ? '/wp-json/ps/v1/' : '',
    js: t.js, player: t.player, music: { showAll: t.music.showAll, showLess: t.music.showLess, count: t.music.count, countOne: t.music.countOne },
    shareOrigin: live ? 'https://פרחישמים.com' : '',
    motionOn: t.motionOn, motionOff: t.motionOff, cities: t.join.cities, chosen: t.join.chosen, choose: t.join.choose, fit: t.join.fit,
    emailForm: live ? undefined : P.emailForm, account: P.account, club: live ? { ...P.club, demoNote: undefined } : P.club, topics: P.topics,
    branches: branches.map((b) => ({ id: b.id, city: b.city, name: b[lang].name, reg: b[lang].reg })),
    videos: Object.fromEntries([...t.stage.shows.map((s) => [s.video, s.title]), ...songs.map((s) => [s.id, s[lang]]), ...shorts.map((s) => [s.id, s[lang]])]),
    meta: Object.fromEntries([...t.stage.shows.map((s) => [s.video, ['live', '']]), ...songs.map((s) => [s.id, [s.vertical ? 'short' : s.cat, s.dur || '']]), ...shorts.map((s) => [s.id, ['short', '']])]),
    adminHref: cfg.admin && !live ? `${B}admin/` : '',
    // סרטונים אנכיים (שורטס) נפתחים בנגן אנכי — גם מספריית השירים וגם מרצועת מאחורי הקלעים
    vertical: [...new Set([...songs.filter((s) => s.vertical).map((s) => s.id), ...shorts.map((s) => s.id)])],
  };
  const X = exclusiveText[lang];
  // ״מאחורי הקלעים״ מסומן בתפריט כתוכן שיש רק באתר
  const navItems = [['join', t.nav.classes], ['music', t.nav.music]]
    .concat(cfg.stage ? [['stage', t.nav.stage]] : [])
    .concat(cfg.behind ? [['behind', lang === 'he' ? 'מאחורי הקלעים' : 'Behind the scenes', 'nav-excl']] : [])
    .concat([['makhalolam', t.nav.makhalolam]])
    .concat(cfg.club ? [['club', P.club.nav]] : [])
    .concat([['about', t.nav.about]]);
  const navHtml = navItems.map(([id, label, cls]) => `<li><a href="#${id}"${cls ? ` class="${cls}" title="${esc(X.badge)}"` : ''}>${esc(label)}</a></li>`).join('\n        ');
  const motionText = `<button type="button" class="motion-text" data-motion-toggle aria-pressed="false">${icon('motion')}<span class="motion-label">${esc(t.motionOff)}</span></button>`;
  const navExtra = `<li class="nav-extra"><a class="btn btn-mint nav-cta" href="#join">${esc(t.hero.cta)}</a></li><li class="nav-extra">${motionText}</li>`;

  // deferred=true: התמונה נטענת רק כשפותחים את ספריית השירים, כדי שהדף יישאר קל
  const songCard = (s, deferred = false) => `
          <li class="song" data-cat="${s.cat}" data-title="${esc(s.he + ' ' + s.en)}">
            <button class="song-btn" type="button" data-play="${s.id}">
              <span class="song-cover"><img ${deferred ? 'data-src' : 'src'}="${A}img/covers/${s.id}-s.webp" alt="" width="360" height="203" loading="lazy" decoding="async"><span class="song-play">${icon('play')}</span><span class="eq" aria-hidden="true"><i></i><i></i><i></i><i></i></span>${s.isNew ? `<span class="badge-new">${t.music.newBadge}</span>` : ''}</span>
              <span class="song-info"><span class="song-title"><span class="sr">${esc(t.music.play)}: </span>${esc(s[lang])}</span><span class="song-meta">${catShort[lang][s.cat]} · <bdi>${s.dur}</bdi></span></span>
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
  <meta name="robots" content="${live ? 'index, follow, max-image-preview:large, max-video-preview:-1' : 'noindex, nofollow'}">
  <meta name="theme-color" content="#0b0812">
  <link rel="canonical" href="${PAGEURL}">
  <link rel="alternate" hreflang="he" href="${ROOTURL}">
  <link rel="alternate" hreflang="en" href="${ROOTURL}en/">
  <link rel="alternate" hreflang="x-default" href="${ROOTURL}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="${lang === 'he' ? 'מקהלת פרחי שמיים' : 'Pirchei Shomayim Boys’ Choir'}">
  <meta property="og:url" content="${PAGEURL}">
  <meta property="og:title" content="${esc(t.title)}">
  <meta property="og:description" content="${esc(t.description)}">
  <meta property="og:image" content="${IMGURL}og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="${esc(t.hero.alts[0])}">
  <meta property="og:locale" content="${lang === 'he' ? 'he_IL' : 'en_US'}">
  <meta property="og:locale:alternate" content="${lang === 'he' ? 'en_US' : 'he_IL'}">
  <meta name="twitter:card" content="summary_large_image">
  <script type="application/ld+json">${JSON.stringify({
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'MusicGroup', '@id': `${ROOTURL}#choir`,
        name: lang === 'he' ? 'מקהלת פרחי שמיים' : 'Pirchei Shomayim Boys’ Choir',
        // כל צורות הכתיב שאנשים מחפשים בפועל
        alternateName: lang === 'he'
          ? ['Pirchei Shomayim Boys’ Choir', 'פרחי שמיים', 'פרחי שמים', 'מקהלת פרחי שמים', 'מקהלת ילדי פרחי שמים', 'מקהלת הילדים פרחי שמיים', 'Pirchei Shomayim', 'Pirchei Shamayim']
          : ['מקהלת פרחי שמיים', 'פרחי שמים', 'Pirchei Shomayim', 'Pirchei Shamayim', 'Pirchei Shomayim Boy’s Choir', 'Pirchei Shomayim Choir'],
        member: [{ '@type': 'OrganizationRole', roleName: t.about.conductorRole, member: { '@type': 'Person', name: lang === 'he' ? 'מרדכי גורדון' : 'Mordechai Gordon', alternateName: lang === 'he' ? ['ר׳ מרדכי גורדון', 'מרדי גורדון', 'Mordechai Gordon', 'Mordi Gordon'] : ['R’ Mordechai Gordon', 'Mordi Gordon', 'מרדכי גורדון', 'מרדי גורדון'], jobTitle: t.about.conductorRole } }],
        description: t.description,
        url: ROOTURL,
        logo: { '@type': 'ImageObject', url: `${IMGURL}icon-256.png`, width: 256, height: 256 },
        image: `${IMGURL}og.jpg`,
        email: CHOIR_EMAIL_HREF,
        genre: lang === 'he' ? 'מוזיקה יהודית, מקהלת ילדים' : 'Jewish music, boys’ choir',
        areaServed: (lang === 'he' ? ['ירושלים', 'בית שמש'] : ['Jerusalem', 'Beit Shemesh']).map((name) => ({ '@type': 'City', name })),
        knowsLanguage: ['he', 'en'],
        sameAs: [CHANNEL_URL],
      },
      { '@type': 'WebSite', '@id': `${ROOTURL}#website`, url: ROOTURL, name: lang === 'he' ? 'מקהלת פרחי שמיים' : 'Pirchei Shomayim Boys’ Choir', inLanguage: ['he', 'en'], publisher: { '@id': `${ROOTURL}#choir` }, creator: { '@type': 'Organization', name: BUILDER.name, url: BUILDER.url } },
      { '@type': 'WebPage', '@id': `${PAGEURL}#page`, url: PAGEURL, name: t.title, description: t.description, inLanguage: lang, isPartOf: { '@id': `${ROOTURL}#website` }, about: { '@id': `${ROOTURL}#choir` }, primaryImageOfPage: `${IMGURL}og.jpg` },
      { '@type': 'FAQPage', '@id': `${PAGEURL}#faq`, inLanguage: lang, mainEntity: S.faq.items.map(([q, a]) => ({ '@type': 'Question', name: q, acceptedAnswer: { '@type': 'Answer', text: a } })) },
    ],
  }).replace(/</g, '\\u003c')}</script>
  <link rel="icon" href="${A}img/icon-64.png" type="image/png">
  <link rel="apple-touch-icon" href="${A}img/icon-180.png">
  <link rel="preload" href="${A}fonts/${lang === 'he' ? 'heebo-hebrew' : 'heebo-latin'}.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="${A}fonts/${lang === 'he' ? 'frank-hebrew' : 'frank-latin'}.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="${A}img/stage/hero-2.webp" as="image" media="(min-width: 721px)" fetchpriority="high">
  <link rel="preload" href="${A}img/stage/hero-stage-m.webp" as="image" media="(max-width: 720px)" fetchpriority="high">
  <link rel="stylesheet" href="${A}site.css?v=${VERSION}">
  <script>document.documentElement.classList.add('js');try{var m=localStorage.getItem('ps-motion');if(m==='reduce'||(!m&&matchMedia('(prefers-reduced-motion: reduce)').matches))document.documentElement.dataset.motion='reduce'}catch(e){if(matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.dataset.motion='reduce'}</script>
  <script defer src="${A}site.js?v=${VERSION}"></script>
</head>
<body>
${sprite}
<a class="skip" href="#main">${t.skip}</a>

<header class="site-header" id="top">
  ${live ? '' : demoBar}
  <div class="wrap header-in">
    <a class="brand" href="#main" aria-label="${esc(t.brand + ' · ' + t.brandSub)}">
      <img class="brand-icon" src="${A}img/icon-180.png" alt="" width="44" height="44">
      <span class="brand-text"><b>${t.brand}</b><small>${t.brandSub}</small></span>
    </a>
    <nav class="main-nav" id="main-nav" aria-label="${lang === 'he' ? 'ניווט ראשי' : 'Main navigation'}">
      <ul>
        ${navHtml}
        ${navExtra}
      </ul>
    </nav>
    <div class="header-actions">
      <a class="lang-link" href="${t.otherHref}" hreflang="${t.other}" lang="${t.other}" aria-label="${esc(t.langShort + ' · ' + t.langAria)}" data-lang-link>${t.langShort}</a>
      <button class="icon-btn motion-btn" type="button" data-motion-toggle aria-pressed="false" aria-label="${esc(t.motionOff)}" title="${esc(t.motionOff)}">${icon('motion')}</button>
      <a class="btn btn-mint btn-sm header-cta is-quiet" href="#join">${t.headerCta}</a>
      <button class="icon-btn menu-btn" type="button" aria-controls="main-nav" aria-expanded="false" data-menu-toggle><span class="sr">${t.menu}</span>${icon('menu', 'ico-menu')}${icon('close', 'ico-close')}</button>
    </div>
  </div>
</header>

<main id="main" tabindex="-1">

  <section class="hero" aria-labelledby="hero-title">
    <div class="hero-media">
      <picture class="hero-slide is-active">
        <source media="(max-width: 720px)" srcset="${A}img/stage/hero-stage-m.webp">
        <img src="${A}img/stage/hero-2.webp" alt="${esc(t.hero.alts[1])}" width="1280" height="922" fetchpriority="high" decoding="async">
      </picture>
      <span class="hero-scrim"></span>
      <span class="beam beam-a"></span>
      <span class="beam beam-b"></span>
    </div>
    <div class="wrap hero-in">
      <div class="hero-copy">
        <h1 id="hero-title"><span class="eyebrow">${esc(t.hero.eyebrow)}</span> <span>${esc(t.hero.h1a)}</span> <span class="h1-accent">${esc(t.hero.h1b)}</span></h1>
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

        <div class="fit" role="group" aria-labelledby="fit-q">
          <p class="fit-q" id="fit-q"><b>${esc(t.join.fit.q)}</b> <span>${esc(t.join.fit.note)}</span></p>
          <div class="fit-ages">${[7, 8, 9, 10, 11, 12, 13].map((n) => `<button type="button" class="chip fit-age" data-age="${n}" aria-pressed="false" aria-label="${esc(t.join.fit.label)}: ${n === 13 ? t.join.fit.older : n}"><bdi dir="ltr">${n === 13 ? t.join.fit.older : n}</bdi></button>`).join('')}</div>
          <p class="fit-result" data-fit-result aria-live="polite"></p>
        </div>

        <div class="city-filter" role="group" aria-label="${esc(t.join.filterLabel)}">
          <button type="button" class="chip" data-city="all" aria-pressed="true">${esc(t.join.all)}</button>
          <button type="button" class="chip" data-city="jerusalem" aria-pressed="false">${esc(t.join.cities.jerusalem)}</button>
          <button type="button" class="chip" data-city="beit-shemesh" aria-pressed="false">${esc(t.join.cities['beit-shemesh'])}</button>
        </div>

        <p class="branches-note"><span>${icon('star')}${esc(t.join.ages)} · ${esc(t.join.audition)}</span><span>${icon('clock')}${esc(t.join.times)}</span></p>
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
        <p class="flyers">${icon('doc')}<span>${esc(t.join.flyers)}</span> <a href="${PDF}jerusalem-hebrew.pdf" target="_blank" rel="noopener" lang="he">${t.join.flyerHe}</a> · <a href="${PDF}jerusalem-english.pdf" target="_blank" rel="noopener" lang="en">${t.join.flyerEn}</a></p>${live ? `
        <p class="more-link"><a class="text-link" href="/${langSuffix}classes/">${esc(S.links.classes)}${icon('arrow', 'ico-dir')}</a></p>` : ''}

        <div class="join-form-area" id="join-form-area">
          <form class="join-form" id="join-form" novalidate aria-labelledby="form-title">
            <h3 id="form-title" tabindex="-1">${esc(t.form.title)}</h3>
            <p class="form-fit" data-form-fit hidden></p>
            <p class="branch-chosen" data-branch-chosen hidden><span>${esc(t.form.chosenLabel)}</span> <b data-branch-chosen-name></b> <button type="button" class="link-btn" data-branch-change>${esc(t.form.change)}</button></p>
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
            ${live ? '' : `<p class="demo-note">${esc(cfg.form === 'email' ? P.emailForm.demoNote : t.form.demoNote)}</p>`}
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
      <p class="kicker">${esc(t.why.kicker)}</p>
      <h2 id="why-title">${esc(t.why.title)}</h2>
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
        <p class="kicker">${esc(t.program.kicker)}</p>
        <h2 id="program-title">${esc(t.program.title)}</h2>
        <p class="section-lead">${esc(t.program.lead)}</p>
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
          <p class="kicker">${esc(t.music.kicker)}</p>
          <h2 id="music-title">${esc(t.music.title)}</h2>
          <p class="section-lead">${esc(cfg.tools ? t.music.lead : t.music.lead.split('.')[0] + '.')}</p>
        </div>
        <a class="text-link" href="${CHANNEL_URL}" target="_blank" rel="noopener">${icon('play')}<span>${esc(t.music.channel)}</span></a>
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
      <ul class="songs songs-home">${homeSongs.map((s) => songCard(s)).join('')}
      </ul>${cfg.tools ? `
      <div class="songs-more"><button type="button" class="btn btn-ghost btn-lg" data-library-open aria-haspopup="dialog" aria-controls="library">${icon('music')}${esc(L.libOpen)}${icon('arrow', 'ico-dir')}</button>${live ? `<a class="text-link" href="/${langSuffix}songs/">${esc(S.links.songs)}${icon('arrow', 'ico-dir')}</a>` : ''}</div>` : ''}
    </div>
  </section>
${cfg.stage ? `
  <section class="stage" id="stage" aria-labelledby="stage-title">
    <div class="wrap">
      <div class="section-head">
        <p class="kicker">${esc(t.stage.kicker)}</p>
        <h2 id="stage-title">${esc(t.stage.title)}</h2>
      </div>
      <div class="stage-grid${live ? ' is-single' : ''}">${live ? '' : `
        <article class="upcoming" data-reveal>
          <p class="kicker">${esc(t.stage.upcomingTitle)}</p>
          <span class="upcoming-ico">${icon('star')}</span>
          <p>${esc(t.stage.upcomingText)}</p>
        </article>`}
        <div class="shows">
          <h3 class="shows-title">${esc(t.stage.pastTitle)}</h3>
          <ul>
            ${t.stage.shows.map((s) => `<li data-reveal><button class="show" type="button" data-play="${s.video}"><img src="${A}img/stage/${s.img}-43.webp" alt="" width="720" height="540" loading="lazy" decoding="async"><span class="show-copy"><b>${esc(s.title)}</b><small>${esc(s.sub)}</small></span><span class="show-play">${icon('play')}</span></button></li>`).join('\n            ')}
          </ul>
        </div>
      </div>
      <div class="booking">
        <div><h3>${esc(t.stage.bookingTitle)}</h3><p>${esc(t.stage.bookingText)}</p></div>
        <a class="btn btn-outline" href="mailto:${CHOIR_EMAIL_HREF}?subject=${encodeURIComponent(t.stage.bookingSubject)}">${icon('mail')}${esc(t.stage.bookingCta)}</a>
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
        <p class="kicker">${esc(t.makhalolam.kicker)}</p>
        <h2 id="mk-title">${esc(t.makhalolam.title)} <span class="h2-sub">${esc(t.makhalolam.subtitle)}</span></h2>
        <p>${esc(t.makhalolam.text)}</p>
        <ul class="ticks">${t.makhalolam.points.map((p) => `<li>${icon('check')}${esc(p)}</li>`).join('')}</ul>
        <div class="mk-videos" data-reveal>
          <button class="mk-video" type="button" data-play="n6tLDS_ioYk"><img src="${A}img/covers/n6tLDS_ioYk-s.webp" alt="" width="360" height="203" loading="lazy" decoding="async"><span>${icon('play')}${esc(t.makhalolam.videoMain)}</span></button>
          <button class="mk-video" type="button" data-play="eSJg_mli2y8"><img src="${A}img/covers/eSJg_mli2y8-s.webp" alt="" width="360" height="203" loading="lazy" decoding="async"><span>${icon('play')}${esc(t.makhalolam.videoPromo)}</span></button>
        </div>
        <a class="btn btn-outline" href="mailto:${CHOIR_EMAIL_HREF}?subject=${encodeURIComponent(t.makhalolam.subject)}">${icon('mail')}${esc(t.makhalolam.cta)}</a>
      </div>
    </div>
  </section>
${cfg.behind ? `
  <section class="exclusive" id="behind" aria-labelledby="behind-title">
    <div class="curtain" data-curtain aria-hidden="true"><span class="curtain-l"></span><span class="curtain-r"></span></div>
    <div class="wrap">
      <div class="excl-head">
        <p class="excl-badge">${icon('star')}${esc(X.badge)}</p>
        <p class="kicker">${esc(live ? X.kickerLive : X.kicker)}</p>
        <h2 id="behind-title">${esc(X.title)}</h2>
        <p class="section-lead">${esc(live ? X.leadLive : X.lead)}</p>
      </div>
      ${live ? `<div class="excl-soon" data-reveal><span class="excl-ico">${icon('star')}</span><div class="excl-soon-copy"><h3>${esc(X.soonTitle)}</h3><p>${esc(X.soonText)}</p></div><a class="btn btn-purple" href="#club">${icon('bell')}${esc(X.notify)}</a></div>` : ''}
      <ul class="excl-grid"${live ? ' hidden' : ''}>
        ${X.items.map((it, i) => {
          const locked = it.teaser && cfg.club;
          return `<li class="excl-card${it.teaser ? ' is-teaser' : ''}" data-reveal style="--d:${i * 80}ms">
          <div class="excl-media"><img src="${A}img/covers/${it.img}.webp" alt="" width="640" height="360" loading="lazy" decoding="async"><span class="excl-tag">${esc(X.badge)}</span>${locked ? `<span class="excl-lock">${icon('bell')}${esc(X.members)}</span>` : ''}</div>
          <div class="excl-body">
            <p class="excl-type">${icon(it.icon)}${esc(it.type)}</p>
            <h3>${esc(it.title)}</h3>
            <p>${esc(it.text)}</p>
            ${locked ? `<a class="text-link" href="#club">${esc(live ? X.notify : X.joinClub)}${icon('arrow', 'ico-dir')}</a>` : `<span class="soon-dark">${esc(live ? X.soonLive : X.soon)}</span>`}
          </div>
        </li>`;
        }).join('\n        ')}
      </ul>
      ${live ? '' : `<p class="excl-note">${esc(X.note)}</p>`}
    </div>
    <div class="channel-strip">
      <div class="wrap"><h3 class="strip-title">${icon('play')}${esc(X.fromChannel)}</h3></div>
      <div class="strip-viewport">
        <ul class="strip-track">
          ${shorts.map((s) => `<li class="strip-item strip-short"><button type="button" data-play="${s.id}"><img src="${A}img/shorts/${s.id}.webp" alt="" width="360" height="640" loading="lazy" decoding="async"><span class="short-cap">${icon('play')}${esc(s[lang])}</span></button></li>`).join('\n          ')}
        </ul>
      </div>
    </div>
  </section>` : ''}
${cfg.club ? `
  <section class="club" id="club" aria-labelledby="club-title">
    <div class="wrap club-grid">
      <div class="club-copy">
        <p class="kicker">${esc(P.club.kicker)}</p>
        <h2 id="club-title">${esc(P.club.title)}</h2>
        <p class="section-lead">${esc(P.club.lead)}</p>
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
          <div class="hp" aria-hidden="true"><label for="c-website">Website</label><input id="c-website" name="website" type="text" tabindex="-1" autocomplete="off"></div>
          <button class="btn btn-purple btn-lg" type="submit">${icon('bell')}${esc(P.club.submit)}</button>
          ${live ? '' : `<p class="demo-note">${esc(P.club.demoNote)}</p>`}
        </form>
        <div class="club-success" id="club-success" hidden tabindex="-1" aria-live="polite"></div>
      </div>
    </div>
  </section>` : ''}

  <section class="about" id="about" aria-labelledby="about-title">
    <div class="wrap about-grid">
      <div class="about-logo" data-reveal><img src="${A}img/logo-full.webp" alt="${esc(t.about.logoAlt)}" width="720" height="508" loading="lazy" decoding="async"></div>
      <div class="about-copy">
        <p class="kicker">${esc(t.about.kicker)}</p>
        <h2 id="about-title">${esc(t.about.title)}</h2>
        ${t.about.paras.map((p) => `<p>${esc(p)}</p>`).join('\n        ')}
        <p class="conductor"><b>${esc(t.about.conductor)}</b><span>${esc(t.about.conductorRole)}</span></p>
      </div>
    </div>
    ${live ? '' : `<div class="wrap">
      <ul class="about-cards">
        ${t.about.cards.map(([h, p]) => `<li data-reveal><h3>${esc(h)}</h3><p>${esc(p)}</p><span class="soon">${esc(t.about.soon)}</span></li>`).join('\n        ')}
        <li class="testimonials" data-reveal><span class="quote-mark" aria-hidden="true">”</span><h3>${esc(t.about.testimonialsTitle)}</h3><p>${esc(t.about.testimonialsText)}</p><span class="soon">${esc(t.about.soon)}</span></li>
      </ul>
    </div>`}
  </section>

  <section class="faq" id="faq" aria-labelledby="faq-title">
    <div class="wrap faq-in">
      <div class="section-head"><p class="kicker">${esc(S.faq.kicker)}</p><h2 id="faq-title">${esc(S.faq.title)}</h2></div>
      <div class="faq-list">
        ${S.faq.items.map(([q, a]) => `<details class="faq-item"><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join('\n        ')}
      </div>
    </div>
  </section>

  <section class="final" aria-labelledby="final-title">
    <span class="final-beam fb-a" aria-hidden="true"></span><span class="final-beam fb-b" aria-hidden="true"></span><span class="final-pool" aria-hidden="true"></span>
    <div class="wrap final-in">
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
      <a href="mailto:${CHOIR_EMAIL_HREF}">${icon('mail')}<span>${esc(t.footer.contact)}</span></a>
      <a href="${CHANNEL_URL}" target="_blank" rel="noopener">${icon('play')}<span>${esc(t.footer.youtube)}</span></a>
      <a href="${t.otherHref}" hreflang="${t.other}" lang="${t.other}" data-lang-link>${t.langLabel}</a>
    </div>
  </div>
  <div class="wrap footer-legal">
    <span>${esc(t.footer.rights)}</span>
    <a href="${live ? legal + '#accessibility' : '#top'}">${esc(t.footer.access)}</a>
    <a href="${legal}">${esc(t.footer.privacy)}</a>
    ${live ? `<a href="/${langSuffix}classes/">${esc(t.nav.classes)}</a><a href="/${langSuffix}songs/">${esc(t.nav.music)}</a>` : ''}
    ${live ? '' : `<span class="footer-demo">${esc(t.footer.demo)}</span>`}
    ${motionText.replace('class="motion-text"', 'class="motion-text footer-motion"')}
    ${credit(t)}
    <p class="footer-names">${esc(S.names)}</p>
  </div>
</footer>

${cfg.tools ? `<div class="library" id="library" role="dialog" aria-modal="true" aria-labelledby="library-title" hidden>
  <div class="library-in">
    <div class="library-head">
      <div class="wrap library-bar">
        <h2 id="library-title">${esc(L.libTitle)}</h2>
        <p class="song-count" aria-live="polite" data-song-count></p>
        <button type="button" class="icon-btn library-close" data-library-close aria-label="${esc(L.libClose)}">${icon('close')}</button>
      </div>
      <div class="wrap music-tools">
        <div class="chips" role="group" aria-label="${lang === 'he' ? 'סינון שירים' : 'Filter songs'}">
          ${Object.entries(t.music.filters).map(([k, v], i) => `<button type="button" class="chip chip-dark" data-filter="${k}" aria-pressed="${i === 0}">${esc(v)}</button>`).join('\n          ')}
        </div>
        <div class="search">
          <label class="sr" for="song-search">${esc(t.music.searchLabel)}</label>
          ${icon('search')}
          <input id="song-search" type="search" placeholder="${esc(t.music.searchPlaceholder)}" autocomplete="off">
        </div>
      </div>
    </div>
    <div class="wrap library-body">
      <ul class="songs lib-songs">${songs.map((s) => songCard(s, true)).join('')}
      </ul>
      <p class="songs-empty" hidden>${esc(t.music.empty)}</p>
    </div>
  </div>
</div>
` : ''}<a class="btn btn-mint sticky-cta" href="#join" data-sticky-cta>${esc(t.hero.cta)}${icon('arrow', 'ico-dir')}</a>
<div class="player" id="player" role="dialog" aria-modal="true" aria-labelledby="player-title" hidden>
  <div class="player-backdrop" data-player-close></div>
  <div class="player-bg" aria-hidden="true"><img alt="" data-player-bg></div>
  <div class="player-box">
    <div class="player-top">
      <span class="player-now"><span class="eq eq-live" aria-hidden="true"><i></i><i></i><i></i><i></i></span>${esc(t.player.nowPlaying)}</span>
      <span class="player-count" data-player-count></span>
      <button type="button" class="icon-btn player-close" data-player-close aria-label="${esc(t.player.close)}">${icon('close')}</button>
    </div>
    <div class="player-main">
      <div class="player-stage">
        <div class="player-frame" data-player-frame></div>
        <p class="player-note">${esc(t.player.note)}</p>
      </div>
      <aside class="player-side" aria-label="${esc(t.player.label)}">
        <div class="player-info">
          <p class="player-tags"><span class="player-cat" data-player-cat></span><span class="player-dur" data-player-dur>${icon('clock')}<bdi dir="ltr"></bdi></span></p>
          <h2 id="player-title" class="player-title"></h2>
          <p class="player-about" data-player-about></p>
          <p class="player-by">${icon('music')}<span>${esc(t.player.by)}</span></p>
        </div>
        <div class="player-actions">
          <button type="button" class="btn btn-ghost btn-sm" data-player-prev aria-label="${esc(t.player.prev)}">${icon('arrow', 'ico-prev')}<span>${esc(t.player.prevShort)}</span></button>
          <button type="button" class="btn btn-ghost btn-sm" data-player-next aria-label="${esc(t.player.next)}"><span>${esc(t.player.nextShort)}</span>${icon('arrow', 'ico-dir')}</button>
          <button type="button" class="btn btn-ghost btn-sm" data-player-share>${icon('share')}<span>${esc(t.player.share)}</span></button>
          <a class="btn btn-ghost btn-sm" data-player-yt href="#" target="_blank" rel="noopener">${icon('external')}<span>${esc(t.player.youtube)}</span></a>
        </div>
        <p class="player-toast" data-player-toast role="status" aria-live="polite"></p>
        <div class="player-upnext" data-player-upnext>
          <h3 class="player-h3">${esc(t.player.upNext)}</h3>
          <ol class="player-queue" data-player-queue></ol>
        </div>
        <div class="player-cta">
          <p>${esc(t.player.ctaTitle)}</p>
          <a class="btn btn-mint" href="#join" data-player-join>${esc(t.player.cta)}${icon('arrow', 'ico-dir')}</a>
        </div>
        <p class="player-keys">${esc(t.player.keys)}</p>
      </aside>
    </div>
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

// ===================================================================
// האתר החי: מסלול 3 בעברית ובאנגלית, לתיקייה dist/live — בדיוק במבנה של public_html בשרת
// ===================================================================
const legalText = {
  he: {
    title: 'מדיניות פרטיות והצהרת נגישות · מקהלת פרחי שמיים', description: 'איך אנחנו שומרים על הפרטים שמשאירים באתר, ומה עשינו כדי שהאתר יהיה נגיש לכולם.',
    back: 'חזרה לאתר', h1: 'מדיניות פרטיות',
    privacy: [
      ['אילו פרטים נאספים', 'כשמשאירים פרטים לחוג: שם ההורה, טלפון, מייל, שם הילד, גיל, חיידר וכיתה, והערות אם נכתבו. כשנרשמים לעדכונים: כתובת מייל, שם אם נכתב, והנושאים שבחרתם.'],
      ['למה הם משמשים', 'כדי לחזור אליכם לגבי החוג ולתאם מבדק התאמה, ולשלוח רק את העדכונים שביקשתם ואישרתם במייל.'],
      ['מי רואה אותם', 'צוות המקהלה בלבד. הפרטים לא נמכרים ולא מועברים לאף גורם אחר.'],
      ['איפה הם נשמרים', 'בשרת האתר, ובהודעת מייל שנשלחת לצוות המקהלה.'],
      ['צפייה, תיקון ומחיקה', 'אפשר לבקש בכל עת לראות, לתקן או למחוק את הפרטים במייל {email}. אפשר להפסיק לקבל עדכונים בכל עת באותו מייל.'],
      ['סרטונים ועוגיות', 'הסרטונים באתר מוטמעים משירות וידאו חיצוני של גוגל, במצב פרטיות מוגברת, ונטענים רק כשלוחצים לנגן. האתר לא משתמש בעוגיות מעקב או פרסום. בדפדפן נשמרת רק ההעדפה אם להציג אנימציות.'],
    ],
    a11yTitle: 'הצהרת נגישות',
    a11y: [
      'האתר נבנה במטרה לעמוד בתקן הישראלי 5568 ובהנחיות WCAG 2.1 ברמה AA.',
      'מה עשינו: ניווט מלא במקלדת, טקסט חלופי לתמונות, ניגודיות צבעים גבוהה, טפסים עם הודעות שגיאה ברורות, התאמה מלאה לנייד, מתג לעצירת אנימציות, וכיבוד הגדרת ״הפחתת תנועה״ של המכשיר.',
      'נתקלתם בקושי או בתקלת נגישות? כתבו לנו ל־{email}, ונטפל בהקדם.',
    ],
    updated: 'עודכן בנובמבר 2026',
    nf: { title: 'הדף לא נמצא · מקהלת פרחי שמיים', h1: 'הדף הזה לא נמצא', text: 'ייתכן שהכתובת השתנתה כשהאתר התחדש. כל מה שחיפשתם נמצא בעמוד הראשי.', home: 'לעמוד הראשי', classes: 'מצאו חוג באזור שלכם' },
  },
  en: {
    title: 'Privacy policy & accessibility · Pirchei Shomayim Boys’ Choir', description: 'How we look after the details you leave on the site, and what we did to make the site accessible to everyone.',
    back: 'Back to the site', h1: 'Privacy policy',
    privacy: [
      ['What we collect', 'When you leave details for a class: parent’s name, phone, email, child’s name, age, cheder and grade, and notes if you wrote any. When you sign up for updates: your email, your name if given, and the topics you chose.'],
      ['What it is used for', 'To get back to you about the class and arrange an audition, and to send only the updates you asked for and confirmed by email.'],
      ['Who sees it', 'Only the choir team. Your details are never sold or passed on to anyone else.'],
      ['Where it is kept', 'On the website’s server, and in an email sent to the choir team.'],
      ['Viewing, correcting and deleting', 'You can ask at any time to see, correct or delete your details by emailing {email}. You can stop receiving updates at any time the same way.'],
      ['Videos and cookies', 'Videos are embedded from an external video service run by Google, in privacy-enhanced mode, and load only when you press play. The site uses no tracking or advertising cookies. Your browser only remembers whether to show animations.'],
    ],
    a11yTitle: 'Accessibility statement',
    a11y: [
      'The site was built with the aim of meeting Israeli Standard 5568 and WCAG 2.1 at level AA.',
      'What we did: full keyboard navigation, text alternatives for images, strong colour contrast, forms with clear error messages, full mobile support, a switch to stop animations, and respect for the device’s “reduce motion” setting.',
      'Ran into a difficulty or an accessibility problem? Email us at {email} and we’ll take care of it promptly.',
    ],
    updated: 'Updated November 2026',
    nf: { title: 'Page not found · Pirchei Shomayim Boys’ Choir', h1: 'We couldn’t find this page', text: 'The address may have changed when the site was renewed. Everything you were looking for is on the home page.', home: 'To the home page', classes: 'Find a class near you' },
  },
};

function simplePage(key, { title, description, path, robots, body }) {
  const t = dict[key]; const L = legalText[key];
  const home = key === 'he' ? '/' : '/en/';
  const alt = path === null ? '' : `
  <link rel="canonical" href="${LIVE}${(key === 'he' ? '' : 'en/') + path}">
  <link rel="alternate" hreflang="he" href="${LIVE}${path}">
  <link rel="alternate" hreflang="en" href="${LIVE}en/${path}">`;
  return `<!doctype html>
<html lang="${key}" dir="${t.dir}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${esc(title)}</title>
  <meta name="description" content="${esc(description)}">
  <meta name="robots" content="${robots}">
  <meta name="theme-color" content="#0b0812">${alt}
  <link rel="icon" href="/ps/assets/img/icon-64.png" type="image/png">
  <link rel="stylesheet" href="/ps/assets/site.css?v=${VERSION}">
</head>
<body class="simple">
  <header class="simple-head"><div class="wrap simple-head-in">
    <a class="brand" href="${home}"><img class="brand-icon" src="/ps/assets/img/icon-180.png" alt="" width="44" height="44"><span class="brand-text"><b>${t.brand}</b><small>${t.brandSub}</small></span></a>
    <a class="btn btn-ghost btn-sm" href="${home}">${esc(L.back)}</a>
  </div></header>
  <main class="wrap legal">${body}</main>
  <footer class="wrap simple-foot"><span>${esc(t.footer.rights)}</span> · <a href="mailto:${CHOIR_EMAIL_HREF}">${CHOIR_EMAIL}</a>${credit(t)}</footer>
</body>
</html>`;
}

const DIST = join(ROOT, 'dist', 'live');
rmSync(DIST, { recursive: true, force: true });
const today = '2026-11-24';
for (const key of ['he', 'en']) {
  const L = legalText[key];
  const fixed = (h) => (key === 'he' ? bidi(h) : h);
  write(join(DIST, 'ps', 'pages', `${key}.html`), fixed(page(dict[key], LIVE_PLAN, true)));
  const mail = `<a href="mailto:${CHOIR_EMAIL_HREF}">${CHOIR_EMAIL}</a>`;
  write(join(DIST, 'ps', 'pages', `privacy-${key}.html`), fixed(simplePage(key, {
    title: L.title, description: L.description, path: 'privacy/', robots: 'index, follow',
    body: `<h1>${esc(L.h1)}</h1>${L.privacy.map(([h, p]) => `<h2>${esc(h)}</h2><p>${esc(p).replace('{email}', mail)}</p>`).join('')}
      <h1 id="accessibility" class="legal-h1-2">${esc(L.a11yTitle)}</h1>${L.a11y.map((p) => `<p>${esc(p).replace('{email}', mail)}</p>`).join('')}
      <p class="legal-updated">${esc(L.updated)}</p>`,
  })));
  write(join(DIST, 'ps', 'pages', `404-${key}.html`), fixed(simplePage(key, {
    title: L.nf.title, description: L.nf.text, path: null, robots: 'noindex',
    body: `<div class="nf"><p class="nf-code" aria-hidden="true">404</p><h1>${esc(L.nf.h1)}</h1><p>${esc(L.nf.text)}</p>
      <div class="nf-actions"><a class="btn btn-mint btn-lg" href="${key === 'he' ? '/' : '/en/'}#join">${esc(L.nf.classes)}</a><a class="btn btn-ghost btn-lg" href="${key === 'he' ? '/' : '/en/'}">${esc(L.nf.home)}</a></div></div>`,
  })));
}
// דפי ה־HTML נקראים רק דרך התוסף, לא ישירות
write(join(DIST, 'ps', 'pages', '.htaccess'), '<IfModule mod_authz_core.c>\n  Require all denied\n</IfModule>\n<IfModule !mod_authz_core.c>\n  Order allow,deny\n  Deny from all\n</IfModule>\n');
cpSync(join(OUT, 'assets'), join(DIST, 'ps', 'assets'), { recursive: true, filter: (src) => !/admin\.(css|js)$/.test(src) });
for (const f of ['jerusalem-hebrew.pdf', 'jerusalem-english.pdf']) cpSync(join(ROOT, 'assets', f), join(DIST, 'ps', 'flyers', f));
cpSync(join(ROOT, 'tools', 'live', 'pirchei-site.php'), join(DIST, 'wp-content', 'mu-plugins', 'pirchei-site.php'));
write(join(DIST, 'robots.txt'), `User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php
Disallow: /ps/pages/

Sitemap: ${LIVE}sitemap.xml
`);
const urlEntry = (path, img) => ['', 'en/'].map((pre) => `  <url>
    <loc>${LIVE}${pre}${path}</loc>
    <lastmod>${today}</lastmod>
    <xhtml:link rel="alternate" hreflang="he" href="${LIVE}${path}"/>
    <xhtml:link rel="alternate" hreflang="en" href="${LIVE}en/${path}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="${LIVE}${path}"/>${img ? `
    <image:image><image:loc>${LIVE}ps/assets/img/og.jpg</image:loc></image:image>
    <image:image><image:loc>${LIVE}ps/assets/img/logo-full.webp</image:loc></image:image>` : ''}
  </url>`).join('\n');
write(join(DIST, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
${urlEntry('', true)}
${urlEntry('privacy/', false)}
</urlset>
`);

// תיאור האתר לכלי בינה מלאכותית (מחליף את הקובץ הישן שנוצר אוטומטית)
write(join(DIST, 'llms.txt'), `# מקהלת פרחי שמיים · Pirchei Shomayim Boys’ Choir

> מקהלת ילדים וחוגי מקהלה ופיתוח קול לבנים בגילאי 8–12 בירושלים ובבית שמש, בניצוח ר׳ מרדכי גורדון. Boys’ choir and choir classes for boys aged 8–12 in Jerusalem and Beit Shemesh, conducted by R’ Mordechai Gordon.

## עמודים · Pages

- [העמוד הראשי](${LIVE}): חוגים, שירים וקליפים, הופעות, מאחורי הקלעים, מקהלולם, עדכונים ואודות
- [English home page](${LIVE}en/): classes, songs and videos, concerts, behind the scenes, Makhalolam, updates and about
- [חוגי מקהלה בירושלים ובבית שמש](${LIVE}classes/)
- [כל השירים והקליפים](${LIVE}songs/)
- [Choir classes (English)](${LIVE}en/classes/)
- [All songs (English)](${LIVE}en/songs/)
- [מדיניות פרטיות והצהרת נגישות](${LIVE}privacy/)
- [Privacy policy and accessibility](${LIVE}en/privacy/)

## חוגים · Classes

- ירושלים: רמת אשכול, נווה יעקב
- בית שמש: רמה א׳, רמה ד׳
- קבלה במבדק התאמה קצר. ההרשמה דרך הטופס באתר.

## קשר · Contact

- מייל: ${CHOIR_EMAIL}
- ערוץ הסרטונים: ${CHANNEL_URL}
`);

// IndexNow: קובץ המפתח שמאשר לבינג ולמנועים נוספים שאנחנו בעלי האתר (המפתח ציבורי מעצם הגדרתו)
const INDEXNOW_KEY = '9710292b37ca4dba4d27677b90ea89e6';
write(join(DIST, `${INDEXNOW_KEY}.txt`), INDEXNOW_KEY);

// ===================================================================
// עמודי תוכן לקידום: חוגים ושירים, בעברית ובאנגלית
// ===================================================================
const isoDur = (d) => { if (!d) return undefined; const p = d.split(':').map(Number); const [h, m, s] = p.length === 3 ? p : [0, p[0], p[1]]; return 'PT' + (h ? h + 'H' : '') + (m ? m + 'M' : '') + (s ? s + 'S' : ''); };
const ytUrl = (s) => (s.vertical ? `https://www.youtube.com/shorts/${s.id}` : `https://www.youtube.com/watch?v=${s.id}`);
const choirRef = (key) => ({ '@type': 'MusicGroup', '@id': `${LIVE}#choir`, name: key === 'he' ? 'מקהלת פרחי שמיים' : 'Pirchei Shomayim Boys’ Choir', url: LIVE });
const crumbsLd = (key, name, url) => ({ '@type': 'BreadcrumbList', itemListElement: [
  { '@type': 'ListItem', position: 1, name: dict[key].brand, item: LIVE + (key === 'he' ? '' : 'en/') },
  { '@type': 'ListItem', position: 2, name, item: url },
] });
const faqHtml = (S) => `<div class="faq-list">${S.faq.items.map(([q, a]) => `<details class="faq-item"><summary>${esc(q)}</summary><p>${esc(a)}</p></details>`).join('')}</div>`;

function contentPage(key, { path, title, description, crumb, body, ld }) {
  const t = dict[key]; const S = seoText[key];
  const pre = key === 'he' ? '' : 'en/';
  const home = '/' + pre;
  const url = LIVE + pre + path;
  const cur = (p) => (p === path ? ' aria-current="page"' : '');
  return `<!doctype html>
<html lang="${key}" dir="${t.dir}" data-motion="full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <title>${esc(title)}</title>
  <meta name="description" content="${esc(description)}">
  <meta name="robots" content="index, follow, max-image-preview:large, max-video-preview:-1">
  <meta name="theme-color" content="#0b0812">
  <link rel="canonical" href="${url}">
  <link rel="alternate" hreflang="he" href="${LIVE}${path}">
  <link rel="alternate" hreflang="en" href="${LIVE}en/${path}">
  <link rel="alternate" hreflang="x-default" href="${LIVE}${path}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="${key === 'he' ? 'מקהלת פרחי שמיים' : 'Pirchei Shomayim Boys’ Choir'}">
  <meta property="og:url" content="${url}">
  <meta property="og:title" content="${esc(title)}">
  <meta property="og:description" content="${esc(description)}">
  <meta property="og:image" content="${LIVE}ps/assets/img/og.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:locale" content="${key === 'he' ? 'he_IL' : 'en_US'}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" href="/ps/assets/img/icon-64.png" type="image/png">
  <link rel="apple-touch-icon" href="/ps/assets/img/icon-180.png">
  <link rel="preload" href="/ps/assets/fonts/${key === 'he' ? 'heebo-hebrew' : 'heebo-latin'}.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="preload" href="/ps/assets/fonts/${key === 'he' ? 'frank-hebrew' : 'frank-latin'}.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/ps/assets/site.css?v=${VERSION}">
  <script type="application/ld+json">${JSON.stringify({ '@context': 'https://schema.org', '@graph': [
    { '@type': 'WebPage', '@id': `${url}#page`, url, name: title, description, inLanguage: key, isPartOf: { '@type': 'WebSite', '@id': `${LIVE}#website`, url: LIVE }, about: { '@id': `${LIVE}#choir` } },
    crumbsLd(key, crumb, url), choirRef(key), ...ld] }).replace(/</g, '\\u003c')}</script>
</head>
<body class="simple cpage">
${sprite}
  <a class="skip" href="#main">${key === 'he' ? 'דילוג לתוכן' : 'Skip to content'}</a>
  <header class="simple-head"><div class="wrap simple-head-in">
    <a class="brand" href="${home}"><img class="brand-icon" src="/ps/assets/img/icon-180.png" alt="" width="44" height="44"><span class="brand-text"><b>${t.brand}</b><small>${t.brandSub}</small></span></a>
    <nav class="cp-nav" aria-label="${key === 'he' ? 'ניווט' : 'Navigation'}"><a href="${home}">${esc(S.links.home)}</a><a href="/${pre}classes/"${cur('classes/')}>${esc(t.nav.classes)}</a><a href="/${pre}songs/"${cur('songs/')}>${esc(t.nav.music)}</a></nav>
    <div class="cp-actions"><a class="lang-link" href="/${key === 'he' ? 'en/' : ''}${path}" hreflang="${t.other}" lang="${t.other}" aria-label="${esc(t.langShort + ' · ' + t.langAria)}">${t.langShort}</a><a class="btn btn-mint btn-sm" href="${home}#join">${esc(S.links.join)}</a></div>
  </div></header>
  <main class="wrap cp-main" id="main">
    <nav class="crumbs" aria-label="${key === 'he' ? 'מיקום בעמוד' : 'Breadcrumb'}"><a href="${home}">${t.brand}</a><span aria-hidden="true">›</span><span aria-current="page">${esc(crumb)}</span></nav>
    ${body}
  </main>
  <footer class="wrap simple-foot cp-foot">
    <span>${esc(t.footer.rights)}</span>
    <a href="${home}">${esc(S.links.home)}</a><a href="/${pre}classes/">${esc(t.nav.classes)}</a><a href="/${pre}songs/">${esc(t.nav.music)}</a><a href="/${pre}privacy/">${esc(t.footer.privacy)}</a>
    <a href="mailto:${CHOIR_EMAIL_HREF}">${CHOIR_EMAIL}</a><a href="${CHANNEL_URL}" target="_blank" rel="noopener">${esc(t.footer.youtube)}</a>
    ${credit(t)}
    <p class="footer-names">${esc(S.names)}</p>
  </footer>
</body>
</html>`;
}

for (const key of ['he', 'en']) {
  const t = dict[key]; const S = seoText[key]; const C = S.classes; const G = S.songs;
  const pre = key === 'he' ? '' : 'en/'; const home = '/' + pre;
  const fixed = (h) => (key === 'he' ? bidi(h) : h);
  // ---- עמוד החוגים ----
  const branchCard = (b) => `<article class="cp-branch" id="${b.id}">
          <p class="cp-city-name">${icon('pin')}${esc(t.join.cities[b.city])}</p>
          <h3>${esc(C.branchTitle.replace('{name}', b[key].name))}</h3>
          <ul class="cp-list">${C.facts.map((f) => `<li>${icon('check')}${esc(f)}</li>`).join('')}</ul>
          <p class="cp-reg"><b>${esc(C.regLabel)}</b> ${esc(b[key].venue)}</p>
          <a class="btn btn-purple" href="${home}?branch=${b.id}#join-form-area">${esc(C.cta)}${icon('arrow', 'ico-dir')}</a>
        </article>`;
  const classesBody = `<h1>${esc(C.h1)}</h1>
    <p class="cp-lead">${esc(C.lead)}</p>
    ${['jerusalem', 'beit-shemesh'].map((city) => `<section class="cp-sec" aria-labelledby="c-${city}"><h2 id="c-${city}">${esc(C.cityTitle[city])}</h2>
      <div class="cp-branches">${branches.filter((b) => b.city === city).map(branchCard).join('')}</div></section>`).join('\n    ')}
    <section class="cp-sec" aria-labelledby="c-how"><h2 id="c-how">${esc(C.howTitle)}</h2><ol class="cp-steps">${C.how.map((s) => `<li>${esc(s)}</li>`).join('')}</ol></section>
    <section class="cp-sec" aria-labelledby="c-faq"><h2 id="c-faq">${esc(S.faq.title)}</h2>${faqHtml(S)}</section>
    <div class="cp-end"><h2>${esc(C.endTitle)}</h2><a class="btn btn-mint btn-lg" href="${home}#join">${esc(C.endCta)}${icon('arrow', 'ico-dir')}</a></div>`;
  const courses = { '@type': 'ItemList', name: C.h1, itemListElement: branches.map((b, i) => ({ '@type': 'ListItem', position: i + 1, item: {
    '@type': 'Course', name: C.branchTitle.replace('{name}', b[key].name), description: C.lead, provider: { '@id': `${LIVE}#choir` },
    url: `${LIVE}${pre}classes/#${b.id}`,
    hasCourseInstance: { '@type': 'CourseInstance', courseMode: 'onsite', location: { '@type': 'Place', name: b[key].venue, address: { '@type': 'PostalAddress', addressLocality: t.join.cities[b.city], addressCountry: 'IL' } } },
  } })) };
  write(join(DIST, 'ps', 'pages', `classes-${key}.html`), fixed(contentPage(key, { path: 'classes/', title: C.title, description: C.description, crumb: t.nav.classes, body: classesBody, ld: [courses] })));

  // ---- עמוד השירים ----
  const order = ['clip', 'medley', 'live', 'makhalolam', 'short'];
  const catOf = (s) => (s.vertical ? 'short' : s.cat);
  const songItem = (s) => `<li class="cp-song"><a class="cp-song-main" href="${home}#play=${s.id}"><img src="/ps/assets/img/covers/${s.id}-s.webp" alt="" width="160" height="90" loading="lazy" decoding="async"><span class="cp-song-text"><span class="cp-song-title">${esc(s[key])}${s.isNew ? ` <b class="cp-new">${esc(G.newLabel)}</b>` : ''}</span><span class="cp-song-meta">${esc(catShort[key][catOf(s)])}${s.dur ? ` · <bdi dir="ltr">${s.dur}</bdi>` : ''}</span></span></a><a class="cp-song-yt" href="${ytUrl(s)}" target="_blank" rel="noopener" aria-label="${esc(s[key] + ' · ' + G.youtube)}" title="${esc(G.youtube)}">${icon('external')}</a></li>`;
  const n = songs.length;
  const songsBody = `<h1>${esc(G.h1)}</h1>
    <p class="cp-lead">${esc(G.lead.replace('{n}', n))}</p>
    ${order.map((cat) => { const list = songs.filter((s) => catOf(s) === cat); return list.length ? `<section class="cp-sec" aria-labelledby="s-${cat}"><h2 id="s-${cat}">${esc(G.cats[cat])} <small>(${list.length})</small></h2><ul class="cp-songs">${list.map(songItem).join('')}</ul></section>` : ''; }).join('\n    ')}
    <div class="cp-end"><h2>${esc(G.endTitle)}</h2><a class="btn btn-mint btn-lg" href="${home}#join">${esc(G.endCta)}${icon('arrow', 'ico-dir')}</a></div>`;
  const tracks = { '@type': 'ItemList', name: G.h1, numberOfItems: n, itemListElement: songs.map((s, i) => ({ '@type': 'ListItem', position: i + 1, item: {
    '@type': 'MusicRecording', name: s[key], url: ytUrl(s), duration: isoDur(s.dur), image: `${LIVE}ps/assets/img/covers/${s.id}.webp`, byArtist: { '@id': `${LIVE}#choir` },
  } })) };
  write(join(DIST, 'ps', 'pages', `songs-${key}.html`), fixed(contentPage(key, { path: 'songs/', title: G.title, description: G.description.replace('{n}', n), crumb: t.nav.music, body: songsBody, ld: [tracks] })));
}
// מפת האתר כוללת גם את עמודי החוגים והשירים
write(join(DIST, 'sitemap.xml'), `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
${urlEntry('', true)}
${urlEntry('classes/', false)}
${urlEntry('songs/', false)}
${urlEntry('privacy/', false)}
</urlset>
`);

// אימות הבעלות ב־Google Search Console — הקובץ חייב להישאר באתר תמיד
write(join(DIST, 'google188571416ee15586.html'), 'google-site-verification: google188571416ee15586.html');
