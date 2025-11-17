import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-follow-read",
    )
)


def get_followed_artists():
    artist_names = []
    response = sp.current_user_followed_artists(limit=50)

    while True:
        items = response["artists"]["items"]

        # Collect only the names
        artist_names.extend([artist["name"] for artist in items])

        # Handle pagination
        after = response["artists"]["cursors"]["after"]
        if after:
            response = sp.current_user_followed_artists(limit=50, after=after)
        else:
            break

    return artist_names
