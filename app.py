import streamlit as st
import pandas as pd
import gspread
from utils.source import *
from utils.query import *
from mypages.debit import DebitPage
from mypages.budget import BudgetPage 
from mypages.credit import CreditPage


if "token" not in st.session_state:
    st.session_state.token = None

st.set_page_config(page_title="Finance Tracker", page_icon="📊")
st.title("📊 Finance Tracker")

debit = DebitPage()
budget = BudgetPage()
credit = CreditPage()

pg = st.navigation([
            st.Page( debit  , title="Expenses", icon="🔥", url_path="debit"),
            st.Page( budget , title="Budget", icon=":material/favorite:", url_path="budget"),
            st.Page( credit , title="Credit", icon=":material/currency_exchange:", url_path="credit"),
        ])



if not st.session_state.token:
    st.write("### Please log in with Google to continue")

    if "code" in st.query_params:
        code = st.query_params["code"]
        token = fetch_token(code, pg._url_path)
        st.session_state.token = token
        reset_query()
        
    else:
        auth_url = get_authorization_url(pg._url_path)
        st.markdown(f"""
            <script>
                function openOAuth() {{
                    window.open("{auth_url}", "_blank");
                }}
            </script>
        """, unsafe_allow_html=True)

        st.button("🔐 Login with Google", on_click=None)
        st.markdown("<script>document.querySelector('button').onclick=openOAuth;</script>", unsafe_allow_html=True)
else:
    st.success("✅ You are logged in!")
    
    pg.run()
   
