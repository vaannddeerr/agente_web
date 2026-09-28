Documentação — Projetos Web AI
Autor: Vanderlei Sousa de Carvalho  
Disciplina: Fundamentos de IA e LLMs para Programadores — Módulo 05  
Instituição: Anhanguera / UNIPDS  
Data: 28/09/2026
---
Sumário
Visão Geral
Projeto 1: J.A.R.V.I.S — Assistente Virtual (Flask + OpenRouter)
Projeto 2: Web AI Demo — Chrome Gemini Nano (Client-Side)
Flags do Chrome Necessárias
Problemas Encontrados e Soluções
Comparativo dos Projetos
Referências
---
1. Visão Geral
Dois projetos de assistente virtual com IA foram desenvolvidos durante o Módulo 05:
Aspecto	J.A.R.V.I.S	Web AI Demo
Tipo de IA	Cloud (OpenRouter API)	Local (Gemini Nano no browser)
Backend	Flask (Python) com rota `/chat`	Flask apenas serve arquivos estáticos
Multimodal	Não	Sim (imagem e áudio)
Tradução	Não	Opcional (requer Chrome Canary)
Streaming	Não	Sim (`promptStreaming`)
API Key	Sim (OpenRouter)	Não
Arquitetura JS	Flat (`app.js`)	MVC (controller, service, view)
---
2. Projeto 1: J.A.R.V.I.S — Assistente Virtual (Flask + OpenRouter)
2.1 Estrutura de Pastas
```
assistente_virtual/
├── static/
│   ├── app.js            ← JavaScript principal
│   └── style.css         ← Estilos CSS
├── templates/
│   └── index.html        ← Interface HTML (Jinja2)
├── .env                  ← Chaves de API (não versionar)
├── app.py                ← Backend Flask
├── requirements.txt      ← Dependências Python
└── venv/                 ← Ambiente virtual
```
2.2 Arquivo `.env`
```env
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=google/gemini-2.0-flash-001
```
2.3 Backend — `app.py`
```python
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url=os.getenv("OPENROUTER_BASE_URL")
)
model = os.getenv("OPENROUTER_MODEL")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        question = data.get("question", "")
        temperature = data.get("temperature", 1.0)
        top_k = data.get("topK", None)

        extra_params = {}
        if top_k is not None:
            extra_params["top_k"] = top_k

        response = client.chat.completions.create(
            model=model,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente de IA que responde de forma clara e objetiva.",
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
            **extra_params,
        )

        return jsonify({"answer": response.choices[0].message.content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
```
2.4 Frontend — `static/app.js`
```javascript
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
```
2.5 HTML — `templates/index.html` (pontos-chave)
```html
<!-- Slider Temperature com min/max/value corretos -->
<input type="range" id="temperature" name="temperature" min="0" max="2" step="0.1" value="1.0">

<!-- Top K com valor padrão -->
<input type="number" id="topK" name="topK" min="1" max="100" value="40">

<!-- Script carregado da pasta static -->
<script src="{{ url_for('static', filename='app.js') }}"></script>
```
2.6 Dependências — `requirements.txt`
```
flask
openai
python-dotenv
```
2.7 Como Executar
```bash
cd assistente_virtual
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python app.py
# Acesse: http://127.0.0.1:5000
```
---
3. Projeto 2: Web AI Demo — Chrome Gemini Nano (Client-Side)
3.1 Estrutura de Pastas
```
exemplo-05-webai03-multimodal/
├── static/
│   ├── app.js                        ← Não utilizado (legado)
│   ├── style.css                     ← Estilos CSS
│   ├── index.js                      ← Entry point (módulo ES6)
│   ├── controllers/
│   │   └── formController.js         ← Lógica do formulário
│   ├── services/
│   │   ├── aiService.js              ← Comunicação com Gemini Nano
│   │   └── translationService.js     ← Tradução (requer Chrome Canary)
│   └── views/
│       └── view.js                   ← Manipulação do DOM
├── templates/
│   └── index.html                    ← Interface HTML
├── .env
├── app.py                            ← Flask (só serve arquivos)
├── package.json
└── venv/
```
IMPORTANTE: Todos os arquivos JS (index.js, controllers/, services/, views/) devem estar dentro de `static/` para o Flask servir corretamente.
3.2 Entry Point — `static/index.js`
```javascript
import { AIService } from './services/aiService.js';
import { View } from './views/view.js';
import { FormController } from './controllers/formController.js';

(async function main() {
    const aiService = new AIService();
    const view = new View();

    view.setYear();

    if (!('LanguageModel' in self)) {
        view.showError([
            "⚠️ As APIs nativas de IA não estão ativas.",
            "Ative: chrome://flags/#prompt-api",
            "Depois reinicie o Chrome."
        ]);
        return;
    }

    // Usa valores fixos (LanguageModel.params não existe em todas as versões)
    view.initializeParameters({
        defaultTemperature: 1.0,
        maxTemperature: 2.0,
        defaultTopK: 3,
        maxTopK: 10
    });

    const controller = new FormController(aiService, null, view);
    controller.setupEventListeners();

    console.log('Application initialized successfully');
})();
```
3.3 AI Service — `static/services/aiService.js`
```javascript
export class AIService {
    constructor() {
        this.session = null;
        this.abortController = null;
    }

    async getParams() {
        return {
            defaultTemperature: 1.0,
            maxTemperature: 2.0,
            defaultTopK: 3,
            maxTopK: 10
        };
    }

    async* createSession(question, temperature, topK, file = null) {
        this.abortController?.abort();
        this.abortController = new AbortController();

        if (this.session) {
            this.session.destroy();
        }

        // Define inputs dinamicamente — só pede multimodal quando tem arquivo
        const expectedInputs = [{ type: "text" }];
        if (file) {
            const fileType = file.type.split('/')[0];
            if (fileType === 'image' || fileType === 'audio') {
                expectedInputs.push({ type: fileType });
            }
        }

        this.session = await LanguageModel.create({
            expectedInputs: expectedInputs,
            expectedOutputLanguages: ["en"],
            temperature: temperature,
            topK: topK,
            initialPrompts: [
                {
                    role: 'system',
                    content: [{
                        type: "text",
                        value: "You are an AI assistant that responds clearly and objectively. Always respond in plain text format instead of markdown."
                    }]
                },
            ],
        });

        const contentArray = [{ type: "text", value: question }];

        if (file) {
            const fileType = file.type.split('/')[0];
            if (fileType === 'image' || fileType === 'audio') {
                const blob = new Blob([await file.arrayBuffer()], { type: file.type });
                contentArray.push({ type: fileType, value: blob });
            }
        }

        const responseStream = await this.session.promptStreaming(
            [{ role: 'user', content: contentArray }],
            { signal: this.abortController.signal }
        );

        for await (const chunk of responseStream) {
            if (this.abortController.signal.aborted) {
                break;
            }
            yield chunk;
        }
    }

    abort() {
        this.abortController?.abort();
    }

    isAborted() {
        return this.abortController?.signal.aborted;
    }
}
```
3.4 Form Controller — `static/controllers/formController.js`
Ajuste principal na linha do translate (adicionado `&& this.translationService`):
```javascript
// Linha 81 — só traduz se translationService existir
if (fullResponse && !this.aiService.isAborted() && this.translationService) {
    this.view.setOutput('Traduzindo resposta...');
    const translatedResponse = await this.translationService.translateToPortuguese(fullResponse);
    this.view.setOutput(translatedResponse);
}
```
3.5 HTML — Script como Módulo ES6
```html
<!-- OBRIGATÓRIO: type="module" para imports funcionarem -->
<script type="module" src="{{ url_for('static', filename='index.js') }}"></script>
```
3.6 Como Executar
```bash
cd exemplo-05-webai03-multimodal
python app.py
# Acesse: http://127.0.0.1:5000
# Requer Google Chrome com flags ativadas (ver seção 4)
```
---
4. Flags do Chrome Necessárias
Para o projeto Web AI Demo funcionar, ativar as seguintes flags em `chrome://flags/`:
4.1 Flags Obrigatórias (Chrome Estável)
Flag	Endereço	Função	Status Recomendado
Prompt API	`chrome://flags/#prompt-api`	Habilita IA local (Gemini Nano)	Enabled
Prompt API Multimodal Input	`chrome://flags/#prompt-api-multimodal-input`	Suporte a imagem e áudio	Enabled
Prompt API Sampling Mode	`chrome://flags/#prompt-api-sampling-mode`	Temperature e Top K funcionarem	Enabled
4.2 Flags Opcionais (Requerem Chrome Canary)
Estas flags NÃO existem no Chrome estável (v153). Precisam do Chrome Canary:
Flag	Endereço	Função
Translation API	`chrome://flags/#translation-api`	Tradução automática EN→PT
Language Detection API	`chrome://flags/#language-detection-api`	Detectar idioma da resposta
4.3 Após Ativar as Flags
Clicar no botão "Reiniciar" que aparece na barra inferior do Chrome
Na primeira execução, o Chrome vai baixar o modelo Gemini Nano (~1.7GB)
Acompanhar o progresso no Console do browser (`F12` → aba Console)
O download é feito apenas uma vez
---
5. Problemas Encontrados e Soluções
5.1 Erro 404 no `app.js`
Sintoma: `"GET /static/app.js HTTP/1.1" 404`  
Causa: O arquivo `app.js` estava na raiz do projeto, fora da pasta `static/`.  
Solução: Mover o `app.js` para dentro de `static/`.
5.2 "Unexpected token '<'"
Sintoma: `Erro de conexão: Unexpected token '<'`  
Causa: O endpoint `/chat` do Flask retornava HTML (página de erro 500) em vez de JSON. O `res.json()` do JavaScript não consegue parsear HTML.  
Solução: Adicionar `try/except` no endpoint `/chat` do `app.py` para sempre retornar JSON:
```python
except Exception as e:
    return jsonify({"error": str(e)}), 500
```
5.3 Temperature e Top K não apareciam
Sintoma: Labels mostravam "Temperature:" e "Top K:" sem valores.  
Causa (J.A.R.V.I.S): O `<input type="range">` não tinha `min`, `max`, `value` definidos. O padrão do browser é 0-100.  
Causa (Web AI Demo): Os módulos JS estavam fora da pasta `static/`, então o `index.js` não era carregado.  
Solução J.A.R.V.I.S: Adicionar atributos no HTML:
```html
<input type="range" min="0" max="2" step="0.1" value="1.0">
<input type="number" min="1" max="100" value="40">
```
Solução Web AI Demo: Mover `index.js`, `controllers/`, `services/`, `views/` para dentro de `static/`.
5.4 "Model capability is not available"
Sintoma: Erro ao enviar pergunta com imagem.  
Causa: O `aiService.js` pedia capacidades multimodal (image + audio) sempre, mesmo quando a flag multimodal não estava ativa.  
Solução: Tornar `expectedInputs` dinâmico — só pedir multimodal quando tem arquivo anexado:
```javascript
const expectedInputs = [{ type: "text" }];
if (file) {
    expectedInputs.push({ type: file.type.split('/')[0] });
}
```
5.5 "LanguageModel.params is not a function"
Sintoma: Erro no console durante inicialização.  
Causa: O método `LanguageModel.params()` não existe nesta versão do Chrome (v153).  
Solução: Usar valores fixos de fallback em vez de chamar `getParams()`:
```javascript
view.initializeParameters({
    defaultTemperature: 1.0,
    maxTemperature: 2.0,
    defaultTopK: 3,
    maxTopK: 10
});
```
5.6 "NotAllowedError: Requires a user gesture"
Sintoma: Erro ao tentar baixar modelo automaticamente na carga da página.  
Causa: O Chrome exige interação do usuário (clique) para iniciar o download do modelo Gemini Nano.  
Solução: Não tentar baixar o modelo no `index.js`. O download acontece automaticamente quando o usuário clica "Enviar" pela primeira vez.
5.7 SyntaxError no `aiService.js`
Sintoma: `Uncaught SyntaxError: Unexpected token '{'`  
Causa: Código colado incorretamente no arquivo (caracteres invisíveis, BOM, etc.).  
Solução: Selecionar tudo (`Ctrl+A`), deletar, e colar o código limpo novamente.
5.8 Translation API e Language Detection API não encontradas
Sintoma: "No matching experiments" ao buscar no `chrome://flags/`.  
Causa: Essas APIs só estão disponíveis no Chrome Canary, não no Chrome estável.  
Solução: Instalar o Chrome Canary ou rodar sem tradução (resposta em inglês).
---
6. Comparativo dos Projetos
Característica	J.A.R.V.I.S (Flask + OpenRouter)	Web AI Demo (Gemini Nano)
Onde a IA roda	Servidor remoto (cloud)	Localmente no browser
Latência	Depende da internet	Instantâneo
Custo	API key paga (por token)	Gratuito
Privacidade	Dados vão para o servidor	Dados ficam no dispositivo
Browser	Qualquer browser	Somente Google Chrome
Modelos	Qualquer modelo do OpenRouter	Apenas Gemini Nano
Qualidade	Alta (GPT-4, Claude, Gemini Pro)	Limitada (modelo nano)
Multimodal	Não (só texto)	Sim (imagem e áudio)
Streaming	Não	Sim
Offline	Não	Sim (após download do modelo)
Arquitetura	MVC simples (app.py + app.js)	MVC completo (ES6 modules)
---
7. Referências
Chrome Built-in AI: https://developer.chrome.com/docs/ai/built-in
LanguageModel API: https://developer.chrome.com/docs/ai/language-model-api
OpenRouter API: https://openrouter.ai/docs
Flask Documentation: https://flask.palletsprojects.com/
Chrome Flags: `chrome://flags/`
Chrome Canary: https://www.google.com/chrome/canary/
---
Documento gerado em 28/09/2026 — Vanderlei Sousa de Carvalho — Engenharia de Dados
