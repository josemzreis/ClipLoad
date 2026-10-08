"""SEO landing-page content. One entry = one indexable URL targeting one keyword cluster.

Every page shares the same tool, but has a unique title, H1, intro, steps and FAQ so that
search engines treat them as distinct, useful pages (not doorway duplicates).
"""

HOME = {
    "slug": "",
    "name": "All platforms",
    "title": "Video Downloader for Your Own Content – HD & MP3",
    "description": "Save videos you own or have permission to use from supported platforms. Check platform rules before downloading. Free, online, no sign-up.",
    "h1": "Save videos you own or have permission to use",
    "lead": "A simple tool for creators to back up authorized videos from supported platforms. Check each platform's rules before downloading.",
    "about": [
        "{site} is a free online tool for creators who need to save copies of their own videos or media they are authorized to use. Paste a supported link, choose an available format, and process the file in your browser without installing an app.",
        "Only use the service where you have the necessary rights and the source platform permits downloading. Publicly viewable content is not automatically free to copy, download, or repost.",
    ],
    "steps": [
        ("Copy the link", "Open the video in the app or website and tap Share, then Copy link."),
        ("Paste it above", "Paste the link into the box. We detect the platform automatically."),
        ("Download", "Choose a quality or MP3. The file saves straight to your device."),
    ],
    "faqs": [
        ("Is {site} free?", "Yes. It's completely free with no limits on the number of downloads. The site is supported by ads."),
        ("Do I need to install anything?", "No. {site} works in any browser on iPhone, Android, Windows, Mac and Linux."),
        ("Which sites are supported?", "The tool can process links from supported services such as TikTok, YouTube, Twitch, Instagram, X, Facebook and Reddit. Availability varies by link and service."),
        ("Can I download any video I can view?", "No. Only submit content you own or have permission to use, and only where the source platform's terms allow downloading."),
        ("Is it legal to download videos?", "That depends on the content, your rights, local law, and the source platform's terms. Publicly viewable content is not automatically authorized for download or reuse."),
    ],
}

PLATFORMS = [
    {
        "slug": "tiktok-downloader",
        "name": "TikTok",
        "title": "TikTok Video Downloader for Your Own Content",
        "description": "Save your own TikTok videos or content you are authorized to use, where TikTok's terms allow it. MP4 or MP3, free and online.",
        "h1": "Save your own TikTok videos",
        "lead": "A simple way for creators to back up their own TikTok videos. Use only content you have permission to download and follow TikTok's terms.",
        "placeholder": "https://www.tiktok.com/@user/video/...",
        "about": [
            "{site} is intended for creators saving copies of their own TikTok videos or content they have permission to use. TikTok's features and terms may limit how content can be saved or reused.",
            "Before downloading, confirm that you have the necessary rights and that your intended use is allowed by TikTok and any applicable law.",
        ],
        "steps": [
            ("Copy the TikTok link", "In TikTok, tap Share on the video, then Copy link."),
            ("Paste the link", "Paste it into the box above. The preview appears instantly."),
            ("Save your authorized copy", "Choose an available format only if you own the content or have permission to use it."),
        ],
        "faqs": [
            ("Can I download any TikTok video?", "Only download videos you own or have permission to use, and only where TikTok's terms allow it."),
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
        "lead": "Extract audio from a supported video you own or have permission to use. Paste the link and choose MP3.",
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
            "{site} processes media links submitted by users. The service does not grant you permission or a license to download, copy, convert, or reuse any content.",
            "Only submit content that you own or are authorized to use, and only when downloading is permitted by the source platform's terms and applicable law. Public availability does not by itself grant permission.",
            "Do not use {site} to infringe copyright, redistribute another person's content without permission, or bypass digital-rights management, access controls, paywalls, or other restrictions.",
            "{site} does not host any media. Files are processed temporarily and deleted automatically shortly afterwards.",
            "The service is provided \"as is\", without warranties of any kind. We may limit or suspend access at any time to prevent abuse.",
        ],
    },
    "privacy": {
        "title": "Privacy Policy",
        "body": [
            "{site} does not require an account and does not ask for personal information.",
            "Links you submit are processed to fetch the media and are not stored beyond the temporary processing window (under 15 minutes). Downloaded files are deleted automatically.",
            "The hosting provider may process technical access logs, such as IP address, browser information, and requested pages, for security and service operation. Log handling and retention may depend on the hosting provider.",
            "If Google AdSense is enabled, Google and its partners may use cookies or similar technologies to serve and measure ads. You can manage Google ad personalization at https://adssettings.google.com. This application does not include a consent-management platform; the site operator must configure an appropriate Google-certified CMP before serving personalized ads where required.",
            "Questions? Email {email}.",
        ],
    },
    "dmca": {
        "title": "DMCA & Copyright",
        "body": [
            "{site} respects intellectual property rights. We do not host or index media libraries. Files are retrieved from third-party sources at a user's request and stored temporarily for processing.",
            "If you are a rights holder and believe {site} is being used to infringe your work, email {email} with the location of the original content, the specific material at issue, proof of ownership or authority, your contact details, and a good-faith statement. We will review complete notices promptly and take appropriate action.",
        ],
    },
}
