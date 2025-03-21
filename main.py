import csv
import re
from urllib.parse import urlparse
from scrapper.amazon_scraper import get_amazon_comments
from scrapper.flipkart_scraper import get_flipkart_comments
from scrapper.myntra_scraper import get_myntra_comments
from sentiment_analysis import analyze_sentiment

# Save Results to CSV
import os

def save_to_csv(comments, filename="reviews.csv"):
    # Ensure 'reviews' folder exists
    if not os.path.exists('reviews'):
        os.makedirs('reviews')

    # Save the file in the 'reviews' folder
    file_path = os.path.join('reviews', filename)
    
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Review", "Sentiment"])
        for comment in comments:
            sentiment = analyze_sentiment(comment)
            writer.writerow([comment, sentiment])
    
    print(f"\n✅ Data successfully saved to **{file_path}**")


# Main Function
def main():
    platform = input("Enter platform (amazon/flipkart/myntra): ").strip().lower()
    product_url = input("Enter product URL: ").strip()

    if "amazon" in platform:
        comments = get_amazon_comments(product_url, max_reviews=50)
    elif "flipkart" in platform:
        parsed_url = urlparse(product_url)
        path_parts = parsed_url.path.strip('/').split('/')
    
        if len(path_parts) >= 3:
            product_name = path_parts[0]
            product_id = path_parts[2]
            product_url = f"https://www.flipkart.com/{product_name}/product-reviews/{product_id}"

        comments = get_flipkart_comments(product_url, max_reviews=50)
    elif "myntra" in platform:
        match = re.search(r'/(\d+)/buy', product_url)
        if match:
            product_id = match.group(1)
            product_url = f"https://www.myntra.com/reviews/{product_id}"
            print("URL=", product_url)

        comments = get_myntra_comments(product_url)
    else:
        print("Invalid platform. Please choose from Amazon, Flipkart, or Myntra.")
        return

    if not comments:
        print("No comments found or URL might be incorrect.")
        return

    save_to_csv(comments, f"{platform}_reviews.csv")

if __name__ == "__main__":
    main()
