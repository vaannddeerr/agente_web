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