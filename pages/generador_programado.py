import openai
import gspread
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
import random
import re

# --- Configuración ---
openai.api_key = "TU_OPENAI_API_KEY"
SPREADSHEET_ID = "1GfknVmvP8Galub6XS2jhbB0ZnBExTWtk5IXAAzp46Wg"
TEMAS = [
    "Curiosidades del mundo",
    "Lugares ocultos de nuestro planeta",
    "Maravillas modernas que pocos conocen",
    "Ciudades perdidas y civilizaciones olvidadas",
    "Fenómenos naturales impresionantes",
    "Secretos de la Tierra que parecen de otro mundo",
    "Lugares místicos y sagrados poco explorados"
]

# --- Google Sheets ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file("clave.json", scopes=scope)  # Asegúrate de tener clave.json en tu carpeta
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID)
hoja = sheet.worksheet("Publicaciones Programadas")

# --- Funciones ---
def generar_slug(texto):
    return re.sub(r'\s+', '-', texto.lower()).replace('ñ', 'n').strip('-')

def generar_contenido(tema):
    prompt = f"""
Genera un artículo detallado y atractivo de más de 2000 palabras para un blog titulado 'Maravilloso Planeta' sobre el tema: {tema}.
Incluye título SEO, meta descripción, keywords, y divide el texto con encabezados (H2, H3).
"""
    respuesta = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta.choices[0].message.content

# --- Crear 7 publicaciones ---
hoy = datetime.now()
for i in range(7):
    fecha_pub = (hoy + timedelta(days=i)).strftime("%Y-%m-%d")
    tema = random.choice(TEMAS)
    contenido_bruto = generar_contenido(tema)

    # Separar por bloques comunes con Regex
    titulo = contenido_bruto.split("\n")[0].replace("#", "").strip()
    texto = "\n".join(contenido_bruto.split("\n")[1:]).strip()
    meta_desc = f"Descubre sobre: {tema} en Maravilloso Planeta."
    keywords = ", ".join(tema.lower().split())
    slug = generar_slug(titulo)

    hoja.append_row([
        fecha_pub,
        tema,
        titulo,
        texto,
        "",  # imagen_url se puede llenar después
        meta_desc,
        keywords,
        slug,
        "pendiente"
    ])

