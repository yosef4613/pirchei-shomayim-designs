'use strict';

const printButton = document.getElementById('print');
const response = document.getElementById('response');
const form = document.getElementById('response-form');
const choice = document.getElementById('choice');
const englishChoice = document.getElementById('english-choice');
const includeEnglish = document.getElementById('include-english');
const englishPrice = document.getElementById('english-price');
const note = document.getElementById('note');
const reply = document.getElementById('reply');
const replyLabel = document.getElementById('reply-label');
const copyButton = document.getElementById('copy');
const status = document.getElementById('response-status');
const buttons = [...document.querySelectorAll('[data-choice]')];

const plans = new Map(buttons.map((button) => {
  const card = button.closest('.plan');
  return [button.dataset.choice, {
    card,
    button,
    title: card.querySelector('h3').textContent,
    amount: card.querySelector('.price bdi').textContent,
    english: Number(card.querySelector('.language-price data').value),
  }];
}));

function updateReply() {
  const selected = plans.get(choice.value);
  for (const plan of plans.values()) {
    plan.card.classList.toggle('selected', plan === selected);
    plan.button.setAttribute('aria-pressed', String(plan === selected));
  }
  const askingToTalk = choice.value === 'talk';
  const hasChoice = Boolean(selected) || askingToTalk;
  reply.hidden = !hasChoice;
  replyLabel.hidden = !hasChoice;
  copyButton.disabled = !hasChoice;
  englishChoice.hidden = !selected;
  status.textContent = '';
  if (!hasChoice) {
    reply.value = '';
    return;
  }

  let message = 'שלום, תודה על הצעת המחיר לאתר פרחי שמיים. אשמח לדבר על המסלולים לפני שאבחר.';
  if (selected) {
    englishPrice.textContent = '+' + selected.english + ' ₪';
    let price = ' במחיר הקמה של ' + selected.amount + ' ש״ח';
    if (includeEnglish.checked) {
      const total = Number(selected.amount.replaceAll(',', '')) + selected.english;
      price = ' עם גרסה אנגלית מלאה, בסכום כולל של ' + total.toLocaleString('he-IL') + ' ש״ח להקמה';
    }
    message = 'שלום, תודה על ההצעה לאתר פרחי שמיים. אני מעוניין להתקדם עם המסלול ״'
      + selected.title + '״' + price + ', בתוספת עלויות הספקים לפי ההצעה. אשמח לתאם את ההמשך.';
  }
  const comment = note.value.trim();
  reply.value = comment ? message + '\n\n' + comment : message;
}

for (const button of buttons) {
  button.addEventListener('click', () => {
    choice.value = button.dataset.choice;
    updateReply();
    response.scrollIntoView({block: 'start'});
    choice.focus({preventScroll: true});
  });
  button.hidden = false;
}

form.addEventListener('submit', (event) => event.preventDefault());
choice.addEventListener('change', updateReply);
includeEnglish.addEventListener('change', updateReply);
note.addEventListener('input', updateReply);
copyButton.addEventListener('click', async () => {
  try {
    if (!navigator.clipboard) throw new Error('Clipboard unavailable');
    await navigator.clipboard.writeText(reply.value);
    status.textContent = 'התשובה הועתקה. אפשר להדביק אותה בהודעה.';
  } catch {
    reply.focus();
    reply.select();
    status.textContent = 'התשובה סומנה. אפשר להעתיק אותה ידנית.';
  }
});

printButton.addEventListener('click', () => window.print());
printButton.hidden = false;
response.hidden = false;
updateReply();
