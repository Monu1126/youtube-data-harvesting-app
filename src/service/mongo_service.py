import streamlit as st
from pymongo import MongoClient
from config.settings import MONGO_URI, MONGO_DB

# Function to store in MoongoDB
def store_in_mongodb(data):
    try:
        client = get_mongoClient()   
        db = client[MONGO_DB]
        collection = db['yt']
        collection.insert_one(data)
    except Exception as e:
        st.error(f"Error during data insertion: {e}")
    finally:
        client.close()
    return "Stored successfully"

 # Connect to MongoDB
def get_mongoClient():
    return MongoClient(MONGO_URI)  
