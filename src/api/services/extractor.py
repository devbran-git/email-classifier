import io
import pdfplumber
from fastapi import HTTPException


def extract_pdf(file_bytes: bytes) -> str:
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]

        full_text = "\n".join(pages).strip()

        if not full_text:
            raise ValueError("Nenhum texto extraído das páginas do PDF.")

        return full_text

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Falha ao extrair texto do PDF: {str(e)}"
        )


def extract_txt(file_bytes: bytes) -> str:
    try:
        text = file_bytes.decode("utf-8", errors="ignore").strip()

        if not text:
            raise ValueError("Arquivo TXT vazio ou ilegível.")

        return text

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Falha ao processar arquivo TXT: {str(e)}"
        )
