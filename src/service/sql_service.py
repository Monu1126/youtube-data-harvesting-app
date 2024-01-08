
from src.service.mongo_service import get_mongoClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.models.table_schema import Channel, Playlist, Video, Comment
import json
import streamlit as st
import pandas as pd

# Create a connection string for SQLAlchemy
def get_sql_engine():
     connection_string = f"mysql+mysqlconnector://root@localhost/leo"
     Base = declarative_base()
     sql_engine = create_engine(connection_string, echo=True)
     Base.metadata.create_all(sql_engine)
     # Create the SQLAlchemy engine
     return sql_engine

#get MongoDB and SQL connection details
mongo_client = get_mongoClient()
mongodb = mongo_client['youtube-data']
collection = mongodb['yt']
sql_engine = get_sql_engine()


# Function to migrate data from MongoDB to SQL
def migrate_to_sql():
    # Create SQL tables

    # Create a SQL session
     Session = sessionmaker(bind=sql_engine)
     sql_session = Session()

    # Query data from MongoDB
     mongo_cursor = collection.find()
     for mongo_document in mongo_cursor:
          mongo_id = mongo_document["_id"]
          channel_name = mongo_document["channel_name"]
          videos = mongo_document["Videos"]

          channel_instance = Channel(
               channel_id=channel_name['Channel_Id'],
               channel_name=channel_name['channel_name'],
               channel_type='entertainment',
               channel_views=channel_name['Channel_Views'],
               channel_description=channel_name['channel_description'],
               channel_status='Available'
          )
          sql_session.add(channel_instance)

          for i in range(0, len(channel_name['playlists'])):
               playlist_instance = Playlist(
                    playlist_id = channel_name['playlists'][i],
                    channel_id = channel_name['Channel_Id'],
                    playlist_name = channel_name['playlist_name'][i],  
               )
               sql_session.add(playlist_instance)
    
          for video in videos:
               video_instance = Video(
                    video_id = video['Video_Id'],
                    playlist_id = video['Playlist_id'],
                    video_name = video['Video_Name'], 
                    video_description = json.dumps(video['Video_Description']),
                    published_date = video['PublishedAt'],
                    view_count = video['View_Count'],
                    like_count = video['Like_Count'], 
                    favorite_count = video['Favorite_Count'],
                    comment_count = video['Comment_Count'],
                    duration = video['Duration'],
                    thumbnail = json.dumps(video['Thumbnail']),
                    caption_status = video['Caption_Status']
               )
               sql_session.add(video_instance)

          for video in videos:
               comments = video['Comments']
               for comment in comments:
                    comment_instance = Comment(
                         comment_id = comment['Comment_Id'],
                         video_id = video['Video_Id'],
                         comment_text = json.dumps(comment['Comment_Text']),
                         comment_author = comment['Comment_Author'],
                         comment_published_date = comment['Comment_PublishedAt']
                    )
                    sql_session.add(comment_instance)

          
    # Commit changes and close session
     sql_session.commit()
     sql_session.close()


# Function to search data in SQL
def search_sql_data(search_option):
     Session = sessionmaker(bind=sql_engine)
     session = Session()
     final_result = None
     # Perform different searches based on the selected option
     if search_option == 'All Channels':
          result = session.query(Channel).all()
          final_result = [{'channel_id': channel.channel_id, 'channel_name': channel.channel_name, 'channel_type': channel.channel_type, 'channel_views': channel.channel_views, 'channel_description': channel.channel_description, 'channel_status': channel.channel_status} for channel in result]

     elif search_option == 'Channel by ID':
          channel_id = st.text_input('Enter Channel ID:')
          if channel_id:
               result = session.query(Channel).filter_by(channel_id=channel_id).first()
               if result: 
                    final_result = {'channel_id': result.channel_id, 'channel_name': result.channel_name, 'channel_type': result.channel_type, 'channel_views': result.channel_views, 'channel_description': result.channel_description, 'channel_status': result.channel_status}

     elif search_option == 'Channel with Videos':
          channel_id_with_videos = st.text_input('Enter Channel ID with Videos:')
          if channel_id_with_videos:
               result = (
                    session.query(Channel, Playlist, Video)
                    .join(Playlist, Channel.channel_id == Playlist.channel_id)
                    .join(Video, Playlist.playlist_id == Video.playlist_id)
                    .filter(Channel.channel_id == channel_id_with_videos).all()
               )
               if result:
                    final_result = [{'channel_id': channel.channel_id, 'channel_name': channel.channel_name, 'playlist_id': playlist.playlist_id,
                         'playlist_name': playlist.playlist_name,'video_id': video.video_id,'video_name': video.video_name} for  channel, playlist, video in result]

     elif search_option == 'Specific Video':
          channel_id_specific_video = st.text_input('Enter Channel ID for Specific Video:')
          video_id_specific_video = st.text_input('Enter Video ID:')
          if channel_id_specific_video and video_id_specific_video:
               result = (
                    session.query(Channel, Playlist, Video)
                    .join(Playlist, Channel.channel_id == Playlist.channel_id)
                    .join(Video, Playlist.playlist_id == Video.playlist_id)
                    .filter(Channel.channel_id == channel_id_specific_video, Video.video_id == video_id_specific_video)
                    .first()
               )
               if result:
                    channel, playlist, video = result
                    final_result = {'channel_id': channel.channel_id, 'channel_name': channel.channel_name, 'playlist_id': playlist.playlist_id,
                         'playlist_name': playlist.playlist_name,'video_id': video.video_id,'video_name': video.video_name}




     # Close the session
     session.close()
     return final_result

