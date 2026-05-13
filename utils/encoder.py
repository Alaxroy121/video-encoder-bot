import os
import subprocess
import time
from pathlib import Path
from config.settings import TEMP_DIR

def get_video_duration(file_path):
    """Get video duration in seconds"""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
             "-of", "default=noprint_wrappers=1:nokey=1:novalue=1", file_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting duration: {e}")
        return 0

def encode_video(input_path, output_path, codec, crf, speed, resolution, ten_bit=False, progress_callback=None):
    """
    Encode video with FFmpeg
    progress_callback: callable(current_frame, total_frames, elapsed_time)
    """
    try:
        duration = get_video_duration(input_path)
        if duration == 0:
            raise Exception("Could not determine video duration")
        
        # Build FFmpeg command
        cmd = ["ffmpeg", "-i", input_path]
        
        # Codec and quality settings
        cmd.extend(["-c:v", codec])
        cmd.extend(["-crf", str(crf)])
        cmd.extend(["-preset", speed])
        
        # 10-bit color support
        if ten_bit and codec == "libx265":
            cmd.extend(["-pix_fmt", "yuv420p10le"])
        
        # Resolution scaling
        if resolution:
            cmd.extend(["-vf", f"scale={resolution}"])
        
        # Audio codec
        cmd.extend(["-c:a", "aac", "-b:a", "128k"])
        
        # Progress reporting
        cmd.extend(["-progress", "pipe:1"])
        cmd.extend(["-loglevel", "error"])
        cmd.append(output_path)
        
        start_time = time.time()
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        for line in process.stdout:
            if line.startswith("frame="):
                try:
                    frame = int(line.split("=")[1].strip())
                    fps = 30  # Assume 30 fps for calculation
                    current_seconds = frame / fps
                    elapsed = time.time() - start_time
                    
                    if progress_callback:
                        progress_callback(current_seconds, duration, elapsed)
                except:
                    pass
        
        process.wait()
        
        if process.returncode != 0:
            raise Exception(f"FFmpeg encoding failed with code {process.returncode}")
        
        return True
    except Exception as e:
        print(f"Encoding error: {e}")
        return False

def cleanup_temp_files(file_path):
    """Delete temporary file"""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Cleanup error: {e}")
