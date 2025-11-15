from fastapi import APIRouter, UploadFile, File, HTTPException
from ..services.extractor import extract_pdf, extract_txt
from ..services.classifier import classify_text
from ..services.responder import generate_reply

router = APIRouter(prefix="/analyze")


@router.post("/file")
async def analyze_file(file: UploadFile = File(...)):
    filename = str(file.filename).lower()
    if filename.endswith(".pdf"):
        text = extract_pdf(await file.read())
    elif filename.endswith(".txt"):
        text = extract_txt(await file.read())
    else:
        raise HTTPException(status_code=400, detail="Envie um arquivo PDF ou TXT.")

    classification = await classify_text(text)
    suggested = await generate_reply(text, classification)

    return {
        "classification": classification,
        "extracted_text": text,
        "suggested_reply": suggested,
    }


@router.post("/text")
async def analyze_text(payload: dict):
    text = payload.get("text", "").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Texto vazio.")

    classification = await classify_text(text)
    suggested = await generate_reply(text, classification)

    return {
        "classification": classification,
        "extracted_text": text,
        "suggested_reply": suggested,
    }
