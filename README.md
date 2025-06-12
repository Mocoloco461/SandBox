# SandBox

This project downloads a collection of YouTube videos as MP3 files.
All URLs are listed in `links.txt` and downloaded to the folder
`שער הביטחון והאמונה`.

## Usage

Run the `download.sh` script from a terminal:

```bash
./download.sh
```

The script automatically installs `yt-dlp` and a static `ffmpeg` binary
(if they are missing) and then downloads every link from `links.txt`
into the target directory.
