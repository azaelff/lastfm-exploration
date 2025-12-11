import requests
import streamlit as st
import pandas as pd
import math
from pathlib import Path
import numpy as np

st.title("[L]ast.fm Artist Recommendation Algorithm")
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
niche = st.sidebar.select_slider("How niche would you like your recommendations?", ["Not Niche", "Sort of Niche", "Niche", "Very Niche"])
st.sidebar.write(f"Showing {niche} artists")
if niche == "Not Niche":
    lim = 3
if niche == "Sort of Niche":
    lim = 10
if niche == "Niche":
    lim = 25
if niche == "Very Niche":
    lim = 50

show_conan = st.sidebar.checkbox("Show Conan Gray Top Tags")
if show_conan:
    url = "http://ws.audioscrobbler.com/2.0/?method=artist.gettoptags&artist=Conan+Gray&api_key=68ec0071f9e7750afbd8f8f53d9659e0&format=json"
    st.write(requests.get(url).json())

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
        urltwo = f"http://ws.audioscrobbler.com/2.0/?method=tag.gettopartists&tag={tagname}&limit={lim}&api_key=68ec0071f9e7750afbd8f8f53d9659e0&format=json"
        artists = requests.get(urltwo).json()["topartists"]["artist"]
        for artist in artists:
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

