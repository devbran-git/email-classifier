import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"\S+@\S+", "", text)
    text = re.sub(r"Atenciosamente,.*", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def remove_stopwords(text: str) -> str:
    stopwords = [
        "o",
        "a",
        "de",
        "da",
        "do",
        "em",
        "um",
        "para",
        "com",
        "por",
        "que",
        "é",
    ]
    words = text.lower().split()
    return " ".join([w for w in words if w not in stopwords])


def preprocess(text: str) -> str:
    text = clean_text(text)
    text = remove_stopwords(text)
    return text
