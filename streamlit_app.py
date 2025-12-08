import requests
import streamlit as st
import pandas as pd
import math
from pathlib import Path
import numpy as np

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
    tags = requests.get(url).json()["toptags"]["tag"]
    countweight = {}
    for tag in tags:
        countweight[tag["name"]] = (100-tag["count"])/10

    data = pd.DataFrame([], columns = ["tags", "artist", "value"])

    for tag in requests.get(url).json()["toptags"]["tag"]:
        tagname = tag["name"]
        urltwo = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettopartists&tag={tagname}&limit=3&api_key=68ec0071f9e7750afbd8f8f53d9659e0&format=json"
        artists = requests.get(urltwo).json()["topartists"]["artist"]
        for artist in artists:
            existingRow = data[data["artist"]==artist["name"]]
            value = 10/19*(20 - (countweight[tagname] + int(artist["@attr"]["rank"])))
            if existingRow.empty:
                data.loc[-1] = [[tagname], artist["name"], value]
                data.index += 1
            else:
                data.at[existingRow.index[0], "tags"].append(tagname)
                data.at[existingRow.index[0], "value"] += value

    

    st.write(data.sort_values("value", ascending=False))

