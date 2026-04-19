self.addEventListener('fetch', event => {
  if (event.request.url.includes('lotto_recent_year.json')) {
    event.respondWith(fetch(event.request)); // 항상 최신
    return;
  }

  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request);
    })
  );
});
