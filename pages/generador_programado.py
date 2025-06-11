import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import re
from openai import OpenAI

st.set_page_config(page_title="⚙️ Generador Automático AIMA")

# --- Autenticación ---
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file",
         "https://www.googleapis.com/auth/drive"]

google_creds = st.secrets["GOOGLE_CREDENTIALS"]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])
hoja = sheet.worksheet("publicaciones_programadas")

# --- Leer temas pendientes ---
data = hoja.get_all_records()
df = pd.DataFrame(data)
pendientes = df[df["estado"].str.lower() == "pendiente"]

if pendientes.empty:
    st.info("🎉 No hay publicaciones pendientes por generar.")
    st.stop()

st.title("🤖 Generador de Publicaciones Automáticas")

openai_api_key = st.secrets["OPENAI_API_KEY"]
client_ai = OpenAI(api_key=openai_api_key)

# --- Procesar cada pendiente ---
for i, fila in pendientes.iterrows():
    tema = fila["tema"]

    st.subheader(f"🧠 Tema: {tema}")
    if st.button(f"✍️ Generar contenido - {tema}"):
        with st.spinner("Generando contenido con GPT..."):
            prompt = f"""
            Crea un artículo largo (más de 2000 palabras) sobre "{tema}", estructurado con encabezados H1, H2 y H3. 
            Añade una meta descripción SEO, keywords, y sugiere un título llamativo. El contenido debe ser informativo, emocional y original.
            """

            respuesta = client_ai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )

            texto = respuesta.choices[0].message.content.strip()

            # --- Título SEO
            titulo = texto.split('\n')[0].replace("#", "").strip()
            meta = f"Explora detalles únicos sobre: {tema}"
            slug = re.sub(r'[^a-zA-Z0-9]+', '-', titulo.lower()).strip('-')
            keywords = ", ".join([x.strip() for x in tema.split()])

            # --- Generar imagen con DALL-E
            img_response = client_ai.images.generate(prompt=tema, n=1, size="1024x1024")
            img_url = img_response.data[0].url

            st.success("✅ Contenido generado")
            st.markdown(f"### 🖼 Imagen generada")
            st.image(img_url, width=400)
            st.markdown("### ✍️ Texto generado")
            st.text_area("Vista previa", value=texto[:2000], height=300)

            # --- Guardar todo
            hoja.update_cell(i + 2, df.columns.get_loc("titulo") + 1, titulo)
            hoja.update_cell(i + 2, df.columns.get_loc("texto") + 1, texto)
            hoja.update_cell(i + 2, df.columns.get_loc("imagen_url") + 1, img_url)
            hoja.update_cell(i + 2, df.columns.get_loc("meta_descripcion") + 1, meta)
            hoja.update_cell(i + 2, df.columns.get_loc("keywords") + 1, keywords)
            hoja.update_cell(i + 2, df.columns.get_loc("slug") + 1, slug)
            hoja.update_cell(i + 2, df.columns.get_loc("estado") + 1, "generado")
