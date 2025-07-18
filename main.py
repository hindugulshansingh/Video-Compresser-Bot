import os
import subprocess
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("compressor_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

quality_options = {
    "240p": "scale=-2:240",
    "360p": "scale=-2:360",
    "480p": "scale=-2:480"
}

@app.on_message(filters.video | (filters.document & filters.video))
async def ask_quality(client, message: Message):
    await message.reply(
        "📥 Video received. Select compression quality:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("240p", callback_data="compress_240p")],
            [InlineKeyboardButton("360p", callback_data="compress_360p")],
            [InlineKeyboardButton("480p", callback_data="compress_480p")]
        ])
    )

@app.on_callback_query()
async def compress_callback(client, callback_query):
    await callback_query.answer()
    data = callback_query.data
    quality = data.split('_')[1]

    message = callback_query.message.reply_to_message
    if not message:
        return

    media = message.video or message.document
    if not media:
        return

    input_path = f"{media.file_id}_input"
    output_path = f"{media.file_id}_{quality}.mp4"
    await message.download(file_name=input_path)

    cmd = [
        "ffmpeg", "-i", input_path,
        "-vf", quality_options[quality],
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "28",
        "-c:a", "aac", "-b:a", "64k",
        output_path
    ]
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if not os.path.exists(output_path):
        return

    await client.send_video(
        chat_id=message.chat.id,
        video=output_path
    )

    os.remove(input_path)
    os.remove(output_path)

app.run()
