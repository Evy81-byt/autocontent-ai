import streamlit as st
from openai import OpenAI
from fpdf import FPDF
from datetime import datetime
import gspread
import json
from google.oauth2.service_account import Credentials
import re
from plantillas import plantillas_contenido

st.set_page_config(page_title="Generador de Contenido")

# --- API KEYS ---
openai_api_key = st.secrets["OPENAI_API_KEY"]
google_creds = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

# --- Conexión Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client_sheets = gspread.authorize(creds)

try:
    sheet = client_sheets.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").sheet1
except Exception as e:
    st.error("❌ No se pudo conectar con Google Sheets.")
    sheet = None

# --- Inicio de sesión ---
if "usuario" not in st.session_state:
    st.session_state.usuario = ""

st.sidebar.title("👤 Iniciar sesión")
usuario_input = st.sidebar.text_input("Tu nombre de usuario", value=st.session_state.usuario)
if st.sidebar.button("Entrar") and usuario_input.strip():
    st.session_state.usuario = usuario_input.strip()
    st.rerun()

if not st.session_state.usuario:
    st.warning("Por favor, inicia sesión con tu nombre de usuario.")
    st.stop()

# --- UI Configuración de contenido ---
st.title("🧠 Generador de Contenido AI")
tipo = st.selectbox("Tipo de contenido", list(plantillas_contenido.keys()))
tono = st.selectbox("Tono de voz", ["Profesional", "Creativo", "Casual", "Inspirador"])

# Mostrar plantillas disponibles para el tipo seleccionado
opciones_plantilla = list(plantillas_contenido[tipo].keys())
plantilla_elegida = st.selectbox("Plantilla", opciones_plantilla)

tema = st.text_area("Tema o idea principal")


# --- Lógica IA y generación ---
def generar_contenido(tema, tipo, tono, plantilla_elegida):
    client = OpenAI(api_key=openai_api_key)
    prompt = plantillas_contenido[tipo][plantilla_elegida].format(tema=tema, tono=tono)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- PDF ---
def generar_pdf(texto, nombre_archivo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    for linea in texto.split("\n"):
        linea = re.sub(r'[^\x00-\x7F\u00A1-\u00FF]+', '', linea)
        pdf.multi_cell(0, 10, linea)
    pdf.output(nombre_archivo)

if st.button("🚀 Crear contenido"):
    if tema:
       texto = generar_contenido(tema, tipo, tono, plantilla_elegida)
 st.text_area("✍️ Contenido generado", value=texto, height=300)

        # Guardar en hoja
        fecha, hora = datetime.now().date(), datetime.now().time()
        if sheet:
            fila = [st.session_state.usuario, tema, str(fecha), str(hora), texto]
            sheet.append_row(fila)
            st.success("✅ Guardado en Google Sheets")

        # Guardar PDF
        nombre_pdf = f"contenido_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        generar_pdf(texto, nombre_pdf)
        with open(nombre_pdf, "rb") as f:
            st.download_button(label="📄 Descargar PDF", data=f, file_name=nombre_pdf, mime="application/pdf")
    else:
        st.warning("Por favor, completa el tema antes de generar contenido.")

