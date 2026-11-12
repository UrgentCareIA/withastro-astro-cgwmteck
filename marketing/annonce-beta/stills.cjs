const { chromium } = require('playwright');
const P = process.argv[2], O = P + '/out/carrousel';
(async () => {
  const b = await chromium.launch(); const errs = [];
  const shot = async (url, file, h, fn) => {
    const p = await b.newPage({ viewport: { width: 1080, height: h } });
    p.on('pageerror', e => errs.push(e.message)); p.on('requestfailed', r => errs.push('fail ' + r.url()));
    await p.goto(url); await p.evaluate(() => window.ready); if (fn) await p.evaluate(fn);
    await p.waitForTimeout(150);
    await p.screenshot({ path: file, type: 'jpeg', quality: 95 }); await p.close();
  };
  const post = 'file://' + P + '/posters.html?a=';
  await shot(post + 'a1', O + '/01-la-beta-est-lancee.jpg', 1350);
  await shot(post + 'a2', O + '/02-les-lieux.jpg', 1350);
  const comp = 'file://' + P + '/comp.html';
  const at = (t, n) => `(() => { seek(${t}); const c = document.createElement('span'); c.className = 'counter'; c.style.zIndex = 60; c.textContent = '${n} / 05'; document.getElementById('stage').appendChild(c); })()`;
  await shot(comp, O + '/03-tu-croises-un-collegue.jpg', 1350, at(12.9, '03'));
  await shot(comp, O + '/04-ton-village-pass.jpg', 1350, at(17.35, '04'));
  await shot(post + 'a5', O + '/05-comment-entrer.jpg', 1350);
  await shot(post + 'a6', O + '/story-la-beta-est-lancee.jpg', 1920);
  console.log('errors', errs); await b.close();
})();
