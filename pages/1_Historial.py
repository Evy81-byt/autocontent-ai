import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="📜 Historial de Contenido")

# --- Leer credenciales ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
google_creds = st.secrets["GOOGLE_CREDENTIALS"]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client = gspread.authorize(creds)

# --- Conectar con la hoja correcta ---
try:
    sheet = client.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").sheet1
except Exception as e:
    st.error("❌ No se pudo conectar con Google Sheets.")
    st.exception(e)
    st.stop()

# --- Verificar usuario activo ---
usuario = st.session_state.get("usuario", "")
if not usuario:
    st.warning("Por favor inicia sesión desde la página principal.")
    st.stop()

# --- Leer datos y filtrar por usuario ---
datos = sheet.get_all_values()
df = pd.DataFrame(datos[1:], columns=datos[0])

if "Usuario" not in df.columns:
    st.error("❌ La hoja no contiene la columna 'Usuario'.")
    st.stop()

df_usuario = df[df["Usuario"] == usuario]

# --- Mostrar datos ---
st.title(f"📜 Historial de {usuario}")
if df_usuario.empty:
    st.info("No hay contenido generado por este usuario.")
else:
    st.dataframe(df_usuario)

