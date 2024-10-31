import streamlit as st
import pandas as pd
import altair as alt

st.title("IPSA Chile")
uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])


if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Datos del CSV", df.head())
    
    try:
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d.%m.%Y', errors='coerce')
    except Exception as e:
        st.error(f"Error al convertir 'Fecha' en formato de fecha: {e}")
    
    df['Último'] = df['Último'].str.replace('.', '', regex=False)  # Eliminar el separador de miles
    df['Último'] = df['Último'].str.replace(',', '.', regex=False)  # Cambiar el separador decimal
    
    df['Último'] = pd.to_numeric(df['Último'], errors='coerce')
    
    df = df.dropna(subset=['Fecha', 'Último'])  # Eliminar filas con valores nulos en 'Fecha' o 'Último'
    
    if df.empty:
        st.warning("No hay datos válidos para mostrar después de la limpieza. Verifica que 'Fecha' y 'Último' tengan valores adecuados.")
    else:
        st.write("Datos del CSV", df.head())
    
    chart = alt.Chart(df).mark_line().encode(
        x='Fecha:T',
        y='Último:Q',
        tooltip=['Fecha', 'Último']
        ).properties(
        title="Gráfico de Último en función de Fecha",
        width=700,
        height=400
    ).interactive()  # Activar zoom y pan
        
    st.altair_chart(chart, use_container_width=True)
    
    
    a = "variable"