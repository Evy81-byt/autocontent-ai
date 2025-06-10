import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="🔓 Iniciar sesión")

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

st.title("🔓 Iniciar sesión")

correo = st.text_input("Correo electrónico")
password = st.text_input("Contraseña", type="password")

if st.button("Entrar"):
    usuarios = usuarios_sheet.get_all_records()
    for u in usuarios:
        if u["correo"] == correo and u["contraseña"] == password:
            st.session_state.usuario = u["nombre"]
            st.success(f"✅ Bienvenido, {u['nombre']}")
            st.experimental_rerun()
            break
    else:
        st.error("❌ Correo o contraseña incorrectos.")
