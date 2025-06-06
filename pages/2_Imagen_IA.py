import streamlit as st
import openai
import base64
from datetime import datetime
import json
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Generador de Imágenes con IA", layout="wide")

st.title("🎨 Generador de Imágenes con Inteligencia Artificial")

# --- Validar usuario ---
usuario = st.session_state.get("usuario", "")
if not usuario:
    st.warning("Debes iniciar sesión desde la página principal.")
    st.stop()

# --- Conexión OpenAI ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Conexión Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(
    json.loads(st.secrets["GOOGLE_CREDENTIALS"]),
    scopes=scope
)
client_sheets = gspread.authorize(creds)

try:
    sheet = client_sheets.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").worksheet("Imagenes")
except Exception as e:
    st.error("❌ No se pudo acceder a la hoja 'Imagenes' en Google Sheets.")
    sheet = None

# --- Interfaz ---
prompt = st.text_area("Describe lo que deseas ver en la imagen", placeholder="Ej: Un castillo medieval flotando sobre nubes de neón", height=150)
num_images = st.slider("Cantidad de imágenes", 1, 4, 1)
resolution = st.selectbox("Resolución", ["256x256", "512x512", "1024x1024"], index=1)

# --- Generación de imágenes ---
if st.button("🎨 Generar imagen"):
    if not prompt.strip():
        st.warning("Por favor, describe lo que deseas generar.")
    else:
        with st.spinner("Generando imagen..."):
            try:
                response = openai.Image.create(
                    prompt=prompt,
                    n=num_images,
                    size=resolution
                )
                st.subheader("🖼️ Resultado(s):")
                for i, image_info in enumerate(response["data"]):
                    img_url = image_info["url"]
                    st.image(img_url, caption=f"Imagen {i+1}", use_column_width=True)
                    st.markdown(f"[🔗 Ver imagen en nueva pestaña]({img_url})", unsafe_allow_html=True)

                    # Registrar en Google Sheets
                    if sheet:
                        ahora = datetime.now()
                        fila = [
                            usuario,
                            ahora.strftime("%Y-%m-%d"),
                            ahora.strftime("%H:%M:%S"),
                            prompt,
                            resolution,
                            img_url
                        ]
                        sheet.append_row(fila)

                st.success("✅ Imágenes registradas correctamente en Google Sheets.")

            except Exception as e:
                st.error(f"❌ Ocurrió un error al generar la imagen: {e}")

