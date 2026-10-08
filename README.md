# ClipLoad: paste a link, get the video

A minimal, SEO-first video downloader powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp). It supports the sites handled by yt-dlp's extractors, including TikTok, YouTube, Twitch, Instagram, X, Reddit and Facebook, plus eligible generic video URLs. Not every app, link, or protected video is supported.

- **One step:** paste a link and it's analyzed right away. One click downloads the best quality.
- **Authorized use:** download only content you own or have permission to use, and follow the source platform's terms.
- **High quality:** the best video and audio streams are merged into a compatible MP4 (up to 4K), or saved as MP3.
- **Built for reach:** server-rendered landing pages per platform, JSON-LD, sitemap, a PWA share target, and ad slots that don't hurt Core Web Vitals.
- **Safe filenames:** downloaded names are normalized to portable ASCII filenames, independently of the title used for the temporary download file.

## Run locally

Requires Python 3.11+ (yt-dlp has deprecated 3.10) and `ffmpeg` on your PATH. [Deno](https://deno.com) is recommended for YouTube.

```bash
python -m venv .venv
.venv/Scripts/activate        # Windows  (macOS/Linux: source .venv/bin/activate)
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://localhost:8000.

## Deploy

The current Docker runtime is the production deployment target. It should not be deployed directly as a Vercel serverless function because downloads rely on `ffmpeg`, an in-memory queue, and temporary files that must survive polling requests. See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the recommended host layout, the future Vercel split, and the ads checklist.

```bash
docker build -t clipload .
docker run -p 8000:8000 --env-file .env clipload
```

Put Cloudflare in front of the server for DNS, TLS, caching of static assets, and bot and abuse protection. Rebuild the image **weekly** so yt-dlp stays current.

### Supported sources

yt-dlp ships extractors for many services and also has a generic extractor, but support is not universal. A platform can block server downloads, require login/cookies, or change without notice. Check the current [yt-dlp supported sites list](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) and test representative links you are authorized to download after deployment.

## Docs

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md): how it works, scaling, and operational risks
- [docs/SEO_STRATEGY.md](docs/SEO_STRATEGY.md): go-to-market, SEO and monetization plan
