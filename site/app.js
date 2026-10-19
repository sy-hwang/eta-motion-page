"use strict";

const config = window.ETA_CONFIG || {};
for (const [id, key] of [["paper-link", "paperUrl"], ["code-link", "codeUrl"], ["supplement-link", "supplementUrl"]]) {
  const link = document.getElementById(id);
  if (!config[key]) continue;
  try {
    const url = new URL(config[key], document.baseURI);
    if (!["http:", "https:", "file:"].includes(url.protocol)) continue;
    link.href = config[key];
    link.hidden = false;
    link.removeAttribute("aria-disabled");
    link.querySelector(".coming-soon")?.remove();
    link.target = "_blank";
    link.rel = "noopener noreferrer";
  } catch { /* Keep unavailable resources in their initial state. */ }
}
if (config.venue) {
  const venue = document.getElementById("venue");
  venue.textContent = config.venue;
  venue.hidden = false;
}
if (config.bibtex) document.getElementById("bibtex").textContent = config.bibtex;
if (config.siteUrl) {
  try {
    const url = new URL(config.siteUrl);
    if (["https:", "http:"].includes(url.protocol)) {
      if (!url.pathname.endsWith("/")) url.pathname += "/";
      const canonical = document.createElement("link");
      canonical.rel = "canonical";
      canonical.href = url.href;
      document.head.append(canonical);
      document.querySelector('meta[property="og:image"]').content = new URL("assets/images/teaser.webp", url).href;
    }
  } catch { /* A local preview does not require a canonical URL. */ }
}

const copyButton = document.getElementById("copy-citation");
let copyTimer;
copyButton.addEventListener("click", async () => {
  const status = document.getElementById("copy-status");
  const citation = document.getElementById("bibtex");
  try {
    if (!navigator.clipboard?.writeText) throw new Error("Clipboard unavailable");
    await navigator.clipboard.writeText(citation.textContent);
    copyButton.textContent = "Copied!";
    status.textContent = "Citation copied to clipboard.";
  } catch {
    const range = document.createRange();
    range.selectNodeContents(citation);
    const selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);
    status.textContent = "Citation selected. Press Ctrl+C (or ⌘C) to copy.";
  }
  clearTimeout(copyTimer);
  copyTimer = setTimeout(() => { copyButton.textContent = "Copy citation"; }, 2500);
});
