import streamlit as st
import pandas as pd
import json
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="📸 Historial de Imágenes")

# --- Verifica sesión ---
if "usuario" not in st.session_state or not st.session_state.usuario:
    st.warning("Por favor, inicia sesión desde la sección de inicio.")
    st.stop()

usuario_actual = st.session_state.usuario

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

# --- Acceder a la hoja 'Imagen' ---
try:
    hoja = client_sheets.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").worksheet("Imagen")
    datos = hoja.get_all_records()
    df = pd.DataFrame(datos)
except Exception as e:
    st.error("❌ No se pudo acceder a la hoja 'Imagen'.")
    st.stop()

st.title("📸 Historial de Imágenes")

# --- Filtro por usuario ---
usuarios_disponibles = df["Usuario"].unique().tolist()
usuario_filtrado = st.selectbox("Filtrar por usuario", ["Todos"] + usuarios_disponibles)

if usuario_filtrado != "Todos":
    df = df[df["Usuario"] == usuario_filtrado]

# --- Mostrar resultados ---
if not df.empty:
    for _, fila in df.iterrows():
        st.subheader(f"🧑 Usuario: {fila['Usuario']} - 🕒 {fila['Fecha']}")
        st.write(f"🎨 Prompt: *{fila['Prompt']}*")
        st.image(fila['URL'], width=300)
        st.markdown(f"[Abrir imagen en nueva pestaña]({fila['URL']})")
        st.markdown("---")
else:
    st.info("No hay imágenes registradas con ese filtro.")
