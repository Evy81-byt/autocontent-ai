import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="📊 Panel de Control de Contenidos")

# --- Autenticación Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

try:
    google_creds = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(google_creds, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1GfknVmvP8Galub6XS2jhbB0ZnBExTWtk5IXAAzp46Wg")
    hoja = sheet.worksheet("Panel")
    data = hoja.get_all_records()
    df = pd.DataFrame(data)

    # Normalización
    df.columns = [col.strip().capitalize() for col in df.columns]

    columnas_necesarias = ["Título", "Tema", "Usuario", "Estado", "Fecha", "Hora"]

    if not all(col in df.columns for col in columnas_necesarias):
        st.error("❌ Las columnas no coinciden con lo esperado.")
        st.markdown("Se esperaban columnas: `Título`, `Tema`, `Usuario`, `Estado`, `Fecha`, `Hora`")
        st.stop()

except Exception as e:
    st.error("❌ No se pudo cargar el panel desde Google Sheets.")
    st.exception(e)
    st.stop()

# --- Filtros ---
st.title("📊 Panel de Control de Contenidos")

usuarios_disponibles = df["Usuario"].dropna().unique().tolist()
usuario_filtro = st.selectbox("Filtrar por usuario", options=["Todos"] + usuarios_disponibles)

estados_disponibles = df["Estado"].dropna().unique().tolist()
estado_filtro = st.selectbox("Filtrar por estado", options=["Todos"] + estados_disponibles)

# --- Aplicar filtros ---
if usuario_filtro != "Todos":
    df = df[df["Usuario"] == usuario_filtro]

if estado_filtro != "Todos":
    df = df[df["Estado"] == estado_filtro]

# --- Mostrar resultados ---
if df.empty:
    st.warning("No hay datos para mostrar con los filtros seleccionados.")
else:
    st.dataframe(df, use_container_width=True)




         
