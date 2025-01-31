from flask import Flask, request, jsonify
import requests
import io
import pdfplumber

app = Flask(__name__)

# Diccionario con las URLs de los aeropuertos y sus categorías
AIP_URLS = {
    "GCLP": {
        "datos_aerodromo": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_en.pdf",
        "STAR_03L_03R": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_STAR_1_en.pdf",
        "STAR_21L_21R": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_STAR_2_en.pdf",
        "SID_03L_03R": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_SID_1_en.pdf",
        "SID_21L_21R": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_SID_2_en.pdf"
    },
    "GCTS": {  # Tenerife Sur
        "datos_aerodromo": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCTS/LE_AD_2_GCTS_en.pdf",
        "STAR_07": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCTS/LE_AD_2_GCTS_STAR_1_en.pdf",
        "STAR_25": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCTS/LE_AD_2_GCTS_STAR_2_en.pdf",
        "SID_07": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCTS/LE_AD_2_GCTS_SID_1_en.pdf",
        "SID_25": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCTS/LE_AD_2_GCTS_SID_2_en.pdf"
    },
    "GCRR": {  # Lanzarote
        "datos_aerodromo": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_en.pdf",
        "STAR_03": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_STAR_1_en.pdf",
        "STAR_03_rnva1_gnss": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_STAR_2_en.pdf",
        "STAR_21": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_STAR_3_en.pdf",
        "STAR_21_rnva1_gnss": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_STAR_4_en.pdf",
        "SID_03": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_SID_1_en.pdf",
        "SID_03_rnav1_gnss": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_SID_2_en.pdf",
        "SID_03_rnav1_dme_dme": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_SID_3_en.pdf",
        "SID_21": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_SID_4_en.pdf",
        "SID_21_rnav1": "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCRR/LE_AD_2_GCRR_SID_5_en.pdf"
    }
}


@app.route("/procesar_pdf", methods=["POST"])
def procesar_pdf():
    try:
        # Obtener datos de la solicitud
        data = request.json
        aerodromo = data.get("aerodromo")
        categoria = data.get("categoria")
        pista = data.get("pista", "")  # Pista opcional
        query = data.get("query")

        # Validar parámetros
        if not aerodromo or not categoria or not query:
            return jsonify({"error": "Faltan parámetros requeridos: aerodromo, categoria, query"}), 400

        # Obtener la URL del PDF según la solicitud
        clave_pdf = f"{categoria}_{pista}" if pista else categoria
        pdf_url = AIP_URLS.get(aerodromo, {}).get(clave_pdf)

        if not pdf_url:
            return jsonify({"error": "No se encontró la URL del PDF para la consulta especificada."}), 404

        # Descargar el PDF
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code != 200:
            return jsonify({"error": "No se pudo descargar el PDF desde ENAIRE."}), 400

        pdf_file = io.BytesIO(pdf_response.content)

        # Extraer texto y buscar la consulta
        resultados = []
        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and query.lower() in text.lower():
                    resultados.append(f"Página {page_num + 1}: {text[:500]}...")

        # Devolver resultados
        if not resultados:
            return jsonify({"resultados": "No se encontraron coincidencias en el PDF."})

        return jsonify({"resumen": f"Se encontraron {len(resultados)} coincidencias.", "detalles": resultados})

    except Exception as e:
        return jsonify({"error": f"Error al procesar el PDF: {str(e)}"}), 500

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Usar el puerto que Render asigna automáticamente
    app.run(host="0.0.0.0", port=port)

