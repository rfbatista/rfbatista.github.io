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
                         "active": False, "desc": "", "desc_html": "", "meta": ""}
            self.entries.append(self._cur)
            if self.groups:
                self.groups[-1]["entries"].append(self._cur)
            self._in = "name"
        elif self._cur and tag == "a" and self._in == "name":
            self._cur["href"] = a.get("href")
            self._cur["ext"] = "ext" in cls
        elif self._cur and tag == "span" and "st" in cls:
            self._cur["active"] = "on" in cls
            self._in = "status"
        elif self._cur and tag == "span" and "meta" in cls:
            self._in = "meta"
        elif self._cur and tag == "dd":
            self._in = "desc"
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
        elif tag in ("span", "dd") and self._in in ("status", "meta", "desc"):
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
            else:
                check(bool(e["href"]), f"{url}: {e['name']} has no link")
        check(all(e["active"] for e in p.groups[0]["entries"]), f"{url}: active labels not highlighted")
        check(not any(e["active"] for e in p.groups[1]["entries"]), f"{url}: earlier labels highlighted")


def test_projects_pages_are_translations_and_in_sitemap():
    pt = page("/projetos/").replace('"', "")
    en = page("/en/projects/").replace('"', "")
    check(re.search(r"<a href=\S*/en/projects/ hreflang=en", pt) is not None, "/projetos/: no switch to the English page")
    check(re.search(r"<a href=\S*/projetos/ hreflang=pt-br", en) is not None, "/en/projects/: no switch to the Portuguese page")
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


TESTS = [
    test_existing_pages_still_render,
    test_projects_pages,
    test_projects_pages_are_translations_and_in_sitemap,
    test_flyer_description_links_to_the_post,
    test_nav_links_to_the_projects_page,
    test_home_pages_show_only_featured_projects,
]

for t in TESTS:
    t()

if failures:
    print("check: FAILED", file=sys.stderr)
    for f in failures:
        print(f"  - {f}", file=sys.stderr)
    sys.exit(1)
print(f"check: {len(TESTS)} checks passed")
