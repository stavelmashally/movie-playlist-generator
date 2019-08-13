import sys
import scraper
import spotipy
import spotipy.util as util

# User keys
SPOTIPY_CLIENT_ID = "your-spotify-client-id"
SPOTIPY_CLIENT_SECRET = "your-spotify-client-secret"
SPOTIPY_REDIRECT_URI = "http://localhost/"


def authenticate(username):
    # Authenticate with spotify
    scope = "playlist-modify-public playlist-modify-private"
    token = util.prompt_for_user_token(
        username=username,
        scope=scope,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )
    if not token:
        raise RuntimeError("Authentication failed")
    sp = spotipy.Spotify(auth=token)
    return sp


def main():
    if not len(sys.argv) > 1:
        raise RuntimeError("Required arguments")

    # Get the username from the prompt
    username = sys.argv[1]
    sp = authenticate(username)

    movie_name = str(input("Movie name: "))
    print("Fetching soundtrack...")
    # Get the soundtrack from imdb
    soundtrack = scraper.fetch_soundtrack(movie_name)
    # If there is a soundtrack to create a playlist
    if soundtrack:
        playlist_name = str(input("Playlist name: "))
        print("Creating playlist...")
        # First, create the playlist
        result = sp.user_playlist_create(username, playlist_name, public=True)
        playlist_id = result['id']
        # Search for the soundtracks in spotify
        for track in soundtrack:
            result = sp.search(track['Name'], limit=1)
            tracks = result['tracks']['items']
            if tracks:
                # Extract IDs of each track
                track_ids = [tracks[0]['id']]
                sp.user_playlist_add_tracks(username, playlist_id, track_ids)
        print('Playlist created successfully!')
    else:
        print("There is no soundtrack to this movie")


if __name__ == '__main__':
        main()
