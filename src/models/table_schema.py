from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

Base = declarative_base()

class Channel(Base):
    __tablename__ = 'channel'
    channel_id = Column(String, primary_key=True)
    channel_name = Column(String)
    channel_type = Column(String)
    channel_views = Column(Integer)
    channel_description = Column(Text)
    channel_status = Column(String)
    playlists = relationship('Playlist', back_populates='channel')

class Playlist(Base):
    __tablename__ = 'playlist'
    playlist_id = Column(String, primary_key=True)
    channel_id = Column(String, ForeignKey('channel.channel_id'))
    playlist_name = Column(String) 
    channel = relationship('Channel', back_populates='playlists')

class Video(Base):
    __tablename__ = 'video'
    video_id = Column(String, primary_key=True)
    playlist_id = Column(String, ForeignKey('playlist.playlist_id'))
    video_name = Column(String) 
    video_description = Column(Text)
    published_date = Column(DateTime)
    view_count = Column(Integer)
    like_count = Column(Integer) 
    favorite_count = Column(Integer)
    comment_count = Column(Integer)
    duration = Column(Integer)
    thumbnail = Column(String)
    caption_status = Column(String)
    playlist = relationship('Playlist')
    
class Comment(Base):
    __tablename__ = 'comment'
    comment_id = Column(String, primary_key=True)
    video_id = Column(String, ForeignKey('video.video_id'))
    comment_text = Column(Text) 
    comment_author = Column(String)
    comment_published_date = Column(DateTime)
    video = relationship('Video')

# Create engine and tables
engine =create_engine("mysql+mysqlconnector://root@localhost/leo")
Base.metadata.create_all(engine)

# Create a SQL session
Session = sessionmaker(bind=engine)
sql_session = Session()

# Your migration code here

# Commit changes and close session
sql_session.commit()
sql_session.close()
