'use strict';
const viewer = document.querySelector('#image-viewer');
const gallery = document.querySelector('.posters');
const locale = document.body.dataset.locale;
let lastPoster;
for (const button of document.querySelectorAll('[data-device]')) {
  if (button.tagName !== 'BUTTON') continue;
  button.addEventListener('click', () => {
    const device = button.dataset.device;
    for (const control of document.querySelectorAll('button[data-device]')) control.setAttribute('aria-pressed', String(control === button));
    gallery.dataset.device = device;
    for (const poster of gallery.querySelectorAll('.poster')) {
      const img = poster.querySelector('img');
      const url = `/assets/screens/${locale}/${device}/${poster.dataset.key}.webp`;
      poster.href = url;
      img.src = url;
      img.width = device === 'ipad' ? 800 : 660;
      img.height = device === 'ipad' ? 1067 : 1434;
      img.alt = img.alt.replace(/iPhone|iPad/g, device === 'ipad' ? 'iPad' : 'iPhone');
    }
  });
}
for (const poster of document.querySelectorAll('.poster')) {
  poster.addEventListener('click', event => {
    if (event.ctrlKey || event.metaKey || event.shiftKey || !viewer.showModal) return;
    event.preventDefault();
    lastPoster = poster;
    const image = viewer.querySelector('img');
    image.src = poster.href;
    image.alt = poster.querySelector('img').alt;
    viewer.showModal();
  });
}
viewer.querySelector('button').addEventListener('click', () => viewer.close());
viewer.addEventListener('click', event => { if (event.target === viewer) viewer.close(); });
viewer.addEventListener('close', () => lastPoster?.focus());
