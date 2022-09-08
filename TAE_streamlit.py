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

@st.cache
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

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

def devolver_layers(lista):
    layers = list()
    if lista[0]:
        layers.append(pdk.Layer(
        'ScatterplotLayer',
            data=df1,
            get_position=["longitude", "latitude"],
            get_color='[255, 0, 0, 160]',
            get_radius=POINT_RADIUS,
            pickable=True,
        ))
    if lista[1]:
        layers.append(pdk.Layer(
        'ScatterplotLayer',
            data=df2,
            get_position=["longitude", "latitude"],
            get_color='[0, 255, 0, 160]',
            get_radius=POINT_RADIUS,
            pickable=True,
        ))
    if lista[2]:
        layers.append(pdk.Layer(
        'ScatterplotLayer',
            data=df3,
            get_position=["longitude", "latitude"],
            get_color='[0, 0, 255, 160]',
            get_radius=POINT_RADIUS,
            pickable=True,
        ))
    else:
        pass
    return layers


df_data = load_data()

df1, df2, df3 = get_kmeans_model_separation(df_data)


#st.map(df_data, zoom=3)
########### SIDEBAR##########
with st.sidebar:
    cluster1 = st.checkbox("Mostrar cluster 1", value = True)
    cluster2 = st.checkbox("Mostrar cluster 2", value = True)
    cluster3 = st.checkbox("Mostrar cluster 3", value = True)

    layers = devolver_layers([cluster1, cluster2, cluster3])
    puntoMedioVisual = mpoint(df_data["latitude"], df_data["longitude"])

r = pdk.Deck(
    map_style="light",
    initial_view_state={
        "latitude": puntoMedioVisual[0],
        "longitude": puntoMedioVisual[1],
        "zoom": 3,
    },
     layers = layers, 
     tooltip={
        'html': '<b>Nombre:</b> {instnm}',
        'style': {
            'color': 'white'
        }
    })


components.html(r.to_html(as_string=True) , width=600, height=600)