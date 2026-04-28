// Capture Play Store screenshots from the running dev server.
// Requires the dev server at http://localhost:8080 to be running.

const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const URL = 'http://localhost:8080';
const OUT = path.resolve(__dirname, '..', 'screenshots');

// 1080x1920 — within Play's 1:1.86 aspect-ratio limit and a common phone size.
const VIEWPORT = { width: 1080, height: 1920, deviceScaleFactor: 1 };

const wait = (ms) => new Promise((r) => setTimeout(r, ms));

async function ready(page) {
  await page.evaluate(() => document.fonts && document.fonts.ready);
  await wait(800);
}

async function reset(page) {
  await page.goto(URL, { waitUntil: 'networkidle0' });
  await ready(page);
}

(async () => {
  if (!fs.existsSync(OUT)) fs.mkdirSync(OUT, { recursive: true });

  const browser = await puppeteer.launch({
    executablePath: CHROME,
    headless: 'new',
    defaultViewport: null,
  });
  const page = await browser.newPage();
  await page.setViewport(VIEWPORT);

  // 1) Flashcard — a multi-syllable word shows off respelling + IPA
  await reset(page);
  await page.evaluate(() => { currentIndex = 59; render(); });   // "people"
  await wait(500);
  await page.screenshot({ path: path.join(OUT, '01-flashcard-people.png') });

  // 2) Flashcard with the Verbs filter active — shows the category system
  await reset(page);
  await page.evaluate(() => { setCategory('verb'); currentIndex = 9; render(); });  // verb #10
  await wait(500);
  await page.screenshot({ path: path.join(OUT, '02-verbs-filter.png') });

  // 3) Fill-in-the-blank mode — secondary feature
  await reset(page);
  await page.evaluate(() => { currentIndex = 92; render(); });   // "because"
  await page.click('#modeBtn');
  await wait(600);
  await page.screenshot({ path: path.join(OUT, '03-fill-in-the-blank.png') });

  // 4) Gamification — stars + happy mascot, on a fun word
  await reset(page);
  await page.evaluate(() => {
    stars = 12;
    document.getElementById('starCount').textContent = stars;
    currentIndex = 145;                                          // "play"
    render();
    setMascot('happy');
  });
  await wait(500);
  await page.screenshot({ path: path.join(OUT, '04-stars-and-fox.png') });

  await browser.close();
  console.log('Screenshots saved to:', OUT);
  for (const f of fs.readdirSync(OUT)) {
    const p = path.join(OUT, f);
    console.log(' ', f, '(' + fs.statSync(p).size + ' bytes)');
  }
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
