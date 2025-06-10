import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="✨ Bienvenido a AIMA", layout="wide")

# --- Conexión con base de usuarios ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(st.secrets["GOOGLE_CREDENTIALS"], scopes=scope)
client = gspread.authorize(creds)
usuarios_sheet = client.open_by_key(st.secrets["SPREADSHEET_ID"]).worksheet("usuarios")

# --- Interfaz de login/registro ---
st.sidebar.title("🔐 Autenticación")

if "usuario" not in st.session_state:
    st.session_state.usuario = ""
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

def autenticar(nombre, contraseña):
    datos = usuarios_sheet.get_all_records()
    for fila in datos:
        if fila["usuario"] == nombre and fila["contraseña"] == contraseña:
            return True
    return False

if not st.session_state.autenticado:
    modo = st.sidebar.radio("Selecciona acción", ["Iniciar sesión", "Registrarse"])

    nombre_input = st.sidebar.text_input("Usuario")
    password_input = st.sidebar.text_input("Contraseña", type="password")

    if modo == "Iniciar sesión":
        if st.sidebar.button("Entrar"):
            if autenticar(nombre_input, password_input):
                st.session_state.usuario = nombre_input
                st.session_state.autenticado = True
                st.success(f"✅ Bienvenido, {nombre_input}")
                st.experimental_rerun()
            else:
                st.error("❌ Credenciales incorrectas.")
    else:  # Registro
        if st.sidebar.button("Registrar"):
            registros = usuarios_sheet.get_all_records()
            if any(u["usuario"] == nombre_input for u in registros):
                st.error("⚠️ El usuario ya existe.")
            else:
                usuarios_sheet.append_row([nombre_input, password_input])
                st.success("✅ Usuario registrado. Ahora puedes iniciar sesión.")
else:
    st.sidebar.success(f"Sesión iniciada como: {st.session_state.usuario}")
    if st.sidebar.button("Cerrar sesión"):
        st.session_state.clear()
        st.experimental_rerun()

# --- Si no está autenticado, detener app ---
if not st.session_state.autenticado:
    st.stop()

# --- Interfaz principal ---
usuario = st.session_state.usuario
st.markdown("""
    <style>
        .stApp { background-color: #ffffff; font-family: 'Segoe UI', sans-serif; }
        h1 { text-align: center; font-size: 2.2em; margin-bottom: 0.5em; color: #1abc9c; }
        .bienvenida { font-size: 1.3em; font-weight: 500; color: #34495e; text-align: center; margin-bottom: 2rem; }
        .card {
            background-color: #f4f7f9;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
            transition: transform 0.2s;
        }
        .card:hover { transform: scale(1.01); }
        .card-title { font-size: 1.4em; font-weight: bold; margin-bottom: 0.5rem; }
        .card-desc { font-size: 1em; margin-bottom: 1rem; color: #34495e; }
        .btn-link {
            background-color: #1abc9c;
            color: white;
            padding: 0.6rem 1.2rem;
            text-decoration: none;
            border-radius: 8px;
            display: inline-block;
            font-weight: bold;
        }
        .btn-link:hover { background-color: #16a085; color: white; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1>🚀 Plataforma de Contenidos AIMA</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='bienvenida'>Hola <strong>{usuario}</strong>, ¿qué deseas hacer hoy?</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='card'>
        <div class='card-title'>📝 Generar Contenido</div>
        <div class='card-desc'>Crea contenido automáticamente con inteligencia artificial.</div>
        <a class='btn-link' href='/Motor_de_Redaccion_AIMA'>Ir al generador</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
        <div class='card-title'>📜 Historial de Contenido</div>
        <div class='card-desc'>Consulta tu historial de contenidos.</div>
        <a class='btn-link' href='/historial'>Ver historial</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='card'>
        <div class='card-title'>📊 Panel de Control</div>
        <div class='card-desc'>Supervisa el estado de los contenidos generados.</div>
        <a class='btn-link' href='/panel_de_control'>Ir al panel</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
        <div class='card-title'>🚀 Publicar en WordPress</div>
        <div class='card-desc'>Publica contenido directamente en tu blog.</div>
        <a class='btn-link' href='/publicar'>Ir a publicar</a>
    </div>
    """, unsafe_allow_html=True)







