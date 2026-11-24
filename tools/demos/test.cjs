// בדיקות מקצה לקצה לשלוש הדגמות המסלולים.
// הרצה: python3 -m http.server 8765 (משורש המאגר), ואז: node tools/demos/test.cjs http://localhost:8765/demos/
const { chromium } = require('playwright');
const assert = require('assert');
const ROOT = process.argv[2] || 'http://localhost:8765/demos/';
const ONLY = process.argv[3]; // אפשר להריץ מסלול אחד: 1 / 2 / 3
const results = [];
async function t(name, fn) {
  try { await fn(); results.push(['PASS', name]); } catch (e) { results.push(['FAIL', name, e.message.replace(/\s+/g, ' ').slice(0, 400)]); }
}
function watch(page) {
  const errs = [];
  page.on('console', (m) => { if (m.type() === 'error' && !/youtube|ytimg|google|doubleclick|ERR_TUNNEL|ERR_CONNECTION|ERR_NAME|mailto/i.test(m.text() + (m.location().url || ''))) errs.push('console: ' + m.text() + ' @ ' + (m.location().url || '')); });
  page.on('pageerror', (e) => errs.push('pageerror: ' + e.message));
  page.on('response', (r) => { if (r.status() >= 400 && !/youtube|ytimg|google/.test(r.url())) errs.push(r.status() + ' ' + r.url()); });
  return errs;
}
async function noOverflow(page, label) {
  const [sw, iw] = await page.evaluate(() => [document.documentElement.scrollWidth, window.innerWidth]);
  assert.ok(sw <= iw, `${label}: horizontal overflow ${sw} > ${iw}`);
}
async function scrollThrough(page) {
  await page.evaluate(async () => {
    for (let y = 0; y < document.documentElement.scrollHeight; y += Math.round(innerHeight * 0.7)) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 110)); }
    window.scrollTo(0, document.documentElement.scrollHeight); await new Promise((r) => setTimeout(r, 400));
  });
}
async function fillJoin(page, lang, branch, name) {
  await page.selectOption('#f-branch', branch);
  await page.fill('#f-parent', name);
  await page.fill('#f-phone', '050-1234567');
  await page.fill('#f-email', 'parent@example.com');
  await page.fill('#f-child', lang === 'he' ? 'יוסי' : 'Yossi');
  await page.fill('#f-age', '9');
  await page.fill('#f-cheder', lang === 'he' ? 'תלמוד תורה' : 'Talmud Torah');
  await page.selectOption('#f-grade', { index: 3 });
  await page.check('#f-consent');
}

(async () => {
  const browser = await chromium.launch();
  for (const plan of [1, 2, 3]) {
    if (ONLY && String(plan) !== ONLY) continue;
    for (const lang of ['he', 'en']) {
      for (const [vw, vh, dev] of [[1440, 900, 'desktop'], [390, 844, 'mobile']]) {
        const url = `${ROOT}${plan}/${lang === 'en' ? 'en/' : ''}`;
        const ctx = await browser.newContext({ viewport: { width: vw, height: vh }, hasTouch: dev === 'mobile', isMobile: dev === 'mobile' });
        const page = await ctx.newPage();
        const errs = watch(page);
        const L = `[P${plan}/${lang}/${dev}]`;
        await page.goto(url, { waitUntil: 'load' });
        await page.waitForTimeout(400);

        await t(`${L} first screen: headline + main button visible at once`, async () => {
          const box = await page.locator('.hero .btn-mint').boundingBox();
          assert.ok(box && box.y + box.height <= vh, 'CTA below fold ' + JSON.stringify(box));
          assert.strictEqual(await page.locator('h1').evaluate((e) => getComputedStyle(e).opacity), '1');
        });
        await t(`${L} sections match the plan`, async () => {
          assert.strictEqual(await page.locator('#stage').count(), plan === 1 ? 0 : 1);
          assert.strictEqual(await page.locator('#behind').count(), plan === 1 ? 0 : 1);
          assert.strictEqual(await page.locator('#club').count(), plan === 3 ? 1 : 0);
          assert.strictEqual(await page.locator('#f-account').count(), plan === 3 ? 1 : 0);
          assert.strictEqual(await page.locator('.plan-switch a[aria-current="page"]').textContent(), String(plan));
        });
        await t(`${L} one button per class card`, async () => {
          const counts = await page.$$eval('.branch', (cards) => cards.map((c) => c.querySelectorAll('a, button').length));
          assert.deepStrictEqual(counts, [1, 1, 1, 1]);
        });
        await t(`${L} choosing a class fills the form and focuses it`, async () => {
          await page.click('[data-choose="neve-yaakov"]');
          await page.waitForTimeout(700);
          assert.strictEqual(await page.inputValue('#f-branch'), 'neve-yaakov');
          assert.strictEqual(await page.evaluate(() => document.activeElement.id), 'f-parent');
        });
        await t(`${L} empty submit shows 9 errors`, async () => {
          await page.selectOption('#f-branch', '');
          await page.click('#join-form button[type="submit"]');
          assert.strictEqual(await page.locator('#join-form [aria-invalid="true"]').count(), 9);
        });
        const parent = lang === 'he' ? 'בדיקה הורה' : 'Test Parent';
        if (plan === 1) {
          await t(`${L} email form opens a ready message (no storage)`, async () => {
            await page.evaluate(() => localStorage.clear());
            await fillJoin(page, lang, 'ramah-a', parent);
            await page.click('#join-form button[type="submit"]');
            await page.waitForTimeout(400);
            assert.ok(await page.locator('#join-success').isVisible());
            const href = await page.getAttribute('[data-mailto]', 'href');
            assert.ok(href.startsWith('mailto:mordi.gordon@gmail.com?subject='), href);
            assert.ok(decodeURIComponent(href).includes(parent), 'body missing parent');
            assert.strictEqual(await page.evaluate(() => localStorage.getItem('ps-inquiries')), null);
            await page.click('[data-again]');
            assert.ok(await page.locator('#join-form').isVisible());
          });
          await t(`${L} landing shows 8 songs without filters`, async () => {
            assert.strictEqual(await page.locator('.song').count(), 8);
            assert.strictEqual(await page.locator('#song-search').count(), 0);
          });
        } else {
          await t(`${L} valid submit saves and shows email preview`, async () => {
            await fillJoin(page, lang, 'ramah-a', parent);
            if (plan === 3) {
              assert.ok(!(await page.locator('[data-account-topics]').isVisible()));
              await page.check('#f-account');
              assert.ok(await page.locator('[data-account-topics]').isVisible());
            }
            await page.click('#join-form button[type="submit"]');
            await page.waitForTimeout(400);
            const txt = await page.textContent('#join-success');
            assert.ok(txt.includes(parent));
            assert.ok(txt.includes(lang === 'he' ? 'מתנ״ס גוונים' : 'Gvanim'));
            const saved = await page.evaluate(() => JSON.parse(localStorage.getItem('ps-inquiries') || '[]'));
            assert.ok(saved[0] && saved[0].branch === 'ramah-a');
            if (plan === 3) {
              const subs = await page.evaluate(() => JSON.parse(localStorage.getItem('ps-subscribers') || '[]'));
              assert.ok(subs[0] && subs[0].source === 'class' && subs[0].topics.length === 3);
              assert.ok(await page.locator('#join-success .email-btn').count() === 1);
            }
            await page.click('[data-again]');
            assert.strictEqual(await page.inputValue('#f-parent'), '');
          });
          await t(`${L} home page stays short: 8 songs, library images not loaded yet`, async () => {
            assert.strictEqual(await page.locator('.songs-home .song:visible').count(), 8);
            assert.ok(!(await page.locator('#library').isVisible()));
            assert.strictEqual(await page.locator('#library img[src]').count(), 0);
          });
          await t(`${L} library: opens on click with all songs, filter and search`, async () => {
            const open = page.locator('[data-library-open]');
            await open.scrollIntoViewIfNeeded(); await open.click();
            assert.ok(await page.locator('#library').isVisible());
            assert.strictEqual(await page.evaluate(() => document.activeElement.id), 'song-search');
            // כל הסרטונים בערוץ, בלי הסרטון הכפול של ״פותח״
            assert.strictEqual(await page.locator('#library .song:visible').count(), 49);
            await page.click('#library [data-filter="makhalolam"]');
            assert.strictEqual(await page.locator('#library .song:visible').count(), 2);
            await page.click('#library [data-filter="all"]');
            await page.fill('#song-search', lang === 'he' ? 'אור חדש' : 'Or Chadash');
            assert.strictEqual(await page.locator('#library .song:visible').count(), 1);
            await page.fill('#song-search', 'zzzz');
            assert.ok(await page.locator('#library .songs-empty').isVisible());
            await page.fill('#song-search', '');
          });
          await t(`${L} short clips open in a visible vertical player above the library`, async () => {
            await page.click('#library [data-filter="short"]');
            assert.strictEqual(await page.locator('#library .song:visible').count(), 6);
            await page.locator('#library .song:visible .song-btn').first().click();
            const box = await page.locator('#player .player-frame').boundingBox();
            assert.ok(box && box.width > 150 && box.height > box.width, 'vertical frame box ' + JSON.stringify(box));
            const ifr = await page.locator('#player iframe').boundingBox();
            assert.ok(ifr && ifr.width > 150 && ifr.height > 250, 'iframe box ' + JSON.stringify(ifr));
            await page.keyboard.press('Escape');
            assert.ok(!(await page.locator('#player').isVisible()));
            assert.ok(await page.locator('#library').isVisible(), 'Esc on the player should keep the library open');
            await page.click('#library [data-filter="all"]');
            await page.keyboard.press('Escape');
            assert.ok(!(await page.locator('#library').isVisible()));
            assert.ok(!(await page.evaluate(() => document.body.classList.contains('is-locked'))));
          });
        }
        if (plan === 3) {
          await t(`${L} updates club: validation then success`, async () => {
            const f = page.locator('#club-form');
            await f.scrollIntoViewIfNeeded();
            await f.locator('[name="c-topic"]').evaluateAll((els) => els.forEach((e) => { e.checked = false; }));
            await f.locator('button[type="submit"]').click();
            assert.ok((await page.textContent('#ce-email')).length > 0);
            assert.ok((await page.textContent('#ce-topics')).length > 0);
            assert.ok((await page.textContent('#ce-consent')).length > 0);
            await page.fill('#c-email', 'fan@example.com');
            await f.locator('[name="c-topic"][value="songs"]').check();
            await page.check('#c-consent');
            await f.locator('button[type="submit"]').click();
            assert.ok(await page.locator('#club-success').isVisible());
            assert.ok((await page.textContent('#club-success')).includes('fan@example.com'));
            const subs = await page.evaluate(() => JSON.parse(localStorage.getItem('ps-subscribers') || '[]'));
            assert.ok(subs.some((s) => s.email === 'fan@example.com' && s.source === 'club'));
          });
        }
        await t(`${L} player opens and Esc closes`, async () => {
          const btn = page.locator('.song-btn').first();
          await btn.scrollIntoViewIfNeeded(); await btn.click();
          assert.ok(await page.locator('#player').isVisible());
          assert.ok((await page.getAttribute('#player iframe', 'src')).includes('youtube-nocookie.com/embed/'));
          const fb = await page.locator('#player iframe').boundingBox();
          assert.ok(fb && fb.width > 200 && fb.height > 100, 'landscape iframe box ' + JSON.stringify(fb));
          await page.keyboard.press('Escape');
          assert.ok(!(await page.locator('#player').isVisible()));
        });
        await t(`${L} scroll through: images load, no overflow`, async () => {
          await scrollThrough(page);
          const broken = await page.$$eval('img', (imgs) => imgs.filter((i) => i.getAttribute('src') && (!i.complete || i.naturalWidth === 0) && !i.closest('.player') && i.offsetParent !== null).map((i) => i.getAttribute('src')));
          assert.deepStrictEqual(broken, []);
          await noOverflow(page, 'after scroll');
        });
        if (dev === 'desktop' && plan !== 1) {
          await t(`${L} behind-the-scenes strip moves sideways`, async () => {
            const top = await page.locator('[data-strip]').evaluate((e) => e.getBoundingClientRect().top + scrollY);
            await page.evaluate((y) => window.scrollTo(0, y + 600), top); await page.waitForTimeout(250);
            const tx = parseFloat(await page.locator('.strip-track').evaluate((e) => e.style.getPropertyValue('--tx')));
            assert.ok(lang === 'he' ? tx > 0 : tx < 0, 'tx ' + tx);
          });
        }
        if (dev === 'mobile') {
          await t(`${L} mobile menu`, async () => {
            await page.evaluate(() => window.scrollTo(0, 0));
            await page.click('[data-menu-toggle]'); await page.waitForTimeout(350);
            assert.ok(await page.locator('.main-nav a').first().isVisible());
            await page.locator('.main-nav a[href="#music"]').click(); await page.waitForTimeout(300);
            assert.strictEqual(await page.getAttribute('[data-menu-toggle]', 'aria-expanded'), 'false');
          });
        }
        await t(`${L} accessibility basics`, async () => {
          assert.strictEqual(await page.$$eval('img', (a) => a.filter((i) => !i.hasAttribute('alt')).length), 0);
          const unlabeled = await page.$$eval('input:not([type=hidden]), select, textarea', (els) => els.filter((e) => !e.closest('.hp') && !(e.labels && e.labels.length) && !e.getAttribute('aria-label')).map((e) => e.id || e.name));
          assert.deepStrictEqual(unlabeled, []);
          const nameless = await page.$$eval('button, a[href]', (els) => els.filter((e) => !(e.getAttribute('aria-label') || e.textContent.trim())).map((e) => e.outerHTML.slice(0, 80)));
          assert.deepStrictEqual(nameless, []);
          const ids = await page.$$eval('[id]', (els) => els.map((e) => e.id));
          assert.deepStrictEqual(ids.filter((x, i) => ids.indexOf(x) !== i), []);
        });
        await t(`${L} language + plan links resolve`, async () => {
          const links = await page.$$eval('.lang-link, .plan-switch a, .flyers a', (as) => as.map((a) => a.href));
          for (const h of links) { const r = await page.request.get(h); assert.ok(r.ok(), h + ' ' + r.status()); }
        });
        await t(`${L} no console errors / missing files`, async () => { assert.deepStrictEqual(errs, []); });
        await ctx.close();
      }
    }
  }

  // לוחות הניהול
  for (const plan of [2, 3]) {
    if (ONLY && String(plan) !== ONLY) continue;
    const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, acceptDownloads: true });
    const page = await ctx.newPage();
    const errs = watch(page);
    const L = `[admin P${plan}]`;
    await page.goto(`${ROOT}${plan}/`, { waitUntil: 'load' });
    await page.click('[data-choose="ramat-eshkol"]');
    await fillJoin(page, 'he', 'ramat-eshkol', 'הורה מהאתר');
    if (plan === 3) await page.check('#f-account');
    await page.click('#join-form button[type="submit"]');
    await page.click('#join-success a.btn');
    await page.waitForLoadState('load');
    await t(`${L} inquiry from the site appears first`, async () => {
      assert.ok((await page.locator('[data-rows] tr').first().textContent()).includes('הורה מהאתר'));
      assert.strictEqual(await page.textContent('[data-stat="new"]'), '3');
    });
    await t(`${L} status change + filters + export`, async () => {
      await page.locator('[data-rows] tr').first().locator('select').selectOption('audition');
      assert.strictEqual(await page.textContent('[data-stat="audition"]'), '2');
      await page.selectOption('#f-branch', 'ramah-a');
      assert.strictEqual(await page.locator('[data-rows] tr').count(), 2);
      await page.selectOption('#f-branch', '');
      const [dl] = await Promise.all([page.waitForEvent('download'), page.click('[data-export]')]);
      const buf = require('fs').readFileSync(await dl.path());
      assert.ok(buf[0] === 0xef && buf.toString('utf8').includes('הורה מהאתר'));
      assert.ok(dl.suggestedFilename().endsWith('.csv'));
    });
    await t(`${L} tabs match plan`, async () => {
      assert.strictEqual(await page.locator('#tab-subscribers').count(), plan === 3 ? 1 : 0);
      assert.strictEqual(await page.locator('#tab-mailing').count(), plan === 3 ? 1 : 0);
    });
    if (plan === 3) {
      await t(`${L} subscribers list includes the site sign-up`, async () => {
        await page.click('#tab-subscribers');
        assert.ok((await page.textContent('[data-subs]')).includes('parent@example.com'));
        assert.strictEqual(await page.textContent('[data-topic-count="classes"]'), '4');
        await page.click('[data-topic-card="shows"]');
        const rows = await page.locator('[data-subs] tr').count();
        assert.ok(rows >= 1 && rows < 8, 'rows ' + rows);
        const [dl] = await Promise.all([page.waitForEvent('download'), page.click('[data-export-subs]')]);
        assert.ok(dl.suggestedFilename().endsWith('.csv'));
      });
      await t(`${L} mailing templates: preview + validation + send`, async () => {
        await page.click('#tab-mailing');
        await page.click('[data-mail-form] button[type="submit"]');
        assert.ok(await page.locator('[data-tpl-fields] [aria-invalid="true"]').count() >= 2);
        await page.fill('[data-tpl-fields] input[name="title"]', 'שיר בדיקה');
        await page.fill('[data-tpl-fields] input[name="link"]', 'https://www.youtube.com/watch?v=-4sE-rfQI1k');
        assert.ok((await page.textContent('[data-mail-preview]')).includes('שיר בדיקה'));
        await page.click('[data-mail-form] button[type="submit"]');
        assert.ok((await page.textContent('[data-mail-form] .form-msg')).includes('נשלח'));
        await page.locator('.tpl', { hasText: 'הופעה' }).click();
        assert.ok(await page.locator('[data-tpl-fields] input[name="date"]').count() === 1);
        assert.ok((await page.textContent('[data-mail-preview]')).includes('הופעה'));
      });
    }
    await t(`${L} mobile has no overflow`, async () => {
      await page.setViewportSize({ width: 390, height: 844 });
      await page.click('#tab-inquiries');
      await noOverflow(page, 'admin mobile');
    });
    await t(`${L} no console errors`, async () => { assert.deepStrictEqual(errs, []); });
    await ctx.close();
  }

  // עמוד הבחירה
  if (!ONLY) {
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
    const errs = watch(page);
    await page.goto(ROOT, { waitUntil: 'load' });
    await t('[hub] all links resolve', async () => {
      const links = await page.$$eval('.hub-card a', (as) => as.map((a) => a.href));
      assert.strictEqual(links.length, 8);
      for (const h of links) { const r = await page.request.get(h); assert.ok(r.ok(), h); }
    });
    await t('[hub] mobile no overflow', async () => { await page.setViewportSize({ width: 390, height: 844 }); await noOverflow(page, 'hub'); });
    await t('[hub] no errors', async () => { assert.deepStrictEqual(errs, []); });
  }
  await browser.close();
  const fails = results.filter((r) => r[0] === 'FAIL');
  fails.forEach((r) => console.log(r.join(' | ')));
  console.log(`\n${results.length - fails.length}/${results.length} passed`);
  process.exit(fails.length ? 1 : 0);
})();
