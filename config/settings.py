import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Config
API_ID = int(os.getenv("API_ID", "0"))
API_HASH = os.getenv("API_HASH", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

# Paths
TEMP_DIR = "temp_files"
THUMBNAIL_DIR = "thumbnails"
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

# Encoding settings
CODEC_OPTIONS = {
    "H.264": "libx264",
    "H.265": "libx265"
}

CRF_MIN = 0
CRF_MAX = 51
CRF_DEFAULT = 23

SPEED_OPTIONS = {
    "ultrafast": "ultrafast",
    "superfast": "superfast",
    "veryfast": "veryfast",
    "faster": "faster",
    "fast": "fast",
    "medium": "medium",
    "slow": "slow",
    "slower": "slower",
    "veryslow": "veryslow"
}

RESOLUTION_OPTIONS = {
    "4K": "3840x2160",
    "2K": "2560x1440",
    "1080p": "1920x1080",
    "720p": "1280x720",
    "540p": "960x540",
    "480p": "854x480",
    "360p": "640x360",
    "original": None
}

# Random reactions
REACTIONS = ["😂", "❤️", "🔥", "✨", "👏", "🎉", "😍", "🚀", "💯", "⚡", "🎬", "💻"]
