const { chromium } = require('/workspace/cache/builderbob/npm/_npx/a4d0c66fe73b166b/node_modules/playwright');
const fs = require('fs');
const assert = require('assert');
const path = '/workspace/repos/builderbob/write-with-purpose/work/blind-longform-review.html';
const fixture = { schema_version: 1, trial_id: 'fixture', cases: [
  { id: 'case-1', title: 'Fixture', author: 'Author', source_url: 'https://example.org/', license_url: 'https://example.org/license', source_attribution: 'Publisher', scope_label: 'Opening', task: 'Review', context_before: 'Before context', context_after: 'After context', original: { text: '# Heading\n\nOriginal **bold**.\n\n- One\n- Two\n\n`code`\n\n<img src=x onerror=window.bad=1>' }, A: { text: 'Alpha [link](https://example.org/)' }, B: { text: 'Beta' } },
  { id: 'case-2', title: 'Second', author: 'Author', source_url: 'https://example.org/', source_attribution: 'Publisher', scope_label: 'Whole piece', task: 'Review', original: { text: 'Text' }, A: { text: 'A' }, B: { text: 'B' } }
] };
(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: '/home/builderbob/.cache/ms-playwright/chromium-1194/chrome-linux/chrome' });
  try {
    const page = await browser.newPage({ viewport: {width:1024,height:900} });
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    await page.addInitScript(() => { window.openai = { setWidgetState: async state => { window.lastState = state; }, sendFollowUpMessage: async message => { window.lastMessage = message; } }; });
    const html = fs.readFileSync(path, 'utf8').replace(/(<script type="application\/json" id="blind-review-data">)[\s\S]*?(<\/script>)/, (_, start, end) => start + JSON.stringify(fixture) + end);
    await page.goto('about:blank'); await page.evaluate(content => { document.open(); document.write(content); document.close(); }, html);
    assert.equal(await page.locator('#blind-choice').inputValue(), '');
    assert.equal(await page.locator('#blind-substantive-improvement').inputValue(), '');
    assert.equal(await page.locator('#blind-attribution a').filter({hasText:'License'}).count(), 1);
    assert.equal(await page.locator('#blind-original ul li').count(), 2);
    assert.equal(await page.locator('#blind-original h3[aria-level=\"4\"]').count(), 1);
    assert.equal(await page.locator('#blind-context').isVisible(), true);
    assert.equal(await page.locator('#blind-context').evaluate(e => e.open), false);
    await page.locator('#blind-context summary').click();
    assert.equal(await page.locator('#blind-context-before').textContent(), 'Before context');
    assert.equal(await page.locator('#blind-original img').count(), 0);
    assert.equal(await page.evaluate(() => window.bad), undefined);
    await page.selectOption('#blind-choice', 'A'); await page.selectOption('#blind-substantive-improvement', 'Both');
    await page.fill('#blind-comment', 'Exact\ncomment');
    await page.waitForFunction(() => window.lastState && window.lastState.privateContent.reviews['case-1'].comment === 'Exact\ncomment');
    const stale = await page.evaluate(() => structuredClone(window.lastState));
    await page.fill('#blind-comment', 'Newer exact comment');
    await page.evaluate(state => window.dispatchEvent(new CustomEvent('openai:set_globals', {detail:{globals:{widgetState:state}}})), stale);
    assert.equal(await page.locator('#blind-comment').inputValue(), 'Newer exact comment');
    await page.fill('#blind-comment', 'Exact\ncomment');
    await page.selectOption('#blind-case', 'case-2'); assert.equal(await page.locator('#blind-context').isVisible(), false); await page.selectOption('#blind-case', 'case-1');
    assert.equal(await page.locator('#blind-comment').inputValue(), 'Exact\ncomment');
    await page.click('#blind-send');
    const msg = await page.evaluate(() => window.lastMessage);
    assert(msg.prompt.includes('\"schema_version\":1')); assert(msg.prompt.includes('\"trial_id\":\"fixture\"')); assert(msg.prompt.includes('Exact\\ncomment')); assert(msg.prompt.includes('\"substantive_improvement\":\"Both\"')); assert(!msg.prompt.includes('Alpha'));
    await page.evaluate(() => window.dispatchEvent(new CustomEvent('openai:set_globals', {detail:{globals:{widgetState:{privateContent:{schema_version:1,trial_id:'fixture',revision:100,selected:'case-2',reviews:{'case-2':{choice:'B',substantive_improvement:'Neither',comment:'restored'}}}}}}})));
    assert.equal(await page.locator('#blind-choice').inputValue(), 'B');
    assert.equal(await page.locator('#blind-substantive-improvement').inputValue(), 'Neither');
    await page.evaluate(() => window.dispatchEvent(new CustomEvent('openai:set_globals', {detail:{globals:{widgetState:{privateContent:{schema_version:1,trial_id:'wrong-trial',revision:1000,selected:'case-1',reviews:{}}}}}})));
    assert.equal(await page.locator('#blind-case').inputValue(), 'case-2');
    assert.equal(await page.locator('#blind-comment').inputValue(), 'restored');
    await page.evaluate(() => window.dispatchEvent(new CustomEvent('openai:set_globals', {detail:{globals:{widgetState:{privateContent:{schema_version:2,trial_id:'fixture',revision:1000,selected:'case-1',reviews:{}}}}}})));
    assert.equal(await page.locator('#blind-case').inputValue(), 'case-2');
    for (const width of [1024, 736, 320]) {
      await page.setViewportSize({width,height:900});
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `overflow at ${width}`);
      const columns = await page.locator('.review-columns section').evaluateAll(es => es.map(e => e.getBoundingClientRect().top));
      assert(width === 320 ? columns[0] < columns[1] && columns[1] < columns[2] : columns[0] === columns[1] && columns[1] === columns[2], `layout at ${width}`);
    }
    await page.fill('#blind-comment', 'x'.repeat(18000));
    assert.equal(await page.locator('#blind-fallback').isVisible(), true);
    assert((await page.locator('#blind-status').textContent()).includes('save limit'));
    await page.evaluate(() => { delete window.openai.setWidgetState; });
    await page.fill('#blind-comment', 'x'.repeat(18001));
    assert.equal(await page.locator('#blind-fallback').isVisible(), true);
    assert((await page.locator('#blind-export').inputValue()).includes('x'.repeat(18001)));
    assert.deepEqual(errors, []);
    console.log('PASS: synthetic fixture; selection, safe rendering, restore, send, fallback, and responsive layout');
  } finally { await browser.close(); }
})().catch(e => { console.error(e); process.exit(1); });
