from utils.page_template import *
from utils.source import *
import streamlit as st
import plotly.express as px

class BudgetPage( PageTemplate ):

    def __init__(self):
        super().__init__()


    def processing(self):

        debit = read_from_excel("Debit")
        budget = read_from_excel("Budget")
        credit = read_from_excel("Credit")

        if debit is not None and budget is not None and credit is not None:

            credit["Date"] = pd.to_datetime(credit["Date"], format="%m/%d/%Y")


            debit["Date"] = pd.to_datetime(debit["Date"], format="%m/%d/%Y")
            debit = debit[ ["Date", "Category", "Subcategory", "Cost"] ]

            budget["Date"] = pd.to_datetime(budget["Date"], format="%m/%d/%Y")
            budget = budget[ ["Date", "Category", "Subcategory", "Amount"] ]

            debit["Year"] = debit["Date"].dt.year
            debit["Month"] = debit["Date"].dt.month
            debit = debit.groupby(["Year", "Month", "Category", "Subcategory"]).agg( {"Cost": "sum"} )


            budget["Year"] = budget["Date"].dt.year
            budget["Month"] = budget["Date"].dt.month
            budget = budget.groupby(["Year", "Month", "Category", "Subcategory"], as_index = False).agg( {"Amount": "sum"} )

            df = debit.merge(
                budget, 
                left_on = ["Year", "Month", "Category", "Subcategory"],
                right_on = ["Year", "Month", "Category", "Subcategory"],
                )
            
            df = df.rename(columns = {"Amount" : "Budget"})
            df["Budget Remain"] = ( df["Budget"] - df["Cost"] ).round(2)

            df["Day"] = 1
            df["Date"] = pd.to_datetime( df[["Year", "Month", "Day"]] )
            df.drop(columns = ["Year", "Month", "Day"])
            

            self.df = { "budget" : df, "credit": credit }

    def render(self):

        if self.df is not None:

            filter_condition = " ( Date >= @self.begin ) and ( Date <= @self.end )"
            budget, credit = self.df["budget"].query(filter_condition), self.df["credit"].query(filter_condition)
             

            col1, col2, col3 = st.columns([1,1, 1])

            total_budget = round(budget["Budget"].sum(), 2)
            total_credit = round(credit["Amount"].sum(), 2)
            budget_remain = round(budget["Budget Remain"].sum(), 2)

            with col1:
                st.metric("Total Budget", total_budget)
            
            with col2:
                st.metric("Forecasted Balance", round(total_credit - total_budget,2))

            with col3:
                st.metric("Budget Remaining", budget_remain)

            st.write("### 📈 Expenses Ratio of Category")
            pie_data = budget.groupby(["Category"], as_index=False).agg({"Budget":"sum"})
            fig = px.pie(pie_data, values='Budget', names='Category')
            st.plotly_chart(fig)

            st.write("### 📄 Budget Remaining")
            st.dataframe(budget[["Year", "Month", "Category", "Subcategory", "Budget", "Cost","Budget Remain"]])




    