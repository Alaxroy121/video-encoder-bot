# Video Encoder Bot - Telegram Bot for FFmpeg Encoding

A Telegram bot that encodes and transcodes videos using FFmpeg on a Kaggle T4 GPU.

## Features

🎬 **Video Encoding**
- Accepts video files via Telegram
- Multiple codec support: H.264 and H.265 (HEVC)
- Quality control: CRF 0-51 (configurable)
- Speed presets: ultrafast to veryslow
- Resolution options: 4K, 2K, 1080p, 720p, 540p, 480p, 360p, or original
- 10-bit color support for HDR

📊 **Progress Tracking**
- Real-time encoding progress bar
- Elapsed time and ETA display
- Live updates during encoding

🎨 **Output Features**
- Anime-style thumbnails on encoded videos
- Random emoji reactions to messages
- Automatic temporary file cleanup

## Requirements

- Python 3.8+
- FFmpeg and FFprobe
- Pyrogram 2.0+
- Pillow (for thumbnail generation)

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file with:

```
API_ID=your_telegram_api_id
API_HASH=your_telegram_api_hash
BOT_TOKEN=your_bot_token
```

Get these values from:
- API_ID & API_HASH: https://my.telegram.org/apps
- BOT_TOKEN: Create a bot with @BotFather on Telegram

## Usage

```bash
python bot.py
```

Send `/start` to the bot on Telegram, then send a video file. Follow the interactive prompts to select your encoding settings.

## Project Structure

```
video-encoder-bot/
├── bot.py              # Main bot handler
├── config/
│   └── settings.py     # Configuration and constants
├── utils/
│   ├── encoder.py      # FFmpeg encoding logic
│   ├── thumbnail.py    # Anime thumbnail generation
│   └── keyboards.py    # Telegram inline keyboards
├── temp_files/         # Temporary video storage
├── thumbnails/         # Generated thumbnails
├── requirements.txt    # Python dependencies
└── .env               # Environment variables
```

## How It Works

1. User sends a video to the bot
2. Bot displays codec selection buttons (H.264/H.265)
3. User selects quality (CRF level)
4. User selects encoding speed
5. User selects resolution
6. User selects color depth (8-bit or 10-bit)
7. Bot encodes the video with real-time progress
8. Bot sends back the encoded video with anime thumbnail

## Performance Notes

- Runs on Kaggle T4 GPU for faster encoding
- Handles videos up to Telegram's file size limit (2GB)
- Progress updates every frame for accurate ETA
- Automatic cleanup of temporary files after upload

## License

MIT
