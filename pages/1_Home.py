import streamlit as st

st.set_page_config(page_title="✨ Bienvenido a AIMA", layout="wide")

# --- Iniciar sesión / Sesión persistente ---
st.sidebar.title("👤 Iniciar sesión")
usuario = st.sidebar.text_input("Escribe tu nombre", value=st.session_state.get("usuario", ""))
if st.sidebar.button("Entrar") and usuario.strip():
    st.session_state["usuario"] = usuario.strip()
    st.experimental_rerun()

if "usuario" not in st.session_state or not st.session_state["usuario"]:
    st.warning("👈 Inicia sesión para continuar.")
    st.stop()

usuario = st.session_state["usuario"]

# --- Estilos ---
st.markdown("""
    <style>
        .stApp {
            background-color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
            color: #2c3e50;
            padding: 1rem;
        }
        h1 {
            text-align: center;
            font-size: 2.2em;
            margin-bottom: 0.5em;
            color: #1abc9c;
        }
        .bienvenida {
            font-size: 1.3em;
            font-weight: 500;
            color: #34495e;
            text-align: center;
            margin-bottom: 2rem;
        }
        .card {
            background-color: #f4f7f9;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            margin-bottom: 1.5rem;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: scale(1.01);
        }
        .card-title {
            font-size: 1.4em;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        .card-desc {
            font-size: 1em;
            margin-bottom: 1rem;
            color: #34495e;
        }
        .btn-link {
            background-color: #1abc9c;
            color: white;
            padding: 0.6rem 1.2rem;
            text-decoration: none;
            border-radius: 8px;
            display: inline-block;
            font-weight: bold;
        }
        .btn-link:hover {
            background-color: #16a085;
            color: white;
        }
        @media (max-width: 600px) {
            h1 { font-size: 1.8em; }
            .card-title { font-size: 1.2em; }
        }
    </style>
""", unsafe_allow_html=True)

# --- Título y bienvenida ---
st.markdown("<h1>🚀 Plataforma de Contenidos AIMA</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='bienvenida'>Bienvenido/a, <strong>{usuario}</strong>. ¿Qué deseas hacer hoy?</div>", unsafe_allow_html=True)

# --- Tarjetas de navegación ---
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='card'>
        <div class='card-title'>📝 Generar Contenido</div>
        <div class='card-desc'>Crea contenido automáticamente con inteligencia artificial en distintos formatos.</div>
        <a class='btn-link' href='/Motor_de_Redaccion_AIMA'>Ir al generador</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
        <div class='card-title'>📜 Historial de Contenido</div>
        <div class='card-desc'>Consulta tu historial de contenidos generados previamente.</div>
        <a class='btn-link' href='/historial'>Ver historial</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='card'>
        <div class='card-title'>📊 Panel de Control</div>
        <div class='card-desc'>Supervisa el estado de los contenidos: pendientes, publicados y más.</div>
        <a class='btn-link' href='/panel_de_control'>Ver panel</a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='card'>
        <div class='card-title'>🚀 Publicar en WordPress</div>
        <div class='card-desc'>Publica directamente los contenidos aprobados en tu sitio WordPress.</div>
        <a class='btn-link' href='/publicar'>Ir a publicar</a>
    </div>
    """, unsafe_allow_html=True)






