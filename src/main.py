# Import necessary libraries
import streamlit as st
from src.service.extract_youtube_data import get_youtube_data
from src.service.mongo_service import store_in_mongodb
from src.service.sql_service import migrate_to_sql,  search_sql_data


# Streamlit UI
def main():
    st.title("YouTube Data Harvesting App")

    # Sidebar for user input
    st.sidebar.header("Channel ID")
    channel_id = st.sidebar.text_input("Enter YouTube Channel ID")

    action = st.button("Retrieve YouTube Data and Store in MongoDB")

    youtube_data = {}
    if action:
        youtube_data = get_youtube_data(channel_id)
        st.write("YouTube Data Retrieved:", youtube_data)

        # Your MongoDB insertion code here
        msg = store_in_mongodb(youtube_data)
        st.write(msg)
    # Migrate data to SQL
    if st.button("Migrate to SQL"):
        migrate_to_sql(youtube_data)
        st.write("Data migrated to SQL")

    # Search and retrieve data from SQL
    st.sidebar.header("Search Options")
    search_options = {}  # Implement logic to get search options from user input
    if st.button("Search SQL Data"):
        result = search_sql_data( search_options)
        st.write("Search Results:", result)

if __name__ == "__main__":
    main()