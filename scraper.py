from bs4 import BeautifulSoup
import requests

IMDB_BASE_URL = "https://www.imdb.com"

# OMDB API
OMDB_API_URL = "http://www.omdbapi.com"
OMDB_API_KEY = "your-omdb-api-key"


def get_movie_id(title):
    """
    Find the imdb movie id by title
    using the OMDB API
    """
    url = f"{OMDB_API_URL}/?apikey={OMDB_API_KEY}&t={title}"
    result = requests.get(url)
    status = result.status_code
    return (result.json()['imdbID'] if status == 200 else None)


def fetch_soundtrack(movie_name):
    """
    Return a list that includes the movie soundtrack
    from imdb
    """
    soundtrack = []
    movie_id = get_movie_id(movie_name)
    if movie_id:
        url = f"{IMDB_BASE_URL}/title/{movie_id}/soundtrack"
        # Get the HTML text to search for a soundtrack
        html_response = requests.get(url)
        soup = BeautifulSoup(html_response.text, "html.parser")
        html_soundtrack = soup.select(".soda")
        soundtrack = [extract(track_data) for track_data in html_soundtrack]
    return soundtrack


def extract(html_track):
    """Extract track information from HTML text"""
    track = {}
    track_details = html_track.text.split("\n")
    track['Name'] = track_details[0].strip()
    # Extract only the necessary data
    for line in track_details[1:]:
        if line.startswith("Performed by"):
            track['Performer'] = line[13:].split(",")[0]
        if line.startswith("Written and Performed by"):
            track['Performer'] = line[25:].split(",")[0]
        if line.startswith("Written by"):
            track['Writer'] = line[11:].split(",")[0]
        if line.startswith("Music by"):
            track['Music by'] = line[9:].split(",")[0]
    return track