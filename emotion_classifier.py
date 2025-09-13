import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load model and tokenizer
model_path = "sajeewa/emotion-classification-bert"
emotion_labels = ["anger", "fear", "disgust", "sadness", "surprise", "joy", "anticipation", "trust"]

tokenizer = BertTokenizer.from_pretrained(model_path)
model = BertForSequenceClassification.from_pretrained(model_path, num_labels=len(emotion_labels)).to(device)

# Emotion prediction function
def predict_emotions(text: str):
    model.eval()
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=50).to(device)
    inputs.pop("token_type_ids", None)

    with torch.no_grad():
        logits = model(**inputs).logits

    probs = torch.sigmoid(logits).cpu().numpy()[0]
    return {label: round(float(score), 4) for label, score in zip(emotion_labels, probs)}

# Example usage
example_text = "I'm feeling lonely today."
predictions = predict_emotions(example_text)
dominant_emotion = max(predictions, key=predictions.get)
print({dominant_emotion: predictions[dominant_emotion]})
