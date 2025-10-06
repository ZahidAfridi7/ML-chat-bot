import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from app.ml.dataset import load_intents_from_json

# Load dataset
texts, labels = load_intents_from_json("data/intents.json")

# Create pipeline: TF-IDF vectorizer + Naive Bayes classifier
model = make_pipeline(TfidfVectorizer(lowercase=True, stop_words="english"), MultinomialNB())

# Train the model
model.fit(texts, labels)

# Save the trained model
joblib.dump(model, "app/ml/intent_classifier.joblib")

print("Intent classifier trained and saved successfully!")
