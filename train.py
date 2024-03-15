import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score
import pickle, os

# Load the data
def load_data(file_name, label):
    with open(file_name, 'r') as f:
        websites = f.read().splitlines()
    labels = [label] * len(websites)
    return websites, labels

# Prepare the data
bad_websites, bad_labels = load_data('bad.txt', 0)
safe_websites, safe_labels = load_data('safe.txt', 1)

# Combine the data
websites = bad_websites + safe_websites
labels = bad_labels + safe_labels

# Feature extraction
vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3))
features = vectorizer.fit_transform(websites)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
model_filename = 'svm_website_classifier.pkl'

# Create a new SVM model
clf = svm.SVC()

# Check if the model file exists
if os.path.exists(model_filename):
    # Load the existing SVM model
    with open(model_filename, 'rb') as file:
        clf = pickle.load(file)
else:
   clf.fit(X_train, y_train)

# Evaluate the model
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

vocab_filename = 'vocabulary.pkl'

# Check if the model file exists
if not os.path.exists(model_filename):
   with open(model_filename, 'wb') as file:
      pickle.dump(clf, file)

with open(vocab_filename, 'wb') as file:
    pickle.dump(vectorizer.vocabulary_, file)

print(f'Model saved to {model_filename}')
print(f'Vocabulary saved to {vocab_filename}')