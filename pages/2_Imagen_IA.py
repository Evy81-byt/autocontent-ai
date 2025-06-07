import streamlit as st
import openai

# --- API Key de OpenAI ---
openai_api_key = st.secrets["OPENAI_API_KEY"]
openai.api_key = openai_api_key

st.title("🎨 Generador de Imágenes con IA")

prompt = st.text_input("Describe la imagen que quieres generar:")

if st.button("🖌️ Crear imagen"):
    if prompt:
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512"
            )
            image_url = response['data'][0]['url']
            st.image(image_url, caption="Imagen generada por IA", use_column_width=True)
        except Exception as e:
            st.error(f"❌ Error al generar imagen: {str(e)}")
    else:
        st.warning("Por favor, escribe una descripción para la imagen.")


