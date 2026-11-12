const { chromium } = require('playwright');
const [P, C] = process.argv.slice(2);
(async () => {
  const b = await chromium.launch(); const errs = [];
  const page = async (h) => { const p = await b.newPage({ viewport: { width: 1080, height: h } }); p.on('pageerror', e => errs.push(e.message)); return p; };
  // slides tirées du teaser (billet3.html), avec compteur et extras injectés
  const p = await page(1350);
  await p.goto('file://' + P + '/billet3.html'); await p.evaluate(() => window.ready);
  const inject = (n, extra) => `(() => { document.querySelectorAll('.inj').forEach(e => e.remove()); const s = document.getElementById('stage'); const c = document.createElement('p'); c.className = 'inj'; c.style.cssText = 'position:absolute;right:64px;top:66px;z-index:99;font:600 34px Mono;letter-spacing:.12em;color:#fff;margin:0'; c.textContent = '${n} / 05'; s.appendChild(c); ${extra || ''} })()`;
  const shots = [
    ['01-la-beta-est-lancee', 4.1, inject('01', `const g = document.createElement('span'); g.className='inj'; g.style.cssText='position:absolute;left:50%;bottom:120px;translate:-50% 0;z-index:99;display:inline-flex;padding:18px 36px;border-radius:99px;border:2px solid #ffffff88;background:#ffffff2e;font:600 32px Grotesk;color:#fff'; g.textContent='Glisse →'; s.appendChild(g);`)],
    ['02-ton-village-pass', 8.45, inject('02')],
    ['03-ton-billet', 16.2, inject('03')],
    ['05-viens-chercher-ton-billet', 22.6, inject('05')],
  ];
  for (const [name, t, js] of shots) { await p.evaluate(t => seek(t), t); await p.evaluate(js); await p.screenshot({ path: `${C}/${name}.png` }); }
  // calques transparents pour les images tirées de la vidéo
  const ov = async (qs, h, file) => { const o = await page(h); await o.goto('file://' + P + '/ovl.html?' + qs); await o.evaluate(() => window.ready); await o.waitForTimeout(150); await o.screenshot({ path: file, omitBackground: true }); await o.close(); };
  await ov('brand=1&n=04', 1350, P + '/out/ov-04.png');
  await ov('h=1920&shade=1&cta=' + encodeURIComponent('Demande ton accès →') + '&cy=1560', 1920, P + '/out/ov-story1.png');
  console.log('errors', errs); await b.close();
})();
