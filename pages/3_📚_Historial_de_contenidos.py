import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="📚 Historial de Contenidos")

# --- Cargar credenciales ---
google_creds = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client_sheets = gspread.authorize(creds)

# --- Conectar con la hoja de cálculo ---
try:
    sheet = client_sheets.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").worksheet("Historial")
    data = sheet.get_all_values()
    if data:
        headers = data[0]
        rows = data[1:]
        df = pd.DataFrame(rows, columns=headers)
    else:
        st.info("📭 La hoja 'Historial' está vacía.")
        df = pd.DataFrame()
except Exception as e:
    st.error("❌ No se pudo acceder a la hoja 'Historial'.")
    st.error(str(e))
    df = pd.DataFrame()

# --- Verificación de usuario ---
usuario_actual = st.session_state.get("usuario", "")

st.title("📚 Historial de Contenidos")

if not usuario_actual:
    st.warning("Debes iniciar sesión para ver tu historial.")
    st.stop()

if df.empty:
    st.info("No hay contenidos generados aún.")
    st.stop()

# --- Comprobación robusta de columnas ---
if "Usuario" in df.columns:
    df_usuario = df[df["Usuario"] == usuario_actual]
    if df_usuario.empty:
        st.info("No hay contenidos generados por este usuario.")
    else:
        st.dataframe(df_usuario)
        csv = df_usuario.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar historial como CSV", data=csv, file_name="historial_contenidos.csv", mime="text/csv")
else:
    st.error("⚠️ La columna 'Usuario' no se encuentra en la hoja. Verifica la estructura.")


