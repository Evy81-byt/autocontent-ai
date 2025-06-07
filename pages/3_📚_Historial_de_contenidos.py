import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

st.set_page_config(page_title="Historial de Contenidos", layout="wide")
st.title("📚 Historial de Contenidos")

# --- Usuario actual ---
if "usuario" not in st.session_state or not st.session_state.usuario:
    st.warning("Por favor, inicia sesión desde la página principal.")
    st.stop()

usuario_actual = st.session_state.usuario

# --- Conectar con Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
google_creds = st.secrets["GOOGLE_CREDENTIALS"]
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client_sheets = gspread.authorize(creds)

try:
    hoja = client_sheets.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").worksheet("Historial")
    datos = hoja.get_all_records()
    df = pd.DataFrame(datos)
except Exception as e:
    st.error("❌ No se pudo cargar el historial desde Google Sheets.")
    st.stop()

# --- Mostrar historial del usuario ---
if df.empty or "Usuario" not in df.columns:
    st.info("No hay registros disponibles aún.")
    st.stop()

df_usuario = df[df["Usuario"] == usuario_actual]
st.dataframe(df_usuario, use_container_width=True)

# --- Descargar como CSV ---
st.markdown("### 📥 Descargar historial")
csv = df_usuario.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📄 Descargar CSV",
    data=csv,
    file_name=f"historial_{usuario_actual}.csv",
    mime='text/csv'
)

# --- Eliminar registros seleccionados ---
st.markdown("### 🗑️ Eliminar registros")
if not df_usuario.empty:
    indices = st.multiselect("Selecciona las filas a eliminar", df_usuario.index.tolist())
    if st.button("Eliminar seleccionados"):
        if indices:
            hoja_valores = hoja.get_all_values()
            cabecera = hoja_valores[0]
            filas_originales = hoja_valores[1:]

            nuevas_filas = [
                fila for i, fila in enumerate(filas_originales)
                if not (i in df_usuario.index and i in indices)
            ]

            hoja.clear()
            hoja.append_row(cabecera)
            for fila in nuevas_filas:
                hoja.append_row(fila)
            st.success("✅ Registros eliminados correctamente.")
            st.rerun()
        else:
            st.warning("No seleccionaste ninguna fila.")



