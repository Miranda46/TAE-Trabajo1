import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit.components.v1 as components
from sklearn.cluster import KMeans


DATA_CSV = "CollegeScorecard.csv"
POINT_RADIUS = 10000


def load_data():
    data = pd.read_csv(DATA_CSV)

    data = data[["UNITID", "INSTNM", "LATITUDE", "LONGITUDE",  "DEP_INC_AVG", "IND_INC_AVG", "GRAD_DEBT_MDN", "CONTROL"]]

    data.replace(to_replace="PrivacySuppressed", value= np.NaN, inplace = True)

    data["DEP_INC_AVG"] = data["DEP_INC_AVG"].astype(float)
    data["IND_INC_AVG"] = data["IND_INC_AVG"].astype(float)
    data["GRAD_DEBT_MDN"] = data["GRAD_DEBT_MDN"].astype(float)

    data = data.dropna()

    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)

    return data

def get_separation(dataframe):
    control1 = dataframe[dataframe["control"] == 1]
    control2 = dataframe[dataframe["control"] == 2]
    control3 = dataframe[dataframe["control"] == 3]
    return (control1, control2, control3)

@st.cache
def get_kmeans_model_separation(dataframe):
    from sklearn import preprocessing
    dfNorm = dataframe.copy()
    data = dataframe.copy()
    dfNorm[["dep_inc_avg", "ind_inc_avg","grad_debt_mdn"]] = preprocessing.MinMaxScaler().fit_transform(dataframe[["dep_inc_avg", "ind_inc_avg","grad_debt_mdn"]])
    dfFinal_3D = np.array(dfNorm[["dep_inc_avg", "ind_inc_avg","grad_debt_mdn"]])

    kmeansModelo = KMeans(n_clusters=3, max_iter=1000).fit(dfFinal_3D)
    kmeansModeloLabels = kmeansModelo.labels_

    data['cluster'] = kmeansModeloLabels

    cluster_0 = data[data['cluster'] == 0]
    cluster_1 = data[data['cluster'] == 1]
    cluster_2 = data[data['cluster'] == 2]

    return (cluster_0, cluster_1, cluster_2)


df_data = load_data()

df1, df2, df3 = get_kmeans_model_separation(df_data)

#st.map(df_data, zoom=3)
r = pdk.Deck(
     layers=[
         pdk.Layer(
            'ScatterplotLayer',
             data=df1,
             get_position=["longitude", "latitude"],
             get_color='[255, 0, 0, 160]',
             get_radius=POINT_RADIUS,
             pickable=True,
         ), 
         pdk.Layer(
            'ScatterplotLayer',
             data=df2,
             get_position=["longitude", "latitude"],
             get_color='[0, 255, 0, 160]',
             get_radius=POINT_RADIUS,
             pickable=True,
         ),
         pdk.Layer(
            'ScatterplotLayer',
             data=df3,
             get_position=["longitude", "latitude"],
             get_color='[0, 0, 255, 160]',
             get_radius=POINT_RADIUS,
             pickable=True,
         ),
     ], tooltip={
        'html': '<b>Nombre:</b> {instnm}',
        'style': {
            'color': 'white'
        }
    })

r.to_html("scatterplot_layer.html")
with open("scatterplot_layer.html", "r") as f:
    components.html(f.read() , width=600, height=600)