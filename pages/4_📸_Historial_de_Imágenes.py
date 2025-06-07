import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

st.title("📸 Historial de Imágenes")

# Conexión segura
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]
creds_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

try:
    sheet = client.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").worksheet("Imagen")
    data = sheet.get_all_records()
    df = pd.DataFrame(data)

    # Normalizar columnas (hacerlas insensibles a mayúsculas/minúsculas)
    df.columns = [col.strip().lower() for col in df.columns]

    if df.empty:
        st.info("No hay imágenes generadas todavía.")
        st.stop()

    # Verificar si hay columnas necesarias
    columnas_requeridas = {"usuario", "prompt", "fecha", "hora", "url"}
    if not columnas_requeridas.issubset(set(df.columns)):
        st.error("❌ Faltan columnas requeridas: asegúrate de tener encabezados como Usuario, Prompt, Fecha, Hora, URL.")
        st.stop()

    usuario_actual = st.session_state.get("usuario", "")
    if not usuario_actual:
        st.warning("Debes iniciar sesión primero.")
        st.stop()

    df_usuario = df[df["usuario"] == usuario_actual]

    if df_usuario.empty:
        st.info("No tienes imágenes guardadas todavía.")
    else:
        for _, fila in df_usuario.iterrows():
            st.markdown(f"**📌 Prompt:** {fila['prompt']}")
            st.image(fila['url'], use_column_width=True)
            st.caption(f"📅 {fila['fecha']} ⏰ {fila['hora']}")
            st.markdown("---")

except Exception as e:
    st.error("Error al conectar con la hoja de cálculo.")
    st.exception(e)

