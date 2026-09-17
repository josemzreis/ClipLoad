FROM python:3.12-slim

# ffmpeg merges video+audio streams and converts MP3; Deno is the JS runtime yt-dlp needs for YouTube.
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg ca-certificates \
    && rm -rf /var/lib/apt/lists/*
COPY --from=denoland/deno:bin /deno /usr/local/bin/deno

WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app

ENV DOWNLOAD_DIR=/tmp/clipload TRUST_PROXY_HEADERS=true
EXPOSE 8000
# One worker on purpose: the job queue lives in process memory. Scale by adding hosts, not workers.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--proxy-headers", "--forwarded-allow-ips", "*"]
