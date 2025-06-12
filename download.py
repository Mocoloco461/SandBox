import os
import sys
import subprocess
import shutil
from pathlib import Path
import urllib.request
import tarfile
import zipfile

OUT_DIR = Path('שער הביטחון והאמונה')
BIN_DIR = Path('bin')
OUT_DIR.mkdir(exist_ok=True)
BIN_DIR.mkdir(exist_ok=True)


def ensure_package(pkg: str):
    try:
        __import__(pkg)
    except ImportError:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', '--user', pkg])


def ensure_ffmpeg() -> Path:
    ffmpeg = shutil.which('ffmpeg')
    if ffmpeg:
        return Path(ffmpeg)

    print('ffmpeg not found. Downloading static build...')
    platform = sys.platform
    if platform.startswith('linux'):
        url = 'https://github.com/yt-dlp/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-linux64-gpl.tar.xz'
        archive = BIN_DIR / 'ffmpeg.tar.xz'
        urllib.request.urlretrieve(url, archive)
        with tarfile.open(archive) as tar:
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith('/ffmpeg'):
                    member.name = os.path.basename(member.name)
                    tar.extract(member, BIN_DIR)
                    ffmpeg_path = BIN_DIR / 'ffmpeg'
                    ffmpeg_path.chmod(0o755)
                    break
        archive.unlink()
    elif platform == 'win32':
        url = 'https://github.com/yt-dlp/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-win64-gpl.zip'
        archive = BIN_DIR / 'ffmpeg.zip'
        urllib.request.urlretrieve(url, archive)
        with zipfile.ZipFile(archive) as z:
            for name in z.namelist():
                if name.endswith('ffmpeg.exe'):
                    z.extract(name, BIN_DIR)
                    extracted = BIN_DIR / name
                    ffmpeg_path = BIN_DIR / 'ffmpeg.exe'
                    extracted.rename(ffmpeg_path)
                    break
        archive.unlink()
    elif platform == 'darwin':
        url = 'https://github.com/yt-dlp/FFmpeg-Builds/releases/latest/download/ffmpeg-master-latest-macos64-gpl.zip'
        archive = BIN_DIR / 'ffmpeg.zip'
        urllib.request.urlretrieve(url, archive)
        with zipfile.ZipFile(archive) as z:
            for name in z.namelist():
                if name.endswith('ffmpeg'):
                    z.extract(name, BIN_DIR)
                    extracted = BIN_DIR / name
                    ffmpeg_path = BIN_DIR / 'ffmpeg'
                    extracted.rename(ffmpeg_path)
                    ffmpeg_path.chmod(0o755)
                    break
        archive.unlink()
    else:
        raise RuntimeError('Unsupported OS for automatic ffmpeg download.')
    return ffmpeg_path


def main():
    ensure_package('yt_dlp')
    from yt_dlp import YoutubeDL

    ffmpeg_path = ensure_ffmpeg()

    ydl_opts = {
        'format': 'bestaudio/best',
        'ffmpeg_location': str(ffmpeg_path),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': str(OUT_DIR / '%(title)s.%(ext)s'),
    }

    with open('links.txt', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(links)


if __name__ == '__main__':
    main()
