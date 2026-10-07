// Hover previews for internal links: fetch the target page, show title, meta and first paragraph.
(function () {
  if (!window.matchMedia("(hover: hover)").matches) return;
  var pop = document.getElementById("pop");
  if (!pop) return;
  var cache = {}, timer, current = null;

  function summarize(html) {
    var doc = new DOMParser().parseFromString(html, "text/html");
    var title = doc.querySelector("h1.title");
    if (!title) return null;
    var meta = doc.querySelector(".meta");
    var body = doc.querySelector(".desc") || doc.querySelector(".prose > p");
    var text = body ? body.textContent.trim() : "";
    if (text.length > 220) text = text.slice(0, 220).replace(/\s+\S*$/, "") + "…";
    var out = document.createDocumentFragment();
    if (meta) { var i = document.createElement("i"); i.textContent = meta.textContent.replace(/\s+/g, " ").trim(); out.appendChild(i); }
    var b = document.createElement("b"); b.textContent = title.textContent.trim(); out.appendChild(b);
    out.appendChild(document.createTextNode(text));
    return out;
  }

  function load(url) {
    if (!cache[url]) {
      cache[url] = fetch(url).then(function (r) { return r.ok ? r.text() : ""; }).catch(function () { return ""; });
    }
    return cache[url];
  }

  function show(a) {
    load(a.href).then(function (html) {
      var content = html && summarize(html);
      if (!content || current !== a) return;
      pop.replaceChildren(content);
      var r = a.getBoundingClientRect();
      pop.style.left = Math.max(12, Math.min(r.left + scrollX, innerWidth - pop.offsetWidth - 12)) + "px";
      pop.style.top = (r.bottom + scrollY + 8) + "px";
      pop.classList.add("on");
    });
  }

  document.querySelectorAll("main a[href]").forEach(function (a) {
    var u = new URL(a.href, location.href);
    if (u.origin !== location.origin || u.pathname === location.pathname || a.closest(".top")) return;
    if (/\.(xml|png|jpe?g|gif|pdf)$/i.test(u.pathname)) return;
    a.addEventListener("mouseenter", function () { current = a; clearTimeout(timer); timer = setTimeout(function () { show(a); }, 300); });
    a.addEventListener("mouseleave", function () { current = null; clearTimeout(timer); pop.classList.remove("on"); });
  });
})();
