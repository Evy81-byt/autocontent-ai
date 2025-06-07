import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="📸 Historial de Imágenes")

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
    sheet = client.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg")
    hoja = sheet.worksheet("Imagenes")
    data = hoja.get_all_records()
    df = pd.DataFrame(data)
except Exception as e:
    st.error("❌ No se pudo cargar el historial desde Google Sheets.")
    st.exception(e)
    st.stop()

# --- Verificar columnas esperadas ---
columnas_esperadas = ["Usuario", "Tema", "Fecha", "Hora", "Imagen"]
if not all(col in df.columns for col in columnas_esperadas):
    st.error("❌ Las columnas de la hoja 'Imagenes' no coinciden con lo esperado.")
    st.markdown("Se esperaban las columnas: `Usuario`, `Tema`, `Fecha`, `Hora`, `Imagen`")
    st.stop()

# --- Filtro por usuario ---
st.title("📸 Historial de Imágenes")

usuarios_disponibles = df["Usuario"].unique().tolist()
usuario_actual = st.selectbox("Selecciona un usuario", usuarios_disponibles)

df_usuario = df[df["Usuario"] == usuario_actual]

if df_usuario.empty:
    st.warning("Este usuario aún no ha generado imágenes.")
else:
    for idx, fila in df_usuario.iterrows():
        st.markdown(f"### 🎯 Tema: {fila['Tema']}")
        st.image(fila["Imagen"], use_column_width=True)
        st.caption(f"🕒 {fila['Fecha']} - {fila['Hora']}")


