with open('tracking.txt', 'r') as tracking_file:
    tracking_content = tracking_file.readlines()

# Extract the websites from everything.txt and tracking.txt
tracking_websites = [line.split()[1] for line in tracking_content if line.strip().startswith('0.0.0.0')]

with open('bad.txt', 'w') as bad_file:
    for tracker in tracking_websites:
        bad_file.write(tracker + '\n')