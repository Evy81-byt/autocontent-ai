import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="🔐 Iniciar sesión - AIMA")

# --- Google Sheets auth ---
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

# --- Funciones ---
def verificar_usuario(usuario, contraseña):
    registros = usuarios_sheet.get_all_records()
    for fila in registros:
        if fila["usuario"] == usuario and fila["contraseña"] == contraseña:
            return True
    return False

def usuario_existe(usuario):
    registros = usuarios_sheet.col_values(1)
    return usuario in registros

def registrar_usuario(usuario, email, contraseña):
    if usuario_existe(usuario):
        return False
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    usuarios_sheet.append_row([usuario, email, contraseña, fecha])
    return True

# --- UI ---
modo = st.radio("Selecciona una opción", ["Iniciar sesión", "Registrarse"])

if modo == "Iniciar sesión":
    st.title("🔐 Iniciar sesión")
    usuario = st.text_input("Usuario")
    contraseña = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if verificar_usuario(usuario, contraseña):
            st.success(f"Bienvenido {usuario}")
            st.session_state.usuario = usuario
            st.switch_page("pages/2_Historial.py")
        else:
            st.error("Usuario o contraseña incorrectos.")

elif modo == "Registrarse":
    st.title("📝 Crear cuenta")
    nuevo_usuario = st.text_input("Nuevo usuario")
    nuevo_email = st.text_input("Correo electrónico")
    nueva_contraseña = st.text_input("Contraseña", type="password")
    if st.button("Registrarme"):
        if registrar_usuario(nuevo_usuario, nuevo_email, nueva_contraseña):
            st.success("✅ Usuario registrado correctamente. Inicia sesión ahora.")
        else:
            st.error("❌ El usuario ya existe.")

