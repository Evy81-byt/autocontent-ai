import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

# --- Conectar con Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

try:
    hoja = client.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").worksheet("Historial")
    datos = hoja.get_all_records()
except Exception as e:
    st.error("❌ No se pudo acceder a la hoja de cálculo.")
    st.stop()

st.title("📚 Historial de contenidos")

if "usuario" not in st.session_state or not st.session_state.usuario:
    st.warning("Debes iniciar sesión primero desde la página principal.")
    st.stop()

usuario_actual = st.session_state.usuario

# Validar que hay datos
if not datos:
    st.info("No hay registros aún en el historial.")
else:
    df = pd.DataFrame(datos)

    # Validar columnas esperadas
    if "Usuario" in df.columns:
        df_usuario = df[df["Usuario"] == usuario_actual]
        if df_usuario.empty:
            st.info("No hay contenidos guardados por este usuario.")
        else:
            st.dataframe(df_usuario)
    else:
        st.error("⚠️ La hoja 'Historial' no contiene una columna llamada 'Usuario'. Revisa los encabezados.")

