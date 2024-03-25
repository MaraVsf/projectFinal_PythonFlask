import requests

def emotion_detector(text_to_analyze):
    if not text_to_analyze.strip():
        return {'anger': None,'disgust': None,'fear': None,'joy': None,'sadness': None,'dominant_emotion': None}

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    myobj = { "raw_document": { "text": text_to_analyze } }
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    
    try:
        response = requests.post(url, json=myobj, headers=header)
        response.raise_for_status()
        response_json = response.json()

        emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness']
        emotion_scores = {emotion: response_json.get(emotion, None) for emotion in emotions}
        dominant_emotion = response_json.get('dominant_emotion', None)

        return {'anger': emotion_scores['anger'],'disgust': emotion_scores['disgust'],'fear': emotion_scores['fear'],'joy': emotion_scores['joy'],'sadness': emotion_scores['sadness'],'dominant_emotion': dominant_emotion}
    except requests.exceptions.HTTPError as err:
        if response.status_code == 400:
            return {'anger': None,'disgust': None,'fear': None,'joy': None,'sadness': None,'dominant_emotion': None}
        else:
            raise err

import json

def emotion_predictor(response_text):
    response_dict = response_text  # No es necesario llamar a json.loads() ya que el resultado ya es un diccionario
    emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness']
    emotion_scores = {}
    for emotion in emotions:
        if emotion in response_dict:
            emotion_scores[emotion] = response_dict[emotion]
        else:
            emotion_scores[emotion] = 0.0
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    output_dict = {
        'anger': emotion_scores['anger'],
        'disgust': emotion_scores['disgust'],
        'fear': emotion_scores['fear'],
        'joy': emotion_scores['joy'],
        'sadness': emotion_scores['sadness'],
        'dominant_emotion': dominant_emotion
    }
    return output_dict