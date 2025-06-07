import streamlit as st
from openai import OpenAI
from fpdf import FPDF
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import json
import re

st.set_page_config(page_title="Motor de Redacción AIMA")

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
except Exception as e:
    st.error("❌ No se pudo conectar con Google Sheets.")
    st.exception(e)
    st.stop()

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

usuario = st.session_state.usuario

# --- Interfaz de usuario ---
st.title("📝 Motor de Redacción AIMA")

tipo = st.selectbox("Tipo de contenido", ["Artículo", "Email", "Video Script", "Post Instagram", "Otro"])
tono = st.selectbox("Tono de voz", ["Formal", "Informal", "Creativo", "Inspirador"])
tema = st.text_area("Tema o idea principal")

openai_api_key = st.secrets["OPENAI_API_KEY"]

def generar_contenido(tema, tipo, tono):
    client = OpenAI(api_key=openai_api_key)
    prompt = f"Escribe un {tipo} con tono {tono} sobre: {tema}"
    respuesta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta.choices[0].message.content

def generar_pdf(texto, nombre_archivo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    for linea in texto.split("\n"):
        linea = re.sub(r'[^\x00-\x7F\u00A1-\u00FF]+', '', linea)
        pdf.multi_cell(0, 10, linea)
    pdf.output(nombre_archivo)

if st.button("✍️ Generar contenido"):
    if tema.strip():
        texto = generar_contenido(tema, tipo, tono)
        st.success("✅ Contenido generado:")
        st.text_area("🧾 Vista previa", value=texto, height=300)

        # Guardar en Google Sheets
        fecha = datetime.now().strftime("%Y-%m-%d")
        hora = datetime.now().strftime("%H:%M:%S")
        fila = [usuario, tema, tipo, tono, fecha, hora, texto]
        hoja.append_row(fila)

        # Descargar PDF
        nombre_pdf = f"{usuario}_redaccion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        generar_pdf(texto, nombre_pdf)
        with open(nombre_pdf, "rb") as f:
            st.download_button("📄 Descargar PDF", data=f, file_name=nombre_pdf, mime="application/pdf")
    else:
        st.warning("Por favor, completa el tema.")


