from flask import Flask, request, jsonify
from flask_cors import CORS  # <-- Importa CORS
import requests
import io
import pdfplumber
import re
from pdf2image import convert_from_bytes
import pytesseract
import os

app = Flask(__name__)
CORS(app)  # <-- Habilita CORS en toda la API

# Diccionario con las URLs de los aeropuertos y sus categorías
AIP_URLS = {
    "GCLP": {
        "datos_aerodromo": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_en.pdf",
        "STAR_03L_03R": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_STAR_1_en.pdf",
        "STAR_21L_21R": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_STAR_2_en.pdf",
        "SID_03L_03R": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_SID_1_en.pdf",
        "SID_21L_21R": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_SID_2_en.pdf"
    },
    "GCRR": {
        "datos_aerodromo": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_en.pdf",
        "STAR_03": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_STAR_1_en.pdf",
        "SID_03": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_SID_1_en.pdf"
    }
}

def extraer_texto_pdf(pdf_url):
    """Descarga un PDF, extrae texto con pdfplumber o usa OCR si es una imagen."""
    response = requests.get(pdf_url, timeout=10)
    if response.status_code != 200:
        return None

    pdf_file = io.BytesIO(response.content)
    texto_extraido = ""

    # Intentar extraer texto con pdfplumber
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                texto_extraido += text + "\n"

    # Si no se encontró texto, usar OCR
    if not texto_extraido.strip():
        images = convert_from_bytes(pdf_file.read())
        for img in images:
            texto_extraido += pytesseract.image_to_string(img) + "\n"

    return texto_extraido.strip()

@app.route("/procesar_pdf", methods=["POST"])
def procesar_pdf():
    try:
        data = request.json
        aerodromo = data.get("aerodromo")
        categoria = data.get("categoria")
        pista = data.get("pista", "")
        query = data.get("query")

        if not aerodromo or not categoria or not query:
            return jsonify({"error": "Faltan parámetros requeridos: aerodromo, categoria, query"}), 400

        clave_pdf = f"{categoria}_{pista}" if pista else categoria
        pdf_url = AIP_URLS.get(aerodromo, {}).get(clave_pdf)

        if not pdf_url:
            return jsonify({"error": "No se encontró la URL del PDF para la consulta especificada."}), 404

        texto_pdf = extraer_texto_pdf(pdf_url)

        if not texto_pdf:
            return jsonify({"error": "No se pudo extraer texto del PDF."}), 500

        resultados = []
        clean_text = re.sub(r'\s+', ' ', texto_pdf.lower())  # Normalizar espacios
        if query.lower() in clean_text:
            resultados.append(f"Texto encontrado en el PDF: {clean_text[:500]}...")

        if not resultados:
            return jsonify({"resultados": "No se encontraron coincidencias en el PDF."})

        return jsonify({"resumen": f"Se encontraron {len(resultados)} coincidencias.", "detalles": resultados})

    except Exception as e:
        return jsonify({"error": f"Error al procesar el PDF: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
