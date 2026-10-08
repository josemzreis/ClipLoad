# Deployment

## Recommended production layout

The current application should not be deployed directly as a Vercel Python Function. The download path depends on:

- `yt-dlp` and `ffmpeg` binaries from the Docker image
- an in-memory job registry and thread pool
- temporary files that must remain available between polling requests
- work that can take longer than a serverless request

Vercel functions are ephemeral, can be terminated between requests, and do not provide the persistent worker and filesystem assumptions above. A direct deployment may render the pages while probes or downloads fail intermittently.

Run the complete app as the existing Docker image on a persistent container host such as Railway, Render, Fly.io, Hetzner, or OVH. Put Cloudflare in front for DNS, TLS, caching, and abuse controls. Keep one Uvicorn worker per host.

## Fastest launch: Railway

Railway can build this repository from its `Dockerfile`, so Docker Desktop is not required on the development machine.

1. Create a GitHub repository and push this project to it. Do not commit `.env`; commit `.env.example` only.
2. Create an account at [railway.app](https://railway.app), choose **New Project**, then **Deploy from GitHub repo**.
3. Select the repository. Railway should detect the root `Dockerfile` automatically.
4. Open the service's **Variables** panel and add:

	```text
    SITE_NAME=ClipLoad
    SITE_URL=https://YOUR-RAILWAY-DOMAIN.up.railway.app
    CONTACT_EMAIL=your-real-abuse-email@example.com
    TRUST_PROXY_HEADERS=true
	```

	Leave the `ADSENSE_*` variables empty for the first deployment.
5. Deploy. In **Settings**, generate a Railway domain and open it in a browser. The value of `SITE_URL` must exactly match that HTTPS URL, without a trailing slash.
6. Open `/`, `/robots.txt`, `/sitemap.xml`, `/terms`, `/privacy`, and `/dmca`. Confirm the pages load before adding a custom domain.
7. Add your domain in Railway's **Networking** panel. Create the DNS record Railway shows at your DNS provider, wait for TLS to become active, then change `SITE_URL` to the custom HTTPS domain and redeploy.
8. Add the domain to Google Search Console and Bing Webmaster Tools, then submit `https://YOUR-DOMAIN/sitemap.xml`.

The service is intentionally one process and one worker. Do not increase worker count: the queue and temporary download files are process-local.

### GitHub upload from Windows

Run these commands from the project folder after creating an empty GitHub repository:

```powershell
git init
git add .
git commit -m "Initial ClipLoad deployment"
git branch -M main
git remote add origin https://github.com/YOUR-USER/YOUR-REPO.git
git push -u origin main
```

If Git is not installed, install Git for Windows, restart the terminal, and run the commands again. If the repository already exists, skip `git init` and add/commit/push only the files you intend to publish.

```bash
docker build -t clipload .
docker run --env-file .env -p 8000:8000 clipload
```

Required production variables:

```text
SITE_URL=https://yourdomain.com
CONTACT_EMAIL=abuse@yourdomain.com
TRUST_PROXY_HEADERS=true
```

The host needs enough temporary disk for the configured file-size limit and enough CPU/bandwidth for `ffmpeg` merges. Monitor disk usage, memory, download success by platform, and yt-dlp updates. Do not add a second worker until job state and files move to shared storage.

## Where Vercel fits

Vercel is a good future home for a static SEO frontend, but moving the whole app there requires an architectural change:

1. Move jobs to a durable queue such as Redis or a managed queue.
2. Move completed files to object storage such as S3 or R2 and return signed download URLs.
3. Run yt-dlp and ffmpeg in a separate worker service with a persistent runtime.
4. Make the Vercel app handle pages, metadata, API orchestration, and status polling only.

That split is worthwhile once traffic justifies it. It is not required for the first launch and should not be simulated with an in-memory queue inside a serverless function.

## Ads launch checklist

1. Deploy with `ADSENSE_CLIENT` and all slot variables empty. The app emits no ad markup in this state. Keep ads disabled unless the ad provider has approved this specific service and its policies permit the site's content and download functionality.
2. Publish and verify Terms, Privacy, and DMCA pages, and use a real abuse/copyright contact address.
3. Configure and test a Google-certified consent management platform for EEA, UK, and Switzerland traffic before enabling AdSense personalization. The application does not include a CMP.
4. Apply to the ad network only after the domain, legal pages, creator-focused positioning, and useful platform pages are live.
5. After approval, set the values from `.env.example`, redeploy, and verify `/ads.txt` contains the exact publisher ID supplied by the network.
6. Check mobile layout, download flow, Core Web Vitals, and accidental ad clicks before increasing ad density.

Do not add fake download buttons, pop-ups, auto-redirects, or ads that obscure the result. They damage user trust and can trigger policy or malware reviews.

## Pre-launch checks

- Set a real `SITE_URL`; otherwise canonical URLs, JSON-LD, sitemap, and `ads.txt` point at localhost.
- Register the sitemap in Google Search Console and Bing Webmaster Tools.
- Test `/`, every platform URL, `/robots.txt`, `/sitemap.xml`, `/ads.txt`, `/terms`, `/privacy`, and `/dmca` over HTTPS.
- Test a TikTok and Twitch download from mobile and desktop, including a failure response.
- Add uptime monitoring and alerting for 5xx responses, disk pressure, memory pressure, and download failure rate.
- Rebuild weekly so yt-dlp stays current.