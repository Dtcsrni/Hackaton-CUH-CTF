const { chromium } = require('O:/Descargas/hackaton/.pwtmp/node_modules/playwright');
(async() => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 2048, height: 1100 } });
  await page.goto('https://45.55.49.111/', { waitUntil: 'networkidle' });
  const data = await page.evaluate(() => {
    const brand = document.querySelector('.ctfcu-brand-frame');
    const brandImg = document.querySelector('.ctfcu-brand-image');
    const collapse = document.querySelector('#base-navbars');
    const panel = document.querySelector('.ctfcu-navbar-panel');
    const pack = (el) => {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return { x:r.x,y:r.y,width:r.width,height:r.height,display:cs.display,position:cs.position,flexDirection:cs.flexDirection,marginTop:cs.marginTop,paddingTop:cs.paddingTop };
    };
    return { brand: pack(brand), brandImg: pack(brandImg), collapse: pack(collapse), panel: pack(panel) };
  });
  console.log(JSON.stringify(data, null, 2));
  await browser.close();
})();
