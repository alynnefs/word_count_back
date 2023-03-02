from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, support_credentials=True)


def remove_duplicate(words: list) -> list:
    return list(dict.fromkeys(words))


@app.route("/count/", methods=["GET"])
@app.route("/count/<text>", methods=["GET"])
def count_the_words(text=""):
    text = text.strip()
    if not text:
        return str(0)

    list_separate_words = text.split(" ")
    without_duplicate = remove_duplicate(list_separate_words)
    filtered = list(filter(lambda x: x, without_duplicate))
    count = len(filtered)

    return str(count)
