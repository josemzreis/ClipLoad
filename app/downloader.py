"""yt-dlp wrapper: URL safety checks, metadata probing and a small in-memory job queue.

Jobs live in process memory, so run a single app worker per host (see docs/ARCHITECTURE.md).
"""
import ipaddress
import logging
import os
import re
import shutil
import socket
import tempfile
import threading
import time
import unicodedata
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Optional
from urllib.parse import urlparse

import yt_dlp

from . import config

logger = logging.getLogger(__name__)


class DownloadError(Exception):
    """Error whose message is safe to show to end users."""


QUALITIES = ("best", "2160", "1440", "1080", "720", "480", "360", "mp3")
_URL_RE = re.compile(r"https?://[^\s<>\"']+")
_VIDEO_EXTENSIONS = {
    "3gp", "avi", "f4v", "flv", "m2ts", "m4v", "mkv", "mov", "mp4", "mpeg", "mpg",
    "m3u8", "mpd", "mts", "ogv", "ts", "vob", "webm", "wmv",
}
_AUDIO_EXTENSIONS = {"aac", "aiff", "au", "flac", "m4a", "mid", "mp3", "ogg", "opus", "wav", "weba", "wma"}

# TikTok (and a few others) expose a watermarked "download" format; never pick it when an alternative exists.
_NO_WATERMARK = "[format_note!*=?watermark]"


def find_url(text: str) -> Optional[str]:
    """Pull the first http(s) link out of arbitrary pasted/shared text."""
    match = _URL_RE.search(text or "")
    return match.group(0).rstrip(").,;!") if match else None


def validate_url(url: str) -> str:
    url = find_url(url)
    if not url or len(url) > 2048:
        raise DownloadError("Please paste a valid link.")
    host = urlparse(url).hostname
    if not host:
        raise DownloadError("Please paste a valid link.")
    try:
        addresses = {info[4][0] for info in socket.getaddrinfo(host, None)}
    except socket.gaierror:
        raise DownloadError("We couldn't reach that website. Check the link and try again.")
    for address in addresses:
        # Block SSRF into private networks via yt-dlp's generic extractor.
        if not ipaddress.ip_address(address.split("%")[0]).is_global:
            raise DownloadError("That link isn't supported.")
    return url


def _base_opts() -> dict:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 20,
        "retries": 3,
        "cachedir": False,
        "restrictfilenames": True,
    }
    if config.COOKIES_FILE:
        opts["cookiefile"] = config.COOKIES_FILE
    if config.PROXY:
        opts["proxy"] = config.PROXY
    return opts


def _friendly(message: str) -> str:
    m = message.lower()
    if "unsupported url" in m:
        return "This website isn't supported yet."
    if "ip address is blocked" in m or "not a bot" in m or "rate-limit" in m or "429" in m:
        return "This platform is temporarily limiting our servers. Please try again in a few minutes."
    if "private" in m or "login" in m or "sign in" in m or "cookies" in m:
        return "This content is private or requires a login, so it can't be downloaded."
    if "copyright" in m or "removed" in m or "unavailable" in m or "not available" in m:
        return "This content is unavailable. It may have been removed or restricted in some regions."
    if "max_filesize" in m or "larger than max" in m:
        return f"This file is larger than our {config.MAX_FILESIZE_MB} MB limit."
    return "We couldn't process this link. Please try again in a moment."


def _extract(url: str) -> dict:
    try:
        with yt_dlp.YoutubeDL(_base_opts()) as ydl:
            info = ydl.extract_info(url, download=False)
    except yt_dlp.utils.DownloadError as exc:
        raise DownloadError(_friendly(str(exc)))
    return _check(info)


def _check(info: dict) -> dict:
    if info.get("_type") in ("playlist", "multi_video"):
        entries = [e for e in info.get("entries") or [] if e]
        if not entries:
            raise DownloadError("Playlists aren't supported. Paste the link of a single video.")
        info = entries[0]
    if info.get("is_live") or info.get("live_status") == "is_live":
        raise DownloadError("Live streams can't be downloaded while they're live. Try again after the stream ends.")
    duration = info.get("duration") or 0
    if duration > config.MAX_DURATION:
        raise DownloadError(f"This video is too long (limit: {config.MAX_DURATION // 3600} hours).")
    return info


def _has_video(info: dict) -> bool:
    formats = info.get("formats") or []
    video_formats = [
        f for f in formats
        if f.get("vcodec") not in (None, "", "none") or f.get("height") or f.get("width")
    ]
    if video_formats or info.get("vcodec") not in (None, "", "none"):
        return True
    ext = (info.get("ext") or "").lower()
    if ext in _VIDEO_EXTENSIONS:
        return True
    return not formats and ext not in _AUDIO_EXTENSIONS


def probe(url: str) -> dict:
    """Return public metadata and the quality options available for a link."""
    url = validate_url(url)
    info = _extract(url)
    formats = info.get("formats") or []
    # "1080p" means the shorter side, like yt-dlp's `res` sort (a 1080x1920 Short is 1080p).
    video_formats = [f for f in formats if f.get("vcodec") not in (None, "", "none") or f.get("height") or f.get("width")]
    resolutions = {
        min(f["width"], f["height"]) if f.get("width") else f["height"]
        for f in video_formats
        if f.get("height")
    }
    has_video = _has_video(info)
    top = max(resolutions) if resolutions else 0
    qualities = [q for q in ("2160", "1440", "1080", "720", "480", "360") if int(q) <= top]
    return {
        "url": url,
        "title": info.get("title") or "Untitled",
        "thumbnail": info.get("thumbnail"),
        "duration": info.get("duration"),
        "uploader": info.get("uploader") or info.get("channel"),
        "platform": info.get("extractor_key") or info.get("extractor"),
        "max_res": top or None,
        "qualities": qualities[:4],
        "has_video": has_video,
    }


def _format_opts(quality: str) -> dict:
    if quality == "mp3":
        return {
            "format": "ba/b",
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}],
        }
    # Highest resolution first (capped if requested), then the most compatible codec/container.
    resolution = f"res:{quality}" if quality.isdigit() else "res"
    return {
        "format": f"bv*{_NO_WATERMARK}+ba/b{_NO_WATERMARK}/bv*+ba/b",
        "format_sort": [resolution, "vcodec:h264", "acodec:aac", "ext:mp4:m4a"],
        "merge_output_format": "mp4",
    }


def _safe_filename(title: str, ext: str) -> str:
    name = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip(" .-_").lower()[:100].rstrip(" .-_")
    name = name or "video"
    if name.split(".", 1)[0].upper() in {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{i}" for i in range(1, 10)),
        *(f"LPT{i}" for i in range(1, 10)),
    }:
        name = f"video-{name}"
    safe_ext = ext.lower() if re.fullmatch(r"[A-Za-z0-9]{1,10}", ext) else "mp4"
    return f"{name}.{safe_ext}"


@dataclass
class Job:
    url: str
    quality: str
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    status: str = "queued"  # queued | downloading | processing | ready | error
    progress: float = 0.0
    error: Optional[str] = None
    workdir: Optional[str] = None
    path: Optional[str] = None
    filename: Optional[str] = None
    created: float = field(default_factory=time.time)

    def public(self) -> dict:
        return {"id": self.id, "status": self.status, "progress": round(self.progress, 1), "error": self.error}


_jobs: dict = {}
_lock = threading.Lock()
_executor = ThreadPoolExecutor(max_workers=config.MAX_CONCURRENT_JOBS, thread_name_prefix="dl")


def create_job(url: str, quality: str) -> Job:
    if quality not in QUALITIES:
        raise DownloadError("Unknown quality option.")
    url = validate_url(url)
    with _lock:
        pending = sum(1 for j in _jobs.values() if j.status in ("queued", "downloading", "processing"))
        if pending >= config.MAX_QUEUED_JOBS:
            raise DownloadError("We're very busy right now. Please try again in a minute.")
        job = Job(url=url, quality=quality)
        _jobs[job.id] = job
    _executor.submit(_run, job)
    return job


def get_job(job_id: str) -> Optional[Job]:
    return _jobs.get(job_id)


def _run(job: Job) -> None:
    try:
        job.workdir = tempfile.mkdtemp(dir=config.DOWNLOAD_DIR)
        streams: dict = {}

        def on_progress(d: dict) -> None:
            if d.get("status") != "downloading":
                return
            job.status = "downloading"
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            streams[d.get("filename")] = (d.get("downloaded_bytes") or 0, total)
            done = sum(s[0] for s in streams.values())
            size = sum(s[1] for s in streams.values())
            if size:
                job.progress = max(job.progress, min(95.0, done / size * 95))

        def on_postprocess(d: dict) -> None:
            if d.get("status") == "started":
                job.status = "processing"

        opts = _base_opts()
        opts.update(_format_opts(job.quality))
        opts.update({
            "outtmpl": os.path.join(job.workdir, "%(id).80s.%(ext)s"),
            "progress_hooks": [on_progress],
            "postprocessor_hooks": [on_postprocess],
            "max_filesize": config.MAX_FILESIZE_MB * 1024 * 1024,
        })
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = _check(ydl.extract_info(job.url, download=False))
            info = ydl.process_ie_result(info, download=True)
        files = [
            os.path.join(job.workdir, f) for f in os.listdir(job.workdir)
            if not f.endswith((".part", ".ytdl", ".temp"))
        ]
        if not files:
            raise DownloadError(_friendly("larger than max" if info.get("filesize_approx") else ""))
        job.path = max(files, key=os.path.getsize)
        ext = job.path.rsplit(".", 1)[-1]
        job.filename = _safe_filename(info.get("title") or "video", ext)
        job.progress = 100.0
        job.status = "ready"
    except DownloadError as exc:
        job.error, job.status = str(exc), "error"
    except yt_dlp.utils.DownloadError as exc:
        job.error, job.status = _friendly(str(exc)), "error"
    except Exception:
        logger.exception("Unexpected failure while processing download job %s", job.id)
        job.error, job.status = _friendly(""), "error"


def _sweep() -> None:
    while True:
        time.sleep(60)
        cutoff = time.time() - config.JOB_TTL_SECONDS
        with _lock:
            expired = [j for j in _jobs.values() if j.created < cutoff and j.status in ("ready", "error")]
            for job in expired:
                _jobs.pop(job.id, None)
        for job in expired:
            if job.workdir:
                shutil.rmtree(job.workdir, ignore_errors=True)


threading.Thread(target=_sweep, daemon=True, name="job-sweeper").start()
