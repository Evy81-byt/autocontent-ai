import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="📊 Panel de Control de Contenidos")
st.markdown("""
    <style>
        .stApp {
            background-color: #f4f7f9;
            color: #2c3e50;
        }
        body, .stApp {
            cursor: pointer;
        }
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif;
            font-weight: 700;
            color: #2c3e50;
        }
        .markdown-text-container {
            font-family: 'Segoe UI', sans-serif;
            font-size: 16px;
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #1abc9c;
            color: white;
            padding: 0.5em 1em;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #16a085;
        }
        textarea, input, select {
            background-color: #ffffff !important;
            border: 1px solid #dfe6e9 !important;
            border-radius: 5px !important;
            padding: 10px !important;
        }
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #ecf0f1;
        }
        ::-webkit-scrollbar-thumb {
            background: #bdc3c7;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #95a5a6;
        }
    </style>
""", unsafe_allow_html=True)

# --- Autenticación Google Sheets ---
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
    sheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])  # Usa ID desde secrets
    hoja = sheet.worksheet("Motor de Redaccion AIMA")  # Hoja unificada
    datos = hoja.get_all_records()
    df = pd.DataFrame(datos)

    # Normalizar nombres de columnas
    df.columns = [col.strip().lower() for col in df.columns]

    # Verificación de columnas esperadas
    columnas_esperadas = ["usuario", "tema", "tipo", "tono", "fecha", "hora", "texto", "estado"]
    if not all(col in df.columns for col in columnas_esperadas):
        st.error("❌ Las columnas no coinciden con lo esperado.")
        st.markdown("Se esperaban columnas: `usuario`, `tema`, `tipo`, `tono`, `fecha`, `hora`, `texto`, `estado`")
        st.stop()

except Exception as e:
    st.error("❌ No se pudo cargar el panel desde Google Sheets.")
    st.exception(e)
    st.stop()

# --- Interfaz de filtros ---
st.title("📊 Panel de Control de Contenidos")

usuarios_disponibles = df["usuario"].dropna().unique().tolist()
usuario_filtro = st.selectbox("Filtrar por usuario", options=["Todos"] + usuarios_disponibles)

estados_disponibles = df["estado"].dropna().unique().tolist()
estado_filtro = st.selectbox("Filtrar por estado", options=["Todos"] + estados_disponibles)

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






         
