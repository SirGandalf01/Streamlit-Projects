import streamlit as st
import pandas as pd
import altair as alt
import statsmodels.api as sm

#Formatea los valores de fecha y números para leerlos correctamente
def clean_data(df):
    try:
        df['Fecha'] = pd.to_datetime(df['Fecha'], format='%d.%m.%Y', errors='coerce') #Este es el formato DD.MM.AA
    except Exception as e:
        st.error(f"Error al convertir 'Fecha' en formato de fecha: {e}")
    df['Último'] = df['Último'].str.replace('.', '', regex=False)  # Eliminar el separador de miles
    df['Último'] = df['Último'].str.replace(',', '.', regex=False)  # Cambiar el separador decimal
    df['Último'] = pd.to_numeric(df['Último'], errors='coerce')
    df = df.dropna(subset=['Fecha', 'Último'])
    df.set_index('Fecha', inplace=True)
    df = df.sort_index(ascending=True).reset_index()
    if df.empty:
        st.warning("No hay datos válidos para mostrar después de la limpieza. Verifica que 'Fecha' y 'Último' tengan valores adecuados.")
    else:
        st.write("Datos formateados", df.head())
    return df

def forecast_model(df):
    model_sarima = sm.tsa.SARIMAX(df['Último'], order=(0,1,1), seasonal_order=(0,0,1,3))  # Cambia según sea necesario
    model_fit_sarima = model_sarima.fit()
    forecast_sarima = model_fit_sarima.forecast(steps=4)
    forecast_df = forecast_sarima.reset_index()
    forecast_df.columns = ['Fecha', 'Predicción']
    #forecast_df['Fecha'] = pd.to_datetime(forecast_df['Fecha'], format = '%d.%m.%Y', errors='coerce')
    return forecast_df

def generate_chart(df):
    chart = alt.Chart(df).mark_line().encode(
        x='Fecha:T',
        y='Último:Q',
        tooltip=['Fecha', 'Último']
        ).properties(
        title="Gráfico de Último en función de Fecha",
        width=700,
        height=400
    ).interactive()  # Activar zoom y pan
    forecast_df = forecast_model(df)
    forecast_chart = alt.Chart(forecast_df).mark_line(color = "red").encode(
        x='Fecha',
        y='Predicción',
        tooltip=['Fecha', 'Predicción']
        )           
    combined_chart = chart + forecast_chart    
    return combined_chart




st.title("IPSA Chile")
uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Previsualización de los datos", df.head())
    
    df = clean_data(df)
    chart = generate_chart(df)
    st.altair_chart(chart, use_container_width=True)
    
    forecast_df = forecast_model(df)
    st.write(forecast_df)