from emotion_detection import emotion_detector

def test_emotion_detection():
    statements = ["I am glad this happened","I am really mad about this","I feel disgusted just hearing about this","I am so sad about this","I am really afraid that this will happen"]

    expected_emotions = ["joy","anger","disgust","sadness","fear"]

    for statement, expected_emotion in zip(statements, expected_emotions):
        result = emotion_detector(statement)
        emotion_scores = result['emotionPredictions'][0]['emotion']
        dominant_emotion = max(emotion_scores, key=emotion_scores.get)
        assert dominant_emotion == expected_emotion, f"Expected emotion {expected_emotion}, but got {dominant_emotion} for statement: {statement}"

if __name__ == "__main__":
    test_emotion_detection()


