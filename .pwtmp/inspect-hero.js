const { chromium } = require('O:/Descargas/hackaton/.pwtmp/node_modules/playwright');
(async() => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 2048, height: 1100 } });
  await page.goto('https://45.55.49.111/', { waitUntil: 'networkidle' });
  const data = await page.evaluate(() => {
    const shell = document.querySelector('.cuhv-cover-shell');
    const image = document.querySelector('.cuhv-cover-image');
    const final = document.querySelector('.cuhv-final-cover');
    const finalImg = document.querySelector('.cuhv-final-cover img');
    const hero = document.querySelector('.cuhv-hero');
    function pack(el) {
      if (!el) return null;
      const r = el.getBoundingClientRect();
      const cs = getComputedStyle(el);
      return {
        width: r.width,
        height: r.height,
        maxWidth: cs.maxWidth,
        maxHeight: cs.maxHeight,
        minHeight: cs.minHeight,
        objectFit: cs.objectFit,
        display: cs.display,
        transform: cs.transform,
        padding: cs.padding,
      };
    }
    return {
      shell: pack(shell),
      image: pack(image),
      final: pack(final),
      finalImg: pack(finalImg),
      hero: pack(hero),
      bodyWidth: document.body.getBoundingClientRect().width,
      htmlSnippet: shell?.outerHTML?.slice(0, 500),
    };
  });
  console.log(JSON.stringify(data, null, 2));
  await browser.close();
})();
