"""
Este módulo proporciona una aplicación Flask para detectar emociones en texto.
"""
from flask import Flask, request, render_template, jsonify
import requests
app = Flask(__name__)
def emotion_detector(text_to_analyze):
    """
    Detects emotions in the given text.

    Args:
        text_to_analyze (str): The text to analyze for emotions.

    Returns:
        dict: A dictionary containing emotion scores and dominant emotion.
    """
    if not text_to_analyze.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    url = 'sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = { "raw_document": { "text": text_to_analyze } }
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    try:
        response = requests.post(url, json=myobj, headers=header, timeout=10)
        response.raise_for_status()
        response_json = response.json()
        emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness']
        emotion_scores = {emotion: response_json.get(emotion, None) for emotion in emotions}
        dominant_emotion = response_json.get('dominant_emotion', None)
        if dominant_emotion is None:
            return {'error': '¡Texto inválido! ¡Por favor, inténtalo de nuevo!'}
        return {
            'anger': emotion_scores['anger'],
            'disgust': emotion_scores['disgust'],
            'fear': emotion_scores['fear'],
            'joy': emotion_scores['joy'],
            'sadness': emotion_scores['sadness'],
            'dominant_emotion': dominant_emotion
        }
    except requests.exceptions.HTTPError:
        if response.status_code == 400:
            return {
                'anger': None,
                'disgust': None,
                'fear': None,
                'joy': None,
                'sadness': None,
                'dominant_emotion': None
            }
        else:
            return {}
@app.route('/')
def index():
    """
    Renders the index.html template.
    """
    return render_template('index.html')
@app.route('/emotionDetector', methods=['GET'])
def emotion_detection():
    """
    Handles emotion detection request.

    Returns:
        dict: A dictionary containing emotion scores and dominant emotion.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    if text_to_analyze is None or text_to_analyze.strip() == "":
        return jsonify({'error': 'No text to analyze provided'}), 400
    response_text = emotion_detector(text_to_analyze)
    return jsonify(response_text)
if __name__ == '__main__':
    app.run(debug=True)
