import os 
import yt_dlp
import subprocess

DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok = True)

def download_youtube_audio(url : str) -> str:
    output_temp = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_temp,
        "postprocessors":[
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            }
        ],
        "quiet":False,
        "nonplaylist": True,
        "cookiefile": "cookies.txt",
        "remote_components": ["ejs:github"], 
        "js_runtimes":{"node": {}}}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url , download = True)
        if "entries" in info:
            info = info["entries"][0]#first vid of playlist

        base, _ = os.path.splitext(ydl.prepare_filename(info))
        wav_path = base + ".wav"
        if not os.path.exists  (wav_path):
            raise FileNotFoundErrir(f"Expected{wav_path}, but it wasn't created.")
     
    return wav_path

data = download_youtube_audio("https://www.youtube.com/watch?v=4y41vk6GpAc")


import os
import subprocess

def convert_to_wav(input_path: str) -> str:
    """Convert any audio/video file to 16 kHz mono WAV using FFmpeg."""
    output_path = os.path.splitext(input_path)[0] + "_converted.wav"
    subprocess.run(
        [
            "ffmpeg", "-y",        # -y: overwrite output if it exists
            "-i", input_path,      # input file (any format)
            "-vn",                 # ignore the video stream, if any
            "-ac", "1",            # mono
            "-ar", "16000",        # 16 kHz
            output_path,
        ],
        check=True,                # raise an error if FFmpeg fails
        capture_output=True,       # keep FFmpeg's noisy output out of your terminal
    )
    return output_path
convert_to_wav(data)

def chunk_audi0(wav_path: str , chunk_minutes: int = 10) -> list:
    audio = 