import streamlit as st
import gspread
import json
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="Historial de Contenido")

# --- Leer credenciales ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client_sheets = gspread.authorize(creds)

# --- Conectar con la hoja ---
try:
    sheet = client_sheets.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").sheet1
except Exception as e:
    st.error("❌ No se pudo conectar con Google Sheets.")
    st.stop()

# --- Filtrar por usuario activo ---
usuario = st.session_state.get("usuario", "")
if not usuario:
    st.warning("Por favor inicia sesión desde la página principal.")
    st.stop()

# --- Obtener los datos ---
datos = sheet.get_all_values()
df = pd.DataFrame(datos[1:], columns=datos[0])
df_usuario = df[df["Usuario"] == usuario]

st.title(f"📜 Historial de {usuario}")
st.dataframe(df_usuario)
