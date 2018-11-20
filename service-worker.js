var CACHE_VERSION = 2.1;
var CACHE_NAME = 'daniel-jianoran-v' + CACHE_VERSION;

// Listen for install event, set callback
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll([
                '/chip8.data',
                '/chip8.js',
                '/chip8.wasm',
                '/index.html',
                '/manifest.json',
                '/images/icons/icon-72x72.png',
                '/images/icons/icon-96x96.png',
                '/images/icons/icon-128x128.png',
                '/images/icons/icon-144x144.png',
                '/images/icons/icon-152x152.png',
                '/images/icons/icon-192x192.png',
                '/images/icons/icon-384x384.png',
                '/images/icons/icon-512x512.png',
            ]);
        })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request).then(function(response) {
            return response || caches.match("/index.html");
        })
    );
});

self.addEventListener('activate', function(event) {
    // Active worker won't be treated as activated until promise
    // resolves successfully.
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
        return Promise.all(
            cacheNames.map(function(cacheName) {
            if (CACHE_NAME !== cacheName) {
                console.log('Deleting out of date cache:', cacheName);
                
                return caches.delete(cacheName);
            }
            })
        );
        })
    );
});
