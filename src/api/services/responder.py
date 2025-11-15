import httpx
from fastapi import HTTPException
from src.config import GROQ_API_KEY, GROQ_CHAT_URL, GROQ_MODEL

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY não configurada.")
if not GROQ_MODEL:
    raise RuntimeError("GROQ_MODEL não configurado.")
if not GROQ_CHAT_URL:
    raise RuntimeError("GROQ_CHAT_URL não configurada.")

REPLY_PROMPT = """
Você é um assistente profissional de atendimento por e-mail.
Escreva respostas educadas, claras e objetivas.
Adapte o tom, a urgência e a formalidade de acordo com a classificação do e-mail.
Nunca explique o processo. Nunca mencione a classificação.
Responda como um atendente humano experiente e prestativo.
""".strip()


async def generate_reply(text: str, classification: str) -> str:
    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": REPLY_PROMPT},
            {
                "role": "user",
                "content": f"""
Classificação: {classification}

Com base nessa classificação, escreva uma resposta adequada para o e-mail abaixo:

---
{text.strip()}
---

Responda diretamente, sem explicar o processo.
                """.strip(),
            },
        ],
        "max_tokens": 300,
        "temperature": 0.7,
        "top_p": 0.9,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(GROQ_CHAT_URL, json=payload, headers=headers)

        if response.status_code == 429:
            raise HTTPException(
                status_code=429,
                detail="Limite de requisições atingido. Tente novamente em alguns segundos.",
            )

        response.raise_for_status()

        try:
            result = response.json()
        except ValueError:
            raise HTTPException(
                status_code=500, detail="Resposta do modelo não é um JSON válido."
            )

        if isinstance(result, dict) and "choices" in result:
            message = result["choices"][0].get("message", {})
            content = message.get("content", "").strip()
            if content:
                return content

        if "error" in result:
            raise HTTPException(
                status_code=500,
                detail=f"Erro do modelo: {result['error'].get('message')}",
            )

        print("Formato inesperado:", result)
        raise HTTPException(
            status_code=500, detail="Formato inesperado de resposta do modelo."
        )

    except httpx.HTTPStatusError as e:
        if e.response.status_code == 401:
            raise HTTPException(401, "API key inválida ou não autorizada.")
        elif e.response.status_code == 429:
            raise HTTPException(429, "Limite de requisições atingido.")
        else:
            raise HTTPException(
                e.response.status_code,
                f"Erro no modelo gerador: {e.response.text}",
            )

    except httpx.TimeoutException:
        raise HTTPException(504, "Timeout ao aguardar resposta do modelo.")

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Falha ao gerar resposta: {str(e)}"
        )
