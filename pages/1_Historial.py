import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="📜 Historial de Contenido")

# --- Autenticación con Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
google_creds = st.secrets["GOOGLE_CREDENTIALS"]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client = gspread.authorize(creds)

# --- Conectar con la hoja específica ---
try:
    sheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])
    hoja = sheet.worksheet("Historial Usuario")
    datos = hoja.get_all_records()
    df = pd.DataFrame(datos)

    # Normalizar nombres de columnas
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

# --- Filtro por usuario ---
st.title("📜 Historial de Contenido")

usuario = st.session_state.get("usuario", "")
if not usuario:
    st.warning("Por favor inicia sesión desde la página principal.")
    st.stop()

df_usuario = df[df["usuario"] == usuario]

if df_usuario.empty:
    st.info("Este usuario aún no tiene historial.")
else:
    for idx, fila in df_usuario.iterrows():
        st.markdown(f"### ✍️ Tema: {fila['tema']}")
        st.markdown(f"**Tipo:** {fila['tipo']}  |  **Tono:** {fila['tono']}")
        st.markdown(f"📅 {fila['fecha']} ⏰ {fila['hora']}")
        st.markdown(f"📝 {fila['texto']}")
        st.markdown("---")



