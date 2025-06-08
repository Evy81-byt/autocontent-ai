import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="📝 Historial de Redacción AIMA")
st.markdown("""
    <style>
        .stApp {
            background-color: #f4f7f9;
            color: #2c3e50;
        }
        body, .stApp {
            cursor: default;
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
        textarea {
            background-color: #ffffff;
            border: 1px solid #dfe6e9;
            border-radius: 5px;
            padding: 10px;
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

google_creds = st.secrets["GOOGLE_CREDENTIALS"]
creds = Credentials.from_service_account_info(google_creds, scopes=scope)
client = gspread.authorize(creds)

try:
    sheet = client.open_by_key("1GfknVmvP8Galub6XS2jhbB0ZnBExTWtk5IXAAzp46Wg")
    hoja = sheet.worksheet("Motor de Redaccion AIMA")
    data = hoja.get_all_records()
    df = pd.DataFrame(data)

    # Normalizar nombres de columnas y renombrar si es necesario
    df.columns = [col.strip().lower() for col in df.columns]
    df = df.rename(columns={"contenido": "texto"})

    columnas_esperadas = ["usuario", "tema", "tipo", "tono", "fecha", "hora", "texto"]

    if not all(col in df.columns for col in columnas_esperadas):
        st.error("❌ Las columnas no coinciden con lo esperado.")
        st.markdown("Se esperaban columnas: `usuario`, `tema`, `tipo`, `tono`, `fecha`, `hora`, `texto`")
        st.stop()

except Exception as e:
    st.error("❌ No se pudo cargar el historial desde Google Sheets.")
    st.exception(e)
    st.stop()

# --- Interfaz de usuario ---
st.title("📝 Historial de Redacción AIMA")

usuarios_disponibles = df["usuario"].dropna().unique().tolist()
usuario_actual = st.selectbox("Selecciona un usuario", usuarios_disponibles)

df_usuario = df[df["usuario"] == usuario_actual]

if df_usuario.empty:
    st.warning("Este usuario aún no ha generado contenido.")
else:
    for idx, fila in df_usuario.iterrows():
        st.markdown(f"### ✏️ Tema: {fila['tema']}")
        st.markdown(f"**Tipo:** {fila['tipo']} | **Tono:** {fila['tono']}")
        st.markdown(f"**Fecha:** {fila['fecha']} - {fila['hora']}")
        st.text_area("📝 Contenido generado:", value=fila["texto"], height=200, key=f"texto_{idx}")
        st.markdown("---")


