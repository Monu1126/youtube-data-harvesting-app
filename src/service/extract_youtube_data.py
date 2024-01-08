from googleapiclient.discovery import build
from config.settings import API_KEY

#function to extract youtube data using channel id
def get_youtube_data(channel_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    channel_response = youtube.channels().list(
        id=channel_id,
        part='snippet,statistics,contentDetails,status'
    )
    channel_data = channel_response.execute()
    channel_name = {
    'channel_name' : channel_data['items'][0]['snippet']['title'],
    'Channel_Id' : channel_id,
    'Subscription_Count': channel_data['items'][0]['statistics']['subscriberCount'],
    'Channel_Views' : channel_data['items'][0]['statistics']['viewCount'] ,
    'channel_description' : channel_data['items'][0]['snippet']['description'],
    'playlists' : [],
    'playlist_name': [] } 

  # you have to fetch respectively more informative data's and create an dictionary for easy access

    playlist_response = youtube.playlists().list(
        channelId=channel_id,
        part='snippet,contentDetails'
    )
    playlist_response.execute()
    playlist_data = playlist_response.execute()
    playlists_names = []
    playlists = []
    Videos =[]

    for playlist in playlist_data['items']:
        playlists_names.append(playlist['snippet']['title'])
        playlists.append(playlist['id'])
        playListItem_response = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=playlist['id']
        )
        playlistItem_data = playListItem_response.execute()
   
        for item in playlistItem_data['items']:
                video_id = item['contentDetails']['videoId']
                video_response = youtube.videos().list(
                    part='snippet,contentDetails,statistics,id,status',
                    id=video_id
                ).execute()
                if video_response['items']:
                    vid = {
                        "Video_Id": video_id,
                        "Video_Name": video_response['items'][0]['snippet']['title'] if 'title' in video_response['items'][0]['snippet'] else "Not Available",
                        "Video_Description": video_response['items'][0]['snippet']['description'],
                        "Playlist_id": playlist['id'],
                        "Tags": video_response['items'][0]['snippet']['tags'],
                        "PublishedAt": video_response['items'][0]['snippet']['publishedAt'],
                        "View_Count": video_response['items'][0]['statistics']['viewCount'],
                        "Like_Count": video_response['items'][0]['statistics']['likeCount'],
                        "Favorite_Count":  video_response['items'][0]['statistics']['favoriteCount'],
                        "Comment_Count":  video_response['items'][0]['statistics']['commentCount'],
                        "Duration": video_response['items'][0]['contentDetails']['duration'],
                        "Thumbnail":  video_response['items'][0]['snippet']['thumbnails'],
                        "Caption_Status": "Available" if video_response['items'][0]['contentDetails']['caption']=="true" else "Not Available",
                        "Comments": []}
                    comments_response = youtube.commentThreads().list(
                    part="snippet,replies",
                    videoId=video_id
                    )
                    comments_data = comments_response.execute()
                    comments= []
                    for comment in comments_data['items']:
                        cid = {
                        "Comment_Id": comment['snippet']['topLevelComment']['id'],
                        "Comment_Text":comment['snippet']['topLevelComment']['snippet']['textDisplay'],
                        "Comment_Author": comment['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        "Comment_PublishedAt": comment['snippet']['topLevelComment']['snippet']["publishedAt"]
                        }
                        comments.append(cid)
                    vid['Comments'] = comments
                    Videos.append(vid)

    channel_name['playlists'] = playlists
    channel_name['playlist_name'] = playlists_names
        
    return {
         'channel_name' : channel_name,
         'Videos': Videos
    }
            