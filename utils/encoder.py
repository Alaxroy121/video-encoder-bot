import os
import subprocess
import time

NVENC_PRESETS = {
    "ultrafast": "fast",
    "superfast": "fast",
    "veryfast": "fast",
    "faster": "fast",
    "fast": "fast",
    "medium": "medium",
    "slow": "slow",
    "slower": "slow",
    "veryslow": "slow",
}


def get_video_duration(file_path):
    """Get video duration in seconds."""
    try:
        result = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                file_path,
            ],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        return float(result.stdout.strip())
    except Exception as e:
        print(f"Error getting duration: {e}")
        return 0


def ffmpeg_encoder_available(encoder_name):
    """Return True when the local FFmpeg build exposes the requested encoder."""
    result = subprocess.run(
        ["ffmpeg", "-hide_banner", "-encoders"],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    return encoder_name in result.stdout


def get_nvenc_codec(codec):
    """Map CPU codecs to the matching NVIDIA encoder when available."""
    if codec == "libx264":
        return "h264_nvenc"
    if codec == "libx265":
        return "hevc_nvenc"
    return None


def format_scale_filter(filter_name, resolution):
    """Build FFmpeg scale filter syntax for WIDTHxHEIGHT settings."""
    width, height = resolution.split("x", 1)
    return f"{filter_name}={width}:{height}"


def build_encode_command(
    input_path, output_path, codec, crf, speed, resolution, ten_bit=False, use_gpu=True
):
    """Build an FFmpeg command, preferring a no-frame-extraction CUDA/NVENC path."""
    gpu_codec = get_nvenc_codec(codec) if use_gpu else None
    use_nvenc = bool(gpu_codec and ffmpeg_encoder_available(gpu_codec))

    cmd = ["ffmpeg", "-y"]

    if use_nvenc:
        cmd.extend(["-hwaccel", "cuda", "-hwaccel_output_format", "cuda"])

    cmd.extend(["-i", input_path])

    if use_nvenc:
        cmd.extend(
            [
                "-c:v",
                gpu_codec,
                "-preset",
                NVENC_PRESETS.get(speed, "fast"),
                "-rc",
                "vbr",
                "-cq",
                str(crf),
                "-b:v",
                "0",
            ]
        )
        if resolution:
            cmd.extend(["-vf", format_scale_filter("scale_cuda", resolution)])
        if ten_bit and gpu_codec == "hevc_nvenc":
            cmd.extend(["-pix_fmt", "p010le"])
    else:
        cmd.extend(["-c:v", codec, "-crf", str(crf), "-preset", speed])
        if ten_bit and codec == "libx265":
            cmd.extend(["-pix_fmt", "yuv420p10le"])
        if resolution:
            cmd.extend(["-vf", format_scale_filter("scale", resolution)])

    cmd.extend(["-c:a", "aac", "-b:a", "128k"])
    cmd.extend(["-progress", "pipe:1", "-nostats", "-loglevel", "error"])
    cmd.append(output_path)
    return cmd, use_nvenc


def run_ffmpeg_command(cmd, duration, progress_callback=None):
    """Run FFmpeg and report progress based on encoded output timestamp."""
    start_time = time.time()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stderr_lines = []

    for line in process.stdout:
        key, _, value = line.strip().partition("=")
        if key == "out_time_ms":
            try:
                current_seconds = max(0, int(value) / 1_000_000)
            except ValueError:
                continue
            elapsed = time.time() - start_time
            if progress_callback:
                progress_callback(current_seconds, duration, elapsed)

    stderr = process.stderr.read()
    if stderr:
        stderr_lines.append(stderr.strip())

    process.wait()
    return process.returncode, "\n".join(stderr_lines)


def encode_video(input_path, output_path, codec, crf, speed, resolution, ten_bit=False, progress_callback=None):
    """
    Encode video with FFmpeg.

    On Kaggle T4 runtimes this prefers CUDA decode, scale_cuda, and NVENC so
    upscale/encode jobs do not get stuck spending hours extracting PNG frames on
    the CPU. If FFmpeg cannot use CUDA for a particular input, it automatically
    falls back to the original CPU encode path.
    """
    try:
        duration = get_video_duration(input_path)
        if duration == 0:
            raise Exception("Could not determine video duration")

        attempts = [True, False]
        last_error = ""

        for use_gpu in attempts:
            cmd, using_nvenc = build_encode_command(
                input_path,
                output_path,
                codec,
                crf,
                speed,
                resolution,
                ten_bit,
                use_gpu=use_gpu,
            )
            mode = "CUDA/NVENC" if using_nvenc else "CPU"
            print(f"Starting {mode} FFmpeg encode: {' '.join(cmd)}")

            returncode, stderr = run_ffmpeg_command(cmd, duration, progress_callback)
            if returncode == 0:
                return True

            last_error = stderr or f"FFmpeg exited with code {returncode}"
            print(f"{mode} encoding failed: {last_error}")
            if os.path.exists(output_path):
                os.remove(output_path)

            if not using_nvenc:
                break

        raise Exception(last_error)
    except Exception as e:
        print(f"Encoding error: {e}")
        return False


def cleanup_temp_files(file_path):
    """Delete temporary file."""
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")
    except Exception as e:
        print(f"Cleanup error: {e}")
