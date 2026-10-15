const CACHE = "kelime-kampi-db9caf096f";
const CORE = ["./", "./index.html", "./manifest.webmanifest", "./icon.svg"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("notificationclick", e => {
  e.notification.close();
  e.waitUntil(clients.matchAll({ type: "window", includeUncontrolled: true }).then(list => {
    const hit = list.find(c => "focus" in c);
    if (hit) return hit.focus();
    if (clients.openWindow) return clients.openWindow("./index.html");
  }));
});
const put = (req, res) => { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)).catch(() => {}); return res; };
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  // the page itself: network first so a new build shows up right away; cache when offline
  if (req.mode === "navigate" || req.url.endsWith("/index.html")) {
    e.respondWith(fetch(req).then(res => res.ok ? put(req, res) : res).catch(() => caches.match(req).then(hit => hit || caches.match("./index.html"))));
    return;
  }
  // everything else (manifest, icon): cache first
  e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => res.ok ? put(req, res) : res)));
});
