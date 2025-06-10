import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="🔐 Registro de Usuario")

# Autenticación con Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(st.secrets["GOOGLE_CREDENTIALS"], scopes=scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])
usuarios_sheet = sheet.worksheet("usuarios")

st.title("🔐 Registro de nuevo usuario")

correo = st.text_input("Correo electrónico")
nombre = st.text_input("Nombre completo")
password = st.text_input("Contraseña", type="password")

if st.button("Registrarse"):
    if correo and nombre and password:
        # Verificar si ya existe el correo
        usuarios = usuarios_sheet.get_all_records()
        if any(u["correo"] == correo for u in usuarios):
            st.warning("⚠️ Ya existe una cuenta con ese correo.")
        else:
            usuarios_sheet.append_row([correo, nombre, password])
            st.success("✅ Registro exitoso. Ahora puedes iniciar sesión.")
    else:
        st.warning("⚠️ Completa todos los campos.")
