'use strict';

(() => {
  const form = document.getElementById('editor-form');
  const type = document.getElementById('editor-type');
  const campaignType = document.getElementById('campaign-type');
  const documentInput = document.getElementById('editor-file');
  const removeFile = document.getElementById('editor-remove-file');
  const fileName = document.getElementById('editor-filename');
  const feedback = document.getElementById('editor-status');
  const sitePreview = document.getElementById('content-preview');
  const emailPreview = document.getElementById('campaign-preview');
  const fields = {
    title: document.getElementById('editor-title'),
    description: document.getElementById('editor-description'),
    timing: document.getElementById('editor-timing'),
    details: document.getElementById('editor-details'),
    link: document.getElementById('editor-link'),
  };

  const records = {
    story: {
      label: 'מאחורי הקלעים',
      timingLabel: 'מועד התיעוד',
      detailsLabel: 'קרדיט או הקשר לתיעוד',
      linkLabel: 'קישור לתיעוד',
      action: 'לצפייה בתיעוד',
      title: 'מחזרה ראשונה לבמה',
      description: 'בעמוד כזה אפשר להסביר איך הילדים בונים את ההרמוניה ולשלב תיעוד מהחזרה.',
      timing: '',
      details: 'דוגמה לתיעוד ולהסבר מטעם המקהלה',
      link: '',
    },
    song: {
      label: 'שיר חדש',
      timingLabel: 'תאריך פרסום',
      detailsLabel: 'קרדיטים ומילים',
      linkLabel: 'קישור לקליפ ביוטיוב',
      action: 'לצפייה בשיר',
      title: 'אתה בחרתנו',
      description: 'מקהלת פרחי שמיים ביתר עילית שרה את מילות תפילת מוסף של ראש השנה.',
      timing: '5 בספטמבר 2026',
      details: 'לחן מרדכי וישראל מאיר גורדון',
      link: 'https://www.youtube.com/watch?v=-4sE-rfQI1k',
      cover: document.body.dataset.assets + '/covers/-4sE-rfQI1k.jpg',
    },
    class: {
      label: 'חוג חדש',
      timingLabel: 'תחילת החוג, ימים ושעות',
      detailsLabel: 'מרכז, גילי הקבוצה ופרטי קשר',
      linkLabel: 'קישור להרשמה לחוג',
      action: 'לפרטי ההרשמה לחוג',
      title: 'חוג מקהלה בירושלים',
      description: 'דוגמה להודעה על פתיחת חוג פיתוח קול ושירה. ההצטרפות בתיאום ובכפוף למבדק התאמה.',
      timing: 'יום ושעה יופיעו לפי מודעת החוג',
      details: 'רמת אשכול, קבוצת גיל לפי פרטי החוג',
      link: '#application',
    },
    show: {
      label: 'הופעה',
      timingLabel: 'תאריך ושעת ההופעה',
      detailsLabel: 'מקום ומשתתפים',
      linkLabel: 'קישור להרשמה להופעה',
      action: 'להרשמה להופעה',
      title: 'מופע פרחי שמיים',
      description: 'דוגמה לפרסום הופעה. כאן מופיעים תיאור הערב, פרטי הגעה והנחיות להרשמה.',
      timing: 'התאריך והשעה יפורסמו עם פתיחת ההרשמה',
      details: 'שם האולם, העיר והאמנים המשתתפים',
      link: '',
    },
  };

  function addText(parent, tag, value, className) {
    const element = document.createElement(tag);
    element.textContent = value;
    if (className) element.className = className;
    parent.append(element);
  }

  function addLink(parent, url, label) {
    const link = document.createElement('a');
    link.href = url;
    link.textContent = label;
    link.target = '_blank';
    link.rel = 'noopener noreferrer';
    link.className = 'text-link';
    parent.append(link);
  }

  function publicLink(value) {
    if (!value) return '';
    try {
      const url = new URL(value, location.href);
      return ['https:', 'http:'].includes(url.protocol) ? url.href : '';
    } catch {
      return '';
    }
  }

  function renderPreview(target, record, mail) {
    target.replaceChildren();
    addText(target, 'p', mail ? 'פרחי שמיים · ' + record.label : record.label, 'kicker');
    addText(target, 'h3', record.title);
    if (record.cover) {
      const cover = document.createElement('img');
      cover.src = record.cover;
      cover.alt = 'עטיפת השיר ' + record.title;
      cover.width = 1280;
      cover.height = 720;
      target.append(cover);
    }
    addText(target, 'p', record.description);
    if (record.timing) addText(target, 'p', record.timing, 'preview-fact');
    if (record.details) addText(target, 'p', record.details, 'preview-fact');

    const links = document.createElement('div');
    links.className = 'preview-links';
    const href = publicLink(record.link);
    if (href) addLink(links, href, record.action);
    if (record.pdf) addLink(links, record.pdf.url, 'פתיחת PDF · ' + record.pdf.name);
    if (links.childElementCount) target.append(links);
    if (mail) addText(target, 'p', 'בתחתית המייל יופיע קישור להסרה ולעדכון העדפות.', 'small');
  }

  function refresh() {
    const record = records[type.value];
    renderPreview(sitePreview, record, false);
    if (emailPreview) renderPreview(emailPreview, records[campaignType.value], true);
    fileName.textContent = record.pdf ? 'PDF שנבחר לדוגמה · ' + record.pdf.name : 'אפשר לבחור קובץ ולהציג אותו בדוגמה.';
    removeFile.hidden = !record.pdf;
  }

  function loadRecord() {
    const record = records[type.value];
    for (const [key, field] of Object.entries(fields)) field.value = record[key];
    document.getElementById('editor-timing-label').textContent = record.timingLabel;
    document.getElementById('editor-details-label').textContent = record.detailsLabel;
    document.getElementById('editor-link-label').textContent = record.linkLabel;
    documentInput.value = '';
    feedback.textContent = 'התוכן והקובץ מוצגים כאן לשם המחשה.';
    refresh();
  }

  type.addEventListener('change', loadRecord);
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const record = records[type.value];
    for (const [key, field] of Object.entries(fields)) record[key] = field.value.trim();
    refresh();
    feedback.textContent = emailPreview && type.value !== 'story'
      ? 'התצוגה באתר עודכנה. תבנית הדיוור המתאימה תציג את אותם הפרטים.'
      : 'התצוגה באתר עודכנה.';
  });

  documentInput.addEventListener('change', async () => {
    const file = documentInput.files[0];
    if (!file) return;
    const record = records[type.value];
    const header = await file.slice(0, 5).text();
    if (documentInput.files[0] !== file) return;
    if (!file.name.toLowerCase().endsWith('.pdf') || header !== '%PDF-') {
      documentInput.value = '';
      feedback.textContent = 'יש לבחור מסמך PDF תקין.';
      return;
    }
    if (record.pdf) URL.revokeObjectURL(record.pdf.url);
    const pdf = file.slice(0, file.size, 'application/pdf');
    record.pdf = {name: file.name, url: URL.createObjectURL(pdf)};
    refresh();
  });
  removeFile.addEventListener('click', () => {
    const record = records[type.value];
    URL.revokeObjectURL(record.pdf.url);
    delete record.pdf;
    documentInput.value = '';
    refresh();
  });

  if (campaignType) {
    campaignType.addEventListener('change', refresh);
    document.querySelector('[data-edit-campaign]').addEventListener('click', () => {
      type.value = campaignType.value;
      loadRecord();
      document.querySelector('[data-panel="content"]').click();
      fields.title.focus();
    });
  }

  loadRecord();
  form.querySelector('[type="submit"]').disabled = false;
})();
