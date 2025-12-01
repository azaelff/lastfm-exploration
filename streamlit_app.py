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
         <a target="_self" href="http://www.last.fm/api/auth/?api_key=68ec0071f9e7750afbd8f8f53d9659e0">
            <button>
                Enable API
            </button>
         </a>
        ''',
        unsafe_allow_html=True
    )

show_conan = st.sidebar.checkbox("Show Conan Gray Top Albums")

if show_conan:
    url = "http://ws.audioscrobbler.com/2.0/?method=artist.gettopalbums&artist=Conan Gray&api_key=68ec0071f9e7750afbd8f8f53d9659e0&format=json"
    st.write(requests.get(url).json())