import os
from dotenv import load_dotenv

load_dotenv()

try:

    import streamlit as st

    if st.runtime.exists():

        supabase_url = st.secrets["supabase_url"]

        supabase_key = st.secrets["supabase_key"]

    else:

        raise Exception()

except Exception:

    supabase_url = os.getenv("supabase_url")

    supabase_key = os.getenv("supabase_key")