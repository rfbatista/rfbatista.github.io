// Seam B extra: at 375px a long code block shows an overflow cue and scrolls by keyboard.
// Env: BROWSER_CHECK_BASE, BROWSER_CHECK_OUT. Run by browser-check.sh after the main pass.
import { createRequire } from "node:module";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const base = process.env.BROWSER_CHECK_BASE, out = process.env.BROWSER_CHECK_OUT;
const browser = await chromium.launch();
let failed = false;
for (const theme of ["light", "dark"]) {
  const page = await (await browser.newContext({ viewport: { width: 375, height: 800 }, colorScheme: theme })).newPage();
  await page.goto(base + "/posts/tp-link-in-arch-linux/", { waitUntil: "networkidle" });
  const idx = await page.evaluate(() => [...document.querySelectorAll("pre")].findIndex((p) => p.scrollWidth > p.clientWidth + 8));
  if (idx < 0) { console.log(`FAIL ${theme}: no code block overflows at 375`); failed = true; continue; }
  const pre = page.locator("pre").nth(idx);
  const bg = await pre.evaluate((e) => getComputedStyle(e).backgroundImage);
  const cue = /gradient/.test(bg);
  await pre.focus();
  const before = await pre.evaluate((e) => e.scrollLeft);
  for (let i = 0; i < 5; i++) await page.keyboard.press("ArrowRight");
  await page.waitForTimeout(400);
  const after = await pre.evaluate((e) => e.scrollLeft);
  await pre.scrollIntoViewIfNeeded();
  await page.screenshot({ path: `${out}/code-cue-375-${theme}.png` });
  const ok = cue && after > before;
  if (!ok) failed = true;
  console.log(`${ok ? "ok  " : "FAIL"} code cue ${theme} gradient=${cue} scrollLeft ${before}->${after}`);
}
await browser.close();
process.exit(failed ? 1 : 0);
