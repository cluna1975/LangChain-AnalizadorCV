from io import BytesIO

from pypdf import PdfReader


def extraer_texto_pdf(archivo_pdf):
    try:
        pdf_bytes = archivo_pdf.read()
        pdf_reader = PdfReader(BytesIO(pdf_bytes))
        texto_completo = ""

        for numero_pagina, pagina in enumerate(pdf_reader.pages, 1):
            texto_pagina = pagina.extract_text() or ""
            if texto_pagina.strip():
                texto_completo += f"\n--- PÁGINA {numero_pagina} ---\n"
                texto_completo += texto_pagina.strip() + "\n"

        texto_completo = texto_completo.strip()

        if not texto_completo:
            return "Error: El PDF parece estar vacío o contener solo imágenes."

        return texto_completo[:12000]

    except Exception as e:
        return f"Error al procesar el archivo PDF: {str(e)}"