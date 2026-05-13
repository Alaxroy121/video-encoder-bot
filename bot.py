import os
import time
import tempfile
from pyrogram import Client, filters
from pyrogram.types import Message
import random

from config.settings import (
    API_ID, API_HASH, BOT_TOKEN, TEMP_DIR, REACTIONS,
    CODEC_OPTIONS, SPEED_OPTIONS, RESOLUTION_OPTIONS
)
from utils.encoder import encode_video, cleanup_temp_files, get_video_duration
from utils.thumbnail import generate_anime_thumbnail
from utils.keyboards import (
    create_codec_keyboard, create_speed_keyboard, 
    create_resolution_keyboard, create_crf_keyboard, create_bitcolor_keyboard
)

app = Client("video_encoder_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# User encoding sessions
user_sessions = {}
reaction_index = {}  # Track reaction index per user

# Anime thumbnails for /start command
ANIME_THUMBNAILS = [
    "assets/thumbnails/thumb_1.jpg",
    "assets/thumbnails/thumb_2.jpg",
    "assets/thumbnails/thumb_3.jpg",
    "assets/thumbnails/thumb_4.jpg",
    "assets/thumbnails/thumb_5.jpg",
    "assets/thumbnails/thumb_6.jpg",
    "assets/thumbnails/thumb_7.jpg",
    "assets/thumbnails/thumb_8.jpg",
    "assets/thumbnails/thumb_9.jpg",
]

# Diverse reactions - TELEGRAM COMPATIBLE ONLY
REACTIONS_DIVERSE = [
    "😂", "🔥", "✨", "🎉", "😍", "🚀", "💯", "⚡",
    "🎬", "💻", "🎨", "💥", "🎯", "😎", "🎪", "🎭",
    "🌈", "💬", "🎸", "🍕", "🌻", "🎃", "💎", "👌",
    "😆", "🔆", "❤", "🖤", "💜", "💚"
]

@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    """Handle /start command with anime photo"""
    user_id = message.from_user.id
    
    # React with rotating reaction
    if user_id not in reaction_index:
        reaction_index[user_id] = 0
    reaction = REACTIONS_DIVERSE[reaction_index[user_id] % len(REACTIONS_DIVERSE)]
    await message.react(reaction)
    reaction_index[user_id] += 1
    
    # Pick random anime thumbnail
    thumb_photo = random.choice(ANIME_THUMBNAILS)
    
    # Send photo with caption
    await client.send_photo(
        chat_id=message.chat.id,
        photo=thumb_photo,
        caption=(
            "🎬 **Video Encoder Bot**\n\n"
            "Send me a video file and I'll encode it with your preferred settings:\n\n"
            "⚙️ **Options:**\n"
            "• Codec: H.264 or H.265 (HEVC)\n"
            "• Quality: CRF 0-51 (lower = better)\n"
            "• Speed: ultrafast to veryslow\n"
            "• Resolution: 4K, 2K, 1080p, 720p, 540p, 480p, 360p, or original\n"
            "• Color: 8-bit or 10-bit HDR\n\n"
            "Just send a video and follow the prompts! 🚀"
        )
    )

@app.on_message(filters.video)
async def video_handler(client: Client, message: Message):
    """Handle incoming video files"""
    user_id = message.from_user.id
    
    # React with rotating reaction
    if user_id not in reaction_index:
        reaction_index[user_id] = 0
    reaction = REACTIONS_DIVERSE[reaction_index[user_id] % len(REACTIONS_DIVERSE)]
    await message.react(reaction)
    reaction_index[user_id] += 1
    
    # Initialize user session
    user_sessions[user_id] = {
        "video_file_id": message.video.file_id,
        "original_path": None,
        "codec": "H.264",
        "crf": 23,
        "speed": "medium",
        "resolution": "1080p",
        "ten_bit": False
    }
    
    # Send codec selection
    await message.reply_text(
        f"📹 Video received! ({message.video.file_size / (1024*1024):.2f} MB)\n\n"
        "Select codec:",
        reply_markup=create_codec_keyboard()
    )

@app.on_callback_query()
async def callback_handler(client: Client, callback_query):
    """Handle button callbacks"""
    user_id = callback_query.from_user.id
    data = callback_query.data
    
    # React with rotating reaction
    if user_id not in reaction_index:
        reaction_index[user_id] = 0
    reaction = REACTIONS_DIVERSE[reaction_index[user_id] % len(REACTIONS_DIVERSE)]
    await callback_query.message.react(reaction)
    reaction_index[user_id] += 1
    
    if user_id not in user_sessions:
        await callback_query.answer("❌ Session expired. Send a video again.")
        return
    
    session = user_sessions[user_id]
    
    # Codec selection
    if data.startswith("codec_"):
        codec = data.split("_")[1]
        session["codec"] = codec
        await callback_query.message.edit_text(
            f"✅ Codec: {codec}\n\nSelect quality (CRF):",
            reply_markup=create_crf_keyboard()
        )
    
    # CRF selection
    elif data.startswith("crf_"):
        crf = int(data.split("_")[1])
        session["crf"] = crf
        await callback_query.message.edit_text(
            f"✅ Quality: CRF {crf}\n\nSelect encoding speed:",
            reply_markup=create_speed_keyboard()
        )
    
    # Speed selection
    elif data.startswith("speed_"):
        speed = data.split("_")[1]
        session["speed"] = speed
        await callback_query.message.edit_text(
            f"✅ Speed: {speed}\n\nSelect resolution:",
            reply_markup=create_resolution_keyboard()
        )
    
    # Resolution selection
    elif data.startswith("resolution_"):
        resolution = data.split("_")[1]
        session["resolution"] = resolution
        await callback_query.message.edit_text(
            f"✅ Resolution: {resolution}\n\nSelect color depth:",
            reply_markup=create_bitcolor_keyboard()
        )
    
    # Color depth selection
    elif data.startswith("bitcolor_"):
        bit = int(data.split("_")[1])
        session["ten_bit"] = (bit == 10)
        
        # Start encoding
        await callback_query.message.edit_text(
            f"✅ Color: {bit}-bit\n\n"
            f"⏳ **Settings Summary:**\n"
            f"• Codec: {session['codec']}\n"
            f"• Quality: CRF {session['crf']}\n"
            f"• Speed: {session['speed']}\n"
            f"• Resolution: {session['resolution']}\n"
            f"• Color: {bit}-bit\n\n"
            f"🚀 Starting encoding..."
        )
        
        await start_encoding(client, callback_query.message, user_id)
    
    await callback_query.answer()

async def start_encoding(client: Client, message: Message, user_id: int):
    """Start the video encoding process"""
    session = user_sessions[user_id]
    
    try:
        # Download video
        progress_message = await message.reply_text("📥 Downloading video...")
        video_path = await client.download_media(session["video_file_id"], file_name=TEMP_DIR)
        session["original_path"] = video_path
        
        # Prepare output
        output_filename = f"encoded_{int(time.time())}.mp4"
        output_path = os.path.join(TEMP_DIR, output_filename)
        
        # Get duration
        duration = get_video_duration(video_path)
        
        # Create progress message
        progress_text = "🎬 Encoding: 0%\n⏱️ Elapsed: 0s | ETA: calculating..."
        progress_msg = await message.reply_text(progress_text)
        
        def progress_callback(current_seconds, total_seconds, elapsed):
            """Update progress message"""
            percent = (current_seconds / total_seconds * 100) if total_seconds > 0 else 0
            eta_seconds = (elapsed / current_seconds * (total_seconds - current_seconds)) if current_seconds > 0 else 0
            
            # Format time
            elapsed_str = f"{int(elapsed // 60)}m {int(elapsed % 60)}s"
            eta_str = f"{int(eta_seconds // 60)}m {int(eta_seconds % 60)}s" if eta_seconds > 0 else "calculating..."
            
            text = (
                f"🎬 Encoding: {percent:.1f}%\n"
                f"⏱️ Elapsed: {elapsed_str} | ETA: {eta_str}\n"
                f"📊 Progress: [{int(percent/5)}{'░'*(20-int(percent/5))}]"
            )
            return text
        
        # Encode video
        await progress_msg.edit_text("🎬 Encoding: Starting...\n⏱️ Elapsed: 0s")
        
        codec = CODEC_OPTIONS[session["codec"]]
        resolution = RESOLUTION_OPTIONS[session["resolution"]]
        
        success = encode_video(
            video_path,
            output_path,
            codec,
            session["crf"],
            session["speed"],
            resolution,
            session["ten_bit"],
            progress_callback
        )
        
        if not success:
            await progress_msg.edit_text("❌ Encoding failed!")
            cleanup_temp_files(video_path)
            return
        
        # Generate thumbnail
        thumbnail_path = os.path.join("thumbnails", f"thumb_{int(time.time())}.jpg")
        generate_anime_thumbnail(output_path, thumbnail_path)
        
        # Upload encoded video
        await progress_msg.edit_text("📤 Uploading encoded video...")
        
        with open(output_path, 'rb') as f:
            await client.send_video(
                chat_id=message.chat.id,
                video=f,
                caption=f"✅ **Video Encoded!**\n\n"
                        f"📋 Settings:\n"
                        f"• Codec: {session['codec']}\n"
                        f"• Quality: CRF {session['crf']}\n"
                        f"• Speed: {session['speed']}\n"
                        f"• Resolution: {session['resolution']}\n"
                        f"• Color: {'10-bit' if session['ten_bit'] else '8-bit'}\n\n"
                        f"💾 Original: {os.path.getsize(video_path) / (1024*1024):.2f} MB\n"
                        f"💾 Encoded: {os.path.getsize(output_path) / (1024*1024):.2f} MB",
                thumb=thumbnail_path if os.path.exists(thumbnail_path) else None
            )
        
        await progress_msg.delete()
        
        # React with final reaction
        if user_id not in reaction_index:
            reaction_index[user_id] = 0
        reaction = REACTIONS_DIVERSE[reaction_index[user_id] % len(REACTIONS_DIVERSE)]
        await message.react(reaction)
        reaction_index[user_id] += 1
        
        # Cleanup
        cleanup_temp_files(video_path)
        cleanup_temp_files(output_path)
        if os.path.exists(thumbnail_path):
            cleanup_temp_files(thumbnail_path)
        
        del user_sessions[user_id]
        
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
        if user_id in user_sessions and user_sessions[user_id]["original_path"]:
            cleanup_temp_files(user_sessions[user_id]["original_path"])

if __name__ == "__main__":
    print("🚀 Video Encoder Bot starting...")
    app.run()
