const { chromium } = require('playwright');
const [P, O] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 5400, height: 1350 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('requestfailed', r => errs.push('fail ' + r.url()));
  await p.goto('file://' + P + '/pano2.html'); await p.evaluate(() => window.ready); await p.waitForTimeout(300);
  await p.screenshot({ path: O + '/panorama.png' });
  console.log(errs); await b.close();
})();
