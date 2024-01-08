
YOUTUBE DATA HARVESTING APPLICATION
===================================
Overview
---------
This project is a Streamlit application that allows users to access and analyze data from multiple YouTube channels. The application leverages the YouTube API for data retrieval, MongoDB for data storage, and a SQL database for data warehousing. Users can input a YouTube channel ID, retrieve relevant data, store it in a MongoDB data lake, migrate selected channels to a SQL database, and perform various searches on the stored data.

Prerequisites
=============
Before running the application, make sure you have the following installed:

Python (version 3.7 or later)
Pip (Python package installer)
Install the required Python packages using:
------------------------------------------
pip install -r requirements.txt

Configuration
=============

YouTube API Key:
---------------
Obtain a YouTube Data API Key from the Google Cloud Console.
Update the config.py file with your API key:
# /config/settings.py
YOUTUBE_API_KEY = "YOUR_YOUTUBE_API_KEY"

MongoDB:
--------
Ensure you have a MongoDB server running. Update the MongoDB connection details in the config.py file if needed:
# /config/settings.py
MONGODB_URI = "mongodb://localhost:27017/"

SQL Database:
-----------
Set up a SQL database (MySQL, PostgreSQL, etc.) and update the connection details in the config.py file:
# /config/settings.py
SQLALCHEMY_DATABASE_URI = "YOUR_SQL_DATABASE_URI"

Running the Application
=======================
Execute the following command to run the Streamlit app:
streamlit run app.py
Visit http://localhost:8501 in your web browser to access the application.

Usage
=====
Retrieve YouTube Data:
----------------------
Enter a YouTube Channel ID in the sidebar.
Click the "Retrieve YouTube Data and Store in MongoDB" button to fetch and store data in MongoDB.

Migrate to SQL:
--------------
After retrieving data for multiple channels, click the "Migrate to SQL" button to migrate selected channels to a SQL database.
Search and Retrieve from SQL:
----------------------------
Use the sidebar to select search options like "All Channels," "Channel by ID," "Channel with Videos," or "Specific Video."
View search results in a table.

Notes
=====
The application retrieves data for up to 10 different YouTube channels.
Ensure proper API key management and security practices.
Customize the MongoDB and SQL configurations based on your setup.

Contributors
Mukesh Kanna P