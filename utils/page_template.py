from abc import ABC, abstractmethod
from typing import Any
from utils.query import *
import pandas as pd

class PageTemplate(ABC):

    def __init__(self) -> None:
        
        self.begin = None
        self.end = None
        self.df = None

    @abstractmethod
    def processing(self) -> pd.DataFrame | None:
        pass

    @abstractmethod
    def render(self) -> None:
        pass


    def filter_header(self) -> None:

        col1, col2, col3, col4 = st.columns([19, 19, 6, 6], vertical_alignment="bottom", width="stretch") 


        with col3:
            if st.button("Today", width="stretch", type="primary"):
                self.begin = pd.Timestamp.today()
                self.end = pd.Timestamp.today()

        with col4:
            if st.button("Reset", width="stretch"):
                self.begin = pd.Timestamp.today().replace(day=1)
                self.end = pd.Timestamp.today() + pd.offsets.MonthEnd(0)

        with col1:
            self.begin = st.date_input("Start Date",  self.begin or pd.Timestamp.today().replace(day=1) )

        with col2:
            self.end = st.date_input("End Date", self.end or pd.Timestamp.today() + pd.offsets.MonthEnd(0) )



    def __call__(self) -> None:

        if input_id():
            self.processing()
        
        if self.df is not None:
            self.filter_header()
            self.render()



