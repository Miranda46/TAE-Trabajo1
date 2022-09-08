
import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import joblib
import streamlit.components.v1 as components
from sklearn.cluster import KMeans
from sklearn import preprocessing



DATA_CSV = "CollegeScorecard.csv"
POINT_RADIUS = 10000

modeloImport = joblib.load("classifier.pkl")

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

def normalizar(columna, valor):
    return (valor - df_data[columna].min())/(df_data[columna].max() - df_data[columna].min())


def predecir(valores):
    valoresNorm = [normalizar("dep_inc_avg", valores[0]), normalizar("ind_inc_avg", valores[1]), normalizar("grad_debt_mdn", valores[2])]

    df = pd.DataFrame([valoresNorm], columns=["DEP_INC_AVG", "IND_INC_AVG", "GRAD_DEBT_MDN"])
    
    return modeloImport.predict(df)[0] + 1


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
    
    return (cluster_0, cluster_1, cluster_2, kmeansModelo)

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


def cargar_mapa():
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

    return r.to_html(as_string=True)

st.title("Aplicativo Web TAE")

######## DATAFRAME PRINCIPAL #########
df_data = load_data()
##################################

df1, df2, df3, modelo = get_kmeans_model_separation(df_data)



#st.map(df_data, zoom=3)
########### SIDEBAR ##########
with st.sidebar:
    cluster1 = st.checkbox("Mostrar cluster 1", value = True)
    cluster2 = st.checkbox("Mostrar cluster 2", value = True)
    cluster3 = st.checkbox("Mostrar cluster 3", value = True)

    layers = devolver_layers([cluster1, cluster2, cluster3])
    puntoMedioVisual = mpoint(df_data["latitude"], df_data["longitude"])

    dep_avg = st.slider(
        "Ingreso de familias de estudiantes dependientes",
        float(df_data["dep_inc_avg"].min()), 
        float(df_data["dep_inc_avg"].max()), 
        float(df_data["dep_inc_avg"].mean())
    )

    ind_avg = st.slider(
        "Ingreso de familias de estudiantes independientes",
        float(df_data["ind_inc_avg"].min()), 
        float(df_data["ind_inc_avg"].max()), 
        float(df_data["ind_inc_avg"].mean())
    )

    grad_mdn = st.slider(
        "Mediana de los estudiantes que luego de graduarse quedan en deuda",
        float(df_data["grad_debt_mdn"].min()), 
        float(df_data["grad_debt_mdn"].max()), 
        float(df_data["grad_debt_mdn"].mean())
    )

    if st.button("Predecir cluster de los valores"):
        st.write(predecir([dep_avg, ind_avg, grad_mdn]))
        st.write([dep_avg, ind_avg, grad_mdn])
#############################

components.html(cargar_mapa(), width=600, height=600)
