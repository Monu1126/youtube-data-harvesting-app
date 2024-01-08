import streamlit as st
from src.service.extract_youtube_data import get_youtube_data
from src.service.mongo_service import store_in_mongodb
from src.service.sql_service import migrate_to_sql,  search_sql_data
import pandas as pd


def stream_app(): 
    st.title("YouTube Data Harvesting App")

    # Sidebar for user input
    st.sidebar.header("Channel ID")
    channel_id = st.sidebar.text_input("Enter YouTube Channel ID")

    action = st.button("Retrieve YouTube Data and Store in MongoDB")

    if action:
        if channel_id:
            # get youtube data
            youtube_data = get_youtube_data(channel_id)
            st.write("YouTube Data Retrieved:", youtube_data)
            # store in mongo db
            msg = store_in_mongodb(youtube_data)
            st.write(msg)
        else:
             st.warning("Enter Channel Id to retrieve data")
           
       
    # Migrate data to SQL
    if st.button("Migrate to SQL"):
        migrate_to_sql()
        st.write("Data migrated to SQL")

    # Search and retrieve data from SQL
    st.sidebar.header("Search Options")

    # Search options
    search_option = st.selectbox('Select Search Option', ['All Channels', 'Channel by ID', 'Channel with Videos', 'Specific Video'])
    result = search_sql_data(search_option)
    # Display the result
    if result:
          st.write('Search Result:')
          df = pd.DataFrame(result, index=[0])
          st.table(df)
    else:
          st.warning('No result found.')

   

