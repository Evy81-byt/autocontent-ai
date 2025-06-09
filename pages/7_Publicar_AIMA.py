import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import requests

st.set_page_config(page_title="🚀 Publicar Contenido AIMA")
st.markdown("""
    <style>
        .stApp {
            background-color: #f4f7f9;
            color: #2c3e50;
        }
        body, .stApp {
            cursor: pointer;
        }
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif;
            font-weight: 700;
            color: #2c3e50;
        }
        .markdown-text-container {
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #1abc9c;
            color: white;
            padding: 0.5em 1em;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #16a085;
        }
        textarea {
            background-color: #ffffff;
            border: 1px solid #dfe6e9;
            border-radius: 5px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

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
    sheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])
    hoja = sheet.worksheet("Motor de Redaccion AIMA")
    datos = hoja.get_all_values()
    columnas = [col.strip().lower() for col in datos[0]]
    contenidos = datos[1:]
except Exception as e:
    st.error("❌ Error conectando con Google Sheets.")
    st.exception(e)
    st.stop()

# --- Verificar columnas necesarias ---
required_columns = ["estado", "usuario", "tema", "contenido"]
missing_columns = [col for col in required_columns if col not in columnas]
if missing_columns:
    st.error(f"❌ Faltan columnas necesarias: {', '.join(missing_columns)}")
    st.stop()

idx_estado = columnas.index("estado")
idx_usuario = columnas.index("usuario")
idx_tema = columnas.index("tema")
idx_contenido = columnas.index("contenido")

# --- Filtrar contenidos pendientes ---
pendientes = [
    fila for fila in contenidos
    if len(fila) > idx_estado and fila[idx_estado].strip().lower() == "pendiente"
]

if not pendientes:
    st.info("✅ No hay contenidos pendientes por publicar.")
    st.stop()

st.title("🚀 Publicar Contenidos AIMA")

for i, fila in enumerate(pendientes):
    if len(fila) <= max(idx_estado, idx_usuario, idx_tema, idx_contenido):
        continue  # Saltar filas incompletas

    usuario = fila[idx_usuario]
    tema = fila[idx_tema]
    contenido = fila[idx_contenido]

    st.markdown(f"### 🧑 Usuario: {usuario} | 📝 Tema: {tema}")
    st.text_area("📄 Contenido", value=contenido, height=250, key=f"contenido_{i}")

    if st.button(f"🌐 Publicar en WordPress - #{i}"):
        try:
            wp_url = st.secrets["WORDPRESS_URL"]
            wp_user = st.secrets["WORDPRESS_USER"]
            wp_pass = st.secrets["WORDPRESS_APP_PASSWORD"]
        except KeyError:
            st.error("❌ Faltan credenciales de WordPress en `secrets.toml`.")
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
            fila_idx = i + 2  # +2 por encabezado y base 1
            hoja.update_cell(fila_idx, idx_estado + 1, "Publicado")
        else:
            st.error(f"❌ Error al publicar: {r.status_code}")
            st.text(r.text)




