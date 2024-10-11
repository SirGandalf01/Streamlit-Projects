import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Data Dashboard Ejemplo")

uploaded_file = st.file_uploader("Subir Annual Summary", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    
    st.subheader("Previsualización de los Datos")               
    st.write(df)
    
    st.subheader("Filtros")                                     #Filtrar datos
    columns = df.columns.tolist()
    columns.remove('description')
    selected_columns = st.multiselect("Filtrar por Escenario: ", columns)
    selected_columns.insert(0, 'description')
    #rows = df['description'].tolist()
    #selected_rows = st.multiselect("Filtrar por Variable: ", rows)
    
    filtered_df = df[selected_columns]
    st.write(filtered_df)
    
    st.subheader("Gráfico")

    if st.button("Generar Gráfico"):
        del filtered_df['description']
        st.line_chart(filtered_df)
        
else:
    st.write("Esperando archivo...")