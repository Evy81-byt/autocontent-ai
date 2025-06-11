import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import smtplib
from email.mime.text import MIMEText

st.set_page_config(page_title="🔑 Recuperar Contraseña")

# --- Conexión Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
google_creds = st.secrets["GOOGLE_CREDENTIALS"]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])
usuarios_sheet = sheet.worksheet("usuarios")

df = pd.DataFrame(usuarios_sheet.get_all_records())

# --- Interfaz ---
st.title("🔑 Recuperar Contraseña")
email = st.text_input("Ingresa tu correo electrónico registrado")

if st.button("Enviar instrucciones"):
    if not email:
        st.warning("Por favor, ingresa tu email.")
    elif email not in df["email"].values:
        st.error("❌ El email no está registrado.")
    else:
        # --- Enviar correo ---
        smtp_user = st.secrets["SMTP_USER"]
        smtp_pass = st.secrets["SMTP_PASS"]
        asunto = "Recuperación de contraseña - AIMA"
        mensaje = f"""
Hola,

Hemos recibido una solicitud para restablecer tu contraseña. 
Actualmente, este sistema aún no permite cambios automáticos por seguridad.

Por favor, contacta al administrador para solicitar un reinicio manual o responde a este mensaje.

Gracias,
Soporte AIMA
        """

        msg = MIMEText(mensaje)
        msg["Subject"] = asunto
        msg["From"] = smtp_user
        msg["To"] = email

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(smtp_user, smtp_pass)
                server.sendmail(smtp_user, email, msg.as_string())
            st.success("📧 Instrucciones enviadas. Revisa tu correo.")
        except Exception as e:
            st.error("❌ No se pudo enviar el correo.")
            st.exception(e)
