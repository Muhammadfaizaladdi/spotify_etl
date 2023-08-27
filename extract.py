# Import necessary Libraries
import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime

def lambda_handler(event, context):
    
    # get client id and secret key
    client_id = os.environ.get('client_id')
    client_secret = os.environ.get('client_secret')
    
    # Authentication process to connet to spotify App
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, 
                                                          client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # Get the URI of spotify top global songs
    playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f&nd=1"
    playlist_uri = playlist_link.split("/")[-1].split("?")[0]
    
    # get list of tracks from top global songs
    spotify_data = sp.playlist_tracks(playlist_uri)
    
    # Create object connection to S3 Bucket
    client = boto3.client('s3')
    
    # Create Filename that will be saved
    filename = "spotify_raw" + str(datetime.now()) + ".json"
    
    # Save the data into the destination folder
    client.put_object(
        Bucket="spotify-etl-aug",
        Key="raw_data/to_processed/"+filename,
        Body=json.dumps(spotify_data)
        )