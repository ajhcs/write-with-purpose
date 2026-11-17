const { chromium } = require('/workspace/cache/builderbob/npm/_npx/a4d0c66fe73b166b/node_modules/playwright');
const fs = require('fs');
const crypto = require('crypto');
const assert = require('assert');
const root = '/workspace/repos/builderbob/write-with-purpose/';
const fragment = fs.readFileSync(root + 'work/blind-longform-review.html', 'utf8');
const dataFile = fs.readFileSync(root + 'experiments/blind-longform-2026-11-16/review/data.json');
const publicData = JSON.parse(dataFile);
const sha = s => crypto.createHash('sha256').update(s).digest('hex');
(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: '/home/builderbob/.cache/ms-playwright/chromium-1194/chrome-linux/chrome' });
  let checks = 0;
  try {
    const page = await browser.newPage({viewport:{width:1024,height:900}});
    const errors = []; page.on('pageerror', e => errors.push(e.message));
    await page.addInitScript(() => { window.openai = {setWidgetState: async s => {window.saved = s},sendFollowUpMessage: async m => {window.sent = m}}; });
    await page.goto('about:blank'); await page.evaluate(content => {document.open();document.write(content);document.close()}, fragment);
    const embedded = await page.locator('#blind-review-data').textContent();
    assert.deepStrictEqual(JSON.parse(embedded), publicData); checks++;
    assert.equal(publicData.cases.length, 16); checks++;
    const licensed = publicData.cases.filter(c => c.license_url); assert(licensed.length >= 2); checks++;
    const options = await page.locator('#blind-case option').count(); assert.equal(options, 16); checks++;
    for (const width of [1024,736,320]) {
      await page.setViewportSize({width,height:900});
      for (const c of publicData.cases) {
        await page.selectOption('#blind-case',c.id);
        assert.equal(await page.locator('#blind-choice').inputValue(),'');
        assert.equal(await page.locator('#blind-substantive-improvement').inputValue(),'');
        assert.equal(await page.locator('#blind-comment').inputValue(),'');
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), `overflow at ${width} for ${c.id}`);
        const top = await page.locator('.review-columns section').evaluateAll(es => es.map(e => e.getBoundingClientRect().top));
        assert(width === 320 ? top[0] < top[1] && top[1] < top[2] : top[0] === top[1] && top[1] === top[2], `layout at ${width} for ${c.id}`);
        const hasContext = !!((c.context_before || '').trim() || (c.context_after || '').trim());
        assert.equal(await page.locator('#blind-context').isVisible(), hasContext);
        if (hasContext) { assert.equal(await page.locator('#blind-context').evaluate(e => e.open),false); await page.locator('#blind-context summary').click(); assert.equal(await page.locator('#blind-context').evaluate(e => e.open),true); }
        assert.equal(await page.locator('#blind-original img, #blind-a img, #blind-b img, #blind-original script, #blind-a script, #blind-b script').count(),0);
        assert.equal(await page.locator('#blind-original').innerText() !== '', true);
        assert.equal(await page.locator('#blind-a').innerText() !== '', true);
        assert.equal(await page.locator('#blind-b').innerText() !== '', true);
        if (c.license_url) { const link = page.locator('#blind-attribution a').filter({hasText:'License'}); assert.equal(await link.count(),1); assert.equal(await link.getAttribute('href'), new URL(c.license_url).href); }
        checks++;
      }
    }
    const codeCase = publicData.cases.find(c => ['original','A','B'].some(k => c[k].text.includes('```')));
    assert(codeCase); await page.selectOption('#blind-case',codeCase.id);
    assert((await page.locator('.review-columns pre code').count()) > 0); checks++;
    const whole = publicData.cases.filter(c => /whole/i.test(c.scope_label)); assert.equal(whole.length,4); checks++;
    await page.selectOption('#blind-choice','Tie'); await page.selectOption('#blind-substantive-improvement','Both'); await page.fill('#blind-comment','Fixture review\nExact text');
    await page.waitForFunction(() => window.saved && Object.values(window.saved.privateContent.reviews).some(r => r.comment === 'Fixture review\nExact text'));
    const saved = await page.evaluate(() => window.saved); checks++;
    await page.selectOption('#blind-case', publicData.cases.find(c => c.id !== codeCase.id).id);
    saved.privateContent.revision += 100;
    await page.evaluate(s => window.dispatchEvent(new CustomEvent('openai:set_globals',{detail:{globals:{widgetState:s}}})), saved);
    assert.equal(await page.locator('#blind-case').inputValue(),codeCase.id); assert.equal(await page.locator('#blind-comment').inputValue(),'Fixture review\nExact text'); checks++;
    await page.click('#blind-send'); const sent = await page.evaluate(() => window.sent); const payload = JSON.parse(sent.prompt.slice(sent.prompt.indexOf('\n')+1));
    assert.equal(payload.trial_id, publicData.trial_id); assert.equal(payload.schema_version,1); assert.equal(payload.reviews.length,1); assert.deepStrictEqual(payload.reviews[0],{id:codeCase.id, choice:'Tie', substantive_improvement:'Both', comment:'Fixture review\nExact text'}); checks++;
    assert.deepStrictEqual(errors, []); checks++;
    console.log(JSON.stringify({status:'pass',checks,case_width_combinations:48,whole_cases:whole.length,licensed_cases:licensed.length,code_case_tested:true,fragment_sha256:sha(fragment),data_sha256:sha(dataFile),host:'mocked'}));
  } finally {await browser.close()}
})().catch(e => {console.error(e.message); process.exit(1)});
