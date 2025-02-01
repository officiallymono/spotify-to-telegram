import spotipy
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import httpx
from httpx import AsyncClient
from loguru import logger
from pyrogram import filters
from pyrogram.client import Client
from pyrogram.enums.parse_mode import ParseMode
from pyrogram.errors.exceptions.bad_request_400 import MessageNotModified
from pyrogram.handlers.message_handler import MessageHandler
from pyrogram.types import Message
from spotipy.oauth2 import SpotifyOAuth

from config import (
    api_hash,
    api_id,
    client_id,
    client_secret,
    redirect_uri,
    scope,
    username,
    chat_id,
    default_message,
    message_id,
    nowplay_message,
    use_channel_nowplay,
    progress_bar_length,
    progress_bar_filled,
    progress_bar_center,
    progress_bar_empty,
    genius_api_key,
)


def create_progress_bar(progress: float) -> str:
    """Creates a progress bar based on the current track progress.
    
    Args:
        progress (float): Current progress ratio (0.0 to 1.0)
    
    Returns:
        str: Formatted progress bar
    """
    filled_length = int(progress * progress_bar_length)
    empty_length = progress_bar_length - filled_length  # calculate empty section correctly

    middle_position = int(progress * progress_bar_length)

    # نوار پروگرس با کاراکترهای پر شده، خالی و نقطه وسط
    bar = progress_bar_filled * middle_position + progress_bar_center + progress_bar_empty * (empty_length - 1)

    return f"{bar}"



import time

def format_time(ms: int) -> str:
    """Converts milliseconds to a formatted time string (MM:SS)"""
    minutes, seconds = divmod(ms // 1000, 60)
    return f"{minutes:02}:{seconds:02}"

async def get_odesli_url(url: str) -> str:
    """Fetches odesli URL from Spotify track URL."""
    try:
        async with AsyncClient() as client:
            response = await client.get(
                url=f"https://odesli.co/{url}", follow_redirects=True
            )
            return response.url
    except Exception as e:
        logger.error(f"Failed to fetch odesli URL: {e}")
        return "Error"

async def create_message(spotify: spotipy.Spotify) -> str:
    """Creates a message with odesli and Spotify links, and adds Genius link."""
    current_song = spotify.current_user_playing_track()
    if current_song is None or not current_song["is_playing"]:
        logger.info("Nothing playing")
        return default_message

    track = current_song["item"]["name"]
    artist = current_song["item"]["artists"][0]["name"]
    url = current_song["item"]["external_urls"]["spotify"]


    other_url = await get_odesli_url(url) 

    duration_ms = current_song["item"]["duration_ms"]
    progress_ms = current_song["progress_ms"]
    progress_ratio = progress_ms / duration_ms if duration_ms > 0 else 0.0
    elapsed_time = format_time(progress_ms)
    total_time = format_time(duration_ms)
    progress_bar = create_progress_bar(progress_ratio)

    new_message = nowplay_message.substitute(
        artist=artist, track=track, spotify=url, progress_bar=progress_bar,
        elapsed_time=elapsed_time, total_time=total_time, other=other_url,
    )

    logger.info(new_message)
    return new_message



async def update_message(
    app: Client, spotify: spotipy.Spotify, chat_id: int, message_id: int
) -> None:
    """Updates the message with the current song and progress bar

    Args:
        app (Client): Pyrogram client
        spotify (spotipy.Spotify): Spotify client
        chat_id (int): Chat ID
        message_id (int): Message ID
    """
    # Await create_message to get the generated message
    text = await create_message(spotify=spotify)

    try:
        await app.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=str(text),
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )
    except MessageNotModified:
        pass


async def send_message(message: Message) -> None:
    """Sends a message with the current song and progress bar

    Args:
        message (Message): Telegram message to edit
    """
    global spotify
    # Await create_message to get the generated message
    text = await create_message(spotify=spotify)

    await message.edit_text(
        text=str(text),
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
    )



if __name__ == "__main__":
    logger.info("Starting Pyrogram...")
    app = Client(name="spotify_to_bio", api_id=api_id, api_hash=api_hash)

    logger.info("Starting Spotify...")
    spotify = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
            username=username,
            scope=scope,
        ),
        language="ru",
    )

    nowplay_handler = MessageHandler(
        callback=send_message,
        filters=(filters.command("nowplay", "!")),
    )
    app.add_handler(nowplay_handler)

    scheduler = AsyncIOScheduler()

    if use_channel_nowplay:
        scheduler.add_job(
            func=update_message,
            kwargs={
                "app": app,
                "spotify": spotify,
                "chat_id": chat_id,
                "message_id": message_id,
            },
            trigger="interval",
            seconds=17,
        )

    scheduler.start()
    app.run()
