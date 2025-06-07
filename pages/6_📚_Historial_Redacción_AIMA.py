import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json
import re
from fpdf import FPDF
from datetime import datetime

st.set_page_config(page_title="📚 Historial Redacción AIMA")

# --- Conexión a Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

try:
   google_creds = st.secrets["GOOGLE_CREDENTIALS"]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client = gspread.authorize(creds)

    sheet = client.open_by_key("1GfknVmvP8Galub6XS2jhbB0ZnBExTWtk5IXAAzp46Wg")
    hoja = sheet.worksheet("Motor de Redaccion AIMA")
    data = hoja.get_all_records()
    df = pd.DataFrame(data)
except Exception as e:
    st.error("❌ No se pudo conectar con Google Sheets.")
    st.exception(e)
    st.stop()

# --- Filtros ---
st.title("📚 Historial de Contenidos (AIMA)")

if df.empty:
    st.warning("Aún no se ha generado contenido.")
    st.stop()

usuarios = df["Usuario"].dropna().unique().tolist()
usuario_seleccionado = st.selectbox("👤 Filtrar por usuario", ["Todos"] + usuarios)

tipos = df["Tipo"].dropna().unique().tolist()
tipo_seleccionado = st.selectbox("📝 Tipo de contenido", ["Todos"] + tipos)

tono_seleccionado = st.selectbox("🎙️ Tono de voz", ["Todos"] + df["Tono"].dropna().unique().tolist())

# Filtrado dinámico
if usuario_seleccionado != "Todos":
    df = df[df["Usuario"] == usuario_seleccionado]

if tipo_seleccionado != "Todos":
    df = df[df["Tipo"] == tipo_seleccionado]

if tono_seleccionado != "Todos":
    df = df[df["Tono"] == tono_seleccionado]

# --- Mostrar contenido ---
for i, fila in df.iterrows():
    st.markdown(f"### 🎯 Tema: {fila['Tema']}")
    st.markdown(f"📝 **Tipo:** {fila['Tipo']} | 🎙️ **Tono:** {fila['Tono']}")
    st.markdown(f"📅 **Fecha:** {fila['Fecha']} 🕒 {fila['Hora']}")
    st.text_area("✍️ Contenido generado", value=fila.get("Contenido", "Sin contenido"), height=250)

    # Botón para descargar como PDF
    texto = fila.get("Contenido", "")
    nombre_pdf = f"{fila['Usuario']}_AIMA_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    def generar_pdf(contenido):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_auto_page_break(auto=True, margin=15)
        for linea in contenido.split("\n"):
            linea = re.sub(r'[^\x00-\x7F\u00A1-\u00FF]+', '', linea)
            pdf.multi_cell(0, 10, linea)
        pdf.output(nombre_pdf)

    generar_pdf(texto)
    with open(nombre_pdf, "rb") as f:
        st.download_button(label="📄 Descargar PDF", data=f, file_name=nombre_pdf, mime="application/pdf")

    st.markdown("---")
