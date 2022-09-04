import streamlit as st
import numpy as np
import pandas as pd

DATA_CSV = "CollegeScorecard.csv"

@st.cache
def load_data():
    data = pd.read_csv(DATA_CSV, )
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data