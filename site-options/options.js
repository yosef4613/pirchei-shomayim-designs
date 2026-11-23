'use strict';

const statuses = ['חדשה', 'נוצר קשר', 'נקבע מבדק'];
const applications = [
  {parent: 'הורה לדוגמה א׳', child: 'ילד לדוגמה א׳', age: '9', branch: 'ירושלים · רמת אשכול', email: 'family-a@example.com', status: 'חדשה'},
  {parent: 'הורה לדוגמה ב׳', child: 'ילד לדוגמה ב׳', age: '11', branch: 'בית שמש · רמה א׳', email: 'family-b@example.com', status: 'נקבע מבדק'},
];
const subscribers = [
  {email: 'listener-a@example.com', topics: ['שירים חדשים ביוטיוב'], status: 'אושר'},
  {email: 'listener-b@example.com', topics: ['הופעות ופתיחת הרשמה'], status: 'ממתין לאישור'},
];

const get = (id) => document.getElementById(id);
const management = get('management-dialog');
const applicationForm = get('application-form');
const clubForm = get('club-form');
const english = document.documentElement.lang === 'en';

function cell(content) {
  const td = document.createElement('td');
  if (typeof content === 'string') td.textContent = content;
  else td.append(content);
  return td;
}

function filteredApplications() {
  const filter = get('lead-filter').value;
  return applications.filter((application) => !filter || application.status === filter);
}

function showApplications() {
  const filtered = filteredApplications();
  const rows = filtered.map((application) => {
    const row = document.createElement('tr');
    const name = cell(application.parent);
    const details = document.createElement('small');
    details.textContent = application.child + ' · גיל ' + application.age;
    name.append(details);

    const status = document.createElement('select');
    status.setAttribute('aria-label', 'סטטוס של ' + application.parent);
    for (const option of statuses) status.add(new Option(option, option));
    status.value = application.status;
    status.addEventListener('change', () => {
      application.status = status.value;
      if (get('lead-filter').value) {
        showApplications();
        get('lead-filter').focus();
      }
    });

    const email = cell(application.email);
    email.dir = 'ltr';
    row.append(name, cell(application.branch), email, cell(status));
    return row;
  });
  get('leads').replaceChildren(...rows);
  get('lead-count').textContent = filtered.length + ' מתוך ' + applications.length + ' פניות בדוגמה';
  get('export').disabled = filtered.length === 0;
}

function showSubscribers() {
  if (!get('subscribers')) return;
  const rows = subscribers.map((subscriber) => {
    const row = document.createElement('tr');
    const email = cell(subscriber.email);
    email.dir = 'ltr';
    row.append(email, cell(subscriber.topics.join(' · ') || 'ללא עדכונים'), cell(subscriber.status));
    return row;
  });
  get('subscribers').replaceChildren(...rows);
}

function displayPanel(name) {
  management.querySelectorAll('[data-panel]').forEach((button) => {
    button.setAttribute('aria-pressed', String(button.dataset.panel === name));
  });
  management.querySelectorAll('[data-managed-panel]').forEach((panel) => {
    panel.hidden = panel.dataset.managedPanel !== name;
  });
  if (name === 'applications') showApplications();
  if (name === 'subscribers') showSubscribers();
}

function csvValue(value) {
  const text = String(value);
  const sanitized = /^[=+@\-\t\r\n]/.test(text.trimStart()) ? "'" + text : text;
  return '"' + sanitized.replaceAll('"', '""') + '"';
}

function exportExample() {
  const rows = [['שם ההורה', 'שם הילד', 'גיל', 'חוג', 'מייל לחזרה', 'סטטוס']];
  for (const {parent, child, age, branch, email, status} of filteredApplications()) {
    rows.push([parent, child, age, branch, email, status]);
  }
  const csv = rows.map((row) => row.map(csvValue).join(',')).join('\r\n');
  const url = URL.createObjectURL(new Blob(['\uFEFF', csv], {type: 'text/csv;charset=utf-8'}));
  const link = document.createElement('a');
  link.href = url;
  link.download = 'pirchei-shomayim-demo-applications.csv';
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

for (const dialog of document.querySelectorAll('dialog')) {
  dialog.querySelector('[data-close]').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
}

if (management) {
  for (const button of document.querySelectorAll('[data-manage]')) {
    button.addEventListener('click', () => {
      displayPanel('applications');
      management.showModal();
    });
  }
  for (const button of management.querySelectorAll('[data-panel]')) {
    button.addEventListener('click', () => displayPanel(button.dataset.panel));
  }
  get('lead-filter').addEventListener('change', showApplications);
  get('export').addEventListener('click', exportExample);

  const requestedPanel = new URLSearchParams(location.search).get('view');
  if (requestedPanel === 'content' || requestedPanel === 'campaign') {
    const entry = [...management.querySelectorAll('[data-panel]')]
      .find((button) => button.dataset.panel === requestedPanel);
    if (entry) {
      displayPanel(requestedPanel);
      management.showModal();
    }
  }
}

const previewApplicantAccount = clubForm ? setupClub() : null;

if (applicationForm) {
  const fields = applicationForm.elements;
  const result = get('application-result');
  const inbox = get('view-inbox');
  applicationForm.querySelector('[type="submit"]').disabled = false;
  for (const card of document.querySelectorAll('[data-branch]')) {
    card.addEventListener('click', () => {
      if (card.dataset.branch) {
        fields.branch.value = card.dataset.branch;
        return;
      }
      const [city, area] = card.children;
      fields.branch.value = city.textContent + ' · ' + area.textContent;
    });
  }
  document.querySelector('[data-fill-application]').addEventListener('click', () => {
    fields.parent.value = english ? 'Sample Parent' : 'הורה לדוגמה ג׳';
    fields.email.value = 'parent@example.com';
    fields.child.value = english ? 'Sample Child' : 'ילד דוגמה';
    fields.age.value = '10';
    if (!fields.branch.value) fields.branch.value = english ? 'Jerusalem · Ramat Eshkol' : 'ירושלים · רמת אשכול';
  });
  applicationForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const {consent, ...info} = Object.fromEntries(new FormData(applicationForm));
    for (const key of Object.keys(info)) info[key] = info[key].trim();
    if (!info.parent || !info.child) {
      result.textContent = english
        ? 'Please enter sample names for the parent and child.'
        : 'יש למלא שם הורה ושם ילד בדויים.';
      return;
    }
    applications.unshift({...info, status: 'חדשה'});
    applicationForm.reset();
    if (previewApplicantAccount) {
      previewApplicantAccount(info.email, Boolean(consent));
    } else {
      result.textContent = english ? 'Demo inquiry complete.' : 'הפנייה נוספה לרשימה בהדגמה.';
    }
    if (inbox) inbox.hidden = false;
  });
}

for (const link of document.querySelectorAll('[data-language-switch]')) {
  link.addEventListener('click', () => { link.hash = location.hash; });
}

function setupClub() {
  const messages = english ? {
    applicationPending: 'Demo inquiry received. Verify the email address to activate your account.',
    signupPending: 'Verify your email address to finish signing up in the demo.',
    accountActive: 'Your demo account is active. You can choose email updates in your account.',
    mailingActive: 'Your demo account is active and your mailing list subscription is confirmed.',
    selectTopics: 'Choose at least one type of update to subscribe.',
    changeTopics: 'Choose at least one type of update or select Unsubscribe.',
    preferencesSaved: 'Your preferences have been saved in the demo.',
    unsubscribed: 'You have been unsubscribed from the demo mailing list.',
  } : {
    applicationPending: 'הפנייה לחוג נוספה בהדגמה. כעת יש לאמת את המייל להפעלת החשבון.',
    signupPending: 'ההרשמה לדוגמה ממתינה לאימות הכתובת.',
    accountActive: 'החשבון הופעל בהדגמה. אפשר לבחור לקבל עדכונים מתוך החשבון.',
    mailingActive: 'החשבון הופעל וההצטרפות לרשימת התפוצה אושרה בהדגמה.',
    selectTopics: 'כדי להצטרף בחרו לפחות סוג אחד של עדכונים.',
    changeTopics: 'בחרו סוג עדכון אחד לפחות, או לחצו על הסרה.',
    preferencesSaved: 'ההעדפות נשמרו בהדגמה.',
    unsubscribed: 'הכתובת הוסרה מרשימת הדיוור בהדגמה.',
  };
  const clubResult = get('club-result');
  const preferences = get('preferences');
  const preferenceResult = get('preference-result');
  const unsubscribe = get('unsubscribe');
  const topicInputs = [...preferences.elements.topics];
  let activeEmail;

  function saveSubscription(email, topics, status) {
    const existing = subscribers.find((entry) => entry.email === email);
    if (existing) {
      Object.assign(existing, {topics, status});
    } else {
      subscribers.unshift({email, topics, status});
    }
  }

  function showPreferences() {
    const subscription = subscribers.find((entry) => entry.email === activeEmail);
    for (const input of topicInputs) {
      input.checked = subscription?.topics.includes(input.value) ?? false;
    }
    unsubscribe.disabled = subscription?.status !== 'אושר';
  }

  function setupVerification(confirmation, view, feedback) {
    let pending;
    let verifiedEmail;
    confirmation.addEventListener('click', () => {
      if (!pending) return;
      verifiedEmail = pending.email;
      if (pending.topics.length) {
        saveSubscription(verifiedEmail, pending.topics, 'אושר');
        feedback.textContent = messages.mailingActive;
      } else {
        feedback.textContent = messages.accountActive;
      }
      pending = undefined;
      confirmation.hidden = true;
      view.hidden = false;
      view.focus();
    });
    view.addEventListener('click', () => {
      activeEmail = verifiedEmail;
      get('member-email').textContent = activeEmail;
      showPreferences();
      preferenceResult.textContent = '';
      get('member-dialog').showModal();
    });
    return (email, topics, message) => {
      pending = {email: email.trim().toLowerCase(), topics};
      feedback.textContent = message;
      confirmation.hidden = false;
      view.hidden = true;
    };
  }

  const previewClub = setupVerification(get('confirm-club'), get('member-view'), clubResult);
  const previewApplication = setupVerification(get('confirm-application'), get('view-application-account'), get('application-result'));
  clubForm.querySelector('[type="submit"]').disabled = false;

  document.querySelector('[data-fill-club]').addEventListener('click', () => {
    clubForm.elements.email.value = 'new-listener@example.com';
  });
  clubForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(clubForm);
    const topics = formData.getAll('topics');
    if (!topics.length) {
      clubResult.textContent = messages.selectTopics;
      return;
    }
    previewClub(formData.get('email'), topics, messages.signupPending);
    clubForm.reset();
  });
  preferences.addEventListener('submit', (event) => {
    event.preventDefault();
    const topics = new FormData(preferences).getAll('topics');
    if (!topics.length) {
      preferenceResult.textContent = messages.changeTopics;
      return;
    }
    saveSubscription(activeEmail, topics, 'אושר');
    showPreferences();
    preferenceResult.textContent = messages.preferencesSaved;
  });
  unsubscribe.addEventListener('click', () => {
    saveSubscription(activeEmail, [], 'הוסר');
    showPreferences();
    preferenceResult.textContent = messages.unsubscribed;
  });

  return (email, consent) => {
    const topics = consent ? topicInputs.map(({value}) => value) : [];
    previewApplication(email, topics, messages.applicationPending);
  };
}

const photos = ['covers/s_CNJzzsA8g.jpg', 'channel-banner.jpg', 'covers/_eX_k4H5WHo.jpg'];
const photoButtons = [...document.querySelectorAll('[data-photo]')];
const heroImage = get('hero-image');
const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
let photoRequest = 0;
for (const button of photoButtons) {
  button.addEventListener('click', () => {
    const wanted = ++photoRequest;
    const next = new Image();
    next.src = document.body.dataset.assets + '/' + photos[Number(button.dataset.photo)];
    next.decode().then(() => {
      if (wanted !== photoRequest) return;
      if (!reduceMotion.matches) heroImage.classList.add('switching');
      setTimeout(() => {
        if (wanted !== photoRequest) return;
        heroImage.src = next.src;
        heroImage.classList.remove('switching');
        for (const control of photoButtons) control.setAttribute('aria-pressed', String(control === button));
      }, reduceMotion.matches ? 0 : 150);
    }).catch(() => {
      if (wanted === photoRequest) heroImage.classList.remove('switching');
    });
  });
}
