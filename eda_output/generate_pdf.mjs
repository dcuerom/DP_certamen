import puppeteer from 'puppeteer-core';
import { fileURLToPath } from 'url';
import path from 'path';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const browser = await puppeteer.launch({
  executablePath: '/usr/bin/google-chrome',
  args: ['--no-sandbox', '--disable-setuid-sandbox'],
  headless: 'new',
});

const page = await browser.newPage();
await page.setViewport({ width: 1920, height: 1080 });

const htmlPath = path.join(__dirname, 'slide_eda_conclusiones.html');
await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0', timeout: 15000 });

// Wait for fonts to load
await new Promise(r => setTimeout(r, 2000));

await page.pdf({
  path: path.join(__dirname, 'slide_eda_conclusiones.pdf'),
  width: '1920px',
  height: '1080px',
  landscape: true,
  printBackground: true,
  margin: { top: 0, right: 0, bottom: 0, left: 0 },
  preferCSSPageSize: true,
});

console.log('✅ PDF generated: slide_eda_conclusiones.pdf (1920x1080 landscape)');

await browser.close();
