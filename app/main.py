from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route("/count/", methods=["GET"])
@app.route("/count/<text>", methods=["GET"])
def count_the_words(text=""):
    text = text.strip()
    if not text:
        return str(0)

    list_separate_words = text.split(" ")
    filtered = list(filter(lambda x: x, list_separate_words))
    count = len(filtered)

    return str(count)
