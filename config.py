from string import Template

# Telegram
api_id = 27042773
api_hash = "c0cfae0388612f6006c83a735718778f"
is_premium = False

#  Telegram Bio
use_bio_nowplay = False
default_bio = "Default Bio"
nowplay_bio = Template("🎧 Now Playing: $artist — $track")

#  Telegram Channel Message
use_channel_nowplay = True
chat_id = SHLSAL
message_id = 3
account = "open.spotify.com/user/31ahyhpqshvgaprpk2xshxfnspfe?si=bb2d223c99a14b7c"
default_message = f"ain't listening to anything rn!| [Spotify Account]({account})"
nowplay_message = Template(f"🎶 Now Playing: \n[$track — $artist]($spotify)\n[Other Links]($other) | [My Account]({account})")

# Spotify
client_id = "b9717f064476401fb3f89d819b380b39"
client_secret = "435b94f7e4ae47619051fa5cf8ba8dd6"
username = "31ahyhpqshvgaprpk2xshxfnspfe"
redirect_uri = "http://5.75.202.115:8889"
scope = "user-read-currently-playing"
