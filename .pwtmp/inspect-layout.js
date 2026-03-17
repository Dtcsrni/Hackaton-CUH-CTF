const { chromium } = require('O:/Descargas/hackaton/.pwtmp/node_modules/playwright');
(async() => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 2048, height: 1100 } });
  await page.goto('https://45.55.49.111/', { waitUntil: 'networkidle' });
  const data = await page.evaluate(() => {
    const hero = document.querySelector('.cuhv-hero');
    const copy = document.querySelector('.cuhv-hero-copy');
    const visual = document.querySelector('.cuhv-hero-visual');
    const nav = document.querySelector('nav.ctfcu-navbar-adaptive');
    const buttons = document.querySelector('.ctfcu-navbar-actions');
    const shell = document.querySelector('.cuhv-cover-shell');
    const pack = (el) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return { x: r.x, y: r.y, width: r.width, height: r.height, display: cs.display, position: cs.position, gridArea: cs.gridArea, gridTemplateColumns: cs.gridTemplateColumns };
    };
    return { nav: pack(nav), hero: pack(hero), copy: pack(copy), visual: pack(visual), buttons: pack(buttons), shell: pack(shell), heroText: copy?.textContent?.slice(0,200) };
  });
  console.log(JSON.stringify(data, null, 2));
  await browser.close();
})();
