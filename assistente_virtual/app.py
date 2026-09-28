from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")
base_url = os.getenv("OPENROUTER_BASE_URL")
model = os.getenv("OPENROUTER_MODEL")

app = Flask(__name__)

client = OpenAI(
    api_key=api_key,
    base_url=base_url
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    question = data.get("question", "")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Você é um assistente de IA que responde "
                    "de forma clara e objetiva."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    return jsonify(
        {
            "answer": response.choices[0].message.content
        }
    )


if __name__ == "__main__":
    app.run(debug=True)