

import streamlit as st
from openai import OpenAI
from docx import Document
from fpdf import FPDF
import base64
import csv
import os

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AutoContent AI", layout="wide")
st.title("🧠 AutoContent AI - Generador de Contenido Automatizado")

if "historial" not in st.session_state:
    st.session_state.historial = []

st.sidebar.header("Configuración del contenido")
tipo_contenido = st.sidebar.selectbox("Tipo de contenido", ["Post de Instagram", "Artículo de Blog", "Email Marketing", "Guión de video"])
tono = st.sidebar.selectbox("Tono de voz", ["Profesional", "Creativo", "Casual", "Inspirador"])
tema = st.sidebar.text_input("Tema o idea principal", "")

def generar_pdf(texto, nombre_archivo):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for linea in texto.split("\n"):
        pdf.multi_cell(0, 10, linea)
    pdf.output(nombre_archivo)

def generar_docx(texto, nombre_archivo):
    doc = Document()
    for linea in texto.split("\n"):
        doc.add_paragraph(linea)
    doc.save(nombre_archivo)

def obtener_descarga_binaria(ruta_archivo):
    with open(ruta_archivo, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def guardar_en_csv(tema, contenido, fecha, hora):
    archivo = "historial.csv"
    existe = os.path.isfile(archivo)
    with open(archivo, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if not existe:
            writer.writerow(["Tema", "Fecha", "Hora", "Contenido"])
        writer.writerow([tema, fecha, hora, contenido])

if st.sidebar.button("Generar Contenido") and tema:
    with st.spinner("Generando contenido con IA..."):
        prompt = f"Escribe un {tipo_contenido.lower()} sobre el tema '{tema}' con un tono {tono.lower()}."
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un experto en marketing y redacción."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        contenido_generado = response.choices[0].message.content

        st.subheader("✍️ Contenido Generado")
        st.markdown(contenido_generado)
        st.code(contenido_generado, language="markdown")

        nombre_pdf = "contenido_generado.pdf"
        nombre_docx = "contenido_generado.docx"

        generar_pdf(contenido_generado, nombre_pdf)
        generar_docx(contenido_generado, nombre_docx)

        pdf_encoded = obtener_descarga_binaria(nombre_pdf)
        docx_encoded = obtener_descarga_binaria(nombre_docx)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📄 Descargar como PDF", base64.b64decode(pdf_encoded), nombre_pdf, "application/pdf")
        with col2:
            st.download_button("📝 Descargar como Word", base64.b64decode(docx_encoded), nombre_docx,
                               "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

        with st.expander("📈 Optimización SEO"):
            st.markdown(f"- Sugerencia de título: `Título atractivo para SEO sobre {tema}`")
            st.markdown(f"- Palabras clave: `{tema.lower()}`, `{tema.lower().split()[0]}`")
            st.markdown("- Meta descripción: Texto breve que resume el contenido de forma efectiva.")

        with st.expander("📅 Programar Publicación"):
            fecha = st.date_input("Selecciona fecha para publicación")
            hora = st.time_input("Hora de publicación")
            if st.button("📌 Guardar programación"):
                st.session_state.historial.append({
                    "tema": tema,
                    "contenido": contenido_generado,
                    "fecha": str(fecha),
                    "hora": str(hora)
                })
                guardar_en_csv(tema, contenido_generado, fecha, hora)
                st.success(f"Contenido agendado para {fecha} a las {hora}.")
else:
    st.info("Ingresa un tema para generar contenido.")

if st.session_state.historial:
    st.subheader("🗓️ Publicaciones Programadas")
    for item in reversed(st.session_state.historial):
        with st.expander(f"{item['fecha']} {item['hora']} - {item['tema']}"):
            st.markdown(item['contenido'])

