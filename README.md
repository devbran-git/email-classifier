# Email Classifier — Classificação Inteligente de E-mails + Sugestão de Resposta

API desenvolvida para o desafio técnico, capaz de:

1. **Extrair texto de arquivos PDF ou TXT**
2. **Classificar automaticamente o conteúdo do e-mail** usando técnicas NLP
3. **Gerar uma resposta profissional sugerida**, baseada na classificação, usando modelo LLM
4. **Expor endpoints REST claros e bem estruturados**
5. **Fornecer uma interface simples e responsiva para testes rápidos**

Deploy: **[https://emailclassifier-xisz.onrender.com/](https://emailclassifier-xisz.onrender.com/)**

---

## 1. Objetivo do Projeto (Conforme o Desafio Técnico)

O desafio exige:

- processamento de arquivos PDF/TXT ou texto inserido na text area
- extração de texto confiável
- classificação semântica do conteúdo
- geração automática de resposta adequada
- API organizada e escalável
- arquitetura limpa, modular e documentada
- deploy funcional em ambiente real
- página inicial simples para teste manual

Este projeto atende **todos os requisitos**, mantendo foco em clareza, rastreabilidade e boas práticas.

---

## 2. Arquitetura do Projeto

```
├── README.md
├── requirements.txt
└── src
    ├── __init__.py
    ├── __pycache__/
    ├── api/
    │   ├── routers/
    │   │   ├── __init__.py
    │   │   └── analyze.py              # Endpoint principal (/analyze)
    │   └── services/
    │       ├── __init__.py
    │       ├── classifier.py           # Classifica e-mails (produtivo / improdutivo)
    │       ├── extractor.py            # Extrai texto (entrada bruta → texto limpio)
    │       ├── nlp_processor.py        # Pré-processamento de texto
    │       └── responder.py            # Gera resposta sugerida
    ├── config.py                        # Configurações e env vars
    ├── main.py                          # App FastAPI
    ├── static/
    │   ├── script.js                    # Lógica do front-end
    │   └── style.css                    # Estilos da interface
    └── templates/
        └── index.html                   # UI para testes
```

---

## 3. Fluxo Interno

### 1) Entrada

- Texto bruto via `/analyze/text`
- Arquivo PDF/TXT via `/analyze/file`

### 2) Extração

- PDF → pdfplumber
- TXT → decode UTF-8 seguro

### 3) Limpeza

- remoção de HTML
- remoção de URLs/emails
- remoção de assinaturas automáticas
- redução de ruído e stopwords básicas

### 4) Classificação

Chamada ao modelo Groq:

- rápido
- barato
- excelente para high-throughput

### 5) Geração da resposta

Modelo recebe:

- classificação
- texto do e-mail
- instruções de otimização

### 6) Retorno consolidado

```json
{
  "classification": "...",
  "extracted_text": "...",
  "suggested_reply": "..."
}
```

---

## 4. Como Rodar Localmente

### 1. Clonar

```bash
git clone https://github.com/devbran-git/email-classifier.git
cd email-classifier
```

### 2. Criar ambiente

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Criar `.env` conforme .env.example

```
GROQ_API_KEY=xxxxx
GROQ_MODEL=modelo_groq_cloud
GROQ_CHAT_URL=url_chat_groq_cloud
```

### 5. Iniciar aplicação

```bash
uvicorn src.main:app --reload
```

Acesse:
`http://localhost:8000`
Docs: `http://localhost:8000/docs`

---

## 5. Endpoints da API

### POST /analyze/text

**Entrada:**

```json
{
  "text": "Olá, gostaria de saber sobre o prazo de entrega..."
}
```

**Retorno:**

```json
{
  "classification": "produtivo",
  "extracted_text": "Olá, gostaria...",
  "suggested_reply": "Olá! Agradeço seu contato..."
}
```

---

### POST /analyze/file

Envia e recebe nos mesmos formatos, após a extração do texto.

---

## 6. Exemplos de Teste Produtivo

### Email:

> “Boa tarde!
> Poderiam me confirmar se a nota fiscal da última compra já foi emitida?”

**Classificação esperada:**
`produtivo`

**Resposta gerada (exemplo):**

> “Boa tarde!
> Agradeço seu contato.
> A nota fiscal da sua última compra já foi emitida e o documento segue anexado a este e-mail. Caso precise de qualquer outra informação, estou à disposição!”

---

## 7. Decisões Técnicas Explicadas

- **FastAPI** pela velocidade e documentação automática.
- **httpx** por ser async-native.
- **pdfplumber** para extração estável de PDFs.
- **Groq** pela latência extremamente baixa e preço acessível e melhor processamento de instruções complexas.
- **Arquitetura modular** para facilitar manutenção e entendimento do código.
- **Prompt isolado em constantes** (boas práticas).
- **Variáveis sensíveis somente no `.env`** (segurança).
- **Deploy no Render** reproduz ambiente real.

---

## 8. Segurança e Boas Práticas Aplicadas

- `.env` ignorado via `.gitignore`
- Nenhuma key exposta no código
- Tratamento completo de erros HTTP
- Timeout configurado
- Sanitização de entrada
- Extração de PDF protegida por `try/except`

---

## 9. Conclusão

Este projeto entrega:

✓ código limpo
✓ modular
✓ estruturado
✓ pronto para produção
✓ deploy funcional
✓ documentação clara
✓ aderência total ao desafio técnico
