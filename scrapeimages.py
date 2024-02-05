import requests
import os
from bs4 import BeautifulSoup

# Function to scrape image URLs from a webpage
def scrape_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_urls = []
    for img in soup.find_all('img', class_='s-image'):
        img_url = img.get('src')
        if img_url:
            image_urls.append(img_url)
    return image_urls
queries = ['gawr gura', 'anime body pillow']
for query in queries: 
    # Example usage
    image_urls = scrape_images(f'https://www.amazon.sg/s?k={query}&ref=nb_sb_noss_2')
    print(image_urls)

    # Folder to save images
    folder = f"./images/{query}/"

    # Create the folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)

    # Download and save each image
    for url in image_urls:
        print(f"Downloading {url}...")
        response = requests.get(url)
        with open(os.path.join(folder, os.path.basename(url)), 'wb') as f:
            f.write(response.content)