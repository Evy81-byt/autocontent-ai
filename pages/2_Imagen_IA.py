import streamlit as st
import openai

st.set_page_config(page_title="Imágenes IA")

st.title("🖼️ Generador de Imágenes con IA")
descripcion = st.text_area("Describe la imagen que deseas generar")

if st.button("🎨 Generar imagen"):
    if descripcion:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        response = client.images.generate(prompt=descripcion, n=1, size="512x512")
        url = response.data[0].url
        st.image(url, caption="Imagen generada")
    else:
        st.warning("Por favor, escribe una descripción.")
