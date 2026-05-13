# IMPLEMENTATION.md - Video Encoder Bot Development Guide

## Project Overview

The Video Encoder Bot is a Telegram bot that:
1. Accepts video files
2. Allows users to configure encoding settings through interactive buttons
3. Encodes videos using FFmpeg with real-time progress tracking
4. Returns the encoded video with an anime-style thumbnail
5. Automatically cleans up temporary files

## Architecture

### Components

1. **bot.py** - Main bot handler using Pyrogram
   - `/start` command handler
   - Video file handler
   - Callback query handler for button interactions
   - Encoding orchestration

2. **config/settings.py** - Configuration
   - Telegram API credentials
   - Encoding presets (codecs, speeds, resolutions, CRF values)
   - Paths and reactions

3. **utils/encoder.py** - FFmpeg integration
   - Video duration detection
   - FFmpeg command building
   - Real-time progress reporting
   - Temporary file cleanup

4. **utils/thumbnail.py** - Thumbnail generation
   - Anime-style image generation using Pillow
   - Gradient overlays and borders
   - Anime-themed text rendering

5. **utils/keyboards.py** - UI/UX
   - Inline keyboard builders for each selection step
   - Clean button layouts

## Workflow

```
User sends video
    ↓
Bot receives video → stores file_id, initializes session
    ↓
Codec selection (H.264/H.265)
    ↓
Quality selection (CRF 0-51)
    ↓
Speed selection (ultrafast→veryslow)
    ↓
Resolution selection (4K→360p)
    ↓
Color depth (8-bit/10-bit)
    ↓
Encoding starts (with progress updates)
    ↓
Generate anime thumbnail
    ↓
Upload encoded video with metadata
    ↓
Cleanup temporary files
```

## Key Features Explained

### 1. Interactive Buttons
- Each step shows relevant options
- User selections update the session
- Previous choices are confirmed at each step

### 2. Progress Tracking
- Real-time progress message updates
- Shows percentage, elapsed time, and ETA
- Visual progress bar

### 3. Anime Thumbnails
- Generated using Pillow with gradient backgrounds
- Custom borders and text
- Saved and sent with the video

### 4. Random Reactions
- Bot reacts to messages with random emojis
- Adds personality to the bot

### 5. Resource Cleanup
- Temporary video files deleted after upload
- Thumbnails cleaned up
- Session data removed after completion

## Configuration Options

### Codecs
- **H.264** (libx264) - More compatible, larger file size
- **H.265** (libx265) - Better compression, newer devices only

### Quality (CRF)
- 0-51 scale (lower = better quality)
- Presets: Low (18), Medium (23), High (28), Very High (35), Maximum (40)

### Speed Presets
- ultrafast → veryslow
- Affects encoding time and quality (to some degree)
- T4 GPU handles faster speeds well

### Resolutions
- 4K (3840x2160)
- 2K (2560x1440)
- 1080p (1920x1080)
- 720p (1280x720)
- 540p (960x540)
- 480p (854x480)
- 360p (640x360)
- Original (no scaling)

### Color Depth
- 8-bit: Standard color (H.264/H.265)
- 10-bit: HDR support (H.265 only)

## Error Handling

The bot handles:
- Missing or expired sessions
- FFmpeg failures
- File download/upload errors
- Invalid video formats

## Future Enhancements

- [ ] Batch video encoding
- [ ] Video format support (WebM, AV1, VP9)
- [ ] Audio codec selection
- [ ] Subtitle handling
- [ ] Advanced FFmpeg filters
- [ ] Encoding history/stats
- [ ] Admin commands and limits
- [ ] Premium tier for faster encoding
- [ ] Watermark support
- [ ] Video compression optimization

## Deployment

### Local Testing
```bash
./setup.sh
python3 bot.py
```

### Kaggle Deployment
- Use Kaggle notebook with T4 GPU
- Install dependencies in notebook
- Set environment variables
- Run bot in notebook

### Cloud Deployment
- Railway: Easy deployment with persistent storage
- AWS EC2: Full control with GPU options
- Google Colab: Free T4 GPU (limited runtime)

## Performance Tips

1. Use "fast" or "medium" presets for good speed/quality balance
2. CRF 23-28 is recommended for most use cases
3. H.265 provides better compression but takes longer
4. Lower resolutions process faster
5. T4 GPU significantly improves encoding speed

## Monitoring

Monitor these metrics:
- Average encoding time per video
- File size reduction percentage
- User session completion rate
- Error rates and types

## Security Considerations

- Validate video files before processing
- Implement rate limiting per user
- Monitor resource usage
- Clean up temp files reliably
- Validate user input from callbacks

## Testing

Run the setup test:
```bash
python3 test_setup.py
```

This checks:
- FFmpeg installation
- Python dependencies
- Environment variables
- Directory structure
