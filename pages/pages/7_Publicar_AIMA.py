import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import json
from datetime import datetime
import requests

st.set_page_config(page_title="🚀 Publicar Contenido AIMA")

# --- Autenticación Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

try:
    google_creds = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    creds = Credentials.from_service_account_info(google_creds, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1GfknVmvP8Galub6XS2jhbB0ZnBExTWtk5IXAAzp46Wg")
    hoja = sheet.worksheet("Motor de Redaccion AIMA")
    datos = hoja.get_all_values()
    columnas = datos[0]
    contenidos = datos[1:]
except Exception as e:
    st.error("❌ Error conectando con Google Sheets.")
    st.exception(e)
    st.stop()

# --- Encabezado ---
st.title("🚀 Publicar Contenidos AIMA")

# --- Encontrar columnas ---
try:
    idx_estado = columnas.index("Estado")
    idx_usuario = columnas.index("Usuario")
    idx_tema = columnas.index("Tema")
    idx_contenido = columnas.index("Contenido")
except ValueError as ve:
    st.error("❌ Error: Asegúrate de que todas las columnas necesarias están en la hoja.")
    st.stop()

# --- Mostrar entradas pendientes ---
pendientes = [fila for fila in contenidos if fila[idx_estado].strip().lower() == "pendiente"]

if not pendientes:
    st.info("✅ No hay contenidos pendientes por publicar.")
    st.stop()

for i, fila in enumerate(pendientes):
    usuario = fila[idx_usuario]
    tema = fila[idx_tema]
    contenido = fila[idx_contenido]

    st.markdown(f"### 🧑 Usuario: {usuario} | 📝 Tema: {tema}")
    st.text_area("📄 Contenido", value=contenido, height=250, key=f"contenido_{i}")

    if st.button(f"🌐 Publicar en WordPress - #{i}"):
        # Datos WordPress desde secrets
        try:
            wp_url = st.secrets["WORDPRESS_URL"]
            wp_user = st.secrets["WORDPRESS_USER"]
            wp_pass = st.secrets["WORDPRESS_APP_PASSWORD"]
        except KeyError:
            st.error("❌ Faltan las credenciales de WordPress en secrets.toml.")
            st.stop()

        token = requests.auth._basic_auth_str(wp_user, wp_pass)
        headers = {"Authorization": token}
        payload = {
            "title": tema,
            "content": contenido,
            "status": "publish"
        }

        r = requests.post(f"{wp_url}/wp-json/wp/v2/posts", headers=headers, json=payload)

        if r.status_code == 201:
            st.success("✅ Publicado exitosamente.")
            fila_idx = datos.index(fila) + 1
            hoja.update_cell(fila_idx + 1, idx_estado + 1, "Publicado")
        else:
            st.error(f"❌ Error al publicar: {r.status_code}")
            st.text(r.text)
