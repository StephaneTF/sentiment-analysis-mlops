# -----
#  APP
# -----

from pathlib import Path
import re
import joblib
from flask import Flask, request, jsonify

# Load the model and vectorizer saved from the notebook
BASE_DIR = Path(__file__).resolve().parent
model = joblib.load(BASE_DIR / "models" / "sentiment_model.joblib")
vectorizer = joblib.load(BASE_DIR / "models" / "tfidf_vectorizer.joblib")

app = Flask(__name__)

# Clean an incoming tweet using the same steps used during preprocessing
def clean_tweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub(r"https?://\S+|www\.\S+", " ", tweet)
    tweet = re.sub(r"@\w+", " ", tweet)
    tweet = re.sub(r"[^a-z\s]", " ", tweet)
    return " ".join(tweet.split())


# Receive a tweet and return its predicted sentiment
@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not data or not isinstance(data.get("tweet"), str) or not data["tweet"].strip():
        return jsonify({"error": "Send a non-empty tweet in the 'tweet' field."}), 400

    cleaned_tweet = clean_tweet(data["tweet"])
    tweet_features = vectorizer.transform([cleaned_tweet])
    prediction = int(model.predict(tweet_features)[0])

    sentiment = "positive" if prediction == 1 else "negative"
    return jsonify({"sentiment": sentiment})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)