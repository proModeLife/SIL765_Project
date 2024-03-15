from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt

# Load the trained SVM model
model_filename = 'svm_website_classifier.pkl'
vocab_filename = 'vocabulary.pkl'

# Load the model and the vocabulary
with open(model_filename, 'rb') as file:
   clf = pickle.load(file)

with open(vocab_filename, 'rb') as file:
   vocabulary = pickle.load(file)

# Create a new CountVectorizer with the same vocabulary
vectorizer = CountVectorizer(analyzer='char', ngram_range=(1, 3), vocabulary=vocabulary)

def extract_website_name(url):
   # Parse the URL to get its components
   parsed_url = urlparse(url)
   # Combine the protocol and the domain name
   website_name = parsed_url.scheme + "://" + parsed_url.netloc
   return website_name

# Function to predict whether a website is a tracker or not
def is_tracker(website_name):
   # Preprocess the website name
   features = vectorizer.transform([website_name])
   # Use the model to predict
   prediction = clf.predict(features)
   return prediction[0] == 0  # 0 indicates a bad website (tracker)

def count_trackers(websites):
   driver = webdriver.Chrome()
   tracker_counts = {}

   for website in websites:
      print('_________', website, '___________')
      driver.get(website)

      # Process the requests and find trackers
      found_trackers = set()
      for request in driver.requests:
            if request.response and 'Content-Type' in request.response.headers:
               content_type = request.response.headers['Content-Type']
               site = extract_website_name(request.url)
               if is_tracker(site):
                  found_trackers.add(site)

      # Store the count of trackers for the current website
      tracker_counts[website] = len(found_trackers)
      print(found_trackers)
      print('\n\n')

   # Close the browser when done
   driver.quit()

   return tracker_counts

def plot_tracker_counts(tracker_counts):
   # Extract website names and their corresponding tracker counts
   websites = list(tracker_counts.keys())
   counts = list(tracker_counts.values())

   # Extract domain names for the x-axis labels
   domain_names = [urlparse(url).netloc for url in websites]

   # Set the style to a more modern one
   plt.style.use('seaborn-v0_8-talk')

   # Create a bar plot with adjusted figure size
   plt.figure(figsize=(10, 6))
   bars = plt.bar(domain_names, counts, color='skyblue')
   plt.xlabel('Websites', fontsize=12)
   plt.ylabel('Number of Trackers', fontsize=12)
   plt.title('Tracker Counts for Different Websites', fontsize=16)
   plt.xticks(rotation=90, fontsize=10)
   plt.yticks(fontsize=10)
   plt.tight_layout()

   # Add data labels to the bars
   for bar in bars:
      yval = bar.get_height()
      plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, int(yval), ha='center', va='bottom', fontsize=10)

   # Show the plot
   plt.savefig('ML-Trackernew.png', dpi=300, bbox_inches='tight')

# Example usage remains the same
websites = [
   'https://www.google.com',
   'https://www.stackoverflow.com',
   'https://www.github.com',
   'https://www.facebook.com',
   'https://www.amazon.com',
   'https://www.youtube.com',
   'https://www.instagram.com',
   'https://www.netflix.com',
   'https://www.linkedin.com',
   'https://www.twitter.com',
   'https://www.pinterest.com',
   'https://www.wikipedia.org',
   'https://www.reddit.com',
   'https://www.imdb.com',
   'https://www.live.com'
]
tracker_counts = count_trackers(websites)
plot_tracker_counts(tracker_counts)