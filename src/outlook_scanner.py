import win32com.client
import joblib
import requests
from io import BytesIO

# -------------------------------
# GitHub Model URLs
# -------------------------------

MODEL_URL = "https://raw.githubusercontent.com/<your-username>/outlook-spam-detector/main/models/spam_model.pkl"
VEC_URL   = "https://raw.githubusercontent.com/<your-username>/outlook-spam-detector/main/models/vectorizer.pkl"

def load_from_github(url):
    content = requests.get(url).content
    return joblib.load(BytesIO(content))

print("Loading model from GitHub...")
model = load_from_github(MODEL_URL)
vectorizer = load_from_github(VEC_URL)
print("Model loaded.")

# -------------------------------
# Outlook Scanner
# -------------------------------

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
inbox = outlook.GetDefaultFolder(6)     # Inbox
junk = outlook.GetDefaultFolder(23)     # Junk folder

messages = inbox.Items
print(f"Checking {len(messages)} emails...\n")

def is_spam(text):
    vec = vectorizer.transform([text])
    return model.predict(vec)[0] == 1

spam_count = 0
for msg in list(messages):
    try:
        text = f"{msg.Subject} {msg.Body}"
        if is_spam(text):
            msg.Move(junk)
            spam_count += 1
            print(f"[SPAM] {msg.Subject} → moved to junk")
        else:
            print(f"[OK] {msg.Subject}")
    except:
        pass

print("\nScan completed.")
print("Total spam moved:", spam_count)
