import requests
import streamlit as st
import pandas as pd
import math
from pathlib import Path

st.title("Explore The last.fm API")
if "token" in st.query_params:
    st.write("API Enabled")
else:
    st.write(f'''
         <a href="http://www.last.fm/api/auth/?api_key=68ec0071f9e7750afbd8f8f53d9659e0">
            <button>
                Enable API
            </button>
         </a>
        ''',
        unsafe_allow_html=True
    )

show_conan = st.sidebar.checkbox("Show Conan Gray Top Tags")
if show_conan:
    url = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=Conan+Gray&api_key=68ec0071f9e7750afbd8f8f53d9659e0&format=json"
    st.write(requests.get(url).json())

choose_artist = st.text_input("Which Artist Do You Like?")
if choose_artist:
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist={choose_artist}&api_key=68ec0071f9e7750afbd8f8f53d9659e0&format=json"
    # requests.get(url).json()["toptags"]["tag"]
    countweight = {}
    for name in tag:
        countweight[tag["name"]] = (100-("count"))/10

    times = {}

    for tag in requests.get(url).json()["toptags"]["tag"]:
        tagname = tag["name"]
        urltwo = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettopartists&tag={tagname}&limit=3&api_key=68ec0071f9e7750afbd8f8f53d9659e0&format=json"
        artists = requests.get(urltwo).json()["topartists"]["artist"]
        for artist in artists:
            if artist["name"] not in times:
               times[artist["name"]] = 1
            else:
               times[artist["name"]] += 1




    
    st.write(times)
    st.write(requests.get(url).json()["toptags"]["tag"])

