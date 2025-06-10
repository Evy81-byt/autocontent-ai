import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="📊 Panel de Control de Contenidos", layout="wide")
st.markdown("""
    <style>
        html, body, .stApp {
            max-width: 100%;
            overflow-x: hidden;
            background-color: #f4f7f9;
            font-family: 'Segoe UI', sans-serif;
            color: #2c3e50;
        }
        h1, h2, h3 {
            font-weight: 700;
            font-size: 1.6em;
        }
        .stTextInput, .stTextArea, .stSelectbox, .stButton>button {
            font-size: 16px !important;
            padding: 10px 14px !important;
        }
        .stButton>button {
            background-color: #1abc9c;
            color: white;
            font-weight: bold;
            border-radius: 6px;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #16a085;
        }
        textarea, input, select {
            background-color: #ffffff !important;
            border: 1px solid #dfe6e9 !important;
            border-radius: 5px !important;
        }
        @media only screen and (max-width: 600px) {
            h1, h2, h3 { font-size: 1.4em; }
            .stTextInput, .stTextArea, .stSelectbox, .stButton>button {
                font-size: 14px !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- Autenticación con Google Sheets ---
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

try:
    google_creds = st.secrets["GOOGLE_CREDENTIALS"]
    creds = Credentials.from_service_account_info(google_creds, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])
    hoja = sheet.worksheet("Motor de Redaccion AIMA")
    datos = hoja.get_all_records()

    if not datos:
        st.info("🔍 Aún no hay datos en la hoja.")
        st.stop()

    df = pd.DataFrame(datos)
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={"contenido": "texto"})

    columnas_esperadas = ["estado", "usuario", "tema", "tipo", "tono", "fecha", "hora", "texto"]
    if not all(col in df.columns for col in columnas_esperadas):
        st.error("❌ Las columnas no coinciden con lo esperado.")
        st.markdown("Se esperaban columnas: `estado`, `usuario`, `tema`, `tipo`, `tono`, `fecha`, `hora`, `texto`")
        st.stop()

except Exception as e:
    st.error("❌ No se pudo cargar el panel desde Google Sheets.")
    st.exception(e)
    st.stop()

# --- Interfaz de filtros ---
st.title("📊 Panel de Control de Contenidos")

usuarios_disponibles = df["usuario"].dropna().unique().tolist()
usuario_filtro = st.selectbox("👤 Filtrar por usuario", options=["Todos"] + usuarios_disponibles)

estados_disponibles = df["estado"].dropna().unique().tolist()
estado_filtro = st.selectbox("📌 Filtrar por estado", options=["Todos"] + estados_disponibles)

# --- Aplicar filtros ---
if usuario_filtro != "Todos":
    df = df[df["usuario"] == usuario_filtro]

if estado_filtro != "Todos":
    df = df[df["estado"] == estado_filtro]

# --- Mostrar resultados ---
if df.empty:
    st.warning("No hay datos para mostrar con los filtros seleccionados.")
else:
    st.dataframe(df[["usuario", "tema", "tipo", "tono", "fecha", "hora", "estado"]], use_container_width=True)








         
