import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from random import randint
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time

st.set_page_config(page_title="🔐 Recuperar Contraseña")

# --- Autenticación Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(st.secrets["GOOGLE_CREDENTIALS"], scopes=scope)
client = gspread.authorize(creds)
hoja_usuarios = client.open_by_key(st.secrets["SPREADSHEET_ID"]).worksheet("usuarios")

# --- Paso 1: Solicitar correo ---
st.title("🔐 Recuperación de contraseña")
email = st.text_input("Ingresa tu correo electrónico")

if "codigo_enviado" not in st.session_state:
    st.session_state.codigo_enviado = False

if st.button("📩 Enviar código") and email:
    registros = hoja_usuarios.get_all_records()
    usuario = next((u for u in registros if u["email"] == email), None)
    if not usuario:
        st.error("❌ Correo no encontrado.")
    else:
        codigo = randint(100000, 999999)
        st.session_state.codigo_verificacion = codigo
        st.session_state.email_recuperacion = email

        smtp_user = st.secrets["SMTP_USER"]
        smtp_pass = st.secrets["SMTP_PASS"]
        msg = MIMEMultipart()
        msg["From"] = smtp_user
        msg["To"] = email
        msg["Subject"] = "Código de recuperación AIMA"
        cuerpo = f"Tu código de recuperación es: {codigo}"
        msg.attach(MIMEText(cuerpo, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            server.quit()
            st.success("✅ Código enviado a tu correo.")
            st.session_state.codigo_enviado = True
        except Exception as e:
            st.error(f"❌ Error enviando el correo: {e}")

# --- Paso 2: Verificar código y cambiar contraseña ---
if st.session_state.codigo_enviado:
    codigo_ingresado = st.text_input("🔑 Ingresa el código recibido")
    nueva_clave = st.text_input("🔒 Nueva contraseña", type="password")
    confirmar_clave = st.text_input("🔒 Confirmar contraseña", type="password")

    if st.button("🔁 Cambiar contraseña"):
        if not (codigo_ingresado and nueva_clave and confirmar_clave):
            st.warning("Todos los campos son obligatorios.")
        elif int(codigo_ingresado) != st.session_state.codigo_verificacion:
            st.error("❌ Código incorrecto.")
        elif nueva_clave != confirmar_clave:
            st.error("❌ Las contraseñas no coinciden.")
        else:
            registros = hoja_usuarios.get_all_records()
            for idx, fila in enumerate(registros, start=2):
                if fila["email"] == st.session_state.email_recuperacion:
                    hoja_usuarios.update_cell(idx, list(fila.keys()).index("contraseña") + 1, nueva_clave)
                    st.success("✅ Contraseña actualizada correctamente.")
                    time.sleep(2)
                    st.rerun()

