import streamlit as st
import openai
import base64
from io import BytesIO
from PIL import Image

st.set_page_config(page_title="Generador de Imágenes con IA", layout="wide")

st.title("🎨 Generador de Imágenes con Inteligencia Artificial")

# --- Validar inicio de sesión ---
usuario = st.session_state.get("usuario", "")
if not usuario:
    st.warning("Debes iniciar sesión desde la página principal.")
    st.stop()

# --- Configurar cliente OpenAI ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Entrada del usuario ---
prompt = st.text_area("Describe lo que deseas ver en la imagen", placeholder="Ej: Un paisaje futurista con montañas y neón", height=150)

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

            except Exception as e:
                st.error(f"❌ Ocurrió un error al generar la imagen: {e}")
