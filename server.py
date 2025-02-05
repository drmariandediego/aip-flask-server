from flask import Flask, request, jsonify
import requests
import gdown
import io
import pdfplumber
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from flask_cors import CORS

import os
from google.oauth2 import service_account

# Obtiene la ruta del archivo de credenciales desde las variables de entorno
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")

if not os.path.exists(CREDENTIALS_PATH):
    raise FileNotFoundError(f"❌ No se encontró el archivo de credenciales en {CREDENTIALS_PATH}")

# Carga las credenciales
creds = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

)

# 🔹 Inicializa el servicio de Google Drive
drive_service = build("drive", "v3", credentials=creds)

# 🔹 Inicializa Flask
app = Flask(__name__)
CORS(app)


# 🔹 Reemplaza esta parte con la lista de enlaces generados en Google Colab 🔹
PDF_URLS = {
   "LE_AD_2_GCLP_en.pdf": "https://drive.google.com/uc?id=1pEzRS8aIk4BpN6nat8Cb__pyCMrL28Am",
"LE_AD_2_GCLP_SID_1_en.pdf": "https://drive.google.com/uc?id=1Ge9W-WF3QFp1aGuHCORUjFLQpWA40a4m",
"LE_AD_2_GCLP_SID_2_en.pdf": "https://drive.google.com/uc?id=12fal0nG892HIJEL-E-dBIvtvhLYKyDUv",
"LE_AD_2_GCLP_STAR_1_en.pdf": "https://drive.google.com/uc?id=1XqpdvCsg_cErLHtdso2JjkzyDO29pUhu",
"LE_AD_2_GCLP_STAR_2_en.pdf": "https://drive.google.com/uc?id=1e3OTC6E03m1e-D-Q3Xx4SjhKDSQm4LwR",
"LE_AD_2_GCLP_VAC_1_en.pdf": "https://drive.google.com/uc?id=1f1Cc_gns262A_P0XK1JPMynMslBCIZU_",
"LE_AD_2_GCLP_VAC_2_en.pdf": "https://drive.google.com/uc?id=1F79rrQNFU-pkieQ-6SDwOkcXod3XDunO",
"PCATS_CNS_GCCC_6.0.pdf": "https://drive.google.com/uc?id=1ZIETC4LhJ85M_M4mt6Uku7EqSXMTAp_N",
"Doc_4444 Amdt 8 EASA PANS ATM Checklist v.5 final Feb 2021 Oficial.pdf": "https://drive.google.com/uc?id=174GptiLug1wsBUkd6XRuK3FM6v8ZDe7K",
"532F14_2024-12-02_11.40.37_EAR-for-Standardised-European-Rules-of-the-Air-SERA.pdf": "https://drive.google.com/uc?id=1O87WiV9Ph3ktmiTpjfBqFulfde2ujjMO",
"GCCC-GCRR-v.6.4.pdf": "https://drive.google.com/uc?id=1pkjeMeb8Otd8hCPvPMDwLSPBF7Y8h5Np",
"20240208_CIN_LOA GCCC-GCRR_Modificación anexos D y F_v1.0.pdf": "https://drive.google.com/uc?id=1LtsvYEEDvzjRZl691uLKl6q0b4bXml0s",
"GCCC-GCFV_v7.0.pdf": "https://drive.google.com/uc?id=1Eqpg1cECsxbX4txG0JmfVemnnJS1KMC_",
"241216_CIN_LoA GCCC-GCFV_v1.1.pdf": "https://drive.google.com/uc?id=1LkzZ5FfNgfzbO458r8QBb-vTzFA5lYOO",
"20240207_CIN_LoA GCCC-GCFV.pdf": "https://drive.google.com/uc?id=1H0WEs8DcSpHS_DqOVYoJcmJ8Td2CoO4G",
"GCCC-GCLA_v.6.2.pdf": "https://drive.google.com/uc?id=13HWRjZR3QIPdkHkHO1u6ijt1aLUMnB7a",
"GCTS-GCXO v.5.0.pdf": "https://drive.google.com/uc?id=1edOeD8GkbPo3oTRv5KQCZfgYW9gdS-KV",
"GCTS-GCGM-v7. 1.pdf": "https://drive.google.com/uc?id=1sctVp_cO4Rfm9HCM083EUs4a4HDLowxV",
"GCCC-GCHI AFIS - v3.3.pdf": "https://drive.google.com/uc?id=1GVL8SR5ccVPyeoq8wpMTev5OjQdQ4t36",
"GCCC-GCHI TWR- v3.3.pdf": "https://drive.google.com/uc?id=1vChNwdewfXPIHXvYeicFWIMW05hjfvmk",
"GCCC-GCLP- v8.0.pdf": "https://drive.google.com/uc?id=1gI9L-twsbPrVoOR-CT_sDAGeejxkIACg",
"GCCC-GCXO v.5.3.pdf": "https://drive.google.com/uc?id=1jOWLM_jBW1-MbwrhoGJrMaEyHZNeDSpe",
"GCCC-GCTS v.6.1.pdf": "https://drive.google.com/uc?id=1WxrxuYhiT5EXFsu1ZAWDdkB-Ley3y5OR",
"C OP ATS n3 entre GCCC_GCLP y Helipuerto Hospital Insular de las Palmas de Gran Canaria.pdf": "https://drive.google.com/uc?id=1BCdM-gaj3vYObk8nDLCo8LNmZA8jD3q0",
"C OP ATS n4 entre GCCC y Helipuerto del Cabildo de Gran Canaria en Artenara.pdf": "https://drive.google.com/uc?id=1MSMUBZxlQryWt-95kEyd5nQTex7zz30m",
"C OP ATS n6 entre GCCC-GCLA-CABILDO (BELLIDO-SAN MAURO).pdf": "https://drive.google.com/uc?id=1kKY71oojC8mlu3vdjabT0ni6kTPQKvFn",
"C OPER ATS Nº1 ADFR DIVATS GANDO JSVICA_.pdf": "https://drive.google.com/uc?id=1uHGb_xKnIibEoy5DgnH-jR1oT4fSLd5X",
"C OP ATS n7 entre GCCC_GCLP y la Base Aerea de Gando.pdf": "https://drive.google.com/uc?id=1v3oGKxJwSsmDxylNIDY55WW956GXN6qP",
"C OP ATS n3 entre AMLAN_GCCC y GCRR.pdf": "https://drive.google.com/uc?id=1WPnxjMeSb5lNlYkJGdWxdKEGvGAfDMQu",
"C OP ATS n3 entre GCCC_GCLP_PLOCAN.pdf": "https://drive.google.com/uc?id=1Fgr9FX22w934TF_9maEBlX4QpYXmXB8Q",
"C OP ATS n2 entre GCCC y Helipuerto Palmas Port.pdf": "https://drive.google.com/uc?id=1CvLjfwdfdQ_QJYxiU-Wdvvrzx6a5iwKA",
"C OP ATS N6_GCCC_GCLP_GCLB.pdf": "https://drive.google.com/uc?id=17f-aO9fkk4p0eydlFumo4Wtp4IUKJQ1Q",
"C OP ATS n2 entre GCCC y BHELMA VI.pdf": "https://drive.google.com/uc?id=1Q6wrogms4g6cpoU6z0Df6Fd6WE4zQZmC",
"20240826_CIN_LoA División ATS-ECAO_HERMES.pdf": "https://drive.google.com/uc?id=17co30xiIc9lTDMczzkvVxkk-DTJ7jJha",
"LoA DIVATS Región Canaria y ECAO Las Palmas_v 5.1.pdf": "https://drive.google.com/uc?id=1QZuJz6s1_E0jK2AE93bphOTwVl-kyrVs",
"20240312_CIN_LoA División ATS-ECAO_MARSA, NR.05 y otros.pdf": "https://drive.google.com/uc?id=1GAz_1O7v5OACRPwWHu8evs_Gp3p6mHz8",
"GCCC_MO_S41-06-MAN-047-17.0_anexo B Núcleo RUTA Procedimientos específicos.pdf": "https://drive.google.com/uc?id=15te0uTKPcvszMXuIwqAKCyY1KwS5gYet",
"GCCC_MO_S41-06-MAN-047-17.0_anexo Z Planes de Respuesta ante Emergencia (ERP).pdf": "https://drive.google.com/uc?id=1jPyitXCSzHAR6JB70mDf1VzP_4iBJpU1",
"GCCC_MO_S41-06-MAN-047-17.0_anexo B Núcleo TMA Procedimientos específicos.pdf": "https://drive.google.com/uc?id=1YvQQQoLz4xBhWz2FeMytAmX_zBDIcSLw",
"GCCC_MO_S41-06-MAN-047-17.0_anexo A Procedimientos generales.pdf": "https://drive.google.com/uc?id=1WnNgPSQjBdlfv8pp0Q2XRMy2DoB6vuXk",
"CIT Integración de la vigilancia ADS-B en el sistema de vigilancia ATS de SACTA 4.0.pdf": "https://drive.google.com/uc?id=1uib4RcP-jTzDaBWPQMYnKpyFsVneMI3c",
"libro_completo_feb2019_v1_-_web.pdf": "https://drive.google.com/uc?id=1x9ymoqZBZaQMn0f5TTO87v4ovTlKloD2",

}

def descargar_pdf_drive(pdf_url):
    """Descarga un PDF desde Google Drive usando gdown."""
    pdf_bytes = io.BytesIO()
    gdown.download(pdf_url, pdf_bytes, quiet=False)
    pdf_bytes.seek(0)
    return pdf_bytes

@app.route("/procesar_pdf", methods=["POST"])
def procesar_pdf():
    try:
        print("📢 Nueva solicitud recibida")

        if not request.is_json:
            print("❌ Error: La solicitud no es JSON")
            return jsonify({"error": "La solicitud debe ser JSON"}), 400
        
        data = request.json
        print(f"📄 JSON recibido: {data}")

        query = data.get("query")

        if not query:
            print("❌ Error: Falta la palabra clave 'query'")
            return jsonify({"error": "Debe proporcionar una palabra clave para buscar."}), 400

        print(f"🔍 Buscando: {query}")

        resultados = {}

        for nombre_pdf, pdf_url in PDF_URLS.items():
            print(f"📥 Descargando {nombre_pdf} desde {pdf_url}")
            pdf_file = descargar_pdf_drive(pdf_url)

            if not pdf_file:
                print(f"⚠ No se pudo descargar {nombre_pdf}")
                continue

            print(f"📂 Intentando abrir {nombre_pdf} con pdfplumber")
            try:
                with pdfplumber.open(pdf_file) as pdf:
                    print(f"✅ PDF abierto correctamente: {nombre_pdf}")

                    coincidencias = []
                    for page_num, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text and query.lower() in text.lower():
                            print(f"✅ Coincidencia en {nombre_pdf}, página {page_num + 1}")
                            coincidencias.append(f"Página {page_num + 1}: {text[:500]}...")

                if coincidencias:
                    resultados[nombre_pdf] = coincidencias
            except Exception as pdf_error:
                print(f"💥 ERROR en pdfplumber: {pdf_error}")
                return jsonify({"error": f"Fallo al leer el PDF: {str(pdf_error)}"}), 500

        if not resultados:
            print("❌ No se encontraron coincidencias en ningún PDF")
            return jsonify({"resultados": "No se encontraron coincidencias en ningún PDF."})

        print("✅ Envío de resultados exitoso")
        return jsonify({"resumen": f"Se encontraron coincidencias en {len(resultados)} documentos.", "detalles": resultados})

    except Exception as e:
        print(f"💥 ERROR GENERAL en el servidor: {e}")
        return jsonify({"error": f"Error interno del servidor: {str(e)}"}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
