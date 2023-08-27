# Import Necessary Library
import json
import boto3
from datetime import datetime
from io import StringIO
import pandas as pd

# Function to read album data
def album(data):
    
    # Create empty list as storage of album element
    album_list = []
    
    # Get relevan album data and append it to the list
    for row in  data['items']:
        album_id = row['track']['album']['id']
        album_name = row['track']['album']['name']
        album_release_date = row['track']['album']['release_date']
        album_total_tracks = row['track']['album']['total_tracks']
        album_url = row['track']['external_urls']['spotify']
        album_elemen = {"album_id": album_id,
                        "name": album_name,
                        "release_date": album_release_date,
                        "total_tracks": album_total_tracks,
                        "url": album_url}
        album_list.append(album_elemen)
    return album_list

# Function to read artist data
def artist(data):
    
    # Create empty list as storage of artist element
    artist_list = []
    
    # Get relevan artist data and append it to the list
    for row in data['items']:
        for key, value in row.items():
            if key=='track':
                for artist in value['artists']:
                    artist_dict = {"artist_id": artist['id'],
                                   "artist_name": artist['name'],
                                   "external_url": artist['href']}
                    artist_list.append(artist_dict)
    return artist_list

# Function to read artist data
def song(data):
    
    # Create empty list as storage of artist element
    song_list = []
    
    # Get relevan artist data and append it to the list
    for row in data['items']:
        song_id = row['track']['id']
        song_name = row['track']['name']
        song_duration = row['track']['duration_ms']
        song_url = row['track']['external_urls']['spotify']
        song_popularity = row['track']['popularity']
        song_added = row['added_at']
        album_id = row['track']['album']['id']
        artist_id = row['track']['album']['artists'][0]['id']
        song_element = {
            'song_id' : song_id,
            'song_name' : song_name,
            'duration_ms' : song_duration,
            'url' : song_url,
            'popularity' : song_popularity,
            'song_added' : song_added,
            'album_id' : album_id,
            'artist_id' : artist_id,
        }
        song_list.append(song_element)
    return song_list


# Function to transform data
def lambda_handler(event, context):
    
    # Create a connection to S3 and load the raw json file
    s3 = boto3.client('s3')
    Bucket = "spotify-etl-aug"
    Key = "raw_data/to_processed/"
    
    # Create empty list as sotrage of file name and content of the files
    spotify_data = []
    spotify_keys = []
    
    # Acces the filename and content from raw folder 
    for file in s3.list_objects(Bucket=Bucket, Prefix=Key)['Contents']:
        file_key = file['Key']
        if file_key.split(".")[-1] == "json":
            response = s3.get_object(Bucket=Bucket, Key=file_key)
            content = response["Body"]
            jsonObject = json.loads(content.read())
            spotify_data.append(jsonObject)
            spotify_keys.append(file_key)
    
    # Transformed Data
    for data in spotify_data:
        
        # Applied function to get album, artist, and song data
        album_list = album(data)
        artist_list = artist(data)
        song_list = song(data)
        
        # Transform album data
        # Convert it to dataframe object
        album_df = pd.DataFrame.from_dict(album_list)
        
        # Drop duplicates id
        album_df = album_df.drop_duplicates(subset="album_id")
        
        # Convert type of date data as date type
        album_df['release_date'] = pd.to_datetime(album_df['release_date'])
        
        # Transform artist data
        # Convert artist data to dataframe object
        artist_df = pd.DataFrame.from_dict(artist_list)
        
        # Drop dupllicates id
        artist_df = artist_df.drop_duplicates(subset="artist_id")
        
        # Transform song data
        # Convert it to dataframe object
        song_df = pd.DataFrame.from_dict(song_list)
        
        # Drop duplicates id
        song_df = song_df.drop_duplicates(subset="song_id")
        
        # convert type of date data as date type
        song_df['song_added'] = pd.to_datetime(song_df['song_added'])
        
        # Save Transformed data
        # Save song data to S3 as csv file
        song_key =  "transformed_data/songs_data/song_transformed_" + str(datetime.now())+ ".csv"
        song_buffer = StringIO()
        song_df.to_csv(song_buffer, index=False)
        song_content = song_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=song_key, Body=song_content)
        
        # Save album data to S3 as csv file
        album_key =  "transformed_data/album_data/album_transformed_" + str(datetime.now())+ ".csv"
        album_buffer = StringIO()
        album_df.to_csv(album_buffer, index=False)
        album_content = album_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=album_key, Body=album_content)
        
        # Save artist data to S3 as csv file
        artist_key =  "transformed_data/artists_data/artist_transformed_" + str(datetime.now())+ ".csv"
        artist_buffer = StringIO()
        artist_df.to_csv(artist_buffer, index=False)
        artist_content = artist_buffer.getvalue()
        s3.put_object(Bucket=Bucket, Key=artist_key, Body=artist_content)
        
    # Copy raw file to processed folder and delete raw file in to_processed f   
    s3_resource = boto3.resource("s3")
    for key in spotify_keys:
        copy_source = {
            "Bucket" : Bucket,
            "Key" : key
        }
        s3_resource.meta.client.copy(copy_source, Bucket, "raw_data/processed/ "+key.split("/")[-1])
        s3_resource.Object(Bucket, key).delete()