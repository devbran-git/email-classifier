import httpx
from fastapi import HTTPException
from src.api.services.nlp_processor import preprocess
from src.config import GROQ_API_KEY, GROQ_MODEL

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY não configurada.")

PROMPT_TEMPLATE = """
Analise o email abaixo e classifique como 'produtivo' ou 'improdutivo'.

REGRAS OBRIGATÓRIAS:
- Classifique como 'produtivo': emails que requerem ação ou resposta específica (suporte, dúvidas, solicitações, atualização de casos).
- Classifique como 'improdutivo': mensagens de cortesia, agradecimentos, felicitações, publicidade ou sem ação requerida.

EMAIL:
{email}

Responda APENAS com uma palavra: "produtivo" ou "improdutivo".
"""


async def classify_text(text: str) -> str:
    preprocessed_text = preprocess(text)
    prompt = PROMPT_TEMPLATE.format(email=preprocessed_text.strip())

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Você é um classificador binário. Responda somente com 'produtivo' ou 'improdutivo'.",
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 10,
        "temperature": 0.1,
    }

    try:
        async with httpx.AsyncClient(timeout=40) as client:
            response = await client.post(url, json=payload, headers=headers)

        if response.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="Limite de requisições atingido. Tente novamente.",
            )

        response.raise_for_status()

        try:
            result = response.json()
        except ValueError:
            raise HTTPException(500, "Resposta do modelo não é JSON válido.")

        choices = result.get("choices")
        if not choices:
            raise HTTPException(500, "Resposta inesperada do modelo.")

        content = choices[0]["message"]["content"].strip().lower()

        if content == "produtivo":
            return "produtivo"
        elif content == "improdutivo":
            return "improdutivo"
        else:
            print(f"Resposta ambígua: {content}")
            return "improdutivo"

    except httpx.HTTPStatusError as e:
        code = e.response.status_code
        if code == 401:
            raise HTTPException(401, "API key inválida ou não autorizada.")
        elif code == 429:
            raise HTTPException(429, "Limite de requisições atingido.")
        else:
            raise HTTPException(code, f"Erro no modelo: {e.response.text}")

    except httpx.TimeoutException:
        raise HTTPException(504, "Timeout ao aguardar resposta do modelo.")

    except Exception as e:
        raise HTTPException(500, f"Falha ao classificar texto: {str(e)}")
