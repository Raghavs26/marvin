from flask import Flask, request, jsonify
from wikipedia import summary
from collections import Counter
from wikipedia.exceptions import *

app = Flask(__name__)

search_history = []


def word_frequency(topic, n):
    try:
        article_text = summary(topic)
    except DisambiguationError as e:
        #if there are multiple topic with same name then choose first one
        article_text = summary(e.options[0])
    except PageError:
        return {"error": "no article found"}

    text = article_text.lower().replace(",", "").replace(".", "").split()
    word_counts = Counter(text)
    top_words = word_counts.most_common(n)
    response = {"topic": topic, "top_words": top_words}
    return response


def add_search_history(topic, top_words):
    search_history.append({"topic": topic, "top_words": top_words})


@app.route("/frequency", methods=["GET"])
def analyze_frequency():
    topic = request.args.get("topic")
    n = int(request.args.get("n", 5))  # set n = 5
    response = word_frequency(topic, n)
    # print(response)
    search_history.append({"topic": topic, "top_words": response["top_words"]})
    # print(search_history)
    return jsonify(response)


@app.route("/history", methods=["GET"])
def get_search_history():
    return jsonify(search_history)


if __name__ == "__main__":
    app.run(debug=True)
