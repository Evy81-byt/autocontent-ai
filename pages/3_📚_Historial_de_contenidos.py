import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="📚 Historial de Contenidos")

# --- Autenticación Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

try:
    creds = Credentials.from_service_account_info(
        st.secrets["GOOGLE_CREDENTIALS"], scopes=scope
    )
    client = gspread.authorize(creds)
    sheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])
    hoja = sheet.worksheet("Historial")
    data = hoja.get_all_records()
    df = pd.DataFrame(data)

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

st.title("📚 Historial de Contenidos")

usuarios_disponibles = df["usuario"].dropna().unique().tolist()
if not usuarios_disponibles:
    st.warning("No hay usuarios disponibles.")
    st.stop()

usuario_actual = st.selectbox("Selecciona un usuario", usuarios_disponibles)
df_usuario = df[df["usuario"] == usuario_actual]

if df_usuario.empty:
    st.info("Este usuario aún no tiene historial.")
else:
    for idx, fila in df_usuario.iterrows():
        st.markdown(f"### ✍️ Tema: {fila['tema']}")
        st.markdown(f"**Tipo:** {fila['tipo']}  |  **Tono:** {fila['tono']}")
        st.markdown(f"📅 {fila['fecha']} ⏰ {fila['hora']}")
        st.markdown(f"📝 {fila['texto']}")
        st.markdown("---")





