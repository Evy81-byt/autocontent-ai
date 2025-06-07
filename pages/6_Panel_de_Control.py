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

    # Normalizar nombres de columnas
    df.columns = [col.strip().lower() for col in df.columns]

    # Verificación básica
    columnas_requeridas = ["título", "tema", "usuario", "estado", "fecha", "hora"]
    if not all(col in df.columns for col in columnas_requeridas):
        st.error("❌ Las columnas no coinciden con lo esperado.")
        st.markdown("Se esperaban columnas: `Título`, `Tema`, `Usuario`, `Estado`, `Fecha`, `Hora`")
        st.stop()

except Exception as e:
    st.error("❌ No se pudo cargar el Panel desde Google Sheets.")
    st.exception(e)
    st.stop()

# --- Filtro de estado ---
st.title("📊 Panel de Control de Contenidos")

estado_filtro = st.selectbox("Filtrar por estado", options=["Todos"] + sorted(df["estado"].dropna().unique().tolist()))

if estado_filtro != "Todos":
    df = df[df["estado"] == estado_filtro]

# --- Mostrar datos ---
st.dataframe(df)
st.success(f"✅ {len(df)} registros mostrados.")


         
