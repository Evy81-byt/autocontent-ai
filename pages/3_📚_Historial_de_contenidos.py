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
    google_creds = st.secrets["GOOGLE_CREDENTIALS"]
    creds = Credentials.from_service_account_info(google_creds, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1GfknVmvP8Galub6XS2jhbB0ZnBExTWtk5IXAAzp46Wg")
    hoja = sheet.worksheet("Historial")
    data = hoja.get_all_records()
    df = pd.DataFrame(data)

    # Normalizar nombres de columnas
    df.columns = [col.strip().lower() for col in df.columns]

    # Verificar columnas necesarias
    columnas_esperadas = ["usuario", "tema", "tipo", "tono", "fecha", "hora", "texto"]
    if not all(col in df.columns for col in columnas_esperadas):
        st.error("❌ Las columnas no coinciden con lo esperado.")
        st.markdown("Se esperaban columnas: `usuario`, `tema`, `tipo`, `tono`, `fecha`, `hora`, `texto`")
        st.stop()

    # Renombrar por consistencia
    df = df.rename(columns={
        "usuario": "Usuario",
        "tema": "Tema",
        "tipo": "Tipo",
        "tono": "Tono",
        "fecha": "Fecha",
        "hora": "Hora",
        "texto": "Texto"
    })

except Exception as e:
    st.error("❌ No se pudo cargar el historial desde Google Sheets.")
    st.exception(e)
    st.stop()

# --- UI ---
st.title("📚 Historial de Contenidos")

usuarios = df["Usuario"].dropna().unique().tolist()
usuario_actual = st.selectbox("Filtrar por usuario", options=["Todos"] + usuarios)

df_filtrado = df if usuario_actual == "Todos" else df[df["Usuario"] == usuario_actual]

if df_filtrado.empty:
    st.warning("No hay contenidos disponibles para mostrar.")
else:
    for _, fila in df_filtrado.iterrows():
        st.markdown(f"### 📝 Tema: {fila['Tema']}")
        st.markdown(f"**Tipo:** {fila['Tipo']} | **Tono:** {fila['Tono']} | 📅 {fila['Fecha']} ⏰ {fila['Hora']}")
        st.markdown(f"**Texto generado:**")
        st.info(fila["Texto"])
        st.markdown("---")




