import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv(".env")

# getting data from Billboard
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"
}

year_of_travel = input("Vous voulez une chanson de quel ann\xe9e? (Ann\xe9e-Mois-jour) :")
year = year_of_travel[0:4]
billboard_url = "https://www.billboard.com/charts/hot-100/" + year_of_travel
response = requests.get(billboard_url, headers=header)
web_page = response.text
soup = BeautifulSoup(web_page,"html.parser")
title_song = soup.select("li ul li h3")
titles = [song.getText().strip() for song in title_song]
print(titles)

# spotify access
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]

song_uris = []
for song in titles:
    result = sp.search(q=song, type="track", limit=1)
    try:
        uri = result["tracks"]['items'][0]['uri']
        song_uris.append(uri)
    except IndexError:
        print(f"La chanson: '{song}', n'est pas disponible sur Spotify...")
print(song_uris)
playlist_name = f"Billboard top 100 - {year}"
description = "Les 100 meilleurs chansons de Billboard."

playlist = sp.user_playlist_create(user=user_id,
                                   name=playlist_name,
                                   description=description,
                                   public=False)
# Adding songs to playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)