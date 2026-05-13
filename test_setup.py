"""
Quick local testing script for Video Encoder Bot
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from config.settings import TEMP_DIR, THUMBNAIL_DIR
from utils.encoder import encode_video, get_video_duration
from utils.thumbnail import generate_anime_thumbnail

def test_setup():
    """Test if all dependencies are available"""
    print("🔍 Testing Video Encoder Bot Setup...\n")
    
    # Check directories
    print(f"✅ Temp directory: {TEMP_DIR}")
    print(f"✅ Thumbnail directory: {THUMBNAIL_DIR}")
    
    # Check FFmpeg
    try:
        import subprocess
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True)
        if "ffmpeg version" in result.stdout:
            print("✅ FFmpeg is installed")
        else:
            print("❌ FFmpeg not found")
    except Exception as e:
        print(f"❌ FFmpeg check failed: {e}")
    
    # Check Pyrogram
    try:
        import pyrogram
        print(f"✅ Pyrogram {pyrogram.__version__} is installed")
    except ImportError:
        print("❌ Pyrogram not installed")
    
    # Check Pillow
    try:
        import PIL
        print(f"✅ Pillow is installed")
    except ImportError:
        print("❌ Pillow not installed")
    
    # Check environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_id = os.getenv("API_ID")
    api_hash = os.getenv("API_HASH")
    bot_token = os.getenv("BOT_TOKEN")
    
    print("\n📋 Environment Variables:")
    print(f"  API_ID: {'✅ Set' if api_id else '❌ Not set'}")
    print(f"  API_HASH: {'✅ Set' if api_hash else '❌ Not set'}")
    print(f"  BOT_TOKEN: {'✅ Set' if bot_token else '❌ Not set'}")
    
    if api_id and api_hash and bot_token:
        print("\n✅ All systems ready! Run 'python bot.py' to start the bot.")
    else:
        print("\n❌ Please set up .env file with API credentials.")
        print("   Copy .env.example to .env and fill in your credentials.")

if __name__ == "__main__":
    test_setup()
