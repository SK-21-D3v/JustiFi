import requests
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Configuration from .env file
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
POSTGRES_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

# Categories and Keywords for all types of law-related news
LAW_CATEGORIES = {
    "societal_laws": "society laws, public policy",
    "human_rights": "human rights",
    "criminal_law": "criminal law, crime policy",
    "civil_law": "civil rights, civil litigation",
    "constitutional_law": "constitutional law, amendments",
    "corporate_law": "corporate law, business regulations"
}

# Fetch data from NewsAPI for a specific category
def fetch_news_data(api_key, keywords):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": keywords,
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        print(f"Error fetching news: {response.status_code}")
        return []

# Connect to PostgreSQL database
def connect_to_postgres(config):
    try:
        conn = psycopg2.connect(**config)
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None

# Create a table to store news articles
def create_news_table(conn):
    try:
        cursor = conn.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS news_articles (
            id SERIAL PRIMARY KEY,
            title TEXT UNIQUE,
            description TEXT,
            url TEXT UNIQUE,
            category TEXT,
            published_at TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Error creating table: {e}")

# Save articles to PostgreSQL database with categories
def save_articles_to_db(conn, articles, category):
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO news_articles (title, description, url, category, published_at)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (title) DO NOTHING;
        """
        for article in articles:
            cursor.execute(insert_query, (
                article.get("title"),
                article.get("description"),
                article.get("url"),
                category,
                article.get("publishedAt")
            ))
        conn.commit()
        cursor.close()
    except psycopg2.Error as e:
        print(f"Error saving articles to database: {e}")

# Main workflow
def main():
    # Connect to PostgreSQL
    conn = connect_to_postgres(POSTGRES_CONFIG)
    if not conn:
        return

    # Create table if not exists
    create_news_table(conn)

    # Fetch and save articles for each category
    for category, keywords in LAW_CATEGORIES.items():
        print(f"Fetching news for category: {category}")
        articles = fetch_news_data(NEWSAPI_KEY, keywords)
        if articles:
            save_articles_to_db(conn, articles, category)
            print(f"Saved {len(articles)} articles under category '{category}'.")
        else:
            print(f"No articles found for category: {category}")

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()

# import requests
# import psycopg2
# from psycopg2 import sql
# from dotenv import load_dotenv
# import os

# # Load environment variables from the .env file
# load_dotenv()

# # Configuration from .env file
# NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
# POSTGRES_CONFIG = {
#     "host": os.getenv("DB_HOST"),
#     "database": os.getenv("DB_NAME"),
#     "user": os.getenv("DB_USER"),
#     "password": os.getenv("DB_PASSWORD")
# }

# # Keywords to fetch societal law-related news
# KEYWORDS = "society laws, legal system, human rights, public policy"

# # Fetch data from NewsAPI
# def fetch_news_data(api_key, keywords):
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": keywords,
#         "language": "en",
#         "sortBy": "relevancy",
#         "apiKey": api_key
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return response.json().get("articles", [])
#     else:
#         print(f"Error fetching news: {response.status_code}")
#         return []

# # Connect to PostgreSQL database
# def connect_to_postgres(config):
#     try:
#         conn = psycopg2.connect(**config)
#         return conn
#     except psycopg2.Error as e:
#         print(f"Error connecting to database: {e}")
#         return None

# # Create a table to store news articles
# def create_news_table(conn):
#     try:
#         cursor = conn.cursor()
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS news_articles (
#             id SERIAL PRIMARY KEY,
#             title TEXT,
#             description TEXT,
#             url TEXT,
#             published_at TIMESTAMP
#         );
#         """
#         cursor.execute(create_table_query)
#         conn.commit()
#         cursor.close()
#     except psycopg2.Error as e:
#         print(f"Error creating table: {e}")

# # Save articles to PostgreSQL database
# def save_articles_to_db(conn, articles):
#     try:
#         cursor = conn.cursor()
#         insert_query = """
#         INSERT INTO news_articles (title, description, url, published_at)
#         VALUES (%s, %s, %s, %s)
#         ON CONFLICT DO NOTHING;
#         """
#         for article in articles:
#             cursor.execute(insert_query, (
#                 article.get("title"),
#                 article.get("description"),
#                 article.get("url"),
#                 article.get("publishedAt")
#             ))
#         conn.commit()
#         cursor.close()
#     except psycopg2.Error as e:
#         print(f"Error saving articles to database: {e}")

# # Main workflow
# def main():
#     # Fetch news articles
#     articles = fetch_news_data(NEWSAPI_KEY, KEYWORDS)
#     if not articles:
#         print("No articles found.")
#         return
    
#     # Connect to PostgreSQL
#     conn = connect_to_postgres(POSTGRES_CONFIG)
#     if not conn:
#         return
    
#     # Create table and save articles
#     create_news_table(conn)
#     save_articles_to_db(conn, articles)
#     print(f"Saved {len(articles)} articles to the database.")
    
#     # Close the connection
#     conn.close()

# if __name__ == "__main__":
#     main()

# import requests
# import psycopg2
# from psycopg2 import sql

# # Configuration
# NEWSAPI_KEY = "095e859489534c7fb8d6c85ec6fca8e2"
# POSTGRES_CONFIG = {
#     "host": "localhost",
#     "database": "postgres",
#     "user": "postgres",
#     "password": "Sonia@#2026"
# }

# # Keywords to fetch societal law-related news
# KEYWORDS = "society laws, legal system, human rights, public policy"

# # Fetch data from NewsAPI
# def fetch_news_data(api_key, keywords):
#     url = "https://newsapi.org/v2/everything"
#     params = {
#         "q": keywords,
#         "language": "en",
#         "sortBy": "relevancy",
#         "apiKey": api_key
#     }
#     response = requests.get(url, params=params)
#     if response.status_code == 200:
#         return response.json().get("articles", [])
#     else:
#         print(f"Error fetching news: {response.status_code}")
#         return []

# # Connect to PostgreSQL database
# def connect_to_postgres(config):
#     try:
#         conn = psycopg2.connect(**config)
#         return conn
#     except psycopg2.Error as e:
#         print(f"Error connecting to database: {e}")
#         return None

# # Create a table to store news articles
# def create_news_table(conn):
#     try:
#         cursor = conn.cursor()
#         create_table_query = """
#         CREATE TABLE IF NOT EXISTS news_articles (
#             id SERIAL PRIMARY KEY,
#             title TEXT,
#             description TEXT,
#             url TEXT,
#             published_at TIMESTAMP
#         );
#         """
#         cursor.execute(create_table_query)
#         conn.commit()
#         cursor.close()
#     except psycopg2.Error as e:
#         print(f"Error creating table: {e}")

# # Save articles to PostgreSQL database
# def save_articles_to_db(conn, articles):
#     try:
#         cursor = conn.cursor()
#         insert_query = """
#         INSERT INTO news_articles (title, description, url, published_at)
#         VALUES (%s, %s, %s, %s)
#         ON CONFLICT DO NOTHING;
#         """
#         for article in articles:
#             cursor.execute(insert_query, (
#                 article.get("title"),
#                 article.get("description"),
#                 article.get("url"),
#                 article.get("publishedAt")
#             ))
#         conn.commit()
#         cursor.close()
#     except psycopg2.Error as e:
#         print(f"Error saving articles to database: {e}")

# # Main workflow
# def main():
#     # Fetch news articles
#     articles = fetch_news_data(NEWSAPI_KEY, KEYWORDS)
#     if not articles:
#         print("No articles found.")
#         return
    
#     # Connect to PostgreSQL
#     conn = connect_to_postgres(POSTGRES_CONFIG)
#     if not conn:
#         return
    
#     # Create table and save articles
#     create_news_table(conn)
#     save_articles_to_db(conn, articles)
#     print(f"Saved {len(articles)} articles to the database.")
    
#     # Close the connection
#     conn.close()

# if __name__ == "__main__":
#     main()
