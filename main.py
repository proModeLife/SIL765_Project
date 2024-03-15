from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from urllib.parse import urlparse
import matplotlib.pyplot as plt


def extract_website_name(url):
    # Parse the URL to get its components
    parsed_url = urlparse(url)
    # Combine the protocol and the domain name
    website_name = parsed_url.scheme + "://" + parsed_url.netloc
    return website_name


trackers = set()
with open("bad.txt", "r") as file:
    for line in file:
        # Assuming each line in the file contains a website URL
        website = line.strip()
        trackers.add(website)


def count_trackers(websites):
    # Read the contents of the file and store them in a set

    driver = webdriver.Chrome()
    tracker_counts = {}

    for website in websites:
        # Go to the website
        print('_________', website, '___________')
        driver.get(website)

        # Process the requests and find trackers
        found_trackers = set()
        for request in driver.requests:
            if request.response and 'Content-Type' in request.response.headers:
                content_type = request.response.headers['Content-Type']
                site = extract_website_name(request.url)
                for tracker in trackers:
                    if tracker in site:
                        found_trackers.add(tracker)
                        break  # Break after finding the tracker to avoid adding duplicates

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
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5,
                 int(yval), ha='center', va='bottom', fontsize=10)
    plt.savefig('Standard-Trackernew.png', dpi=300, bbox_inches='tight')

    # Show the plot
    plt.show()


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
