# Ultimate Telegram Video Compressor Bot

## 🔥 Features
- Select video quality (240p / 360p / 480p)
- Keeps original caption (removes links)
- Adds custom credit: 🌟 Extracted By : @GUL5H4N 🖤
- Shows status: Downloading, Compressing, Uploading
- Works with all formats (MP4, MKV, etc.)
- Docker + .env secure config

## 🐳 Docker Run
```bash
docker build -t gulshan-video-bot .
docker run --env-file .env gulshan-video-bot
```

Replace `your_bot_token_here` in `.env` file.
