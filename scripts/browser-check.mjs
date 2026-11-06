// Browser pass over the built site. Env: BROWSER_CHECK_BASE, BROWSER_CHECK_OUT.
// Writes <out>/<page>-<w>-<theme>.png, <out>/report.json, prints a summary.
// Exit 1 if axe finds a violation or layout shift exceeds the limit.
import { createRequire } from "node:module";
import { readFileSync, writeFileSync } from "node:fs";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const axeSrc = readFileSync(require.resolve("axe-core/axe.min.js"), "utf8");

const base = process.env.BROWSER_CHECK_BASE;
const out = process.env.BROWSER_CHECK_OUT;
const CLS_LIMIT = Number(process.env.BROWSER_CHECK_CLS || 0.01);

const pages = {
  "home-pt": "/", "home-en": "/en/",
  "writing-pt": "/posts/", "writing-en": "/en/posts/",
  "post-pt": "/posts/tp-link-in-arch-linux/", "post-en": "/en/posts/tp-link-in-arch-linux/",
  "about-pt": "/about/", "about-en": "/en/about/",
  "projects-pt": "/projetos/", "projects-en": "/en/projects/",
  "garden-pt": "/jardim/", "photos-pt": "/photos/",
};
const only = process.env.BROWSER_CHECK_ONLY?.split(",");
const widths = { 375: 800, 1280: 900 };

const browser = await chromium.launch();
const report = [];
let failed = false;
for (const theme of ["light", "dark"]) {
  for (const [w, h] of Object.entries(widths)) {
    const ctx = await browser.newContext({
      viewport: { width: +w, height: h }, colorScheme: theme, reducedMotion: "reduce",
    });
    for (const [name, path] of Object.entries(pages)) {
      if (only && !only.includes(name)) continue;
      const page = await ctx.newPage();
      await page.addInitScript(() => {
        window.__cls = 0;
        new PerformanceObserver((l) => {
          for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value;
        }).observe({ type: "layout-shift", buffered: true });
      });
      // Delay the web fonts so the swap happens after first paint: the shift it causes is what we measure.
      await page.route("**/*.woff2", async (r) => { await new Promise((ok) => setTimeout(ok, 700)); await r.continue(); });
      const resp = await page.goto(base + path, { waitUntil: "load" });
      if (!resp || resp.status() !== 200) { console.log(`FAIL ${name}: HTTP ${resp?.status()}`); failed = true; await page.close(); continue; }
      await page.waitForFunction(() => [...document.fonts].some((f) => f.status === "loaded"), null, { timeout: 5000 }).catch(() => {});
      await page.evaluate(() => document.fonts.ready);
      await page.waitForTimeout(300);
      const fonts = await page.evaluate(() => [...document.fonts].filter((f) => f.status === "loaded").map((f) => `${f.family} ${f.weight}${f.style === "italic" ? "i" : ""}`));
      const cls = await page.evaluate(() => window.__cls);
      await page.screenshot({ path: `${out}/${name}-${w}-${theme}.png`, fullPage: true });
      await page.evaluate(axeSrc);
      const res = await page.evaluate(() => axe.run(document, {
        runOnly: { type: "tag", values: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"] },
      }));
      const violations = res.violations.map((v) => ({ id: v.id, impact: v.impact, nodes: v.nodes.length }));
      report.push({ page: name, width: +w, theme, cls: +cls.toFixed(4), fonts, violations });
      const bad = violations.length > 0 || cls > CLS_LIMIT;
      if (bad) failed = true;
      console.log(`${bad ? "FAIL" : "ok  "} ${name} ${w} ${theme} cls=${cls.toFixed(4)} ${violations.map((v) => `${v.id}×${v.nodes}`).join(" ")}`);
      await page.close();
    }
    await ctx.close();
  }
}
await browser.close();
writeFileSync(`${out}/report.json`, JSON.stringify(report, null, 1));
process.exit(failed ? 1 : 0);
