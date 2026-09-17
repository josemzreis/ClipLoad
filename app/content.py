"""SEO landing-page content. One entry = one indexable URL targeting one keyword cluster.

Every page shares the same tool, but has a unique title, H1, intro, steps and FAQ so that
search engines treat them as distinct, useful pages (not doorway duplicates).
"""

HOME = {
    "slug": "",
    "name": "All platforms",
    "title": "Video Downloader – Save Clips in HD, No Watermark",
    "description": "Paste a link from TikTok, YouTube Shorts, Twitch, Instagram, X or Reddit and download the video in HD or MP3. Free, fast, no watermark, no sign-up.",
    "h1": "Download any video clip in HD",
    "lead": "Paste a link from TikTok, YouTube, Twitch, Instagram, X, Reddit and 1,000+ other sites. No watermark, no sign-up, no app.",
    "about": [
        "{site} is a free online video downloader built for speed. Paste a link, pick a quality and your file starts downloading, usually within seconds. There's nothing to install and no account to create.",
        "We always fetch the highest-quality source the platform offers, up to 4K when available, and remove platform watermarks where a clean version exists. You can also save just the audio as an MP3.",
    ],
    "steps": [
        ("Copy the link", "Open the video in the app or website and tap Share, then Copy link."),
        ("Paste it above", "Paste the link into the box. We detect the platform automatically."),
        ("Download", "Choose a quality or MP3. The file saves straight to your device."),
    ],
    "faqs": [
        ("Is {site} free?", "Yes. It's completely free with no limits on the number of downloads. The site is supported by ads."),
        ("Do I need to install anything?", "No. {site} works in any browser on iPhone, Android, Windows, Mac and Linux."),
        ("Which sites are supported?", "TikTok, YouTube and YouTube Shorts, Twitch clips and VODs, Instagram Reels, X (Twitter), Facebook, Reddit, Vimeo, Dailymotion and more than 1,000 other sites."),
        ("Are downloaded videos watermarked?", "No. We never add a watermark, and for platforms like TikTok we fetch the original version without the platform watermark whenever it's available."),
        ("Is it legal to download videos?", "Download only content you own, content in the public domain, or content you have permission to use. Respect creators and each platform's terms."),
    ],
}

PLATFORMS = [
    {
        "slug": "tiktok-downloader",
        "name": "TikTok",
        "title": "TikTok Downloader – Save TikTok Videos Without Watermark",
        "description": "Download TikTok videos without watermark in HD. Paste the TikTok link and save the MP4 or MP3 instantly. Free, no app, no login.",
        "h1": "TikTok video downloader without watermark",
        "lead": "Save TikTok videos in HD with no watermark and no logo. Works on iPhone, Android and desktop.",
        "placeholder": "https://www.tiktok.com/@user/video/...",
        "about": [
            "TikTok adds a moving watermark with the creator's username when you save a video from the app. {site} fetches the original upload instead, so you get a clean MP4 at the best resolution TikTok stores.",
            "It's ideal for creators backing up their own videos or reposting their content to Reels and Shorts without a competitor's logo on it.",
        ],
        "steps": [
            ("Copy the TikTok link", "In TikTok, tap Share on the video, then Copy link."),
            ("Paste the link", "Paste it into the box above. The preview appears instantly."),
            ("Save without watermark", "Tap Download to save the clean MP4, or MP3 for the sound only."),
        ],
        "faqs": [
            ("How do I download a TikTok without the watermark?", "Copy the video's link, paste it into {site} and tap Download. The file you get has no TikTok watermark."),
            ("Can I download TikTok sounds as MP3?", "Yes. After pasting the link, choose MP3 to save just the audio."),
            ("Does it work on iPhone?", "Yes. On iOS, open {site} in Safari, paste the link and tap Download. The video is saved to the Files app, and from there you can save it to Photos."),
            ("Can I download private TikTok videos?", "No. Only public videos can be downloaded."),
        ],
    },
    {
        "slug": "youtube-shorts-downloader",
        "name": "YouTube Shorts",
        "title": "YouTube Shorts Downloader – Save Shorts in HD MP4",
        "description": "Download YouTube Shorts in HD quality. Paste the Shorts link and save it as MP4 or MP3 in seconds. Free and no sign-up.",
        "h1": "YouTube Shorts downloader",
        "lead": "Save YouTube Shorts as full-quality vertical MP4 files. Just paste the link.",
        "placeholder": "https://youtube.com/shorts/...",
        "about": [
            "Shorts are vertical videos up to three minutes long. {site} saves them at their original resolution, keeping the 9:16 format, so they're ready to edit or repost to other short-form platforms.",
            "Paste links in any format, whether youtube.com/shorts/, youtu.be or a mobile share link, and we'll handle the rest.",
        ],
        "steps": [
            ("Copy the Shorts link", "Tap Share on the Short, then Copy link."),
            ("Paste the link", "Paste it into the box above."),
            ("Download MP4", "Pick a quality and the Short saves to your device."),
        ],
        "faqs": [
            ("What quality are downloaded Shorts?", "We save the highest quality available, usually 1080x1920."),
            ("Can I convert a Short to MP3?", "Yes. Choose MP3 after pasting the link."),
            ("Does it work with youtu.be links?", "Yes. Every YouTube link format is supported."),
        ],
    },
    {
        "slug": "youtube-video-downloader",
        "name": "YouTube",
        "title": "YouTube Video Downloader – Save in 1080p & 4K",
        "description": "Download YouTube videos in 1080p, 4K or MP3. Paste the link and save the file in seconds. Free online YouTube downloader, no software.",
        "h1": "YouTube video downloader",
        "lead": "Save YouTube videos in up to 4K, or as MP3 audio. No software, no sign-up.",
        "placeholder": "https://www.youtube.com/watch?v=...",
        "about": [
            "{site} merges YouTube's highest-quality video and audio streams into a single MP4 that plays on any device. Choose 4K, 1440p, 1080p or 720p, whichever suits your storage and connection.",
            "Use it to archive your own uploads, save Creative Commons footage for editing, or keep lectures you have permission to watch offline.",
        ],
        "steps": [
            ("Copy the video URL", "Copy the link from your browser's address bar or the Share button."),
            ("Paste the link", "Paste it into the box above. Available qualities appear automatically."),
            ("Choose quality", "Tap 1080p, 4K or MP3 and your download begins."),
        ],
        "faqs": [
            ("Can I download YouTube videos in 4K?", "Yes, whenever the video was uploaded in 4K. The available resolutions are shown after you paste the link."),
            ("Is there a length limit?", "Videos up to 3 hours long are supported."),
            ("Can I download playlists?", "Not yet. Paste the links of individual videos."),
        ],
    },
    {
        "slug": "twitch-clip-downloader",
        "name": "Twitch",
        "title": "Twitch Clip Downloader – Download Twitch Clips & VODs",
        "description": "Download Twitch clips and past broadcasts in source quality. Paste the clip link and save the MP4 instantly. Free, fast, no login.",
        "h1": "Twitch clip downloader",
        "lead": "Save Twitch clips and VODs in source quality, perfect for TikTok, Shorts and highlight reels.",
        "placeholder": "https://clips.twitch.tv/...",
        "about": [
            "Streamers and editors use {site} to grab their best Twitch moments in source quality (often 1080p60) and turn them into TikToks, Shorts and YouTube highlight videos.",
            "Both clips.twitch.tv and twitch.tv/channel/clip/ links work, as well as past broadcasts (VODs) up to 3 hours long.",
        ],
        "steps": [
            ("Copy the clip link", "On Twitch, click Share on the clip and copy the link."),
            ("Paste the link", "Paste it into the box above."),
            ("Download", "Save the MP4 in source quality."),
        ],
        "faqs": [
            ("Can I download Twitch VODs?", "Yes. Past broadcasts up to 3 hours long are supported. Live streams can be downloaded once they've ended."),
            ("What quality are Twitch clips?", "We download the source quality, which is usually 1080p at 60fps."),
            ("Can I download clips from other streamers?", "Only download clips you have the rights or the streamer's permission to use."),
        ],
    },
    {
        "slug": "instagram-reels-downloader",
        "name": "Instagram",
        "title": "Instagram Reels Downloader – Save Reels & Videos in HD",
        "description": "Download Instagram Reels and videos in HD. Paste the Instagram link and save the MP4 in seconds. No login or app required.",
        "h1": "Instagram Reels downloader",
        "lead": "Save public Instagram Reels and videos in HD. No login needed.",
        "placeholder": "https://www.instagram.com/reel/...",
        "about": [
            "{site} saves public Instagram Reels and feed videos at their original quality, audio included.",
            "It's useful for backing up your own Reels or collecting references for your next edit.",
        ],
        "steps": [
            ("Copy the Reel link", "Tap the ••• or Share icon on the Reel, then Copy link."),
            ("Paste the link", "Paste it into the box above."),
            ("Download", "Save the Reel as MP4 or MP3."),
        ],
        "faqs": [
            ("Can I download private Instagram videos?", "No. Only videos from public accounts are supported."),
            ("Does the account owner know I downloaded their Reel?", "No. Downloads are anonymous, but please respect creators' rights."),
        ],
    },
    {
        "slug": "twitter-video-downloader",
        "name": "X (Twitter)",
        "title": "Twitter Video Downloader – Save X Videos & GIFs in HD",
        "description": "Download videos and GIFs from X (Twitter) in the highest quality. Paste the post link and save the MP4 instantly. Free and no login.",
        "h1": "X (Twitter) video downloader",
        "lead": "Save videos and GIFs from X posts in the highest quality available.",
        "placeholder": "https://x.com/user/status/...",
        "about": [
            "Paste any x.com or twitter.com post link and {site} finds the highest-bitrate version of the video.",
            "GIFs are saved as MP4 files, which work everywhere and are much smaller.",
        ],
        "steps": [
            ("Copy the post link", "Tap Share on the post, then Copy link."),
            ("Paste the link", "Paste it into the box above."),
            ("Download", "Save the video as MP4."),
        ],
        "faqs": [
            ("Do twitter.com links still work?", "Yes. Both x.com and twitter.com links are supported."),
            ("Can I download videos from protected accounts?", "No. Only public posts are supported."),
        ],
    },
    {
        "slug": "reddit-video-downloader",
        "name": "Reddit",
        "title": "Reddit Video Downloader – Save Reddit Videos With Sound",
        "description": "Download Reddit videos with audio in HD. Paste the Reddit post link and save the MP4 with sound. Free, no login.",
        "h1": "Reddit video downloader with sound",
        "lead": "Reddit stores video and audio separately, so saving a video often loses the sound. We merge them for you.",
        "placeholder": "https://www.reddit.com/r/.../comments/...",
        "about": [
            "Reddit's player streams audio and video separately, which is why many tools save silent clips. {site} combines both into one MP4 with sound.",
            "It works with reddit.com, old.reddit.com, v.redd.it and mobile share links.",
        ],
        "steps": [
            ("Copy the post link", "Tap Share on the post, then Copy link."),
            ("Paste the link", "Paste it into the box above."),
            ("Download", "Save the MP4 with audio."),
        ],
        "faqs": [
            ("Why do other Reddit downloads have no sound?", "Reddit hosts audio as a separate file. We download both and merge them."),
            ("Do v.redd.it links work?", "Yes."),
        ],
    },
    {
        "slug": "facebook-video-downloader",
        "name": "Facebook",
        "title": "Facebook Video Downloader – Save FB Videos & Reels in HD",
        "description": "Download Facebook videos and Reels in HD. Paste the Facebook link and save the MP4 in seconds. Free, no app, no login.",
        "h1": "Facebook video downloader",
        "lead": "Save public Facebook videos and Reels in HD quality.",
        "placeholder": "https://www.facebook.com/watch?v=...",
        "about": [
            "{site} downloads public Facebook videos, Reels and Watch videos in HD whenever it's available.",
            "Links shared from the Facebook app, including fb.watch short links, work too.",
        ],
        "steps": [
            ("Copy the video link", "Tap Share on the video, then Copy link."),
            ("Paste the link", "Paste it into the box above."),
            ("Download", "Choose HD and save the MP4."),
        ],
        "faqs": [
            ("Can I download videos from private groups?", "No. Only public videos are supported."),
            ("Do fb.watch links work?", "Yes."),
        ],
    },
    {
        "slug": "video-to-mp3",
        "name": "MP3",
        "title": "Video to MP3 Converter – Extract Audio From Any Video Link",
        "description": "Convert TikTok, YouTube, Twitch and other video links to MP3 online. Paste the link and download high-quality audio. Free and fast.",
        "h1": "Video to MP3 converter",
        "lead": "Turn any video link into a high-quality MP3. Paste the link, tap MP3, done.",
        "placeholder": "Paste a video link",
        "about": [
            "{site} extracts the best audio stream from a video and converts it to a 192 kbps MP3 that plays everywhere.",
            "It's great for podcasts, interviews, lectures, and voice-overs you have the rights to reuse.",
        ],
        "steps": [
            ("Copy the video link", "Copy the link of the video you want the audio from."),
            ("Paste the link", "Paste it into the box above."),
            ("Tap MP3", "Your audio file downloads right away."),
        ],
        "faqs": [
            ("What bitrate are the MP3 files?", "192 kbps, a good balance between quality and file size."),
            ("Which sites can I convert to MP3?", "Any site we support for video downloads also works for MP3."),
        ],
    },
]

PLATFORMS_BY_SLUG = {p["slug"]: p for p in PLATFORMS}

LEGAL = {
    "terms": {
        "title": "Terms of Use",
        "body": [
            "By using {site} you agree to these terms.",
            "{site} is a tool that lets you save publicly available media for personal use. You are solely responsible for how you use it. Only download content that you own, that is in the public domain, or that you have permission from the rights holder to download.",
            "Do not use {site} to infringe copyright, to redistribute other people's content without permission, or in any way that violates the terms of the platform the content comes from.",
            "{site} does not host any media. Files are processed temporarily and deleted automatically shortly afterwards.",
            "The service is provided \"as is\", without warranties of any kind. We may limit or suspend access at any time to prevent abuse.",
        ],
    },
    "privacy": {
        "title": "Privacy Policy",
        "body": [
            "{site} does not require an account and does not ask for personal information.",
            "Links you submit are processed to fetch the media and are not stored beyond the temporary processing window (under 15 minutes). Downloaded files are deleted automatically.",
            "We keep standard server logs (IP address, browser, and requested pages) for security and abuse prevention, for up to 30 days.",
            "We use Google AdSense to show ads. Google and its partners use cookies to serve ads based on your previous visits to this and other websites. You can opt out of personalized advertising at https://adssettings.google.com. Visitors in the EEA, the UK and Switzerland are asked for consent through a certified consent management platform.",
            "Questions? Email {email}.",
        ],
    },
    "dmca": {
        "title": "DMCA & Copyright",
        "body": [
            "{site} respects intellectual property rights. We don't host, cache or index any media. Every file is fetched on demand from the original platform at a user's request and deleted shortly afterwards.",
            "If you're a rights holder and believe {site} is being used to infringe your work, email {email} with: the URL of the original content, proof of ownership, your contact details, and a statement made in good faith. We'll respond promptly, including by blocking specific URLs from being processed.",
        ],
    },
}
