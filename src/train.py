import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import joblib
import os

# -----------------------------------------------------------------------------
# 1. Load the dataset from GitHub (no download required)
# -----------------------------------------------------------------------------

DATA_URL = "https://raw.githubusercontent.com/justmarkham/DAT8/master/data/sms.tsv"

df = pd.read_csv(DATA_URL, sep="\t", names=["label", "text"])
df['label'] = df['label'].map({'ham': 0, 'spam': 1})

print("Dataset loaded:", df.shape)

# -----------------------------------------------------------------------------
# 2. Prepare data
# -----------------------------------------------------------------------------

X = df['text']
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------------------------------------------------------------
# 3. Train model
# -----------------------------------------------------------------------------

model = MultinomialNB()
model.fit(X_train_vec, y_train)

preds = model.predict(X_test_vec)
acc = accuracy_score(y_test, preds)

print("Training Completed")
print("Accuracy:", acc)

# -----------------------------------------------------------------------------
# 4. Save model + vectorizer
# -----------------------------------------------------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/spam_model.pkl")
joblib.dump(vectorizer, "models/vectorizer.pkl")

print("Model saved to /models")
