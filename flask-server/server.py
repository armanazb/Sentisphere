import os
import time
import torch
from google.cloud import firestore
from google.oauth2 import service_account
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import scrapes
import requests
import json

# Initialize Flask app
app = Flask(__name__)
CORS(app)

def download_model_with_retry(model_name):
    while True:
        try:
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            return model, tokenizer
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error: {e}. Retrying in 5 seconds...")
            time.sleep(5)

model, tokenizer = download_model_with_retry("ProsusAI/finbert")

def generate_sentim(stock_name):
    new_stock = scrapes.stock(stock_name)
    info_list = new_stock.scrape()
    
    if isinstance(info_list, int):
        # If info_list is an int, return or handle the error case appropriately
        return {"error": "Failed to scrape stock information"}

    news_description = info_list[5]
    overall_score = [0, 0, 0]

    for description in news_description:
        inputs = tokenizer(description, padding=True, truncation=True, return_tensors='pt')
        outputs = model(**inputs)
        sentiment_scores = torch.nn.functional.softmax(outputs.logits, dim=-1)

        first_number = sentiment_scores[0, 0].item()
        second_number = sentiment_scores[0, 1].item()
        third_number = sentiment_scores[0, 2].item()

        overall_score[0] += float(first_number)*100
        overall_score[1] += float(second_number)*100
        overall_score[2] += float(third_number)*100

    overall_score[0] /= len(news_description)
    overall_score[1] /= len(news_description)
    overall_score[2] /= len(news_description)

    return {
        "positive": overall_score[0],
        "neutral": overall_score[1],
        "negative": overall_score[2],
        "stockname": info_list[0],
        "articletitle": info_list[4],
        "articledesc": info_list[5],
        "articlepicture": info_list[6],
        "articlelink": info_list[7]
    }

load_dotenv()

@app.route("/sentiment", methods=["GET"])
def sentiment():
    stock_name = request.args.get("stock_name")
    if not stock_name:
        return jsonify({"error": "No stock name provided"}), 400
    
    try:
        sentiment_scores = generate_sentim(stock_name)
        return jsonify(sentiment_scores)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/graph', methods=["GET"])
def get_graph_by_query():
    ticker = request.args.get("ticker")

    if not ticker:
        return jsonify({"error": "No ticker provided"}), 400

    stocker = scrapes.stock(ticker)
    graph_json = stocker.generate_graph()
    return jsonify(json.loads(graph_json))

service_account_key_path = os.path.join(os.path.dirname(__file__), 'credentials', 'hawkhacks-423710-bc7d29174d93.json')

credentials = service_account.Credentials.from_service_account_file(service_account_key_path)

db = firestore.Client(credentials=credentials)

if __name__ == "__main__":
    app.run(debug=True)
