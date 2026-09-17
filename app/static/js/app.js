(() => {
  const $ = (id) => document.getElementById(id);
  const form = $("grab"), input = $("url"), go = $("go"), pasteBtn = $("paste");
  const statusEl = $("status"), result = $("result"), actions = $("actions");
  const progress = $("progress"), bar = $("bar");

  if ("serviceWorker" in navigator) navigator.serviceWorker.register("/sw.js").catch(() => {});
  loadAdsWhenIdle();
  if (!form) return;

  let current = null;  // probe result for the link on screen
  let busy = false;

  const setStatus = (text, isError = false) => {
    statusEl.textContent = text;
    statusEl.classList.toggle("is-error", isError);
  };

  async function api(path, body) {
    const res = await fetch(path, body ? {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body),
    } : undefined);
    const data = await res.json().catch(() => ({}));
    if (!res.ok) throw new Error(data.detail || "Something went wrong. Please try again.");
    return data;
  }

  const looksLikeUrl = (v) => /^https?:\/\/\S+\.\S+/i.test(v.trim());

  async function analyze() {
    const url = input.value.trim();
    if (!url || busy) return;
    if (!looksLikeUrl(url)) return setStatus("Please paste a full link starting with https://", true);
    busy = true; go.disabled = true; result.hidden = true;
    setStatus("Fetching video info…");
    try {
      current = await api("/api/probe", { url });
      render(current);
      setStatus("");
    } catch (err) {
      setStatus(err.message, true);
    } finally {
      busy = false; go.disabled = false;
    }
  }

  function formatDuration(s) {
    if (!s) return "";
    s = Math.round(s);
    const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = String(s % 60).padStart(2, "0");
    return h ? `${h}:${String(m).padStart(2, "0")}:${sec}` : `${m}:${sec}`;
  }

  function button(label, quality, primary) {
    const b = document.createElement("button");
    b.type = "button";
    b.className = `btn btn--small ${primary ? "btn--primary" : "btn--ghost"}`;
    b.textContent = label;
    b.addEventListener("click", () => download(quality));
    return b;
  }

  function render(info) {
    const thumb = $("thumb");
    thumb.hidden = !info.thumbnail;
    if (info.thumbnail) thumb.src = info.thumbnail;
    $("title").textContent = info.title;
    $("meta").textContent = [info.platform, info.uploader, formatDuration(info.duration)].filter(Boolean).join(" · ");
    actions.replaceChildren();
    if (info.has_video) {
      const best = info.max_res ? `Download MP4 · ${info.max_res}p` : "Download MP4";
      actions.append(button(best, "best", true));
      info.qualities.filter((q) => Number(q) !== info.max_res).forEach((q) => actions.append(button(`${q}p`, q)));
    }
    actions.append(button(info.has_video ? "MP3" : "Download MP3", "mp3", !info.has_video));
    progress.hidden = true;
    result.hidden = false;
  }

  async function download(quality) {
    if (!current || busy) return;
    busy = true;
    actions.querySelectorAll("button").forEach((b) => (b.disabled = true));
    progress.hidden = false;
    progress.classList.add("is-indeterminate");
    bar.style.width = "";
    setStatus("Preparing your file…");
    try {
      const job = await api("/api/jobs", { url: current.url, quality });
      const done = await poll(job.id);
      const fileUrl = `/api/jobs/${done.id}/file`;
      window.location.href = fileUrl;  // Content-Disposition: attachment keeps the page open
      statusEl.classList.remove("is-error");
      statusEl.innerHTML = `Your download has started. Didn't start? <a href="${fileUrl}">Click here</a>.`;
    } catch (err) {
      setStatus(err.message, true);
      progress.hidden = true;
    } finally {
      busy = false;
      actions.querySelectorAll("button").forEach((b) => (b.disabled = false));
    }
  }

  async function poll(id) {
    for (;;) {
      await new Promise((r) => setTimeout(r, 900));
      const job = await api(`/api/jobs/${id}`);
      if (job.status === "error") throw new Error(job.error);
      if (job.status === "ready") {
        progress.classList.remove("is-indeterminate");
        bar.style.width = "100%";
        return job;
      }
      if (job.progress > 0) {
        progress.classList.remove("is-indeterminate");
        bar.style.width = `${job.progress}%`;
      }
      setStatus(job.status === "processing" ? "Almost done, finalizing your file…" :
        job.progress > 0 ? `Downloading… ${Math.round(job.progress)}%` : "Preparing your file…");
    }
  }

  form.addEventListener("submit", (e) => { e.preventDefault(); analyze(); });
  // "No extra steps": a pasted link starts immediately.
  input.addEventListener("paste", () => setTimeout(analyze, 0));

  if (navigator.clipboard && navigator.clipboard.readText) {
    pasteBtn.hidden = false;
    pasteBtn.addEventListener("click", async () => {
      try {
        input.value = (await navigator.clipboard.readText()).trim();
        analyze();
      } catch { input.focus(); }
    });
  }

  // Links arriving via ?url= (share target, bookmarklet, external links).
  if (form.dataset.prefill) {
    input.value = form.dataset.prefill;
    analyze();
  }

  // Ads load after the first interaction or 3.5s, so they never slow down first paint (Core Web Vitals).
  function loadAdsWhenIdle() {
    const client = document.body.dataset.adsense;
    if (!client || !document.querySelector(".adsbygoogle")) return;
    let loaded = false;
    const load = () => {
      if (loaded) return;
      loaded = true;
      const s = document.createElement("script");
      s.async = true;
      s.crossOrigin = "anonymous";
      s.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${client}`;
      s.onload = () => document.querySelectorAll(".adsbygoogle").forEach(() => {
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      });
      document.head.append(s);
    };
    ["pointerdown", "keydown", "scroll", "touchstart"].forEach((ev) => addEventListener(ev, load, { once: true, passive: true }));
    setTimeout(load, 3500);
  }
})();
