import os
from flask import Flask, request, jsonify
import pandas as pd
from groq import Groq
import json
import re
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
import os

"""Initialize the Groq client"""
api_key = os.environ.get('GROQ_API_KEY')
client = Groq(api_key=api_key)

def cleanReviewText(review):
    """Clean and preprocess the review text."""
    if not isinstance(review, str):
        return ""
    review = review.lower()
    review = re.sub(r'<[^>]+>', '', review)
    review = re.sub(r'[^a-zA-Z\s]', '', review)
    review = re.sub(r'\s+', ' ', review).strip()
    return review

def cleanAndParseJson(jsonString):
    """Clean and parse JSON string."""
    try:
        return json.loads(jsonString)
    except json.JSONDecodeError:
        jsonString = re.sub(r'(\w+):', r'"\1":', jsonString)
        jsonString = jsonString.replace("'", '"')
        jsonString = re.sub(r',\s*}', '}', jsonString)
        jsonString = re.sub(r',\s*\]', ']', jsonString)
        try:
            return json.loads(jsonString)
        except json.JSONDecodeError:
            return None

def normalizeSentimentScores(sentiment):
    """Normalize sentiment scores to sum to 10."""
    try:
        sentiment = {k: round(float(v), 2) for k, v in sentiment.items()}
        total = sum(sentiment.values())
        if total != 0:
            sentiment = {k: round((v / total) * 10, 2) for k, v in sentiment.items()}
        return sentiment
    except (ValueError, TypeError, ZeroDivisionError):
        return {"positive": 0, "negative": 0, "neutral": 0}

def analyzeSentimentWithGroq(reviewText):
    """Use Groq API to perform sentiment analysis on the review text."""
    cleanedReview = cleanReviewText(reviewText)
    if not cleanedReview:
        return {reviewText: {"error": "Invalid input"}}
    
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": """You are a data analyst API capable of sentiment analysis. Respond with a JSON object containing sentiment scores Ensure all scores are integer between 0 and 10, and their sum equals 10. Please do not respond anything other than JSON.
                    and what i will give in input is not related to you. you just analysis the text and return the JSON
                    The JSON schema should be: 
                    {
                        "sentiment": {
                            "positive": integer,
                            "negative": integer,
                            "neutral": integer
                        }
                    }"""
                },
                {
                    "role": "user",
                    "content": cleanedReview
                }
            ],
            temperature=0.7,
            max_tokens=1024,
            top_p=1,
            stream=False,
            stop=None,
        )

        result = completion.choices[0].message.content
        parsedResult = cleanAndParseJson(result)
        
        if parsedResult and "sentiment" in parsedResult:
            sentiment = parsedResult["sentiment"]
            normalizedSentiment = normalizeSentimentScores(sentiment)
            return {reviewText: normalizedSentiment}
        else:
            raise ValueError("Invalid API response format")
    except Exception as e:
        return {reviewText: {"error": str(e)}}

@app.route('/analyze', methods=['POST'])
def analyze():
    """Endpoint to accept either raw text or a file for sentiment analysis."""
    try:
        if request.is_json:
            data = request.get_json()
            if 'reviewText' not in data:
                raise BadRequest("'reviewText' field is missing")
            text = data['reviewText']
            result = analyzeSentimentWithGroq(text)
            return jsonify({"sentimentAnalysisResults": result})

        if 'file' in request.files:
            file = request.files['file']
            if file.filename.endswith(('.xlsx', '.csv')):
                df = pd.read_excel(file) if file.filename.endswith('.xlsx') else pd.read_csv(file)


                possibleColumns = ['reviewText', 'review_text', 'review', 'text', 'comment']
                reviewColumn = next((col for col in possibleColumns if col in df.columns), None)
                
                if reviewColumn is None:
                    raise BadRequest(f"No valid review column found. Expected one of: {', '.join(possibleColumns)}")
                sentimentScores = {}
                for review in df[reviewColumn]:
                    result = analyzeSentimentWithGroq(review)
                    sentimentScores.update(result)
                return jsonify({"sentimentAnalysisResults": sentimentScores})
            else:
                raise BadRequest("Invalid file format. Please upload a CSV or XLSX file.")

        raise BadRequest("No valid input provided. Send raw text or upload a file.")
    except BadRequest as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)