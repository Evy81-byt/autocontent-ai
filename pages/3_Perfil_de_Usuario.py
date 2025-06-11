import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

st.set_page_config(page_title="👤 Mi Perfil")

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

# --- Verificación de sesión ---
if "usuario" not in st.session_state or not st.session_state.usuario:
    st.warning("⚠️ Por favor, inicia sesión primero.")
    st.stop()

usuario_actual = st.session_state.usuario
registros = hoja_usuarios.get_all_records()
usuario_data = next((u for u in registros if u["usuario"] == usuario_actual), None)

if not usuario_data:
    st.error("❌ Usuario no encontrado.")
    st.stop()

# --- Mostrar y editar perfil ---
st.title("👤 Mi Perfil")

nuevo_usuario = st.text_input("Nombre de usuario", value=usuario_data["usuario"])
nuevo_email = st.text_input("Correo electrónico", value=usuario_data["email"])
nueva_contrasena = st.text_input("Nueva contraseña", type="password", placeholder="Dejar en blanco para no cambiar")

if st.button("💾 Guardar cambios"):
    fila_index = registros.index(usuario_data) + 2  # +2 por encabezado y base 1
    hoja_usuarios.update_cell(fila_index, 1, nuevo_usuario)
    hoja_usuarios.update_cell(fila_index, 3, nuevo_email)
    if nueva_contrasena.strip():
        hoja_usuarios.update_cell(fila_index, 2, nueva_contrasena)
    st.success("✅ Perfil actualizado correctamente.")
    st.session_state.usuario = nuevo_usuario
