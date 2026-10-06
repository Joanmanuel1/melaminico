(function () {
  'use strict';
  try {
    var root = document.getElementById("__P__-root");
    if (!root || root.dataset.fitInit) return;
    root.dataset.fitInit = "1";

    var fit = function () {
      var sbw = Math.max(0, window.innerWidth - document.documentElement.clientWidth);
      root.style.setProperty("--__P__-sbw", sbw + "px");
    };
    fit();

    if ("ResizeObserver" in window) {
      new ResizeObserver(fit).observe(document.documentElement);
    } else {
      window.addEventListener("resize", fit, { passive: true });
    }
  } catch (e) {}
})();
