import streamlit as st

def input_id():

    if st.query_params.get( "sheetId" , False):

        sheetId = st.query_params["sheetId"]
        input_sheetId = st.text_input("Sheet Id", sheetId)

        if input_sheetId != sheetId:
            st.query_params["sheetId"] = input_sheetId
            st.rerun()       

        st.session_state.sheetId = sheetId

        return True

    if st.session_state.get("sheetId", False):
        st.query_params["sheetId"] = st.session_state.sheetId
        st.rerun()


    SHEET_ID = st.text_input("Sheet Id")

    if(SHEET_ID == ''):
        return False
    
    st.session_state.sheetId = SHEET_ID
    st.query_params["sheetId"] = st.session_state.sheetId
    st.rerun()


def reset_query():

    split_state = st.query_params["state"].split(" sheetId=")
    
    if( len(split_state) == 1 ):
        st.query_params.clear()
    else:
        st.query_params.clear(); 
        st.query_params["sheetId"] = split_state[1]

    st.rerun()