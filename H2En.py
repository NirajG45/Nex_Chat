from flask import Flask, render_template, request, jsonify
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message", "")
    if not user_input.strip():
        return jsonify({"response": ""})
    
    # Google Translate (Hinglish/ Hindi → English)
    translation = translator.translate(user_input, src='hi', dest='en')
    return jsonify({"response": translation.text})

if __name__ == "__main__":
    app.run(debug=True)
