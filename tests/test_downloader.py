import unittest

from app.downloader import _has_video, _safe_filename


class SafeFilenameTests(unittest.TestCase):
    def test_normalizes_unsupported_characters(self):
        self.assertEqual(_safe_filename("Café 東京 🎬: clip/name?", "MP4"), "cafe-clip-name.mp4")

    def test_uses_fallback_for_titles_without_ascii_characters(self):
        self.assertEqual(_safe_filename("🎬 東京", "mp4"), "video.mp4")

    def test_avoids_windows_reserved_device_names(self):
        self.assertEqual(_safe_filename("CON.txt", "mp4"), "video-con.txt.mp4")

    def test_limits_name_length_and_sanitizes_extension(self):
        filename = _safe_filename("clip" * 40, "../MP4")
        self.assertEqual(filename, f'{"clip" * 25}.mp4')


class VideoDetectionTests(unittest.TestCase):
    def test_detects_direct_mp4_without_codec_metadata(self):
        info = {"ext": "mp4", "formats": [{"ext": "mp4", "vcodec": None, "acodec": None}]}
        self.assertTrue(_has_video(info))

    def test_does_not_detect_audio_only_mp3_as_video(self):
        info = {"ext": "mp3", "formats": [{"ext": "mp3", "vcodec": "none", "acodec": "mp3"}]}
        self.assertFalse(_has_video(info))


if __name__ == "__main__":
    unittest.main()
