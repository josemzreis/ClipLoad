import os
import time
from collections import defaultdict, deque
from datetime import date

from fastapi import FastAPI, HTTPException, Request
from fastapi.concurrency import run_in_threadpool
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, PlainTextResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.gzip import GZipMiddleware

from . import config, content, downloader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")
BUILD_DATE = date.today().isoformat()

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
templates.env.globals.update(
    cfg=config,
    platforms=content.PLATFORMS,
    has_og_image=os.path.exists(os.path.join(STATIC_DIR, "og.png")),
)
templates.env.filters["site"] = lambda s: _fill(s)


@app.middleware("http")
async def headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "public, max-age=604800"
    return response


# --- Rate limiting (per process; put Cloudflare in front for real protection) ---
_hits: dict = defaultdict(deque)


def _client_ip(request: Request) -> str:
    if config.TRUST_PROXY_HEADERS:
        forwarded = request.headers.get("cf-connecting-ip") or request.headers.get("x-forwarded-for", "")
        if forwarded:
            return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _rate_limit(request: Request) -> None:
    now = time.monotonic()
    window = _hits[_client_ip(request)]
    while window and now - window[0] > 60:
        window.popleft()
    if len(window) >= config.RATE_LIMIT_PER_MINUTE:
        raise HTTPException(429, "Too many requests. Please wait a minute and try again.")
    window.append(now)


# --- Pages ---
def _fill(text: str) -> str:
    return text.replace("{site}", config.SITE_NAME).replace("{email}", config.CONTACT_EMAIL)


def _schema(page: dict, canonical: str) -> dict:
    """JSON-LD: WebApplication (+ free Offer), FAQPage and BreadcrumbList for rich results."""
    graph = [
        {
            "@type": "WebApplication",
            "name": config.SITE_NAME if not page["slug"] else f"{config.SITE_NAME} {page['name']} Downloader",
            "url": canonical,
            "description": _fill(page["description"]),
            "applicationCategory": "MultimediaApplication",
            "operatingSystem": "Any",
            "browserRequirements": "Requires JavaScript",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        },
        {
            "@type": "FAQPage",
            "mainEntity": [
                {"@type": "Question", "name": _fill(q), "acceptedAnswer": {"@type": "Answer", "text": _fill(a)}}
                for q, a in page["faqs"]
            ],
        },
    ]
    if page["slug"]:
        graph.append({
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{config.SITE_URL}/"},
                {"@type": "ListItem", "position": 2, "name": page["name"], "item": canonical},
            ],
        })
    return {"@context": "https://schema.org", "@graph": graph}


def _page(request: Request, page: dict, status_code: int = 200):
    shared = request.query_params.get("url") or request.query_params.get("text") or ""
    canonical = f"{config.SITE_URL}/{page['slug']}"
    return templates.TemplateResponse(
        request,
        "tool.html",
        {"page": page, "prefill": downloader.find_url(shared) or "", "canonical": canonical,
         "schema": _schema(page, canonical)},
        status_code=status_code,
    )


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return _page(request, content.HOME)


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    return f"User-agent: *\nDisallow: /api/\nAllow: /\n\nSitemap: {config.SITE_URL}/sitemap.xml\n"


@app.get("/sitemap.xml")
async def sitemap():
    paths = [""] + [p["slug"] for p in content.PLATFORMS] + list(content.LEGAL)
    urls = "".join(
        f"<url><loc>{config.SITE_URL}/{p}</loc><lastmod>{BUILD_DATE}</lastmod></url>" for p in paths
    )
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(xml, media_type="application/xml")


@app.get("/ads.txt", response_class=PlainTextResponse)
async def ads_txt():
    if not config.ADSENSE_CLIENT:
        raise HTTPException(404)
    pub = config.ADSENSE_CLIENT.replace("ca-", "")
    return f"google.com, {pub}, DIRECT, f08c47fec0942fa0\n"


@app.get("/manifest.webmanifest")
async def manifest():
    return JSONResponse(
        {
            "name": f"{config.SITE_NAME} – Video Downloader",
            "short_name": config.SITE_NAME,
            "start_url": "/",
            "display": "standalone",
            "background_color": "#ffffff",
            "theme_color": "#5b4bff",
            "icons": [{"src": "/static/icon.svg", "sizes": "any", "type": "image/svg+xml", "purpose": "any maskable"}],
            # Android: "Share" a video from TikTok/YouTube straight into the installed app.
            "share_target": {"action": "/", "method": "GET", "params": {"title": "title", "text": "text", "url": "url"}},
        },
        media_type="application/manifest+json",
    )


@app.get("/sw.js")
async def service_worker():
    return FileResponse(os.path.join(STATIC_DIR, "sw.js"), media_type="application/javascript",
                        headers={"Cache-Control": "no-cache"})


@app.get("/{slug}", response_class=HTMLResponse)
async def landing(request: Request, slug: str):
    if slug in content.PLATFORMS_BY_SLUG:
        return _page(request, content.PLATFORMS_BY_SLUG[slug])
    if slug in content.LEGAL:
        return templates.TemplateResponse(
            request, "legal.html",
            {"doc": content.LEGAL[slug], "canonical": f"{config.SITE_URL}/{slug}"},
        )
    raise HTTPException(404)


# --- API ---
class ProbeIn(BaseModel):
    url: str


class JobIn(BaseModel):
    url: str
    quality: str = "best"


@app.post("/api/probe")
async def api_probe(body: ProbeIn, request: Request):
    _rate_limit(request)
    try:
        return await run_in_threadpool(downloader.probe, body.url)
    except downloader.DownloadError as exc:
        raise HTTPException(400, str(exc))


@app.post("/api/jobs")
async def api_create_job(body: JobIn, request: Request):
    _rate_limit(request)
    try:
        job = await run_in_threadpool(downloader.create_job, body.url, body.quality)
    except downloader.DownloadError as exc:
        raise HTTPException(400, str(exc))
    return job.public()


@app.get("/api/jobs/{job_id}")
async def api_job_status(job_id: str):
    job = downloader.get_job(job_id)
    if not job:
        raise HTTPException(404, "This download has expired. Please paste the link again.")
    return job.public()


@app.get("/api/jobs/{job_id}/file")
async def api_job_file(job_id: str):
    job = downloader.get_job(job_id)
    if not job or job.status != "ready" or not job.path or not os.path.exists(job.path):
        raise HTTPException(404, "This download has expired. Please paste the link again.")
    return FileResponse(job.path, filename=job.filename, headers={"Cache-Control": "no-store"})


@app.exception_handler(StarletteHTTPException)
async def http_error(request: Request, exc: StarletteHTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)
    if exc.status_code == 404:
        return templates.TemplateResponse(request, "404.html", {"canonical": config.SITE_URL}, status_code=404)
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)
