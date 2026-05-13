# Kaggle Notebook Setup Instructions

## Running on Kaggle T4 GPU

If you want to run this bot on Kaggle with T4 GPU acceleration:

### 1. Create a Kaggle Notebook
- Go to https://www.kaggle.com/code/new
- Select GPU (T4) as the accelerator
- Copy the bot code into cells

### 2. Install Dependencies

```python
!pip install pyrogram TgCrypto ffmpeg-python Pillow python-dotenv
!apt-get install -y ffmpeg ffprobe
```

### 3. Set Environment Variables

```python
import os
os.environ['API_ID'] = 'your_api_id'
os.environ['API_HASH'] = 'your_api_hash'
os.environ['BOT_TOKEN'] = 'your_bot_token'
```

### 4. Run the Bot

```python
%run bot.py
```

### 5. Keep Notebook Alive (Optional)

Since Kaggle notebooks timeout after inactivity, you might want to use a polling mechanism or deploy to a cloud service instead.

## Alternative: Cloud Deployment

Consider deploying on:
- **Railway** - Easy deployment with persistent sessions
- **Replit** - No GPU, but always-on
- **AWS EC2** - Full control with GPU options
- **Google Colab** - Free T4 GPU (but limited runtime)

## Performance Tips

- T4 GPU significantly speeds up H.265 encoding
- Use "fast" or "medium" presets for reasonable quality/speed balance
- CRF 23-28 provides good quality without excessive file sizes
- Original resolution recommended for maximum quality
