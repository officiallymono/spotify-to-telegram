from string import Template

# Telegram
api_id = 27042773
api_hash = "c0cfae0388612f6006c83a735718778f"
is_premium = False

# Telegram Bio
default_bio = "Meow!"
nowplay_bio = Template("🎧 Now Playing: $artist — $track")
use_bio_nowplay = False

# Telegram Channel Message
use_channel_nowplay = True
chat_id = "SHLSAL"
message_id = 3
account = "open.spotify.com/user/31ahyhpqshvgaprpk2xshxfnspfe?si=bb2d223c99a14b7c"
default_message = f"Nothing!"
nowplay_message = Template("""♪ 𝖭𝗈𝗐 𝗉𝗅𝖺𝗒𝗂𝗇𝗀:  
[$track]($spotify) — $artist
`$elapsed_time` $progress_bar `$total_time`
➔ [𝖮𝗍𝗁𝖾𝗋 𝗅𝗂𝗇𝗄𝗌]($other)""")


# Spotify
client_id = "ec85dc5f6a0a4fdd81b93bcf0b6ab8ea"
client_secret = "a9ca928905284d809b2f1195eea686b8"
username = "31ahyhpqshvgaprpk2xshxfnspfe"
redirect_uri = "http://localhost:8888/callback"
scope = "user-read-currently-playing"

# Progress Bar Settings
progress_bar_length = 12  # Length of the progress bar in characters
progress_bar_filled = "━"  # Character to represent filled progress
progress_bar_empty = "─"  # Character to represent unfilled progress
progress_bar_center = "●"  # Character for the center marker
