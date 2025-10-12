from utils.page_template import *
from utils.source import *
import streamlit as st
import plotly.express as px

class CreditPage( PageTemplate ):

    def __init__(self):
        super().__init__()


    def processing(self):

        credit = read_from_excel("Credit")

        if credit is not None:
            credit["Date"] = pd.to_datetime(credit["Date"], format="%m/%d/%Y")
       
            self.df = {"credit": credit }

    def render(self):

        if self.df is not None:

            filter_condition = " ( Date >= @self.begin ) and ( Date <= @self.end )"
            credit = self.df["credit"].query(filter_condition)

            col1, = st.columns([1])

            total_credit = round( credit["Amount"].sum(), 2)

            with col1:
                st.metric("Total Balance", total_credit )


            st.write("### 📄 Credit")
            st.dataframe(credit)




    