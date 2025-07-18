import os
import re
import asyncio
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("compressor", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

quality_options = {
    "240p": "scale=-2:240",
    "360p": "scale=-2:360",
    "480p": "scale=-2:480"
}

def clean_caption(caption):
    if not caption:
        return "🌟 Extracted By : @GUL5H4N 🖤"
    caption = re.sub(r"https?://\S+|www\.\S+", "", caption)  # remove links
    return caption.strip() + "\n\n🌟 Extracted By : @GUL5H4N 🖤"

@app.on_message(filters.video | filters.document.video)
async def ask_quality(client, message: Message):
    await message.reply(
        "📥 Video received. Select compression quality:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("240p", callback_data=f"compress_240p")],
            [InlineKeyboardButton("360p", callback_data=f"compress_360p")],
            [InlineKeyboardButton("480p", callback_data=f"compress_480p")],
        ])
    )

@app.on_callback_query()
async def compress_callback(client, callback_query):
    await callback_query.answer()
    data = callback_query.data
    quality = data.split('_')[1]
    message = callback_query.message.reply_to_message
    media = message.video or message.document
    caption = clean_caption(media.caption)

    msg = await callback_query.message.edit_text(f"📥 Downloading video...")
    input_path = f"{media.file_id}_input"
    output_path = f"{media.file_id}_{quality}.mp4"
    await message.download(file_name=input_path)

    await msg.edit(f"⚙️ Compressing to {quality}...")
    cmd = [
        "ffmpeg", "-i", input_path,
        "-vf", quality_options[quality],
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
        "-c:a", "aac", "-b:a", "64k",
        output_path
    ]
    process = subprocess.run(cmd)

    if process.returncode != 0 or not os.path.exists(output_path):
        await msg.edit("❌ Compression failed.")
        os.remove(input_path)
        return

    await msg.edit("📤 Uploading...")
    await message.reply_video(output_path, caption=caption)
    os.remove(input_path)
    os.remove(output_path)
    await msg.delete()

app.run()
