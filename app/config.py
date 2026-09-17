"""Runtime configuration, read once from environment variables."""
import os
import tempfile


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


SITE_NAME = os.getenv("SITE_NAME", "ClipLoad")
SITE_URL = os.getenv("SITE_URL", "http://localhost:8000").rstrip("/")
CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "contact@example.com")

# Ads: leave ADSENSE_CLIENT empty to render no ad markup at all.
ADSENSE_CLIENT = os.getenv("ADSENSE_CLIENT", "")  # e.g. ca-pub-1234567890123456
ADSENSE_SLOTS = {
    "top": os.getenv("ADSENSE_SLOT_TOP", ""),
    "result": os.getenv("ADSENSE_SLOT_RESULT", ""),
    "bottom": os.getenv("ADSENSE_SLOT_BOTTOM", ""),
}

# Abuse / cost limits
MAX_DURATION = _int("MAX_DURATION_SECONDS", 3 * 60 * 60)
MAX_FILESIZE_MB = _int("MAX_FILESIZE_MB", 2048)
MAX_CONCURRENT_JOBS = _int("MAX_CONCURRENT_JOBS", 4)
MAX_QUEUED_JOBS = _int("MAX_QUEUED_JOBS", 40)
JOB_TTL_SECONDS = _int("JOB_TTL_SECONDS", 15 * 60)
RATE_LIMIT_PER_MINUTE = _int("RATE_LIMIT_PER_MINUTE", 20)
TRUST_PROXY_HEADERS = os.getenv("TRUST_PROXY_HEADERS", "false").lower() == "true"

# Extraction
COOKIES_FILE = os.getenv("YTDLP_COOKIES_FILE", "")
PROXY = os.getenv("YTDLP_PROXY", "")

DOWNLOAD_DIR = os.getenv("DOWNLOAD_DIR", os.path.join(tempfile.gettempdir(), "clipload"))
os.makedirs(DOWNLOAD_DIR, exist_ok=True)
