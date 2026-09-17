// Minimal service worker: makes the site installable (enables the Android share target).
// Intentionally network-only so users never see a stale page.
self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));
self.addEventListener("fetch", () => {});
