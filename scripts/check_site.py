"""Checks the HTML Hugo generated. Usage: check_site.py <public dir>"""
import sys
import re
from html.parser import HTMLParser
from pathlib import Path

PUBLIC = Path(sys.argv[1])
failures = []


def page(url):
    f = PUBLIC / url.strip("/") / "index.html"
    if not f.is_file():
        failures.append(f"{url}: page was not generated")
        return ""
    return f.read_text(encoding="utf-8")


def check(ok, message):
    if not ok:
        failures.append(message)


class ProjectsParser(HTMLParser):
    """Collects <h2 class="sec"> groups and their <dl class="proj"> entries."""

    def __init__(self):
        super().__init__()
        self.groups = []  # [{"heading", "entries": [...]}]
        self.entries = []  # every entry, in page order
        self._in = None  # (kind, buffer) currently capturing text
        self._cur = None
        self._h2 = False
        self._depth_dl = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = (a.get("class") or "").split()
        if tag == "h2" and "sec" in cls:
            self._h2 = True
            self.groups.append({"heading": "", "entries": []})
        elif tag == "dl" and "proj" in cls:
            self._depth_dl += 1
        elif self._depth_dl and tag == "dt":
            self._cur = {"name": "", "href": None, "ext": False, "status": "",
                         "active": False, "private_marked": False, "desc": "", "desc_html": "", "meta": ""}
            self.entries.append(self._cur)
            if self.groups:
                self.groups[-1]["entries"].append(self._cur)
            self._in = "name"
        elif self._cur and tag == "a" and self._in == "name":
            self._cur["href"] = a.get("href")
            self._cur["ext"] = "ext" in cls
        elif self._cur and tag == "dd" and "st" in cls:
            self._cur["active"] = "on" in cls
            self._in = "status"
            self._status_dd = True
        elif self._cur and tag == "span" and "meta" in cls:
            self._in = "meta"
        elif self._cur and tag == "dd":
            self._in = "desc"
        elif self._cur and tag == "span" and "priv" in cls:
            self._cur["private_marked"] = True
        elif self._cur and self._in == "desc":
            self._cur["desc_html"] += self.get_starttag_text()

    def handle_endtag(self, tag):
        if tag == "h2":
            self._h2 = False
        elif tag == "dl":
            self._depth_dl = max(0, self._depth_dl - 1)
            self._cur = None
        elif tag == "dt" and self._in == "name":
            self._in = None
        elif tag in ("span", "dd") and self._in in ("status", "meta", "desc") and not (tag == "span" and self._in == "status"):
            self._in = None
        elif self._cur and self._in == "desc":
            self._cur["desc_html"] += f"</{tag}>"

    def handle_data(self, data):
        if self._h2 and self.groups:
            self.groups[-1]["heading"] += data
        elif self._cur and self._in:
            self._cur[self._in] += data
            if self._in == "desc":
                self._cur["desc_html"] += data


class NavParser(HTMLParser):
    """Collects the main navigation's links as (text, href, aria-current)."""

    def __init__(self):
        super().__init__()
        self.links = []
        self._nav = False
        self._cur = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "nav":
            self._nav = True
        elif tag == "a" and self._nav:
            self._cur = [ "", a.get("href"), a.get("aria-current") ]
            self.links.append(self._cur)

    def handle_endtag(self, tag):
        if tag == "nav":
            self._nav = False
        elif tag == "a":
            self._cur = None

    def handle_data(self, data):
        if self._cur is not None:
            self._cur[0] += data


def nav(url):
    p = NavParser()
    p.feed(page(url))
    return p.links


def projects(url):
    p = ProjectsParser()
    p.feed(page(url))
    for e in p.entries:
        for k in ("name", "status", "desc", "meta"):
            e[k] = e[k].strip()
    return p


ACTIVE_PT = ["harness", "spillway", "llmkit", "harnesskit", "dotfiles"]
EARLIER = ["flyer-layout-generator", "API Tooling", "Go Hydrate", "Captain Capybara"]

# (status pt, status en, desc pt, desc en) by name, from the spec's content table.
TEXT = {
    "harness": ("agentes", "agents", "Meu harness para agentes de código, com meu jeito e meu gosto.", "My own harness for coding agents, built my way."),
    "spillway": ("proxy", "proxy", "Proxy reverso para backends de LLM que respeita rate limits.", "A rate-limit-aware reverse proxy for LLM backends."),
    "llmkit": ("privado", "private", "Roda agentes de código como sessões gerenciadas.", "Runs coding agents as managed sessions."),
    "harnesskit": ("privado", "private", "Blocos em Go para apps que dirigem agentes: skills, ferramentas e MCP.", "Go building blocks for apps that drive coding agents: skills, tools and MCP."),
    "dotfiles": ("sempre", "always", "Neovim, tmux, zsh. Meu ambiente, versionado.", "Neovim, tmux, zsh. My environment, versioned."),
    "flyer-layout-generator": ("algoritmo", "algorithm", "Gera layouts de flyers proceduralmente; escrevi sobre isso em um post.", "Procedurally generates flyer layouts; I wrote a post about it."),
    "API Tooling": ("ferramenta", "tool", "Ferramentas code-first para APIs REST: a API é definida em Go e a documentação sai do código.", "Code-first REST API tooling: the API is defined in Go code and the docs are generated from it."),
    "Go Hydrate": ("go", "go", "Renderiza aplicações React a partir de Go, no estilo do Next.js.", "Renders React applications from Go, Next.js-style."),
    "Captain Capybara": ("jogo", "game", "Jogo de game jam com fases procedurais.", "Game jam game with procedural levels."),
}
PRIVATE = ["llmkit", "harnesskit"]


def test_projects_pages():
    for url, lang, headings in [
        ("/projetos/", 0, ["em andamento", "anteriores"]),
        ("/en/projects/", 1, ["active", "earlier"]),
    ]:
        p = projects(url)
        if not p.groups:
            failures.append(f"{url}: no project groups")
            continue
        got = [g["heading"].strip() for g in p.groups]
        check(got == headings, f"{url}: group headings {got}, want {headings}")
        if len(p.groups) != 2:
            continue
        check([e["name"] for e in p.groups[0]["entries"]] == ACTIVE_PT, f"{url}: active order {[e['name'] for e in p.groups[0]['entries']]}")
        check([e["name"] for e in p.groups[1]["entries"]] == EARLIER, f"{url}: earlier order {[e['name'] for e in p.groups[1]['entries']]}")
        for e in p.entries:
            want = TEXT.get(e["name"])
            if not want:
                continue
            check(e["status"] == want[lang], f"{url}: {e['name']} status {e['status']!r}")
            check(e["desc"] == want[2 + lang], f"{url}: {e['name']} desc {e['desc']!r}")
            if e["name"] in PRIVATE:
                check(e["href"] is None, f"{url}: {e['name']} must not link")
                check(e["private_marked"], f"{url}: {e['name']} is not visibly marked as not linked")
            else:
                check(bool(e["href"]), f"{url}: {e['name']} has no link")
        check(all(e["active"] for e in p.groups[0]["entries"]), f"{url}: active labels not highlighted")
        check(not any(e["active"] for e in p.groups[1]["entries"]), f"{url}: earlier labels highlighted")


def test_projects_pages_are_translations_and_in_sitemap():
    pt = page("/projetos/").replace('"', "")
    en = page("/en/projects/").replace('"', "")
    check(re.search(r"<a href=\S*/en/projects/ hreflang=en", pt) is not None, "/projetos/: no switch to the English page")
    check(re.search(r"<a href=\S*/projetos/ hreflang=pt-br", en) is not None, "/en/projects/: no switch to the Portuguese page")
    for stray in ["/en/en/projects/", "/en/projetos/"]:
        check(not (PUBLIC / stray.strip("/") / "index.html").exists(), f"{stray}: stray Projects page was generated")
    # /sitemap.xml is an index of one sitemap per language.
    for lang, url in [("pt-br", "/projetos/"), ("en", "/en/projects/")]:
        sm = (PUBLIC / lang / "sitemap.xml").read_text(encoding="utf-8")
        check(f"<loc>https://rfbatista.github.io{url}</loc>" in sm, f"{lang} sitemap lacks {url}")


def test_flyer_description_links_to_the_post():
    p = projects("/projetos/")
    flyer = [e for e in p.entries if e["name"] == "flyer-layout-generator"]
    check(bool(flyer) and "/posts/procedure-layout-generation/" in flyer[0]["desc_html"], "flyer description does not link to its post")


def test_nav_links_to_the_projects_page():
    base = "https://rfbatista.github.io"
    want = {
        "pt": (["escritos", "jardim", "projetos", "sobre"], f"{base}/projetos/"),
        "en": (["writing", "garden", "projects", "about"], f"{base}/en/projects/"),
    }
    for url, lang in [("/", "pt"), ("/projetos/", "pt"), ("/en/", "en"), ("/en/projects/", "en")]:
        names, href = want[lang]
        links = nav(url)
        check([l[0] for l in links[:4]] == names, f"{url}: nav is {[l[0] for l in links[:4]]}, want {names}")
        entry = [l for l in links if l[0] == names[2]]
        check(bool(entry) and entry[0][1] == href, f"{url}: nav {names[2]!r} does not link to {href}")
        is_projects_page = url in ("/projetos/", "/en/projects/")
        check(bool(entry) and (entry[0][2] == "page") == is_projects_page, f"{url}: aria-current on the projects link should be {is_projects_page}")


def test_home_pages_show_only_featured_projects():
    featured = ["harness", "spillway", "Go Hydrate", "Captain Capybara"]
    for url, lang, link_text, href in [
        ("/", 0, "todos os projetos →", "https://rfbatista.github.io/projetos/"),
        ("/en/", 1, "all projects →", "https://rfbatista.github.io/en/projects/"),
    ]:
        html = page(url)
        p = projects(url)
        check([e["name"] for e in p.entries] == featured, f"{url}: featured projects {[e['name'] for e in p.entries]}")
        for e in p.entries:
            want = TEXT.get(e["name"])
            if want:
                check(e["desc"] == want[2 + lang] and e["status"] == want[lang], f"{url}: {e['name']} text differs from the Project list")
        m = re.search(r'<p class=more><a href=%s>([^<]*)</a>' % re.escape(href), html.replace('"', ""))
        check(m is not None and m.group(1).strip() == link_text, f"{url}: no {link_text!r} link to {href}")


def test_existing_pages_still_render():
    for url in ["/", "/en/", "/posts/", "/jardim/", "/about/", "/en/about/"]:
        check("<h" in page(url) or url == "/", f"{url}: renders no content")


def all_pages():
    return sorted(PUBLIC.rglob("*.html"))


def font_faces():
    """[(css text of one @font-face, its src urls)] from the site's own stylesheets."""
    faces = []
    for css in (PUBLIC / "css").glob("*.css"):
        for m in re.finditer(r"@font-face\s*\{(.*?)\}", css.read_text(encoding="utf-8"), re.S):
            faces.append((m.group(1), re.findall(r"url\(\s*['\"]?([^)'\"]+)", m.group(1))))
    return faces


LATIN_EXT = "latin-ext"


def font_file(url):
    """The built file a @font-face url points to (relative to css/, or site-absolute)."""
    u = url.split("?")[0]
    return (PUBLIC / "css" / u).resolve() if not u.startswith("/") else PUBLIC / u.lstrip("/")


def test_fonts_are_self_hosted():
    faces = font_faces()
    check(faces, "no @font-face in the site's CSS")
    for body, urls in faces:
        for u in urls:
            check("://" not in u or u.startswith("data:"), f"@font-face source outside the site: {u}")
            check(font_file(u).is_file(), f"@font-face source not in the built site: {u}")
    for f in all_pages():
        html = f.read_text(encoding="utf-8")
        check(not re.search(r"fonts\.(googleapis|gstatic)\.com|use\.typekit|fonts\.bunny", html),
              f"{f.relative_to(PUBLIC)}: references a third-party font host")
    for css in (PUBLIC / "css").glob("*.css"):
        check(not re.search(r"fonts\.(googleapis|gstatic)\.com", css.read_text(encoding="utf-8")),
              f"{css.name}: references a third-party font host")


def test_font_families_and_weights():
    have = set()
    for body, _ in font_faces():
        fam = re.search(r"font-family:\s*['\"]?([^;'\"]+)", body)
        wt = re.search(r"font-weight:\s*([^;]+)", body)
        st = re.search(r"font-style:\s*(\w+)", body)
        if fam and wt:
            have.add((fam.group(1).strip(), wt.group(1).strip(), (st.group(1) if st else "normal")))
    for want in [("Spectral", "400", "normal"), ("Spectral", "400", "italic"), ("Spectral", "600", "normal"),
                 ("Familjen Grotesk", "500", "normal"), ("Familjen Grotesk", "600", "normal")]:
        check(want in have, f"missing @font-face {want}")


def test_latin_budget_and_extended_on_demand():
    latin = 0
    for body, urls in font_faces():
        if "size-adjust" in body or not urls:
            continue
        for u in urls:
            if "local(" in body and not u:
                continue
            if LATIN_EXT in u:
                check("unicode-range" in body, f"Latin Extended face has no unicode-range: {u}")
            else:
                check("unicode-range" in body, f"Latin face has no unicode-range: {u}")
                f = font_file(u)
                if f.is_file():
                    latin += f.stat().st_size
    check(0 < latin <= 120 * 1024, f"Latin-subset WOFF2 total is {latin / 1024:.1f} KB, want 0 < size <= 120 KB")


def test_fallback_faces_have_metric_overrides():
    fb = [b for b, _ in font_faces() if "local(" in b]
    check(len(fb) >= 3, "want tuned local() fallback faces for the Reading and Heading face")
    for b in fb:
        for prop in ("size-adjust", "ascent-override", "descent-override"):
            check(prop in b, f"fallback face lacks {prop}")


def test_reading_face_is_preloaded_on_every_page():
    for f in all_pages():
        if f.name != "index.html" or "sitemap" in str(f):
            continue
        html = f.read_text(encoding="utf-8")
        if "<html" not in html or "http-equiv=refresh" in html.replace('"', ""):
            continue
        check(re.search(r'<link[^>]+rel=["\']?preload["\']?[^>]+spectral-latin-400-normal\.woff2[^>]*>', html)
              and re.search(r'as=["\']?font', html) and "crossorigin" in html,
              f"{f.relative_to(PUBLIC)}: no preload of the Reading face")


def test_font_licences_ship_with_the_fonts():
    for name in ("spectral", "familjen-grotesk"):
        check(any((PUBLIC / "fonts").glob(f"LICENSE-{name}*")), f"no licence file for {name} in fonts/")


def site_css():
    return (PUBLIC / "css" / "site.css").read_text(encoding="utf-8")


def luminance(hex_colour):
    c = [int(hex_colour.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def theme_tokens():
    """{"light": {token: hex}, "dark": {token: hex}} from the :root blocks of site.css."""
    css = site_css()
    out = {}
    light = re.search(r":root\{(.*?)\}", css, re.S).group(1)
    dark = re.search(r":root\[data-theme=dark\]\{(.*?)\}", css, re.S).group(1)
    for name, body in (("light", light), ("dark", dark)):
        out[name] = dict(re.findall(r"--(\w+):(#[0-9a-fA-F]{6})", body))
    return out


def test_faint_text_passes_wcag_aa_in_both_themes():
    for theme, t in theme_tokens().items():
        for bg in ("bg", "wash"):
            ratio = contrast(t["faint"], t[bg])
            check(ratio >= 4.5, f"--faint on --{bg} ({theme}) is {ratio:.2f}:1, want >= 4.5")


def test_mark_and_soft_stay_accessible():
    for theme, t in theme_tokens().items():
        for token in ("soft", "mark", "ink"):
            for bg in ("bg", "wash"):
                ratio = contrast(t[token], t[bg])
                check(ratio >= 4.5, f"--{token} on --{bg} ({theme}) is {ratio:.2f}:1, want >= 4.5")


def test_heading_face_carries_headings_and_metadata():
    css = site_css()
    check("--sans:" in css, "no --sans token for the Heading face")
    for sel in ("h1.title", "h2.sec", "ul.list .d", ".meta", ".top nav"):
        check(re.search(re.escape(sel) + r"\{[^}]*(font-family:var\(--sans\)|font:[^;}]*var\(--sans\))", css),
              f"{sel} is not set in the Heading face")
    check("oldstyle-nums" not in css, "oldstyle-nums is still in site.css")
    check("lining-nums" in css, "no lining-nums on metadata")


def test_hyphenation_only_in_running_text():
    css = site_css()
    check(not re.search(r"(^|\})p\{[^}]*hyphens:auto", css), "bare `p` hyphenates: titles' siblings and the Home intro would split")
    check(re.search(r"article\.prose[^{]*\{[^}]*hyphens:auto", css), "running text in posts does not hyphenate")
    check(not re.search(r"overflow-wrap:anywhere", css), "inline code may still break mid-word (overflow-wrap:anywhere)")
    check(re.search(r"code\{[^}]*hyphens:none", css), "inline code is not protected from hyphenation")


def content_pages():
    """Generated pages that carry the site chrome (not redirects, 404 or the feed)."""
    out = []
    for f in all_pages():
        html = f.read_text(encoding="utf-8")
        if '<header class=top>' in html or '<header class="top">' in html:
            out.append((f, html))
    return out


def test_wordmark_is_in_every_header_and_links_home():
    pages = content_pages()
    check(len(pages) > 50, f"found only {len(pages)} pages with the site header")
    for f, html in pages:
        rel = f.relative_to(PUBLIC)
        m = re.search(r'<header class="?top"?>\s*<a class="?name"? href="?([^" >]+)"?[^>]*>(.*?)</a>', html, re.S)
        if not m:
            failures.append(f"{rel}: no Wordmark link at the start of the header")
            continue
        text = re.sub(r"<[^>]+>", "", m.group(2))
        check(text == "rfbatista", f"{rel}: Wordmark text is {text!r}")
        en = re.search(r'<html lang="?en', html) is not None
        check(m.group(1).rstrip("/").endswith("/en") if en else not m.group(1).rstrip("/").endswith("/en"),
              f"{rel}: Wordmark links to {m.group(1)}, not the home of its language")


def test_browser_title_starts_with_the_brand():
    for f, html in content_pages():
        t = re.search(r"<title>(.*?)</title>", html, re.S)
        check(t and t.group(1).startswith("rfbatista"), f"{f.relative_to(PUBLIC)}: title is {t.group(1) if t else None!r}")


def test_language_links_and_toggle_are_labelled():
    for f, html in content_pages():
        rel = f.relative_to(PUBLIC)
        header = re.search(r"<header class=\"?top\"?>.*?</header>", html, re.S).group(0)
        for tag in re.findall(r"<a [^>]*hreflang=[^>]*>", header):
            check(re.search(r'\blang="?\w', tag), f"{rel}: language link has no lang: {tag}")
            check("aria-label=" in tag, f"{rel}: language link has no accessible name: {tag}")
        btn = re.search(r"<button[^>]*theme-toggle[^>]*>", html)
        check(btn and "aria-pressed=" in btn.group(0), f"{rel}: theme toggle has no aria-pressed")


def test_project_list_markup_is_a_valid_description_list():
    """R10: only dt and dd inside each dl > div; the Status label is a dd, not a stray span."""
    for url in ["/", "/en/", "/projetos/", "/en/projects/"]:
        html = page(url)
        for dl in re.findall(r"<dl class=\"?proj\"?>(.*?)</dl>", html, re.S):
            for group in re.findall(r"<div>(.*?)</div>", dl, re.S):
                rest = re.sub(r"<(dt|dd)[^>]*>.*?</\1>", "", group, flags=re.S).strip()
                check(not rest, f"{url}: stray markup directly inside a dl > div: {rest[:60]}")
                check(re.search(r"<dt\b", group) and re.search(r"<dd[^>]*\bst\b", group), f"{url}: entry lacks dt or Status dd")


def test_link_cue_on_touch_for_list_titles():
    css = site_css()
    check(re.search(r"@media \(hover:none\)\{[^@]*ul\.list \.t a[^@]*dl\.proj dt a|@media \(hover:none\)\{[^@]*dl\.proj dt a[^@]*ul\.list \.t a", css),
          "no visible link cue under (hover:none) for list titles and project names")


def test_home_has_exactly_one_h1():
    for url in ["/", "/en/"]:
        check(len(re.findall(r"<h1[\s>]", page(url))) == 1, f"{url}: Home must have exactly one h1")


def test_home_featured_projects_dl_is_valid_and_private_is_unlinked():
    for url in ["/", "/en/"]:
        html = page(url)
        dls = re.findall(r"<dl class=\"?proj\"?>(.*?)</dl>", html, re.S)
        check(dls, f"{url}: no Featured projects dl")
        for dl in dls:
            for group in re.findall(r"<div>(.*?)</div>", dl, re.S):
                check(re.search(r"<dd[^>]*\bst\b", group), f"{url}: entry lacks Status dd")
                if 'class=priv' in group or 'class="priv"' in group:
                    check("<a " not in re.sub(r"<dd.*", "", group, flags=re.S), f"{url}: Private project is linked")


def test_home_is_scoped_and_intro_not_hyphenated():
    css = site_css()
    m = re.search(r"/\* page: home \*/(.*?)/\* end page: home \*/", css, re.S)
    check(m, "site.css lacks the page: home block")
    if m:
        for sel in re.findall(r"([^{}]+)\{", m.group(1)):
            for part in sel.split(","):
                check(part.strip().startswith(("main.home", "@media")), f"home rule not scoped: {part.strip()}")
        check("hyphens:auto" not in m.group(1), "Home intro must not hyphenate")
    check('class="home' in page("/") or "class=home" in page("/"), "Home main lacks the home class")

def post_pages():
    """Generated post pages (an article.prose under a posts/ path), both languages."""
    out = []
    for f, html in content_pages():
        rel = f.relative_to(PUBLIC).as_posix()
        if re.search(r"(^|/)posts/[^/]+/index\.html$", rel) and re.search(r"<article class=\"?prose", html):
            out.append((rel, html))
    return out


def test_post_title_is_the_only_h1_and_body_headings_are_demoted():
    """R05: exactly one h1 per post page; no markdown heading is an h1."""
    posts = post_pages()
    check(len(posts) >= 8, f"found only {len(posts)} post pages")
    for rel, html in posts:
        check(len(re.findall(r"<h1\b", html)) == 1, f"{rel}: expected exactly one h1")
    html = page("/en/posts/find-replace-neovim/")
    body = re.search(r"<article class=\"?prose.*?</article>", html, re.S).group(0)
    check(not re.search(r"<h1\b", body) and len(re.findall(r"<h2\b", body)) == 5 and not re.search(r"<h3\b", body),
          "the neovim post's four '## Step' headings and its stray '# References' should all be h2, with no skipped level")


def test_post_year_headings_exclude_the_count_from_their_name():
    for url in ["/posts/", "/en/posts/"]:
        html = page(url)
        heads = re.findall(r"<h2>(.*?)</h2>", html, re.S)
        check(heads, f"{url}: no year headings")
        for h in heads:
            name = re.sub(r"<small[^>]*aria-hidden=\"?true\"?[^>]*>.*?</small>", "", h, flags=re.S)
            name = re.sub(r"<[^>]+>", "", name).strip()
            check(re.fullmatch(r"\d{4}", name), f"{url}: year heading name is not just the year: {name!r}")


def test_post_neovim_images_have_alt_text_in_both_languages():
    for url in ["/posts/find-replace-neovim/", "/en/posts/find-replace-neovim/"]:
        imgs = re.findall(r"<img\b[^>]*>", page(url))
        check(len(imgs) == 3, f"{url}: expected 3 images, found {len(imgs)}")
        for tag in imgs:
            m = re.search(r"\balt=(?:\"([^\"]*)\"|([^\s>]+))", tag)
            check(m and (m.group(1) or m.group(2)).strip(), f"{url}: image without alt: {tag[:80]}")


def test_post_code_blocks_are_focusable_and_labelled():
    """R08: every pre scrolls by keyboard and has an accessible name."""
    seen = 0
    for rel, html in post_pages():
        for tag in re.findall(r"<pre\b[^>]*>", html):
            seen += 1
            check(re.search(r"tabindex=\"?0", tag), f"{rel}: pre without tabindex=0: {tag[:60]}")
            check(re.search(r"role=\"?region", tag) and re.search(r"aria-label=", tag), f"{rel}: pre without region label: {tag[:60]}")
    check(seen > 5, f"only {seen} code blocks found")


def test_post_code_blocks_show_an_overflow_cue():
    css = site_css()
    block = css[css.find("/* page: post */"):css.find("/* end page: post */")]
    check(block, "no page: post CSS block")
    check(re.search(r"pre[^{]*\{[^}]*(background[^;]*\blocal\b|mask|box-shadow)", block), "code blocks have no overflow cue")


def test_headings_do_not_skip_levels_in_content_pages():
    """The heading render hook demotes only pages that use "#": no page jumps from h1 to h3."""
    bad = []
    for sub in ("posts", "en/posts", "about", "en/about"):  # garden notes skip levels in their own markdown
        for f in (PUBLIC / sub).rglob("index.html"):
            html = f.read_text(encoding="utf-8")
            main = re.search(r"<main.*?</main>", html, re.S)
            levels = [int(x) for x in re.findall(r"<h([1-6])[ >]", main.group(0) if main else "")]
            prev = 0
            for lv in levels:
                if lv > prev + 1:
                    bad.append(str(f.relative_to(PUBLIC)))
                    break
                prev = lv
    check(not bad, f"heading levels skip on {len(bad)} pages, first: {bad[:3]}")


TESTS = [
    test_existing_pages_still_render,
    test_projects_pages,
    test_projects_pages_are_translations_and_in_sitemap,
    test_flyer_description_links_to_the_post,
    test_nav_links_to_the_projects_page,
    test_home_pages_show_only_featured_projects,
    test_fonts_are_self_hosted,
    test_font_families_and_weights,
    test_latin_budget_and_extended_on_demand,
    test_fallback_faces_have_metric_overrides,
    test_reading_face_is_preloaded_on_every_page,
    test_font_licences_ship_with_the_fonts,
    test_faint_text_passes_wcag_aa_in_both_themes,
    test_mark_and_soft_stay_accessible,
    test_heading_face_carries_headings_and_metadata,
    test_hyphenation_only_in_running_text,
    test_wordmark_is_in_every_header_and_links_home,
    test_browser_title_starts_with_the_brand,
    test_language_links_and_toggle_are_labelled,
    test_project_list_markup_is_a_valid_description_list,
    test_link_cue_on_touch_for_list_titles,
    test_home_has_exactly_one_h1,
    test_home_featured_projects_dl_is_valid_and_private_is_unlinked,
    test_home_is_scoped_and_intro_not_hyphenated,

    test_post_title_is_the_only_h1_and_body_headings_are_demoted,
    test_post_year_headings_exclude_the_count_from_their_name,
    test_post_neovim_images_have_alt_text_in_both_languages,
    test_post_code_blocks_are_focusable_and_labelled,
    test_post_code_blocks_show_an_overflow_cue,
    test_headings_do_not_skip_levels_in_content_pages,
]

for t in TESTS:
    t()

if failures:
    print("check: FAILED", file=sys.stderr)
    for f in failures:
        print(f"  - {f}", file=sys.stderr)
    sys.exit(1)
print(f"check: {len(TESTS)} checks passed")
