const form = document.getElementById("emailForm");
const emailText = document.getElementById("emailText");
const emailFile = document.getElementById("emailFile");
const fileName = document.getElementById("fileName");
const submitBtn = document.getElementById("submitBtn");

const loadingIndicator = document.getElementById("loadingIndicator");
const resultsCard = document.getElementById("resultsCard");
const categoryBadge = document.getElementById("categoryBadge");
const confidence = document.getElementById("confidence");
const responseText = document.getElementById("responseText");
const originalTextSection = document.getElementById("originalTextSection");
const originalText = document.getElementById("originalText");

const errorMessage = document.getElementById("errorMessage");
const errorText = document.getElementById("errorText");

const dropZone = document.getElementById("dropZone");

emailFile.addEventListener("change", (e) => {
  if (e.target.files.length > 0) {
    fileName.textContent = `Arquivo selecionado: ${e.target.files[0].name}`;
    fileName.classList.remove("hidden");
    emailText.value = "";
  } else {
    fileName.classList.add("hidden");
  }
});

emailText.addEventListener("input", () => {
  if (emailText.value.trim()) {
    emailFile.value = "";
    fileName.classList.add("hidden");
  }
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  clearError();
  resultsCard.classList.add("hidden");

  const hasText = emailText.value.trim();
  const hasFile = emailFile.files.length > 0;

  if (!hasText && !hasFile) {
    showError("Por favor, forneça texto ou selecione um arquivo.");
    return;
  }

  loadingIndicator.classList.remove("hidden");
  submitBtn.disabled = true;

  try {
    let response;

    if (hasFile) {
      const formData = new FormData();
      formData.append("file", emailFile.files[0]);
      response = await fetch("/analyze/file", { method: "POST", body: formData });
    } else {
      const payload = { text: emailText.value.trim() };
      response = await fetch("/analyze/text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    }

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Erro ao processar e-mail.");
    }

    displayResults({
      category: data.classification,
      response: data.suggested_reply,
      original_text: data.extracted_text,
      confidence: null,
    });
  } catch (err) {
    showError(err.message || "Erro ao processar e-mail. Tente novamente.");
  } finally {
    loadingIndicator.classList.add("hidden");
    submitBtn.disabled = false;
  }
});

function displayResults(data) {
  const isProdutivo = data.category === "produtivo";
  categoryBadge.textContent = data.category.charAt(0).toUpperCase() + data.category.slice(1);
  categoryBadge.className = `inline-block px-4 py-2 rounded-full text-sm font-semibold ${
    isProdutivo ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"
  }`;

  confidence.textContent = data.confidence ? `(confiança: ${(data.confidence * 100).toFixed(1)}%)` : "";
  responseText.textContent = data.response || "Nenhuma resposta gerada.";

  if (data.original_text) {
    originalText.textContent = data.original_text.slice(0, 500);
    originalTextSection.classList.remove("hidden");
  } else {
    originalTextSection.classList.add("hidden");
  }

  resultsCard.classList.remove("hidden");
  resultsCard.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function showError(message) {
  errorText.textContent = message;
  errorMessage.classList.remove("hidden");
  errorMessage.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function clearError() {
  errorText.textContent = "";
  errorMessage.classList.add("hidden");
}

dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("ring-2", "ring-blue-400", "bg-blue-50/50");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("ring-2", "ring-blue-400", "bg-blue-50/50");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("ring-2", "ring-blue-400", "bg-blue-50/50");

  const file = e.dataTransfer.files[0];
  if (!file) return;

  const dt = new DataTransfer();
  dt.items.add(file);
  emailFile.files = dt.files;

  fileName.textContent = `Arquivo selecionado: ${file.name}`;
  fileName.classList.remove("hidden");

  emailText.value = "";
});
