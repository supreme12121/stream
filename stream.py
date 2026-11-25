import asyncio
import logging
import os

import discord
from discord.ext.native_voice import FFmpegMediaSource, StreamClient, VoiceClient

logging.basicConfig(level=logging.DEBUG)  # lower to INFO once it works

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("token not entered")
CHANNEL_ID = "1575118260515635221" # voice channel id
VIDEO_FILE = "test.mp4"

client = discord.Client()
started = False  # on_ready can fire more than once


@client.event
async def on_ready():   
    global started
    if started:
        return
    started = True
    print(f"[+] Logged in as {client.user}")

    try:
        channel = client.get_channel(CHANNEL_ID) or await client.fetch_channel(CHANNEL_ID)
        print(f"[*] Joining {channel}...")
        voice = await channel.connect(cls=VoiceClient)
        print("[+] Joined voice.")

        print("[*] Creating Go Live stream...")
        stream = await voice.create_stream(cls=StreamClient)
        print("[+] Stream created.")

        source = FFmpegMediaSource.from_file(
            VIDEO_FILE,
            "H264",
            width=1280,
            height=720,
            fps=30,
            bitrate=4_000_000,
        )
        stream.play(source)
        print("[+] Playing. Press Ctrl+C to stop.")

    except Exception as e:
        logging.exception("Failed")
        await client.close()


client.run(TOKEN)
