const form = document.getElementById("question-form");
const output = document.getElementById("output");
const askButton = document.getElementById("ask-button");
const tempSlider = document.getElementById("temperature");
const tempValue = document.getElementById("temp-value");
const topkValue = document.getElementById("topk-value");
const topkInput = document.getElementById("topK");
const yearSpan = document.getElementById("year");

// Exibe o ano atual no footer
yearSpan.textContent = new Date().getFullYear();

// Atualiza o display do slider de temperature
tempValue.textContent = tempSlider.value;
tempSlider.addEventListener("input", () => {
  tempValue.textContent = tempSlider.value;
});

// Atualiza o display do Top K
topkValue.textContent = topkInput.value;
topkInput.addEventListener("input", () => {
  topkValue.textContent = topkInput.value;
});

// Intercepta o submit do formulário
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const question = document.getElementById("question").value.trim();
  if (!question) return;

  askButton.disabled = true;
  askButton.textContent = "Aguarde...";
  output.innerHTML = "<p><em>Pensando...</em></p>";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        question: question,
        temperature: parseFloat(tempSlider.value),
        topK: parseInt(topkInput.value) || null,
      }),
    });

    const data = await res.json();

    if (data.answer) {
      output.innerHTML = `<div class="answer">${data.answer}</div>`;
    } else if (data.error) {
      output.innerHTML = `<div class="error">Erro: ${data.error}</div>`;
    }
  } catch (err) {
    output.innerHTML = `<div class="error">Erro de conexão: ${err.message}</div>`;
  } finally {
    askButton.disabled = false;
    askButton.textContent = "Enviar";
  }
});