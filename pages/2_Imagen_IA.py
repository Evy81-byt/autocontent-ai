import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO
import json
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --- CONFIGURACIÓN DE API ---
openai.api_key = st.secrets["OPENAI_API_KEY"]
google_creds = st.secrets["GOOGLE_CREDENTIALS"]

# --- Conexión a Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client_sheets = gspread.authorize(creds)

# --- Intentar acceder a la hoja 'Imagen' ---
try:
    sheet_imagen = client_sheets.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").worksheet("Imagen")
except Exception as e:
    sheet_imagen = None
    st.error("❌ No se pudo conectar con la hoja 'Imagen' de Google Sheets.")

# --- Estilos modernos y puntero ---
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
        input[type="text"] {
            background-color: #ffffff;
            border: 1px solid #dfe6e9;
            border-radius: 5px;
            padding: 8px;
        }
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #ecf0f1;
        }
        ::-webkit-scrollbar-thumb {
            background: #bdc3c7;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #95a5a6;
        }
    </style>
""", unsafe_allow_html=True)

# --- INICIO DE APLICACIÓN ---
st.title("🎨 Generador de Imágenes con IA")

# Verificar usuario
if "usuario" not in st.session_state or not st.session_state.usuario:
    st.warning("Por favor, inicia sesión desde la sección de inicio.")
    st.stop()
usuario = st.session_state.usuario

# --- Entrada del usuario ---
prompt = st.text_input("Describe la imagen que quieres generar:")

# --- Crear imagen con OpenAI ---
if st.button("🖌️ Crear imagen"):
    if prompt:
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512"
            )
            image_url = response["data"][0]["url"]
            st.image(image_url, caption="Imagen generada por IA", use_column_width=True)

            # Descargar imagen
            image_response = requests.get(image_url)
            img = Image.open(BytesIO(image_response.content))

            # Botón JPG
            buf_jpg = BytesIO()
            img.save(buf_jpg, format="JPEG")
            st.download_button(
                label="📥 Descargar como JPG",
                data=buf_jpg.getvalue(),
                file_name="imagen_generada.jpg",
                mime="image/jpeg"
            )

            # Botón PNG
            buf_png = BytesIO()
            img.save(buf_png, format="PNG")
            st.download_button(
                label="📥 Descargar como PNG",
                data=buf_png.getvalue(),
                file_name="imagen_generada.png",
                mime="image/png"
            )

            # Guardar en hoja
            if sheet_imagen:
                fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                fila = [usuario, prompt, fecha, image_url]
                sheet_imagen.append_row(fila)
                st.success("✅ Imagen registrada en Google Sheets.")

        except Exception as e:
            st.error(f"❌ Error al generar o registrar la imagen: {e}")
    else:
        st.warning("Por favor, describe la imagen que quieres generar.")



