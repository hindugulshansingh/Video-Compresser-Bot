from pyrogram import Client, filters
import os
import subprocess

API_ID = 26259762
API_HASH = "6f33406b8cb80f659d268fccd7329b0f"
BOT_TOKEN = "7876584681:AAFosfsph9Bbd4EknXP885_DobBmwdCSwXk"

app = Client("video_compressor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.video)
async def compress_video(client, message):
    video = message.video
    if video.file_size > 100 * 1024 * 1024:
        await message.reply("🚫 Video size limit 100MB tak hai.")
        return

    msg = await message.reply("📥 Downloading video...")

    input_path = f"{video.file_id}.mp4"
    output_path = f"compressed_{video.file_id}.mp4"
    await message.download(file_name=input_path)

    await msg.edit("⚙️ Compressing to 360p...")
    cmd = [
        "ffmpeg", "-i", input_path,
        "-vf", "scale=-2:360",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
        "-c:a", "aac", "-b:a", "64k",
        output_path
    ]
    subprocess.run(cmd)

    await msg.edit("📤 Uploading...")
    await message.reply_video(output_path, caption="✅ Converted to 360p")

    os.remove(input_path)
    os.remove(output_path)
    await msg.delete()

app.run()
