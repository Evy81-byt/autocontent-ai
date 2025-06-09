import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="📝 Historial de Redacción AIMA")

# --- Estilos personalizados ---
st.markdown("""
    <style>
        .stApp {
            background-color: #f4f7f9;
            color: #2c3e50;
        }
        body, .stApp { cursor: default; }
        h1, h2, h3 {
            font-family: 'Segoe UI', sans-serif;
            font-weight: 700;
            color: #2c3e50;
        }
        .stButton>button {
            background-color: #1abc9c;
            color: white;
            border-radius: 6px;
            font-weight: bold;
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
    </style>
""", unsafe_allow_html=True)

# --- Autenticación con Google Sheets ---
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
    sheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])
    hoja = sheet.worksheet("Motor de Redaccion AIMA")
    data = hoja.get_all_records()
    df = pd.DataFrame(data)
    st.write("Columnas reales detectadas:", df.columns.tolist())


  # Limpiar y normalizar columnas
df.columns = [col.strip().lower().replace("á", "a").replace("é", "e").replace("í", "i")
              .replace("ó", "o").replace("ú", "u") for col in df.columns]

# Renombrar posibles variantes a "texto"
for posible in ["contenido", "text", "content"]:
    if posible in df.columns:
        df = df.rename(columns={posible: "texto"})


    columnas_esperadas = ["usuario", "tema", "tipo", "tono", "fecha", "hora", "texto", "estado"]
    if not all(col in df.columns for col in columnas_esperadas):
        st.error("❌ Las columnas no coinciden con lo esperado.")
        st.markdown("Se esperaban columnas: `usuario`, `tema`, `tipo`, `tono`, `fecha`, `hora`, `texto`, `estado`")
        st.stop()

except Exception as e:
    st.error("❌ No se pudo cargar o sincronizar con Google Sheets.")
    st.exception(e)
    st.stop()

# --- Interfaz de selección de usuario ---
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
        st.markdown(f"📅 {fila['fecha']} ⏰ {fila['hora']}")
        st.text_area("📝 Contenido generado:", value=fila["texto"], height=250, key=f"texto_{idx}")
        st.markdown("---")







