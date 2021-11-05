import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="ffc4c1c607de49489dc5b071b326727e",
                                                           client_secret="4fd9dfe58f914768b24a034e1da88c2b"))

# song = sp.track('spotify:track:4KJQkJSDOvQtSDf9rRn25n')
# print(song['preview_url'])

playlist_uri = sp.playlist('spotify:playlist:4taxX9mVX4deBsqG6ffEbP')
# dict_keys(['collaborative', 'description', 'external_urls', 'followers', 'href', 'id', 'images', 'name', 'owner', 'primary_color', 'public', 'snapshot_id', 'tracks', 'type', 'uri']) ของplaylist
#a = playlist_uri['tracks']['items']  # playlist
a = playlist_uri['name']
# dict_keys(['added_at', 'added_by', 'is_local', 'primary_color', 'track', 'video_thumbnail']) ของแต่ละitems
# dict_keysของtrack(['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'episode', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track', 'track_number', 'type', 'uri'])

# แต่ละlistจะมีdictอีกที
#count = 0
#playlistObj = {}
#for i in a:
#    songObj = {
#        "artist": i['track']['artists'][0]['name'],
#        "image": i['track']['album']['images'][0]['url'],
#        "song": i['track']['name'],
#        "uri": i['track']['preview_url']
#    }
#    playlistObj[f"{count}"] = songObj
#    count += 1
#print(playlistObj["2"]["song"])
print(a)