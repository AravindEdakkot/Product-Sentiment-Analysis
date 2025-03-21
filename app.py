import streamlit as st
from scrapper.amazon_scraper import get_amazon_comments
from scrapper.flipkart_scraper import get_flipkart_comments
from scrapper.myntra_scraper import get_myntra_comments
from sentiment_analysis import analyze_sentiment
import pandas as pd
import re
from urllib.parse import urlparse

# Mapping functions
SCRAPER_FUNCTIONS = {
    "Amazon": get_amazon_comments,
    "Flipkart": get_flipkart_comments,
    "Myntra": get_myntra_comments
}

# URL Formatter for Flipkart and Myntra
def format_url(platform, url):
    if platform == "Flipkart":
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) >= 3:
            product_name = path_parts[0]
            product_id = path_parts[2]
            return f"https://www.flipkart.com/{product_name}/product-reviews/{product_id}"
    elif platform == "Myntra":
        match = re.search(r'/(\d+)/buy', url)
        if match:
            product_id = match.group(1)
            return f"https://www.myntra.com/reviews/{product_id}"
    return url

# Streamlit Interface
st.title("🛒 E-commerce Review Sentiment Analyzer")

platform = st.selectbox("Select Platform", ["Amazon", "Flipkart", "Myntra"])
url = st.text_input("Enter Product URL")

if st.button("Analyze Reviews"):
    if not url:
        st.error("⚠️ Please enter a valid URL.")
    else:
        formatted_url = format_url(platform, url)
        scrape_function = SCRAPER_FUNCTIONS.get(platform)
        
        with st.spinner("Scraping reviews..."):
            comments = scrape_function(formatted_url)

        if not comments:
            st.error("❌ No reviews found or invalid URL.")
        else:
            # Perform Sentiment Analysis
            data = [{"Review": c, "Sentiment": analyze_sentiment(c)} for c in comments]
            df = pd.DataFrame(data)
            
            # Save as CSV
            csv_file = f"{platform.lower()}_reviews.csv"
            df.to_csv(f'reviews/{csv_file}', index=False)

            st.success(f"✅ Reviews analyzed successfully!")
            sentiment_counts = df['Sentiment'].value_counts()
            most_common_sentiment = sentiment_counts.idxmax()
            st.header(f"**🏆 Most Common Sentiment:** {most_common_sentiment}")
            st.dataframe(df)
            st.download_button("📥 Download CSV", data=df.to_csv(index=False), file_name=csv_file, mime="text/csv")
            
