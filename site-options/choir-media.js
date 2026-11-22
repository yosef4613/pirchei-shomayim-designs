'use strict';

(() => {
  const english = document.documentElement.lang === 'en';
  const language = english ? 'en' : 'he';
  const assets = document.body.dataset.assets;
  const tracks = [
    {
      id: '-4sE-rfQI1k', duration: '4:10',
      he: ['אתה בחרתנו', 'מקהלת ביתר עילית', 'שירת ילדי המקהלה על מילות מוסף של ראש השנה, בלחן מרדכי וישראל מאיר גורדון.'],
      en: ['Ata Bechartanu', 'Beitar Illit choir', 'The boys sing words from the Rosh Hashanah Mussaf prayer, set to music by Mordechai and Yisrael Meir Gordon.'],
    },
    {
      id: 'rWHE6woblu4', duration: '6:20',
      he: ['אור חדש', 'מקהלת בית שמש', 'ביצוע על הבמה לשיר של צליל וזמר בלחן יוסי גרין, בעיבוד מוזיקלי של אבי דויטש.'],
      en: ['Or Chadash', 'Beit Shemesh choir', 'The boys perform Yossi Green’s song from the Tzlil V’Zemer repertoire, arranged by Avi Deutsch.'],
    },
    {
      id: 'aFhQjhm1if8', duration: '5:45',
      he: ['פתח ליבי', 'מקהלת רמת אשכול', 'קליפ לכבוד לומדי התורה, שצולם בכותל ובישיבת אש התורה בירושלים.'],
      en: ['Petach Libi', 'Ramat Eshkol choir', 'A tribute to Torah learners, filmed at the Western Wall and Yeshivat Aish HaTorah in Jerusalem.'],
    },
    {
      id: 'yjBQLelJDKw', duration: '15:10',
      he: ['מחרוזת שמחת תורה', 'עם שמחה פרידמן', 'ילדי פרחי שמיים ושמחה פרידמן שרים יחד מחרוזת שירי תורה.'],
      en: ['Simchat Torah medley', 'With Simcha Friedman', 'The choir and Simcha Friedman sing a medley of songs celebrating Torah.'],
    },
    {
      id: 'sAeFaXlxv0E', duration: '7:15',
      he: ['מחרוזת שירי תשובה', 'עם מוישי רוט', 'מחרוזת לימים הנוראים עם ״אבינו מלכנו״ ו״קחו עמכם״, בעיבוד מוישי רוט.'],
      en: ['Teshuvah medley', 'With Moishy Roth', 'A High Holy Days medley with Avinu Malkeinu and Kchu Imachem, arranged by Moishy Roth.'],
    },
    {
      id: 's_CNJzzsA8g', duration: '6:04',
      he: ['כי הם חיינו', 'ביצוע מהמקהלה', 'ביצוע ״כי הם חיינו״ מתוך ערוץ פרחי שמיים.'],
      en: ['Ki Hem Chayeinu', 'Choir performance', 'The choir performs Ki Hem Chayeinu.'],
    },
    {
      id: '_owLJAU6yx8', duration: '3:51', remoteCover: true,
      he: ['אם היו בני אדם', 'שיר לקראת שבועות', 'אחד משני השירים שהמקהלה פרסמה לקראת חג השבועות, על מתיקות לימוד התורה.'],
      en: ['Im Hayu Bnei Adam', 'A song for Shavuot', 'One of two songs the choir released for Shavuot, celebrating the sweetness of Torah study.'],
    },
    {
      id: '_eX_k4H5WHo', duration: '4:47',
      he: ['אהבת תורה', 'ביצוע מהמקהלה', 'ילדי פרחי שמיים שרים על אהבת התורה.'],
      en: ['Ahavat Torah', 'Choir performance', 'The boys sing about the love of Torah.'],
    },
    {
      id: 'Jboco7s9T2I', duration: '2:04', remoteCover: true,
      he: ['שישו ושמחו', 'קומזיץ בביתר עילית', 'שירה מתוך הקומזיץ של מקהלת פרחי שמיים בביתר עילית.'],
      en: ['Sisu Vesimchu', 'Beitar Illit kumzitz', 'A performance from the choir’s kumzitz in Beitar Illit.'],
    },
  ];

  const watchUrl = (id) => 'https://www.youtube.com/watch?v=' + id;
  const coverUrl = (track) => track.remoteCover
    ? 'https://i.ytimg.com/vi/' + track.id + '/mqdefault.jpg'
    : assets + '/covers/' + track.id + '.jpg';
  const playLabel = (name) => english ? 'Play ' + name : 'לנגן את ' + name;
  const musicPlayer = document.querySelector('[data-music-player]');
  const trackList = document.querySelector('[data-track-list]');
  const trackCards = new Map();
  let activePlayer;

  function setCover(image, track) {
    image.hidden = false;
    image.src = coverUrl(track);
  }

  function stop(player) {
    if (!player) return;
    player.querySelector('iframe')?.remove();
    player.querySelector('[data-play-video]').hidden = false;
    player.querySelector('[data-stop-video]').hidden = true;
    activePlayer = null;
  }

  function play(player) {
    const poster = player.querySelector('[data-play-video]');
    const id = new URL(poster.href).searchParams.get('v');
    if (!/^[a-zA-Z0-9_-]{11}$/.test(id)) return;
    stop(activePlayer);

    const frame = document.createElement('iframe');
    frame.title = poster.getAttribute('aria-label');
    frame.src = 'https://www.youtube-nocookie.com/embed/' + id + '?autoplay=1&rel=0&playsinline=1&hl=' + language;
    frame.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
    frame.allowFullscreen = true;
    frame.referrerPolicy = 'strict-origin-when-cross-origin';
    poster.parentElement.append(frame);
    poster.hidden = true;
    player.querySelector('[data-stop-video]').hidden = false;
    activePlayer = player;
    frame.focus({preventScroll: true});
  }

  function unmodifiedClick(event) {
    return !event.defaultPrevented && event.button === 0
      && !event.altKey && !event.ctrlKey && !event.metaKey && !event.shiftKey;
  }

  function selectTrack(track) {
    const [name, credit, description] = track[language];
    const poster = musicPlayer.querySelector('[data-play-video]');
    poster.href = watchUrl(track.id);
    poster.setAttribute('aria-label', playLabel(name));
    setCover(poster.querySelector('img'), track);
    musicPlayer.querySelector('[data-track-title]').textContent = name;
    musicPlayer.querySelector('[data-track-credit]').textContent = credit + ' · ' + track.duration;
    musicPlayer.querySelector('[data-track-description]').textContent = description;
    musicPlayer.querySelector('[data-watch-video]').href = poster.href;
    for (const [id, card] of trackCards) {
      if (id === track.id) card.setAttribute('aria-current', 'true');
      else card.removeAttribute('aria-current');
    }
  }

  function playTrack(event, track) {
    if (!unmodifiedClick(event)) return;
    event.preventDefault();
    selectTrack(track);
    musicPlayer.scrollIntoView({block: 'start'});
    play(musicPlayer);
  }

  function makeCard(track) {
    const card = document.createElement('a');
    const [name, credit] = track[language];
    card.className = 'media-track';
    card.href = watchUrl(track.id);
    card.setAttribute('aria-label', playLabel(name));
    const artwork = document.createElement('span');
    artwork.className = 'track-art';
    const image = document.createElement('img');
    image.alt = '';
    image.loading = 'lazy';
    image.width = 1280;
    image.height = 720;
    image.addEventListener('error', () => { image.hidden = true; });
    setCover(image, track);
    const duration = document.createElement('span');
    duration.className = 'track-length';
    duration.textContent = track.duration;
    artwork.append(image, duration);
    const info = document.createElement('span');
    info.className = 'track-info';
    const title = document.createElement('strong');
    title.textContent = name;
    const detail = document.createElement('small');
    detail.textContent = credit;
    info.append(title, detail);
    card.append(artwork, info);
    card.addEventListener('click', (event) => playTrack(event, track));
    trackCards.set(track.id, card);
    return card;
  }

  for (const player of document.querySelectorAll('[data-player]')) {
    const poster = player.querySelector('[data-play-video]');
    poster.querySelector('img').addEventListener('error', (event) => { event.currentTarget.hidden = true; });
    poster.addEventListener('click', (event) => {
      if (!unmodifiedClick(event)) return;
      event.preventDefault();
      play(player);
    });
    player.querySelector('[data-stop-video]').addEventListener('click', () => {
      stop(player);
      poster.focus({preventScroll: true});
    });
  }

  if (musicPlayer && trackList) {
    trackList.append(...tracks.map(makeCard));
    trackList.previousElementSibling.hidden = false;
    selectTrack(tracks[0]);
    for (const link of document.querySelectorAll('[data-story-track]')) {
      const track = tracks.find((song) => song.id === link.dataset.storyTrack);
      if (!track) continue;
      link.addEventListener('click', (event) => playTrack(event, track));
    }
  }
})();
