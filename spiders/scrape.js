const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({headless: "true"});
  const page = await browser.newPage();
  await page.goto('https://inkertattoo.com.br');
  await page.screenshot({ path: 'example.png' });

  await browser.close();
})();