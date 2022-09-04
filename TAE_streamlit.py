import streamlit as st
import numpy as np
import pandas as pd

DATA_CSV = "CollegeScorecard.csv"

@st.cache
def load_data():
    data = pd.read_csv(DATA_CSV)

    data = data[["UNITID", "INSTNM", "LATITUDE", "LONGITUDE",  "DEP_INC_AVG", "IND_INC_AVG", "GRAD_DEBT_MDN", "CONTROL"]]
    #data["DEP_INC_AVG"] = data["DEP_INC_AVG"].astype(float)
    #data["IND_INC_AVG"] = data["IND_INC_AVG"].astype(float)
    #data["GRAD_DEBT_MDN"] = data["GRAD_DEBT_MDN"].astype(float)

    #data = data.dropna()

    #lowercase = lambda x: str(x).lower()
    #data.rename(lowercase, axis='columns', inplace=True)

    return data

df_data = load_data()

#st.map(df_data)