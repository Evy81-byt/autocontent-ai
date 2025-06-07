import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="📊 Panel de Control")

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

    # Normalizar columnas a minúsculas sin espacios
   estado_filtro = st.selectbox("Filtrar por estado", options=["Todos"] + df["estado"].unique())

   # Renombrar a nombres esperados
    columnas_esperadas = {
        "título": "titulo",
        "tema": "tema",
        "usuario": "usuario",
        "estado": "estado",
        "fecha": "fecha",
        "hora": "hora",
        "✔️": "check",
        "observaciones": "observaciones"
    }
    df = df.rename(columns=columnas_esperadas)

except Exception as e:
    st.error("❌ No se pudo conectar con Google Sheets.")
    st.exception(e)
    st.stop()

st.title("📊 Panel de Control de Contenidos")

# --- Filtros dinámicos ---
st.write("Columnas encontradas en Google Sheets:", df.columns.tolist())
estado_filtro = st.selectbox("Filtrar por estado", options=["Todos"] + sorted(df["estado"].dropna().unique()))
usuario_filtro = st.selectbox("Filtrar por usuario", options=["Todos"] + sorted(df["usuario"].dropna().unique()))

filtro = df.copy()
if estado_filtro != "Todos":
    filtro = filtro[filtro["estado"] == estado_filtro]
if usuario_filtro != "Todos":
    filtro = filtro[filtro["usuario"] == usuario_filtro]

if filtro.empty:
    st.warning("No hay resultados con los filtros seleccionados.")
else:
    for idx, fila in filtro.iterrows():
        st.markdown(f"### 📝 Título: {fila['titulo']}")
        st.markdown(f"🎯 Tema: {fila['tema']}")
        st.markdown(f"👤 Usuario: {fila['usuario']} | 📅 Fecha: {fila['fecha']} {fila['hora']}")
        st.markdown(f"💬 Estado actual: **{fila['estado']}**")

        if st.button(f"✅ Marcar como Publicado ({idx})"):
            hoja.update_cell(idx + 2, df.columns.get_loc("estado") + 1, "Publicado")
            st.success("✅ Estado actualizado a 'Publicado'")
            st.rerun()

         
