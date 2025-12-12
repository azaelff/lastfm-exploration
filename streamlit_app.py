import requests
import streamlit as st
import pandas as pd
import math
from pathlib import Path
import numpy as np


@st.cache_data
def getArtists(tagName):
    url = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettopartists&tag={tagName}&limit=1000&api_key=68ec0071f9e7750afbd8f8f53d9659e0&format=json"
    return requests.get(url).json()["topartists"]["artist"]


st.title("[L]ast.fm Artist Recommendation Algorithm")
if "token" in st.query_params:
    st.sidebar.write("API Enabled")
else:
    st.sidebar.write(f'''
         <a href="http://www.last.fm/api/auth/?api_key=68ec0071f9e7750afbd8f8f53d9659e0">
            <button>
                Enable API
            </button>
         </a>
        ''',
        unsafe_allow_html=True
    )

st.sidebar.write("How niche would you like your recommendations?")
minNiche = st.sidebar.slider("Minimum artist ranking:", 1, 999, 1)
maxNiche = st.sidebar.slider("Maximum artist ranking:", minNiche, 1000, min(minNiche + 9, 1000))
st.sidebar.write(f"Showing artists ranked between #{minNiche} and #{maxNiche}")

show_conan = st.sidebar.checkbox("Show Conan Gray Top Tags")
picture = st.sidebar.camera_input("Take a picture", disabled=not show_conan)
if picture:
    st.image(picture)

choose_artist = st.text_input("Which Artist Do You Like?")
if choose_artist:
    st.write(f"Similar Artists to {choose_artist}:")
    url = f"http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist={choose_artist}&api_key=68ec0071f9e7750afbd8f8f53d9659e0&format=json"
    tags = requests.get(url).json()["toptags"]["tag"]
    countweight = {}
    for tag in tags:
        countweight[tag["name"]] = tag["count"]/10

    data = pd.DataFrame([], columns = ["artist", "tags", "value"])

    for tag in requests.get(url).json()["toptags"]["tag"]:
        tagname = tag["name"]
        artists = getArtists(tagname)
        for artist in artists[minNiche:maxNiche]:
            existingRow = data[data["artist"]==artist["name"]]
            value = countweight[tagname]/10 + 100/(10+int(artist["@attr"]["rank"]))
            if existingRow.empty:
                data.loc[-1] = [artist["name"], [tagname], value]
                data.index += 1
            else:
                data.at[existingRow.index[0], "tags"].append(tagname)
                data.at[existingRow.index[0], "value"] += value

    
    df_final = data.sort_values("value", ascending=False).reset_index(drop=True)
    df_final.index += 1
    st.write(df_final)

    st.write(f'''
            <a href="https://forms.gle/ovHbXLhv2TcNYe2D6">
                <button>
                    After testing the algorithm, Give us your thoughts!
                </button>
            </a>
            ''',
            unsafe_allow_html=True
        )