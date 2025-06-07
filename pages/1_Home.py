import streamlit as st
from openai import OpenAI
from fpdf import FPDF
from datetime import datetime
import gspread
import json
from google.oauth2.service_account import Credentials
import re

st.set_page_config(page_title="Generador de Contenido AI", layout="wide")

# --- Cargar claves desde secrets ---
openai_api_key = st.secrets["OPENAI_API_KEY"]
google_creds = json.loads(st.secrets["GOOGLE_CREDENTIALS"])

# --- Conexión con Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client_sheets = gspread.authorize(creds)

try:
    sheet = client_sheets.open_by_key("1e0WAgCTEaTzgjs0ehUd7rdkEJgeUL4YR_uoftV1lRyg").worksheet("Historial")
except Exception as e:
    st.error("❌ No se pudo conectar con la hoja de Google Sheets.")
    sheet = None

# --- Sesión de usuario ---
if "usuario" not in st.session_state:
    st.session_state.usuario = ""

st.sidebar.title("👤 Iniciar sesión")
usuario_input = st.sidebar.text_input("Tu nombre de usuario", value=st.session_state.usuario)
if st.sidebar.button("Entrar") and usuario_input.strip():
    st.session_state.usuario = usuario_input.strip()
    st.rerun()

if not st.session_state.usuario:
    st.warning("Por favor, inicia sesión para acceder.")
    st.stop()

usuario = st.session_state.usuario
st.success(f"Bienvenido, {usuario} 👋")

# --- Interfaz ---
st.title("🧠 Generador de Contenido con IA")

tipo = st.selectbox("📌 Tipo de contenido", ["Post de Instagram", "Artículo de Blog", "Email Marketing", "Guión de video", "TikTok / Reel"])
tono = st.selectbox("🎙️ Tono de voz", ["Profesional", "Creativo", "Casual", "Inspirador"])
tema = st.text_area("💡 Tema o idea principal")
plantilla_elegida = st.selectbox("📋 Plantilla (opcional)", ["Plantilla 1", "Plantilla 2", "Ninguna"])

# --- Función IA ---
def generar_contenido(tema, tipo, tono):
    client = OpenAI(api_key=openai_api_key)
    prompt = f"Genera un {tipo} con tono {tono} sobre: {tema}"
    if plantilla_elegida != "Ninguna":
        prompt += f". Usa la estructura de la {plantilla_elegida.lower()}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# --- Función PDF ---
def generar_pdf(texto, nombre_archivo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_auto_page_break(auto=True, margin=15)
    for linea in texto.split("\n"):
        linea = re.sub(r'[^\x00-\x7F\u00A1-\u00FF]+', '', linea)
        pdf.multi_cell(0, 10, linea)
    pdf.output(nombre_archivo)

# --- Botón Crear ---
if st.button("🚀 Crear contenido"):
    if tema:
        texto = generar_contenido(tema, tipo, tono)
        st.text_area("✍️ Contenido generado", value=texto, height=300)

        fecha, hora = datetime.now().date(), datetime.now().strftime("%H:%M:%S")
        if sheet:
            fila = [usuario, tema, tipo, tono, plantilla_elegida, str(fecha), str(hora), texto]
            sheet.append_row(fila)
            st.success("✅ Guardado correctamente en Google Sheets")

        nombre_pdf = f"contenido_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        generar_pdf(texto, nombre_pdf)
        with open(nombre_pdf, "rb") as f:
            st.download_button("📄 Descargar PDF", data=f, file_name=nombre_pdf, mime="application/pdf")
    else:
        st.warning("Por favor, completa el campo de tema.")


