import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Historial de Contenidos", layout="wide")

# --- Leer credenciales desde st.secrets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(json.loads(st.secrets["GOOGLE_CREDENTIALS"]), scopes=scope)
client_sheets = gspread.authorize(creds)

# --- Acceso a la hoja ---
try:
    sheet = client_sheets.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").worksheet("Historial")
    datos = sheet.get_all_records()
except Exception as e:
    st.error("❌ No se pudo acceder a la hoja 'Historial'.")
    st.stop()

# --- Interfaz de usuario ---
st.title("📚 Historial de contenidos")

usuario_actual = st.session_state.get("usuario", "")
if not usuario_actual:
    st.warning("Debes iniciar sesión desde la página principal.")
    st.stop()

# --- Filtrar datos del usuario ---
df = pd.DataFrame(datos)
df_usuario = df[df["Usuario"] == usuario_actual]

if df_usuario.empty:
    st.info("Aún no has generado contenidos.")
else:
    st.dataframe(df_usuario, use_container_width=True)
