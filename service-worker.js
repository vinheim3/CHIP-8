var CACHE_VERSION = 2;
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
                '/manifest.json'
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
