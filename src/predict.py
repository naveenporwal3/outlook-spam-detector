import joblib
import requests
from io import BytesIO

MODEL_URL = "https://raw.githubusercontent.com/<your-username>/outlook-spam-detector/main/models/spam_model.pkl"
VEC_URL   = "https://raw.githubusercontent.com/<your-username>/outlook-spam-detector/main/models/vectorizer.pkl"

def load_from_github(url):
    content = requests.get(url).content
    return joblib.load(BytesIO(content))

model = load_from_github(MODEL_URL)
vectorizer = load_from_github(VEC_URL)

def predict_text(text):
    vec = vectorizer.transform([text])
    return "SPAM" if model.predict(vec)[0] == 1 else "HAM"

print(predict_text("You won a free iPhone"))
