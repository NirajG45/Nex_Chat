from flask import Flask, render_template, request, jsonify
import re
import difflib

app = Flask(__name__)

# Hinglish → English dictionary
LEXICON = {
    "main": "I",
    "mujhe": "I",
    "mujhko": "me",
    "tum": "you",
    "tu": "you",
    "aap": "you",
    "mera": "my",
    "meri": "my",
    "mere": "my",
    "hai": "is",
    "hain": "are",
    "chahiye": "need",
    "chahta": "want",
    "chahti": "want",
    "karo": "do",
    "karte": "do",
    "karta": "does",
    "kitab": "book",
    "pani": "water",
    "khana": "food",
    "ghar": "home",
    "kaise": "how",
    "ho": "are",
    "theek": "fine",
    "dhanyavaad": "thank you",
    "shukriya": "thank you",
    "kripya": "please",
    "ek": "one",
    "do": "two",
    "teen": "three",
    "char": "four",
    "paanch": "five",
    "chhe": "six",
    "saat": "seven",
    "aath": "eight",
    "nau": "nine",
    "das": "ten",
    "kya": "what",
    "kab": "when",
    "kahan": "where",
    "kyun": "why",
    "kaun": "who",
    "mera": "mine",
    "meri": "mine",
    "mere": "mine",
    "tumhara": "yours",
    "tumhari": "yours",
    "tumhare": "yours",
    "aapka": "yours",
    "aapki": "yours",
    "aapke": "yours",
    "achha": "good",
    "bura": "bad",
    "naya": "new",
    "purana": "old",
    "bada": "big",
    "chhota": "small",
    "lamba": "long",
    "chhota": "short",
    "tez": "fast",
    "dheere": "slow",
    "garam": "hot",
    "thanda": "cold",
    "sundar": "beautiful",
    "bhari": "heavy",
    "halka": "light",
    "sasta": "cheap",
    "mehnga": "expensive",
    "majboot": "strong",
    "kamzor": "weak",
    "safed": "white",
    "kala": "black",
    "laal": "red",
    "neela": "blue",
    "hara": "green",
    "peela": "yellow",
    "bhura": "brown",
    "gulabi": "pink",
    "narangi": "orange",
    "baingani": "purple",
    "dhundhla": "grey",
    "sone": "gold",
    "chandi": "silver",
    "naam": "name",
    "pyaar": "love",
    "dost": "friend",
    "parivaar": "family",
    "ghar": "house",
    "school": "school",
    "kaam": "work",
    "chutti": "holiday",
    "bazaar": "market",
    "duniya": "world",
    "samay": "time",
    "din": "day",
    "raat": "night",
    "hafta": "week",
    "mahina": "month",
    "saal": "year",
    "kal": "yesterday/tomorrow",
    "aaj": "today",
    "subah": "morning",
    "shaam": "evening",
    "dopehar": "afternoon",
    "raat": "night",
    "saptah": "week",
    "mahina": "month",
    "saal": "year",
    "kabhi": "sometimes",
    "hamesha": "always",
    "kabhi nahi": "never",
    "shubh": "auspicious",
    "mangal": "auspicious",
    "safar": "journey",
    "yatra": "journey",
    "khushi": "happiness",
    "dukh": "sadness",
    "gussa": "anger",
    "dar": "fear",
    "shanti": "peace",
    "sahas": "courage",
    "safalta": "success",
    "asafalta": "failure",
    "swagat": "welcome",
    "alvida": "goodbye",
    "ekdam": "absolutely",
    "shayad": "maybe",
    "zaroor": "surely",
    "ho sakta hai": "might be",
    "bilkul": "exactly",
    "thik hai": "okay",
    "sadar": "always",
    "kripya": "please",
    "sada": "white",
    "kala": "black",
    "laal": "red",
    "neela": "blue",
    "hara": "green",
    "peela": "yellow",
    "bhura": "brown",
    "gulabi": "pink",
    "narangi": "orange",
    "baingani": "purple",
    "dhundhla": "grey",
    "sone": "gold",
    "chandi": "silver",
    "haan": "yes",
    "nahi": "no",
    "nahin": "no",
    "theek": "fine",
    "theek hai": "alright",
    "hu": "am",
    "ladak": "boy",
    "ladki": "girl",
    "aadmi": "man",
    "aurat": "woman",
    "bacha": "child",
    "ghar": "home",
    "shahar": "city",
    "gaon": "village",
    "desh": "country",
    "kharab": "bad",
}

# Tokenizer
def tokenize(text):
    return re.findall(r"\w+|[.,!?;:]", text)

# Token Translator
def translate_token(token):
    lower_tok = token.lower()
    if lower_tok in LEXICON:
        return LEXICON[lower_tok]
    close = difflib.get_close_matches(lower_tok, LEXICON.keys(), n=1, cutoff=0.8)
    if close:
        return LEXICON[close[0]]
    return token

# Sentence Translator
def translate_sentence(sentence):
    tokens = tokenize(sentence)
    translated = []
    for tok in tokens:
        if re.fullmatch(r"[.,!?;:]", tok):
            translated.append(tok)
        else:
            translated.append(translate_token(tok))

    out = ''
    for i, t in enumerate(translated):
        if i > 0 and not re.fullmatch(r"[.,!?;:]", t):
            out += ' '
        out += t
    return out

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Chat API
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.form.get("message", "")
    if user_input.strip() == "":
        return jsonify({"response": ""})
    translation = translate_sentence(user_input)
    return jsonify({"response": translation})

if __name__ == "__main__":
    app.run(debug=True)
