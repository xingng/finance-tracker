import streamlit as st
import gspread
from google.oauth2.credentials import Credentials
from authlib.integrations.requests_client import OAuth2Session
from google.auth.exceptions import RefreshError
import pandas as pd

CLIENT_ID = st.secrets["google_oauth"]["client_id"]
CLIENT_SECRET = st.secrets["google_oauth"]["client_secret"]
AUTH_URI = st.secrets["google_oauth"]["auth_uri"]
TOKEN_URI = st.secrets["google_oauth"]["token_uri"]

REDIRECT_URIS = {
    "debit": st.secrets["google_oauth"]["redirect_uri_debit"],
    "budget": st.secrets["google_oauth"]["redirect_uri_budget"],
    "credit": st.secrets["google_oauth"]["redirect_uri_credit"]
}

SCOPE = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

def fetch_token(code, path):

    REDIRECT_URI= REDIRECT_URIS[path]
    oauth = OAuth2Session(CLIENT_ID, CLIENT_SECRET, scope=SCOPE, redirect_uri = REDIRECT_URI)
    token = oauth.fetch_token(TOKEN_URI, code=code)
    return token

def get_authorization_url(path):

    REDIRECT_URI= REDIRECT_URIS[path]
    oauth = OAuth2Session(
        CLIENT_ID, 
        CLIENT_SECRET,
        scope=SCOPE, 
        redirect_uri=REDIRECT_URI
        )
    
    _, random_state = oauth.create_authorization_url(AUTH_URI)
    uri, _ = oauth.create_authorization_url(AUTH_URI, state = random_state + (f" sheetId={st.query_params["sheetId"]}" if st.query_params.get("sheetId", False) else "") )

    return uri


def get_credentials(token):
    return Credentials(
        token["access_token"],
        refresh_token=token.get("refresh_token"),
        token_uri=TOKEN_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scopes=SCOPE
    )

def read_from_excel(page) -> pd.DataFrame | None:
   
    SHEET_ID = st.session_state.sheetId

    try:
        creds = get_credentials(st.session_state.token)
        gc = gspread.authorize(creds)

        sheet = gc.open_by_key(SHEET_ID).worksheet(page)
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        
        return df

    except gspread.exceptions.SpreadsheetNotFound:
        st.error("File Not Found")

    except RefreshError:
        st.warning("Session expired. Please log in again.")
        st.session_state.token = None
        st.rerun()