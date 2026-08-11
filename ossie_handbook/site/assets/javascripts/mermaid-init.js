// Mermaid browser runtime — initializes on DOMContentLoaded, picks theme based
// on the user's color-scheme preference. Loaded after mermaid.min.js via
// `extra_javascript` in mkdocs.yml.
//
// Note: as of Mermaid 10, labels containing parentheses (e.g. `N·(N-1)`) must
// be wrapped in double quotes, or the parser raises "Syntax error in text".
// Keep the 41 <pre class="mermaid"> blocks in src/ consistent with this rule.
(function () {
  function renderAll() {
    if (typeof mermaid === "undefined") return;
    var dark =
      window.matchMedia &&
      window.matchMedia("(prefers-color-scheme: dark)").matches;
    mermaid.initialize({
      startOnLoad: true,
      theme: dark ? "dark" : "default",
      securityLevel: "loose",
      flowchart: { useMaxWidth: true, htmlLabels: true }
    });
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderAll);
  } else {
    renderAll();
  }
})();
