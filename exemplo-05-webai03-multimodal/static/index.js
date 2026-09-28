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

    // Usa valores fixos (LanguageModel.params não existe nesta versão)
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