// KhetSathi 360 — Offline Field Service Worker (PWA)
// Enables zero-connectivity field operations for Indian farmers

const CACHE_NAME = 'khetsathi-v2.0';
const STATIC_ASSETS = [
  '/',
  '/ui',
  '/manifest.json',
  '/legacy',
  'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700;800&display=swap'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[KhetSathi SW] Pre-caching static assets for v2.0');
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('[KhetSathi SW] Pre-cache non-fatal error:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[KhetSathi SW] Evicting stale cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // For API calls: Network-first with cache fallback
  if (url.pathname.startsWith('/api/v1/')) {
    event.respondWith(
      fetch(req)
        .then((response) => {
          if (response && response.status === 200) {
            const respClone = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(req, respClone);
            });
          }
          return response;
        })
        .catch(async () => {
          const cached = await caches.match(req);
          if (cached) {
            console.log('[KhetSathi SW] Serving cached API response for:', url.pathname);
            return cached;
          }
          // Return offline fallback JSON
          return new Response(
            JSON.stringify({
              offline: true,
              message: 'इंटरनेट कनेक्शन उपलब्ध नहीं है। ऑफलाइन मोड सक्रिय है।',
              note: 'Using stored agronomic models and district baselines.'
            }),
            {
              status: 200,
              headers: { 'Content-Type': 'application/json' }
            }
          );
        })
    );
    return;
  }

  // For HTML & static assets: Stale-while-revalidate / Cache-first
  event.respondWith(
    caches.match(req).then((cached) => {
      const fetchPromise = fetch(req)
        .then((networkResp) => {
          if (networkResp && networkResp.status === 200) {
            const respClone = networkResp.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, respClone));
          }
          return networkResp;
        })
        .catch(() => cached);

      return cached || fetchPromise;
    })
  );
});
