import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

if "supabase_url" in st.secrets:

    supabase_url = st.secrets["supabase_url"]

    supabase_key = st.secrets["supabase_key"]

else:

    supabase_url = os.getenv("supabase_url")

    supabase_key = os.getenv("supabase_key")