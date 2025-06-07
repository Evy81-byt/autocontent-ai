import streamlit as st
import openai
import requests
from PIL import Image
from io import BytesIO
import base64

# --- Configuración inicial ---
st.title("🎨 Generador de Imágenes con IA")

# --- Clave de API ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

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

            # Descargar la imagen
            image_response = requests.get(image_url)
            img = Image.open(BytesIO(image_response.content))

            # Mostrar botones para descargar
            buf_jpg = BytesIO()
            img.save(buf_jpg, format="JPEG")
            st.download_button(
                label="📥 Descargar como JPG",
                data=buf_jpg.getvalue(),
                file_name="imagen_generada.jpg",
                mime="image/jpeg"
            )

            buf_png = BytesIO()
            img.save(buf_png, format="PNG")
            st.download_button(
                label="📥 Descargar como PNG",
                data=buf_png.getvalue(),
                file_name="imagen_generada.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"❌ Error al generar imagen: {e}")
    else:
        st.warning("Por favor, describe la imagen que quieres generar.")


