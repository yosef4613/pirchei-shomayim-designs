'use strict';

(() => {
  const filters = document.querySelector('[data-area-filters]');
  const groups = [...document.querySelectorAll('[data-class-area]')];
  const buttons = [...filters.querySelectorAll('[data-filter-area]')];
  const count = document.querySelector('[data-class-count]');
  const flyer = document.querySelector('[data-jerusalem-flyer]');
  const english = document.documentElement.lang === 'en';

  function showArea(active) {
    const area = active.dataset.filterArea;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button === active)));
    groups.forEach(group => { group.hidden = area !== 'all' && group.dataset.classArea !== area; });
    flyer.hidden = area === 'beit-shemesh';
    const results = groups.filter(group => !group.hidden).length;
    count.textContent = english
      ? results + (results === 1 ? ' group' : ' groups')
      : results === 1 ? 'קבוצה אחת' : results + ' קבוצות';
  }

  for (const button of buttons) button.addEventListener('click', () => showArea(button));
  showArea(buttons[0]);
  filters.hidden = false;

  const motion = document.querySelector('[data-toggle-spotlights]');
  const hero = motion.closest('.hero');
  motion.addEventListener('click', () => {
    const paused = hero.toggleAttribute('data-spotlights-paused');
    motion.textContent = paused ? motion.dataset.resume : motion.dataset.pause;
  });
  motion.hidden = false;
})();
