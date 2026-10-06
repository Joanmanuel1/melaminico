(function () {
  'use strict';
  try {
  var root = document.getElementById("__P__-root");
  if (!root || root.dataset.videoInit) return;
  root.dataset.videoInit = "1";

  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var yt = root.querySelector("iframe");
  if (yt && reduce) {
    yt.parentNode.removeChild(yt);
    return;
  }

  var video = root.querySelector("video");
  if (!video) return;

  if (reduce) {
    video.removeAttribute("autoplay");
    video.pause();
    return;
  }
  if (!("IntersectionObserver" in window)) return;

  new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        var p = video.play();
        if (p && p.catch) p.catch(function () {});
      } else {
        video.pause();
      }
    });
  }, { threshold: 0.2 }).observe(video);
  } catch (e) {}
})();
