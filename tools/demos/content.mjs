// תוכן שלוש הדגמות המסלולים — מקור אחד לעברית ולאנגלית.
// כל פרט כאן מבוסס על הערוץ, המודעות ותשובות מרדכי לשאלון. פרטים שעדיין חסרים מסומנים בטקסט עצמו.

export const CHOIR_EMAIL = 'mordi.gordon@gmail.com';
export const CHANNEL_URL = 'https://www.youtube.com/@-pircheishomayimboyschoir7232';

export const branches = [
  {
    id: 'ramat-eshkol', city: 'jerusalem',
    he: { name: 'רמת אשכול', venue: 'בתיאום עם צוות המקהלה', reg: 'הרישום נעשה ישירות מול צוות המקהלה' },
    en: { name: 'Ramat Eshkol', venue: 'Arranged with the choir team', reg: 'registration is completed directly with the choir team' },
  },
  {
    id: 'neve-yaakov', city: 'jerusalem',
    he: { name: 'נווה יעקב', venue: 'מינהל קהילתי נווה יעקב', reg: 'הרישום הרשמי נעשה במינהל הקהילתי נווה יעקב' },
    en: { name: 'Neve Yaakov', venue: 'Neve Yaakov Community Administration', reg: 'official registration is completed at the Neve Yaakov Community Administration' },
  },
  {
    id: 'ramah-a', city: 'beit-shemesh',
    he: { name: 'רמה א׳', venue: 'מתנ״ס גוונים', reg: 'הרישום הרשמי נעשה במתנ״ס גוונים' },
    en: { name: 'Ramah A', venue: 'Gvanim Community Center', reg: 'official registration is completed at the Gvanim Community Center' },
  },
  {
    id: 'ramah-d', city: 'beit-shemesh',
    he: { name: 'רמה ד׳', venue: 'מרכז קהילתי דורות', reg: 'הרישום הרשמי נעשה במרכז הקהילתי דורות' },
    en: { name: 'Ramah D', venue: 'Dorot Community Center', reg: 'official registration is completed at the Dorot Community Center' },
  },
];

// שירים מהערוץ הרשמי. cat: clip | live | medley | makhalolam
export const songs = [
  { id: '-4sE-rfQI1k', cat: 'clip', dur: '4:11', isNew: true, he: 'אתה בחרתנו', en: 'Ata Bechartanu' },
  { id: 'rWHE6woblu4', cat: 'clip', dur: '6:20', he: 'אור חדש', en: 'Or Chadash' },
  { id: 'aFhQjhm1if8', cat: 'clip', dur: '5:45', he: 'פתח ליבי', en: 'Pesach Libi' },
  { id: 'yjBQLelJDKw', cat: 'medley', dur: '15:10', he: 'מחרוזת שמחת תורה', en: 'Simchat Torah Medley' },
  { id: 'sAeFaXlxv0E', cat: 'medley', dur: '7:15', he: 'מחרוזת שירי תשובה', en: 'Teshuvah Medley' },
  { id: 'n6tLDS_ioYk', cat: 'makhalolam', dur: '4:34', he: 'מקהלולם: שמע קולינו', en: 'Makhalolam: Shema Koleinu' },
  { id: 'eSJg_mli2y8', cat: 'makhalolam', dur: '1:06', he: 'מקהלולם — הסרטון הראשון', en: 'Makhalolam — the first film' },
  { id: 's_CNJzzsA8g', cat: 'clip', dur: '6:04', he: 'כי הם חיינו', en: 'Ki Hem Chayeinu' },
  { id: '_owLJAU6yx8', cat: 'clip', dur: '3:51', he: 'אם היו בני אדם', en: 'Im Hayu Bnei Adam' },
  { id: '_eX_k4H5WHo', cat: 'clip', dur: '4:47', he: 'אהבת תורה', en: 'Ahavat Torah' },
  { id: 'Jboco7s9T2I', cat: 'clip', dur: '2:04', he: 'שישו ושמחו', en: 'Sisu VeSimchu' },
  { id: 'WJEaMpIPNWM', cat: 'clip', dur: '3:48', he: 'בזכות התורה', en: 'Bizchut HaTorah' },
  { id: 'NnokjYF8JvI', cat: 'clip', dur: '5:29', he: 'בעבור אבותינו', en: 'Ba’avur Avoteinu' },
  { id: 'y4BIVTB0MY4', cat: 'live', dur: '6:46', he: 'התנערי · בהופעה חיה', en: 'Hitna’ari · live' },
  { id: 'FzzkmO2WIhg', cat: 'clip', dur: '6:52', he: 'ויהי זרעי', en: 'Vihi Zar’i' },
  { id: '1k5nTf6ppAY', cat: 'medley', dur: '1:32:15', he: 'מופע משותף · המופע המלא', en: 'Joint concert · full show' },
  { id: 'YQ9De5UZt84', cat: 'clip', dur: '5:03', he: 'נר לרגלי', en: 'Ner Leragli' },
  { id: 'tGtW5cxt5oY', cat: 'clip', dur: '3:38', he: 'ויהי נועם', en: 'Vihi Noam' },
  { id: 'oUmK0zXEw2E', cat: 'clip', dur: '4:25', he: 'שערי שמים', en: 'Sha’arei Shamayim' },
  { id: 'atwgGKj6Y9I', cat: 'clip', dur: '5:52', he: 'ירא שמים', en: 'Yerei Shamayim' },
  { id: 'ajZDXwC5jBI', cat: 'clip', dur: '5:34', he: 'לב טהור', en: 'Lev Tahor' },
  { id: 'zZWHpRHyAbs', cat: 'clip', dur: '4:15', he: 'אנעים זמירות', en: 'Anim Zemirot' },
  { id: '7-AmDfqfrok', cat: 'clip', dur: '4:42', he: 'המרחם', en: 'HaMerachem' },
  { id: 'PHbWcgVHTSQ', cat: 'live', dur: '42:51', he: 'ירושלים תתן קולה · המופע המלא', en: 'Yerushalayim Titen Kolah · full concert' },
  { id: 'XGaDjl3KRh0', cat: 'live', dur: '4:39', he: 'עוד ישבו · מהמופע', en: 'Od Yeshvu · live' },
  { id: 'Y_ErdPnw5Kc', cat: 'live', dur: '5:43', he: 'על נהרות בבל · מהמופע', en: 'Al Naharot Bavel · live' },
  { id: '9--ZpQoS3AQ', cat: 'live', dur: '3:18', he: 'יבנה המקדש · מהמופע', en: 'Yibaneh HaMikdash · live' },
  { id: '-YVq0aOq93w', cat: 'live', dur: '4:23', he: 'תשאלו אותי · מהמופע', en: 'Tish’alu Oti · live' },
  { id: '6Qws8NivelM', cat: 'live', dur: '4:36', he: 'אם אשכחך · מהמופע', en: 'Im Eshkachech · live' },
  { id: 'um36ZZ_t4mo', cat: 'live', dur: '7:01', he: 'הוא יבנה · מהמופע', en: 'Hu Yivneh · live' },
  { id: 'kwvhIhsS_xE', cat: 'live', dur: '3:20', he: 'אורו של עולם · מהמופע', en: 'Oro Shel Olam · live' },
  { id: '-HOL1_oerL4', cat: 'live', dur: '5:33', he: 'הרים סביב לה · מהמופע', en: 'Harim Saviv Lah · live' },
  { id: 'jtdnDpvR28Y', cat: 'clip', dur: '2:37', he: 'השמים', en: 'HaShamayim' },
  { id: 'SMaJPYSJYcw', cat: 'clip', dur: '5:35', he: 'התעוררי · סולני המקהלה', en: 'Hitoreri · the choir soloists' },
  { id: 'WaYXAWNG8NU', cat: 'medley', dur: '1:00:36', he: 'מופע קומזיץ · המופע המלא', en: 'Kumzitz concert · full show' },
  { id: 'Ut1gk8aJJNw', cat: 'clip', dur: '5:22', he: 'צאצאינו', en: 'Tze’etza’einu' },
  { id: 'Sc-5oBrQUMM', cat: 'clip', dur: '5:50', he: 'אל ינום שומריך', en: 'Al Yanum Shomrecha' },
  { id: 'wXBTCtf1J2k', cat: 'clip', dur: '3:41', he: 'הללו', en: 'Halelu' },
  { id: 'lqDnD8YW_Tg', cat: 'clip', dur: '4:24', he: 'מה גדלו', en: 'Mah Gadlu' },
  { id: '1Q4bhHmNr5E', cat: 'clip', dur: '4:58', he: 'צבא השמים', en: 'Tzva HaShamayim' },
  { id: 'YXJ0u05ttNE', cat: 'clip', dur: '3:37', he: 'פותח', en: 'Pote’ach' },
  { id: 'GHTjw3OqKjA', cat: 'live', dur: '0:24', he: 'יזכרם · סולו מהמופע', en: 'Yizkerem · a solo from the show' },
  { id: '8Rqvt2fKKgg', cat: 'live', dur: '0:54', he: 'הזמנה למופע', en: 'Invitation to the concert' },
  // קטעים קצרים (שורטס) — נפתחים בנגן אנכי
  { id: 'msGYIMeWm7A', cat: 'short', dur: '0:26', vertical: true, he: 'בך בטחנו · רגע מהבמה', en: 'Becha Batachnu · from the stage' },
  { id: 'f_hTQft3Iig', cat: 'short', dur: '0:45', vertical: true, he: 'כי לישועתך · מתוך המופע', en: 'Ki Lishuatcha · from the show' },
  { id: 'XvpJspILYYo', cat: 'short', dur: '1:07', vertical: true, he: 'דואט סולנים מהמופע', en: 'A soloists’ duet from the show' },
  { id: 'GQssCbEjlEk', cat: 'short', dur: '0:10', vertical: true, he: 'בחזרות לקראת המופע', en: 'Rehearsing for the show' },
  { id: 'c0K4HqAjGaI', cat: 'short', dur: '1:14', vertical: true, he: 'חזרה פתוחה בפארק', en: 'An open rehearsal in the park' },
  { id: 'ecYCW85qXEQ', cat: 'short', dur: '1:18', vertical: true, he: 'רגע לפני שעולים לבמה', en: 'Moments before going on stage' },
];

export const shorts = [
  { id: 'GQssCbEjlEk', he: 'בחזרות לקראת המופע', en: 'Rehearsing for the show' },
  { id: 'ecYCW85qXEQ', he: 'רגע לפני שעולים לבמה', en: 'Moments before going on stage' },
  { id: 'XvpJspILYYo', he: 'דואט סולנים מהמופע', en: 'A soloists’ duet from the show' },
  { id: 'msGYIMeWm7A', he: 'בך בטחנו · מהבמה', en: 'Becha Batachnu · from the stage' },
  { id: 'f_hTQft3Iig', he: 'כי לישועתך · מתוך המופע', en: 'Ki Lishuatcha · from the show' },
];

const he = {
  lang: 'he', dir: 'rtl', other: 'en', otherHref: 'en/', base: '',
  title: 'מקהלת פרחי שמיים · חוגי מקהלה ופיתוח קול לבנים',
  description: 'חוגי מקהלה ופיתוח קול מקצועי לבנים בגילאי 8–12 בירושלים ובבית שמש, ביחס אישי לכל ילד. מצאו חוג באזור שלכם והשאירו פרטים בדקה.',
  demoBar: 'הדגמה · מסלול 2: אתר והרשמה לחוגים · העיצוב להמחשה',
  demoAdmin: 'אזור הניהול לדוגמה',
  skip: 'דילוג לתוכן',
  brand: 'פרחי שמיים', brandSub: 'מקהלת הילדים',
  nav: { classes: 'החוגים', music: 'השירים', stage: 'על הבמה', makhalolam: 'מקהלולם', about: 'אודות' },
  langLabel: 'English', langShort: 'EN', langAria: 'Switch to English',
  motionOff: 'עצירת אנימציות', motionOn: 'הפעלת אנימציות',
  menu: 'תפריט', close: 'סגירה',
  headerCta: 'השאירו פרטים',

  hero: {
    eyebrow: 'חוגי מקהלה ופיתוח קול · לבנים בגילאי 8–12',
    h1a: 'הבן שלכם אוהב לשיר?',
    h1b: 'כאן הקול שלו עולה לבמה.',
    lead: 'פיתוח קול מקצועי, שירה בהרמוניה והקלטות באולפן — ביחס אישי לכל ילד, בניצוחו של ר׳ מרדכי גורדון.',
    cta: 'מצאו חוג באזור שלכם',
    listen: 'האזינו למקהלה',
    trust: ['חוגים בירושלים ובבית שמש', 'קבלה במבדק התאמה', 'פיתוח קול בשיטת משה בערק'],
    motto: 'מקהלה. מקצועיות. חוויה.',
    alts: ['מקהלת פרחי שמיים על הבמה, מול מסך גדול עם לוגו המקהלה', 'המקהלה והמנצח על במה גדולה באור זרקורים', 'ילדי המקהלה שרים יחד בהופעה'],
  },

  join: {
    kicker: 'הצטרפות למקהלה',
    title: 'איזה חוג קרוב אליכם?',
    lead: 'בחרו חוג, השאירו פרטים בדקה, וצוות המקהלה יחזור אליכם לתיאום מבדק התאמה קצר.',
    steps: ['בוחרים חוג', 'משאירים פרטים', 'מתאמים מבדק'],
    filterLabel: 'סינון לפי עיר', all: 'כל החוגים',
    cities: { jerusalem: 'ירושלים', 'beit-shemesh': 'בית שמש' },
    ages: 'גילאי 8–12', audition: 'קבלה במבדק התאמה',
    times: 'ימים ושעות נשלחים אליכם במייל',
    regLabel: 'רישום רשמי:', choose: 'לחוג הזה', chosen: 'החוג נבחר',
    // טעימה לפני פרטים (כלל 5): תשובה מיידית אם החוג מתאים, בלי להשאיר כלום
    fit: {
      q: 'בן כמה הבן?', note: 'בדיקה מהירה, בלי להשאיר פרטים', older: '13+', label: 'גיל הבן',
      ok: 'בגיל {n} הוא בדיוק בגיל החוגים. בחרו חוג קרוב, והגיל כבר ימולא בטופס.',
      young: 'החוגים מיועדים לגילאי 8–12. אפשר להשאיר פרטים כבר עכשיו, וצוות המקהלה יחזור אליכם.',
      old: 'החוגים מיועדים לגילאי 8–12. השאירו פרטים, וצוות המקהלה יבדוק איתכם מה מתאים.',
    },
    flyers: 'מודעת חוגי ירושלים:', flyerHe: 'עברית', flyerEn: 'English',
  },

  form: {
    title: 'השאירו פרטים — נחזור אליכם',
    branch: 'החוג', branchPlaceholder: 'בחרו חוג',
    parent: 'שם ההורה', phone: 'טלפון', email: 'מייל',
    child: 'שם הילד', age: 'גיל', cheder: 'חיידר / תלמוד תורה', grade: 'כיתה', gradePlaceholder: 'בחרו כיתה',
    grades: ['א׳', 'ב׳', 'ג׳', 'ד׳', 'ה׳', 'ו׳', 'ז׳', 'ח׳'],
    notes: 'משהו שחשוב שנדע? (רשות)',
    consent: 'אני מאשר/ת לצוות המקהלה לפנות אליי בנושא החוג. הפרטים לא יועברו לאף גורם אחר.',
    submit: 'שליחת הפרטים',
    privacy: 'הפרטים נשמרים אצל צוות המקהלה בלבד ומשמשים לתיאום המבדק.',
    demoNote: 'בהדגמה הפרטים לא נשלחים. הפנייה תופיע באזור הניהול לדוגמה.',
    nextTitle: 'מה קורה אחרי השליחה?',
    next: ['מייל אישור מגיע אליכם מיד.', 'צוות המקהלה חוזר אליכם לתיאום מבדק התאמה קצר.', 'אחרי המבדק מקבלים הנחיות לרישום הרשמי בחוג.'],
  },

  why: {
    kicker: 'למה פרחי שמיים',
    title: 'מקהלה שמלמדת באמת לשיר',
    items: [
      ['יחס אישי לכל ילד', 'כל ילד מקבל הקשבה, הכוונה ומקום משלו בתוך המקהלה — ויוצא עם ביטחון בכישרון שלו.'],
      ['פיתוח קול מקצועי', 'עבודה קולית שיטתית בשיטתו של משה בערק: נשימה, טכניקה וביטחון בשירה.'],
      ['יוצרים ומקליטים', 'כתיבה והלחנה, הקלטות מקצועיות באולפן, ובכל שנה קליפ או הופעה — לפי התוכנית של הקבוצה.'],
      ['מוזיקה שמחזקת', 'המקהלה מטפחת את הכישרון לצד הלימוד בחיידר, והשירים יוצאים לחזק את כולם בעבודת הבורא.'],
    ],
  },

  stats: [
    { value: 40, suffix: '+', label: 'שירים וקליפים' },
    { value: 4, suffix: '', label: 'חוגים בירושלים ובבית שמש' },
    { value: 125, suffix: ' אלף', label: 'צפיות בערוץ' },
    { text: '8–12', label: 'גילאי החוג' },
  ],

  program: {
    kicker: 'מה לומדים בחוג',
    title: 'מהצליל הראשון — ועד השיר הגמור',
    lead: 'שנה בחוג היא מסע. כל שלב בונה את הביטחון לשלב הבא.',
    steps: [
      ['פיתוח קול', 'נשימה נכונה, טכניקה קולית ושמירה על הקול.', 'FzzkmO2WIhg', 'ילדי המקהלה שרים בריכוז'],
      ['שירה בהרמוניה', 'מקשיבים זה לזה ובונים יחד צליל אחד של מקהלה.', 'PHbWcgVHTSQ', 'ילדי המקהלה שרים יחד'],
      ['כתיבה והלחנה', 'מכירים מושגי יסוד במוזיקה ומנסים ליצור בעצמם.', 'zZWHpRHyAbs', 'ילדי המקהלה בהכנות לקליפ'],
      ['הקלטה באולפן', 'הקלטות מקצועיות של שירי המקהלה, עם הכוונה קולית צמודה.', 'tGtW5cxt5oY', 'ילד מהמקהלה שר מול מיקרופון'],
      ['קליפ או במה', 'את פרי העבודה רואים בקליפ מקצועי או בהופעה — לפי התוכנית של אותה שנה.', 'ajZDXwC5jBI', 'המקהלה על במה גדולה'],
    ],
  },

  music: {
    kicker: 'השירים שלנו',
    title: 'האזינו למקהלה',
    lead: 'קליפים, הופעות ומחרוזות מהערוץ הרשמי. שיר חדש שעולה לפלייליסט מופיע כאן אוטומטית.',
    featuredLabel: 'השיר החדש',
    featuredText: 'שירת ילדי המקהלה על מילות תפילת מוסף של ראש השנה, בלחן מרדכי וישראל מאיר גורדון.',
    filters: { all: 'הכול', clip: 'קליפים', live: 'מהבמה', medley: 'מחרוזות ומופעים משותפים', makhalolam: 'מקהלולם', short: 'קטעים קצרים' },
    searchLabel: 'חיפוש שיר', searchPlaceholder: 'חיפוש שיר…',
    showAll: 'הצגת כל השירים', showLess: 'הצגת פחות',
    empty: 'לא נמצאו שירים. נסו מילה אחרת.',
    play: 'ניגון', newBadge: 'חדש',
    count: '{n} שירים',
    channel: 'כל הסרטונים בערוץ',
  },

  player: {
    label: 'נגן המקהלה', close: 'סגירת הנגן', prev: 'השיר הקודם', next: 'השיר הבא',
    youtube: 'לצפייה ביוטיוב', note: 'אם הנגן לא נטען אצלכם, אפשר לצפות ישירות ביוטיוב.',
  },

  stage: {
    kicker: 'על הבמה',
    title: 'רגעים מהבמה, שבונים ביטחון ומרגשים את הקהל',
    upcomingTitle: 'ההופעה הבאה',
    upcomingText: 'ההופעה הבאה תפורסם כאן, עם המודעה, המקום והשעה.',
    pastTitle: 'מהופעות קודמות',
    shows: [
      { img: '9--ZpQoS3AQ', video: 'PHbWcgVHTSQ', title: 'ירושלים תתן קולה', sub: 'המופע המלא · 42 דקות' },
      { img: 'f_hTQft3Iig', video: 'f_hTQft3Iig', title: 'שומע תפילה', sub: 'רגעים מהמופע' },
      { img: '1k5nTf6ppAY', video: '1k5nTf6ppAY', title: 'מופע משותף', sub: 'המופע המלא · שעה וחצי' },
    ],
    bookingTitle: 'מקהלה לאירוע או למופע קהילתי?',
    bookingText: 'ספרו לנו על האירוע במייל, ונחזור אליכם עם הצעה.',
    bookingCta: 'בקשה להזמנת הופעה',
    bookingSubject: 'בקשה להזמנת הופעה – מקהלת פרחי שמיים',
  },

  makhalolam: {
    kicker: 'לקהילות, למתנ״סים ולעיריות',
    title: 'מקהלולם',
    subtitle: 'מקהלה מלמדת קהל',
    text: 'מופע שבו הקהל הופך לחלק מהמקהלה. המקהלה והמנצח מלמדים את הקהל את התפקידים, ובסוף כולם שרים יחד. חוויה קהילתית, חינוכית ומוזיקלית — שמתאימה במיוחד למתנ״סים ולאירועי קהילה.',
    points: ['הקהל לא רק צופה — הוא שר', 'מתאים לאולמות ולמתנ״סים', 'חוויה משותפת לכל המשפחה'],
    choir: 'המקהלה שרה', audience: 'הקהל עונה', together: 'כולם יחד',
    videoMain: 'מקהלולם · שמע קולינו', videoPromo: 'מקהלולם · הסרטון הראשון',
    cta: 'הזמנת מקהלולם לקהילה שלכם',
    subject: 'מקהלולם לקהילה שלנו – פנייה מהאתר',
    logoAlt: 'לוגו מקהלולם — מקהלה מלמדת קהל',
  },

  behind: {
    kicker: 'מאחורי הקלעים',
    title: 'מה שלא רואים בקליפ',
    lead: 'חזרות, הכנות ורגעים מהבמה — הצצה לעבודה שמאחורי כל שיר.',
    exclusiveTag: 'בלעדי לאתר',
    exclusiveTitle: 'תיעוד מהחזרות ומהאולפן',
    exclusiveText: 'הסברים קוליים, טייקים מהאולפן וטעימות לפני פרסום — יעלו כאן לפני כל מקום אחר.',
    stories: [
      { img: '-4sE-rfQI1k', title: 'אתה בחרתנו · מאחורי הצילומים', text: 'הקליפ צולם בבית משפחה, סביב שולחן החג. הלחן נכתב בידי מרדכי וישראל מאיר גורדון, ור׳ מרדכי גם ניצח וכתב את העיבוד הקולי.' },
      { img: 'aFhQjhm1if8', title: 'פתח ליבי · מהכותל לבית המדרש', text: 'ילדי רמת אשכול עבדו על השיר והקליפ במשך השנה. הצילומים שילבו תפילה בכותל ולימוד בחברותות בעיר העתיקה.' },
    ],
    watch: 'צפייה',
  },

  about: {
    kicker: 'בואו להכירנו מקרוב',
    title: 'מקהלת פרחי שמיים',
    paras: [
      'פרחי שמיים היא מקהלת ילדים וחוג מוזיקלי שפועל בכמה ערים בארץ. המטרה שלנו: לעודד ילדים מוזיקליים, לתת להם הרגשה טובה ולנסוך בהם ביטחון בכישרון שהקב״ה חנן אותם — כך שיתחזקו גם בלימודם בחיידר, ולא להפך.',
      'המקהלה מוציאה שירים וקליפים ומופיעה מעת לעת, והשירים יוצאים כדי שכולם יוכלו ליהנות ולהתחזק מהם בעבודת הבורא.',
    ],
    conductor: 'ר׳ מרדכי גורדון', conductorRole: 'מנצח המקהלה, מלחין ומעבד קולי',
    logoAlt: 'לוגו מקהלת הילדים פרחי שמיים',
    cards: [
      ['הצוות שלנו', 'המנצח, המורים והמלווים — עם תמונות ותפקידים.'],
      ['המטרות שלנו', 'חינוך, ביטחון עצמי והתקדמות ברוחניות דרך המוזיקה.'],
      ['לעיריות ולמתנ״סים', 'הופעות, מקהלולם ושיתופי פעולה לקהילה.'],
    ],
    soon: 'יושלם מחומרי המקהלה',
    testimonialsTitle: 'המלצות הורים',
    testimonialsText: 'כאן יוצגו המלצות של הורים, גם בסרטון, באישור המשפחות.',
  },

  final: {
    title: 'הקול שלו מחכה לבמה.',
    text: 'השאירו פרטים בדקה, ונחזור אליכם לתיאום מבדק התאמה.',
    cta: 'מצאו חוג באזור שלכם',
  },

  footer: {
    contact: 'יצירת קשר במייל', youtube: 'הערוץ ביוטיוב',
    access: 'הצהרת נגישות', privacy: 'מדיניות פרטיות',
    rights: '© מקהלת פרחי שמיים', demo: 'הדגמה לאתר · התוכן והעיצוב להמחשה',
  },

  js: {
    required: 'שדה חובה', email: 'כתובת המייל לא תקינה', phone: 'מספר טלפון לא תקין',
    age: 'גיל בין 5 ל־16', branch: 'בחרו חוג', consent: 'יש לאשר את הפנייה',
    summary: 'יש לתקן {n} שדות לפני השליחה',
    successTitle: 'תודה, {parent}! הפנייה התקבלה.',
    successText: 'צוות המקהלה יחזור אליכם בימים הקרובים לגבי {child} וחוג {branch}.',
    emailLabel: 'כך נראה מייל האישור שתקבלו',
    emailFrom: 'מקהלת פרחי שמיים',
    emailSubject: 'קיבלנו את הפנייה שלכם · מקהלת פרחי שמיים',
    emailLines: ['שלום {parent},', 'תודה על הפנייה לגבי {child} לחוג {branch}.', 'צוות המקהלה יחזור אליכם בימים הקרובים לתיאום מבדק התאמה קצר.', 'אחרי המבדק: {reg}.', 'מחכים לשמוע את הקול שלו!', 'צוות מקהלת פרחי שמיים'],
    toAdmin: 'צפייה בפנייה באזור הניהול', again: 'פנייה נוספת',
    branchFormat: '{name} · {city}',
  },
};

const en = {
  lang: 'en', dir: 'ltr', other: 'he', otherHref: '../', base: '../',
  title: 'Pirchei Shomayim Boys’ Choir · Choir classes & voice training for boys',
  description: 'Choir classes and professional voice training for boys aged 8–12 in Jerusalem and Beit Shemesh, with personal attention for every child. Find a class near you and leave your details in a minute.',
  demoBar: 'Demo · Option 2: website with class sign-up · design for illustration',
  demoAdmin: 'Sample admin area',
  skip: 'Skip to content',
  brand: 'Pirchei Shomayim', brandSub: 'Boys’ Choir',
  nav: { classes: 'Classes', music: 'Music', stage: 'On stage', makhalolam: 'Makhalolam', about: 'About' },
  langLabel: 'עברית', langShort: 'עב', langAria: 'מעבר לעברית',
  motionOff: 'Pause animations', motionOn: 'Play animations',
  menu: 'Menu', close: 'Close',
  headerCta: 'Leave your details',

  hero: {
    eyebrow: 'Choir classes & voice training · boys aged 8–12',
    h1a: 'Does your son love to sing?',
    h1b: 'Here, his voice finds its stage.',
    lead: 'Professional voice training, singing in harmony and studio recording — with personal attention for every boy, under the direction of R’ Mordechai Gordon.',
    cta: 'Find a class near you',
    listen: 'Listen to the choir',
    trust: ['Classes in Jerusalem & Beit Shemesh', 'Admission by a short audition', 'Voice training in the Moshe Burk method'],
    motto: 'Choir. Professionalism. Experience.',
    alts: ['Pirchei Shomayim on stage in front of a large screen with the choir logo', 'The choir and conductor on a large stage under spotlights', 'Choir boys singing together in concert'],
  },

  join: {
    kicker: 'Join the choir',
    title: 'Which class is closest to you?',
    lead: 'Choose a class, leave your details in a minute, and the choir team will get back to you to arrange a short audition.',
    steps: ['Choose a class', 'Leave your details', 'Arrange an audition'],
    filterLabel: 'Filter by city', all: 'All classes',
    cities: { jerusalem: 'Jerusalem', 'beit-shemesh': 'Beit Shemesh' },
    ages: 'Ages 8–12', audition: 'Admission by audition',
    times: 'Days and times are sent to you by email',
    regLabel: 'Official registration:', choose: 'Choose this class', chosen: 'Class selected',
    fit: {
      q: 'How old is your son?', note: 'A quick check, no details needed', older: '13+', label: 'Your son’s age',
      ok: 'At {n} he is right in the class age range. Pick a nearby class and his age is already filled in on the form.',
      young: 'Classes are for ages 8–12. You can leave your details now and the choir team will get back to you.',
      old: 'Classes are for ages 8–12. Leave your details and the choir team will see with you what fits.',
    },
    flyers: 'Jerusalem class flyer:', flyerHe: 'עברית', flyerEn: 'English',
  },

  form: {
    title: 'Leave your details — we’ll get back to you',
    branch: 'Class', branchPlaceholder: 'Choose a class',
    parent: 'Parent’s name', phone: 'Phone', email: 'Email',
    child: 'Child’s name', age: 'Age', cheder: 'Cheder / Talmud Torah', grade: 'Grade', gradePlaceholder: 'Choose a grade',
    grades: ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th'],
    notes: 'Anything we should know? (optional)',
    consent: 'I agree that the choir team may contact me about the class. My details will not be shared with anyone else.',
    submit: 'Send my details',
    privacy: 'Your details are kept by the choir team only and used to arrange the audition.',
    demoNote: 'In this demo nothing is sent. Your inquiry will appear in the sample admin area.',
    nextTitle: 'What happens next?',
    next: ['A confirmation email reaches you right away.', 'The choir team contacts you to arrange a short audition.', 'After the audition you receive instructions for official registration.'],
  },

  why: {
    kicker: 'Why Pirchei Shomayim',
    title: 'A choir that truly teaches boys to sing',
    items: [
      ['Personal attention', 'Every boy is heard, guided and given his own place in the choir — and grows confident in his talent.'],
      ['Professional voice training', 'Step-by-step vocal training in the Moshe Burk method: breathing, technique and singing with confidence.'],
      ['Create and record', 'Songwriting and composing, professional studio recordings — and each year a music video or a performance, depending on the group’s program.'],
      ['Music with a purpose', 'The choir nurtures each boy’s talent alongside his learning in cheder, and its songs are made to inspire avodas Hashem.'],
    ],
  },

  stats: [
    { value: 40, suffix: '+', label: 'songs and music videos' },
    { value: 4, suffix: '', label: 'classes in Jerusalem & Beit Shemesh' },
    { value: 125, suffix: 'K+', label: 'views on our channel' },
    { text: '8–12', label: 'ages in the class' },
  ],

  program: {
    kicker: 'What the boys learn',
    title: 'From the first note — to the finished song',
    lead: 'A year in the choir is a journey, and every step builds the confidence for the next.',
    steps: [
      ['Voice training', 'Correct breathing, vocal technique and caring for the voice.', 'FzzkmO2WIhg', 'Choir boys singing with focus'],
      ['Singing in harmony', 'Listening to each other and building one choir sound together.', 'PHbWcgVHTSQ', 'Choir boys singing together'],
      ['Writing & composing', 'Learning the basics of music and trying their own compositions.', 'zZWHpRHyAbs', 'Choir boys getting ready for a music-video shoot'],
      ['In the studio', 'Professional recordings of the choir’s songs, with close vocal coaching.', 'tGtW5cxt5oY', 'A choir boy singing at the microphone'],
      ['Music video or stage', 'The year’s work comes to life in a professional music video or on stage — depending on that year’s program.', 'ajZDXwC5jBI', 'The choir on a large stage'],
    ],
  },

  music: {
    kicker: 'Our music',
    title: 'Listen to the choir',
    lead: 'Music videos, concerts and medleys from the official channel. A new song added to the playlist appears here automatically.',
    featuredLabel: 'New release',
    featuredText: 'The boys sing words from the Rosh Hashanah Musaf prayer, to a melody by Mordechai and Yisrael Meir Gordon.',
    filters: { all: 'All', clip: 'Music videos', live: 'Live', medley: 'Medleys & joint concerts', makhalolam: 'Makhalolam', short: 'Short clips' },
    searchLabel: 'Search songs', searchPlaceholder: 'Search songs…',
    showAll: 'Show all songs', showLess: 'Show fewer',
    empty: 'No songs found. Try another word.',
    play: 'Play', newBadge: 'New',
    count: '{n} songs',
    channel: 'All videos on the channel',
  },

  player: {
    label: 'Choir player', close: 'Close player', prev: 'Previous song', next: 'Next song',
    youtube: 'Watch on YouTube', note: 'If the player doesn’t load for you, you can watch directly on YouTube.',
  },

  stage: {
    kicker: 'On stage',
    title: 'Moments on stage that build confidence — and move the audience',
    upcomingTitle: 'Next concert',
    upcomingText: 'The next concert will be announced here, with the flyer, venue and time.',
    pastTitle: 'From past concerts',
    shows: [
      { img: '9--ZpQoS3AQ', video: 'PHbWcgVHTSQ', title: 'Yerushalayim Titen Kolah', sub: 'Full concert · 42 minutes' },
      { img: 'f_hTQft3Iig', video: 'f_hTQft3Iig', title: 'Shomea Tefillah', sub: 'Moments from the show' },
      { img: '1k5nTf6ppAY', video: '1k5nTf6ppAY', title: 'Joint concert', sub: 'Full show · 1.5 hours' },
    ],
    bookingTitle: 'The choir at your event or community concert?',
    bookingText: 'Tell us about your event by email and we’ll get back to you with an offer.',
    bookingCta: 'Request a performance',
    bookingSubject: 'Performance request – Pirchei Shomayim Choir',
  },

  makhalolam: {
    kicker: 'For communities, community centers & municipalities',
    title: 'Makhalolam',
    subtitle: 'The choir teaches the audience',
    text: 'A concert where the audience becomes part of the choir. The choir and conductor teach the audience their parts, and in the end everyone sings together. A communal, educational and musical experience — ideal for community centers and community events.',
    points: ['The audience doesn’t just watch — it sings', 'Suited to halls and community centers', 'A shared experience for the whole family'],
    choir: 'The choir sings', audience: 'The audience answers', together: 'Everyone together',
    videoMain: 'Makhalolam · Shema Koleinu', videoPromo: 'Makhalolam · the first film',
    cta: 'Bring Makhalolam to your community',
    subject: 'Makhalolam for our community – website inquiry',
    logoAlt: 'Makhalolam logo — the choir teaches the audience',
  },

  behind: {
    kicker: 'Behind the scenes',
    title: 'What you don’t see in the music video',
    lead: 'Rehearsals, preparations and moments from the stage — a look at the work behind every song.',
    exclusiveTag: 'Only on this site',
    exclusiveTitle: 'From rehearsals and the studio',
    exclusiveText: 'Vocal explanations, studio takes and previews before release — published here first.',
    stories: [
      { img: '-4sE-rfQI1k', title: 'Ata Bechartanu · behind the shoot', text: 'The video was filmed in a family home, around the holiday table. The melody was written by Mordechai and Yisrael Meir Gordon, and R. Mordechai also conducted and wrote the vocal arrangement.' },
      { img: 'aFhQjhm1if8', title: 'Pesach Libi · from the Kotel to the beis midrash', text: 'The boys of Ramat Eshkol worked on the song and video throughout the year. The shoot combined tefillah at the Kotel with chavrusa learning in the Old City.' },
    ],
    watch: 'Watch',
  },

  about: {
    kicker: 'Get to know us',
    title: 'Pirchei Shomayim Boys’ Choir',
    paras: [
      'Pirchei Shomayim is a boys’ choir and music class active in several cities in Israel. Our goal: to encourage musical children, give them a good feeling and instill confidence in the talent Hashem has blessed them with — so that they grow stronger in their learning in cheder, not the other way around.',
      'The choir releases songs and music videos and performs from time to time, so that everyone can enjoy them and be strengthened in avodas Hashem.',
    ],
    conductor: 'R’ Mordechai Gordon', conductorRole: 'Conductor, composer and vocal arranger',
    logoAlt: 'Pirchei Shomayim Boys’ Choir logo',
    cards: [
      ['Our team', 'The conductor, teachers and staff — with photos and roles.'],
      ['Our goals', 'Education, self-confidence and spiritual growth through music.'],
      ['For municipalities & centers', 'Concerts, Makhalolam and community partnerships.'],
    ],
    soon: 'To be completed with the choir’s materials',
    testimonialsTitle: 'Parent testimonials',
    testimonialsText: 'Parent testimonials, including video, will appear here with the families’ permission.',
  },

  final: {
    title: 'His voice deserves a stage.',
    text: 'Leave your details in a minute and we’ll get back to you to arrange an audition.',
    cta: 'Find a class near you',
  },

  footer: {
    contact: 'Contact us by email', youtube: 'Our YouTube channel',
    access: 'Accessibility statement', privacy: 'Privacy policy',
    rights: '© Pirchei Shomayim Boys’ Choir', demo: 'Website demo · content and design for illustration',
  },

  js: {
    required: 'Required', email: 'Please enter a valid email', phone: 'Please enter a valid phone number',
    age: 'Age between 5 and 16', branch: 'Please choose a class', consent: 'Please confirm to continue',
    summary: 'Please fix {n} fields before sending',
    successTitle: 'Thank you, {parent}! We received your inquiry.',
    successText: 'The choir team will get back to you soon about {child} and the {branch} class.',
    emailLabel: 'This is the confirmation email you will receive',
    emailFrom: 'Pirchei Shomayim Choir',
    emailSubject: 'We received your inquiry · Pirchei Shomayim Choir',
    emailLines: ['Hello {parent},', 'Thank you for your inquiry about {child} for the {branch} class.', 'The choir team will contact you soon to arrange a short audition.', 'After the audition: {reg}.', 'We look forward to hearing his voice!', 'The Pirchei Shomayim Choir team'],
    toAdmin: 'View the inquiry in the admin area', again: 'Send another inquiry',
    branchFormat: '{name} · {city}',
  },
};

export const dict = { he, en };
