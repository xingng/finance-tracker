from utils.page_template import *
from utils.source import *
import streamlit as st
import plotly.express as px

class DebitPage( PageTemplate ):

    def __init__(self):
        super().__init__()


    def processing(self):

        debit = read_from_excel("Debit")
        credit = read_from_excel("Credit")

        if debit is not None and credit is not None:
            debit["Date"] = pd.to_datetime(debit["Date"], format="%m/%d/%Y")
            debit = debit[ ["Date", "Category", "Subcategory", "Cost"] ]

            credit["Date"] = pd.to_datetime(credit["Date"], format="%m/%d/%Y")
            

            self.df = { "debit" : debit, "credit": credit }

    def render(self):

        if self.df is not None:

            filter_condition = " ( Date >= @self.begin ) and ( Date <= @self.end )"
            debit, credit = self.df["debit"].query(filter_condition), self.df["credit"].query(filter_condition)

            col1, col2 = st.columns([1,1])

            total_credit = round( credit["Amount"].sum(), 2)
            total_debit = round( debit["Cost"].sum(), 2)

            with col1:
                st.metric("Total Expenses", total_debit)

            with col2:
                st.metric("Total Balance", round(total_credit - total_debit,2) )

            st.write("### 📈 Expenses Ratio of Category")
            pie_data = debit.groupby(["Category"], as_index=False).agg({"Cost":"sum"})
            fig = px.pie(pie_data, values='Cost', names='Category')
            st.plotly_chart(fig)

            st.write("### 📄 Sub Category Expenses")
            st.dataframe(debit.groupby(["Category", "Subcategory"]).agg({"Cost":"sum"}) )




    