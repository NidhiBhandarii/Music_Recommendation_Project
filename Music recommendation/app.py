import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        # Default image if no result is found
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    try:
        index = music[music['song'] == song].index[0]
    except IndexError:
        return [], []

    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]]['artist']
        song_name = music.iloc[i[0]]['song']
        recommended_music_posters.append(get_song_album_cover_url(song_name, artist))
        recommended_music_names.append(song_name)

    return recommended_music_names, recommended_music_posters

st.header('Music Recommender System')

# Load data
try:
    music = pickle.load(open('df.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError as e:
    st.error(f"Error loading files: {e}")
    st.stop()

print(music)

# Song selection
music_list = music['song'].values
selected_song = st.selectbox("Type or select a song from the dropdown", music_list)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_song)

    if not recommended_music_names:
        st.write("No recommendations available.")
    else:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            if idx < len(recommended_music_names):
                col.text(recommended_music_names[idx])
                col.image(recommended_music_posters[idx])
