from flask import Flask, request, jsonify
import requests
import io
import pdfplumber

app = Flask(__name__)

@app.route("/procesar_pdf", methods=["POST"])
def procesar_pdf():
    data = request.json
    aerodromo = data.get("aerodromo")
    categoria = data.get("categoria")
    pista = data.get("pista", "")
    query = data.get("query")

    pdf_url = "https://aip.enaire.es/AIP/contenido_AIP/AD/AD2/GCLP/LE_AD_2_GCLP_STAR_1_en.pdf"

    try:
        pdf_response = requests.get(pdf_url)
        pdf_file = io.BytesIO(pdf_response.content)

        resultados = []
        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text and query.lower() in text.lower():
                    resultados.append(f"Página {page_num + 1}: {text[:500]}...")

        if not resultados:
            return jsonify({"resultados": "No se encontraron coincidencias en el PDF."})

        return jsonify({"resumen": f"Se encontraron {len(resultados)} coincidencias.", "detalles": resultados})

    except Exception as e:
        return jsonify({"error": f"Error al procesar el PDF: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
