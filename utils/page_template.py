from abc import ABC, abstractmethod
from typing import Any
from utils.query import *
import pandas as pd

class PageTemplate(ABC):

    def __init__(self) -> None:

        self.df = None
        self.set_begin()
        self.set_end()

    @abstractmethod
    def processing(self) -> pd.DataFrame | None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    def set_begin(self, date = None):

        if(date == None and st.session_state.get( "begin") == None):
            self.begin = pd.Timestamp.today().replace(day=1).date()
            st.session_state["begin"] = self.begin
            return
        
        if(date != None):
            self.begin = date
            st.session_state["begin"] = date
            return
        
        self.begin = st.session_state["begin"]
        

    def set_end(self, date = None):

        if(date == None and st.session_state.get("end") == None):
            self.end = ( pd.Timestamp.today() + pd.offsets.MonthEnd(0) ).date()
            st.session_state["end"] = self.end
            return
        
        if(date != None):
            self.end = date
            st.session_state["end"] = date
            return
        
        self.end = st.session_state["end"]



    def filter_header(self) -> None:

        col1, col2, col3, col4 = st.columns([19, 19, 6, 6], vertical_alignment="bottom", width="stretch") 

        with col3:
            if st.button("Today", width="stretch", type="primary"):
                self.set_begin(pd.Timestamp.today().date())
                self.set_end(pd.Timestamp.today().date())

        with col4:
            if st.button("Reset", width="stretch"):
                self.set_begin(pd.Timestamp.today().replace(day=1).date())
                self.set_end( (pd.Timestamp.today() + pd.offsets.MonthEnd(0)).date() )

        with col1:
            self.begin = st.date_input("Start Date", key = "begin" )

        with col2:
            self.end = st.date_input("End Date", key = "end" )




    def __call__(self) -> None:

        if input_id():
            self.processing()
        
        if self.df is not None:
            self.filter_header()
            self.render()



