import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import hashlib

st.set_page_config(page_title="Inicio de sesión")

# --- Establecer conexión con Google Sheets ---
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

# --- Cargar los datos existentes ---
usuarios_data = usuarios_sheet.get_all_records()
df_usuarios = pd.DataFrame(usuarios_data)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

st.title("🔐 Inicio de Sesión")

menu = ["Iniciar Sesión", "Registrarse"]
choice = st.sidebar.selectbox("Navegación", menu)

if choice == "Iniciar Sesión":
    st.subheader("Ingresa tus credenciales")
    usuario = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar sesión"):
        if usuario and password:
            if not df_usuarios.empty and usuario in df_usuarios["usuario"].values:
                fila = df_usuarios[df_usuarios["usuario"] == usuario].iloc[0]
                if hash_password(password) == fila["contraseña"]:
                    st.success(f"Bienvenido {usuario}")
                    st.session_state.usuario = usuario
                    st.rerun()
                else:
                    st.error("Contraseña incorrecta.")
            else:
                st.error("Usuario no registrado.")
        else:
            st.warning("Por favor completa ambos campos.")

elif choice == "Registrarse":
    st.subheader("Crear nueva cuenta")
    nuevo_usuario = st.text_input("Nuevo nombre de usuario")
    nuevo_email = st.text_input("Correo electrónico")
    nueva_pass = st.text_input("Nueva contraseña", type="password")
    if st.button("Registrarme"):
        if nuevo_usuario and nuevo_email and nueva_pass:
            if nuevo_usuario in df_usuarios["usuario"].values:
                st.warning("⚠️ El usuario ya existe.")
            else:
                hashed = hash_password(nueva_pass)
                nueva_fila = [nuevo_usuario, hashed, nuevo_email]
                usuarios_sheet.append_row(nueva_fila)
                st.success("✅ Registro exitoso, ahora inicia sesión.")
                st.rerun()
        else:
            st.warning("Todos los campos son obligatorios.")

# --- Cierre de sesión ---
if "usuario" in st.session_state:
    st.sidebar.markdown(f"👤 Usuario actual: `{st.session_state['usuario']}`")
    if st.sidebar.button("Cerrar sesión"):
        del st.session_state["usuario"]
        st.rerun()








