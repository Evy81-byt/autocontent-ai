import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="📝 Historial de Redacción AIMA")

# --- Autenticación Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

google_creds = st.secrets["GOOGLE_CREDENTIALS"]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client = gspread.authorize(creds)

try:
    sheet = client.open_by_key("1GfknVmvP8Galub6XS2jhbB0ZnBExTWtk5IXAAzp46Wg")
    hoja = sheet.worksheet("Motor de Redaccion AIMA")
    data = hoja.get_all_records()
    df = pd.DataFrame(data)

    # Normalizar columnas
    df.columns = [col.strip().lower() for col in df.columns]

    columnas_esperadas = ["usuario", "tema", "tipo", "tono", "fecha", "hora", "texto"]

    if not all(col in df.columns for col in columnas_esperadas):
        st.error("❌ Las columnas no coinciden con lo esperado.")
        st.markdown("Se esperaban columnas: `usuario`, `tema`, `tipo`, `tono`, `fecha`, `hora`, `texto`")
        st.stop()

except Exception as e:
    st.error("❌ No se pudo cargar el historial desde Google Sheets.")
    st.exception(e)
    st.stop()

# --- Interfaz de usuario ---
st.title("📝 Historial de Redacción AIMA")

usuarios_disponibles = df["usuario"].dropna().unique().tolist()
usuario_actual = st.selectbox("Selecciona un usuario", usuarios_disponibles)

df_usuario = df[df["usuario"] == usuario_actual]

if df_usuario.empty:
    st.warning("Este usuario aún no ha generado contenido.")
else:
    for idx, fila in df_usuario.iterrows():
        st.markdown(f"### ✏️ Tema: {fila['tema']}")
        st.markdown(f"**Tipo:** {fila['tipo']} | **Tono:** {fila['tono']}")
        st.markdown(f"**Fecha:** {fila['fecha']} - {fila['hora']}")
        st.text_area("📝 Contenido generado:", value=fila["texto"], height=200)
        st.markdown("---")

