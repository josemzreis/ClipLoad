# Architecture

## Design goals and how the architecture serves them

| Goal | Decision |
|---|---|
| Rank in search | Server-rendered HTML (Jinja), with one indexable URL per platform keyword and no client-side framework. Content is visible to crawlers without JavaScript. |
| Fast pages (Core Web Vitals) | No framework and no web fonts. About 8 KB of CSS and 6 KB of JS, gzip, and a long cache on static files. Ads load only after the first interaction or 3.5 s, and ad slots reserve their height, so the layout doesn't shift (CLS ≈ 0). |
| "Paste → download, no extra steps" | Pasting runs the analysis automatically. The primary button is always "best quality MP4". The file arrives via `Content-Disposition: attachment`, so the page stays open. |
| Mobile users (most of this traffic) | Mobile-first layout, a clipboard "Paste" button, and a PWA share target: on Android, *Share → ClipLoad* in the TikTok or YouTube app opens the site with the link and starts automatically. |
| Monetization | Three ad slots: top, **result** (shown while the file is being prepared, which is the highest-viewability moment) and bottom. They render only when `ADSENSE_CLIENT` is set. `ads.txt` is generated automatically. |
| Cheap to run | A single Python process with yt-dlp and ffmpeg. Files are temporary and deleted after 15 minutes. There's no database. |

## Request flow

```
Browser                         FastAPI (app/main.py)                yt-dlp + ffmpeg
───────                         ─────────────────────                ───────────────
paste link ──POST /api/probe──▶ rate-limit, SSRF check ────────────▶ extract_info (no download)
           ◀── title, thumb, qualities ─┘
click MP4  ──POST /api/jobs───▶ enqueue Job (thread pool) ─────────▶ download best streams,
           ◀── job id                                                merge → MP4 / MP3
poll       ──GET /api/jobs/id─▶ status + progress %
ready      ──GET /api/jobs/id/file──▶ FileResponse (attachment) ─── sweeper deletes after TTL
```

Why use a job and polling instead of streaming the download directly?

1. High-quality YouTube, Reddit and Twitch VOD downloads need two streams merged by ffmpeg. That can't reliably be piped as one HTTP response while also reporting progress.
2. Direct CDN links are often IP-locked to the server, so they can't simply be handed to the browser.
3. The waiting time becomes a visible progress screen, which is a good place for an ad slot.

## Files

```
app/
  main.py        routes: pages, API, sitemap, robots, ads.txt, manifest
  downloader.py  yt-dlp wrapper, URL safety checks, job queue, cleanup sweeper
  content.py     SEO copy for every landing page and the legal pages  ← add pages here
  config.py      environment variables
  templates/     base, tool (every landing page), legal, 404, ad macro
  static/        css, js, icon, service worker
```

Adding a new platform page means adding one dict to `PLATFORMS` in `content.py`. It then shows up automatically in the sitemap, footer links, internal link grid and JSON-LD.

## Quality and watermark rules (downloader.py)

- Video: `bv*[no watermark]+ba / b[no watermark] / bv*+ba / b`, sorted by resolution (capped when the user picks one), then H.264/AAC/MP4 for playback compatibility. The output is merged to MP4.
- Audio: best audio stream → MP3 at 192 kbps.
- Formats whose `format_note` contains "watermark" are skipped whenever an alternative exists.

## Security and abuse controls

- **SSRF:** the hostname is resolved and non-public IPs are rejected before yt-dlp's generic extractor can fetch internal addresses.
- Per-IP rate limit (20 requests/min), a cap on queued jobs, and limits on duration (3 h) and file size (2 GB).
- Playlists and live streams are rejected. Error messages are user-friendly and never leak internals.
- API docs are disabled, and `/api/` is disallowed in robots.txt.

## Scaling path

The job registry lives in memory, so **run one worker per host**. In order of need:

1. **Cloudflare** in front: TLS, static caching, WAF and bot rules. Turnstile can be added to `/api/jobs` if bots abuse it.
2. **Vertical scaling:** bandwidth and CPU for ffmpeg merges are the real costs. Choose a host with generous egress (Hetzner or OVH rather than AWS or GCP).
3. **Horizontal scaling:** move job state to Redis and file storage to local disk plus sticky routing (or R2/S3 with signed URLs), then run N identical hosts behind a load balancer.
4. **Split roles:** web and SEO pages (could become static on a CDN) vs. download workers.

## Operational risks (read this)

- **YouTube blocks datacenter IPs** ("Sign in to confirm you're not a bot"). This is the #1 source of breakage. Mitigations: keep yt-dlp updated, install Deno (already in the Dockerfile), and use residential or rotating proxies via `YTDLP_PROXY`. A cookies file is possible (`YTDLP_COOKIES_FILE`), but only use a throwaway account.
- **Instagram and Facebook** increasingly require login. Expect lower success rates there.
- **Platform changes** break extractors regularly. Rebuild the Docker image weekly (or run `pip install -U yt-dlp` on a schedule) and monitor error rates per platform.
