from flask import Flask, request, jsonify
from wikipedia import summary
from collections import Counter
from wikipedia.exceptions import *

app = Flask(__name__)

search_history = []


def word_frequency(topic: str, n: int):
    temp_topic = topic
    topic = topic.strip().replace(" ", "")
    try:
        article_text = summary(topic)
    except DisambiguationError as e:
        # if there are multiple topic with same name then choose first one
        article_text = summary(e.options[0])
    except PageError:
        return {"error": "no article found"}

    text = article_text.lower().replace(",", "").replace(".", "").split()
    # using set becuase it's lookup is is faster
    stop_words = set(
        [
            "the",
            "a",
            "an",
            "and",
            "are",
            "as",
            "be",
            "but",
            "by",
            "for",
            "if",
            "in",
            "into",
            "is",
            "it",
            "no",
            "not",
            "of",
            "on",
            "to",
            "then",
            "their",
            "they",
        ]
    )
    # we can add more words

    text = [word for word in text if word not in stop_words]

    word_counts = Counter(text)
    top_words = word_counts.most_common(n)
    response = {"topic": temp_topic, "top_words": top_words}
    return response


def add_search_history(topic, top_words):
    search_history.append({"topic": topic, "top_words": top_words})


@app.route("/frequency", methods=["GET"])
def analyze_frequency():
    topic = request.args.get("topic")
    n = int(request.args.get("n", 5))  # set default of n is is not present
    # if there is no topic or n < 1 return error
    if topic is None:
        return jsonify({"error": "topic is required"}), 400
    if n < 1:
        return jsonify({"error": "n must be greater than 0"}), 400
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
