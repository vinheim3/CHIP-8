// Listen for install event, set callback
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open('daniel-jianoran-v1').then(function(cache) {
            return cache.addAll([
                '/chip8.data',
                '/chip8.js',
                '/chip8.wasm',
                '/index.html'
            ]);
        })
    );
});