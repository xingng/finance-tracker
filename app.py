import streamlit as st
import pandas as pd
import gspread
from authlib.integrations.requests_client import OAuth2Session
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.exceptions import RefreshError
import json
import os

# Google OAuth Config
with open("client_secret.json") as f:
    client_config = json.load(f)["web"]

CLIENT_ID = client_config["client_id"]
CLIENT_SECRET = client_config["client_secret"]
AUTH_URI = client_config["auth_uri"]
TOKEN_URI = client_config["token_uri"]
REDIRECT_URI = client_config["redirect_uris"][0]
SCOPE = ["https://www.googleapis.com/auth/spreadsheets.readonly",
         "https://www.googleapis.com/auth/drive.readonly"]

# --- Streamlit App ---
st.set_page_config(page_title="Google Sheets Line Chart", page_icon="📊")
st.title("📊 Google Sheets Line Chart with Login")

# Initialize session state
if "token" not in st.session_state:
    st.session_state.token = None

def get_authorization_url():
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    uri, _ = oauth.create_authorization_url(AUTH_URI)
    return uri

def fetch_token(code):
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI)
    token = oauth.fetch_token(TOKEN_URI, code=code)
    return token

def get_credentials(token):
    return Credentials(
        token["access_token"],
        refresh_token=token.get("refresh_token"),
        token_uri=TOKEN_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPE
    )

# Login Section
if not st.session_state.token:
    st.write("### Please log in with Google to continue")
    auth_url = get_authorization_url()
    st.markdown(f"[🔑 Login with Google]({auth_url})")

    # When Google redirects back with ?code=...
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        code = query_params["code"][0]
        token = fetch_token(code)
        st.session_state.token = token
        st.experimental_set_query_params()  # clear URL
        st.rerun()
else:
    st.success("✅ You are logged in!")

    # --- Access Google Sheet ---
    try:
        creds = get_credentials(st.session_state.token)
        gc = gspread.authorize(creds)

        # 👉 Replace this with your Sheet ID
        SHEET_ID = "1uvAU3ad77f2KcOoAxIpLqZAH8T51HH45ColXPGQ9-Ts"
        sheet = gc.open_by_key(SHEET_ID).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)

        st.write("### 📄 Google Sheet Data")
        st.dataframe(df)

        st.write("### 📈 Line Chart")
        st.line_chart(df.set_index(df.columns[0]))

    except RefreshError:
        st.warning("Session expired. Please log in again.")
        st.session_state.token = None
        st.rerun()
