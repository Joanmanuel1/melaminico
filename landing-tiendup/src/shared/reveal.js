(function () {
  'use strict';
  try {
  var root = document.getElementById("__P__-root");
  if (!root || root.dataset.motionInit) return;
  root.dataset.motionInit = "1";

  var els = root.querySelectorAll(".__P__-reveal");
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduce || !("IntersectionObserver" in window)) return;

  root.classList.add("__P__-js");

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add("__P__-is-visible");
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });

  els.forEach(function (el) { io.observe(el); });

  setTimeout(function () {
    els.forEach(function (el) { el.classList.add("__P__-is-visible"); });
  }, 4000);
  } catch (e) {}
})();
