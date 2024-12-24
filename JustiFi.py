import streamlit as st
import psycopg2
from psycopg2 import sql
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get credentials from the .env file
POSTGRES_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# Connect to PostgreSQL Database
def connect_to_postgres(config):
    try:
        conn = psycopg2.connect(**config)
        return conn
    except psycopg2.Error as e:
        st.error(f"Error connecting to the database: {e}")
        return None

# Fetch data from the database based on user query
def fetch_data_from_db(conn, query):
    try:
        cursor = conn.cursor()
        fetch_query = sql.SQL("""
        SELECT title, description, url, published_at 
        FROM news_articles
        WHERE title ILIKE %s OR description ILIKE %s
        ORDER BY published_at DESC
        LIMIT 5;
        """)
        cursor.execute(fetch_query, (f"%{query}%", f"%{query}%"))
        results = cursor.fetchall()
        cursor.close()
        return results
    except psycopg2.Error as e:
        st.error(f"Error fetching data from database: {e}")
        return []

# Fetch data from NewsAPI
def fetch_from_newsapi(query, category=None):
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "relevancy",
        "apiKey": NEWSAPI_KEY
    }
    if category:
        params["q"] += f" {category}"  # Add category for filtering
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        st.error(f"Error fetching data from NewsAPI: {response.status_code}")
        return []

# Combined function: Fetch from DB or NewsAPI
def fetch_data_from_db_or_api(conn, query, category=None):
    results = fetch_data_from_db(conn, query)  # Search database first
    if not results:  # If database has no data, use NewsAPI
        st.write("No relevant data found in the database. Fetching live results from NewsAPI...")
        articles = fetch_from_newsapi(query, category)
        results = [(a['title'], a['description'], a['url'], a['publishedAt']) for a in articles]
    return results

# Log unanswered queries
def log_unanswered_query(query):
    with open("unanswered_queries.log", "a") as log_file:
        log_file.write(f"{datetime.now()}: {query}\n")

# Chatbot interface in Streamlit
def chatbot_interface():
    st.title("JustiFi - Legal News Chatbot")
    st.write("Ask me about societal laws, legal systems, or public policies!")

    # User Input
    user_query = st.text_input("Enter your query:", placeholder="e.g., human rights, criminal law, corporate law")
    
    # Law categories dropdown
    category = st.selectbox("Select a category:", options=[
        "All", "Criminal Law", "Corporate Law", "Constitutional Law", "Human Rights", "Environmental Law"
    ], index=0)

    if user_query:
        # Connect to PostgreSQL
        conn = connect_to_postgres(POSTGRES_CONFIG)
        if conn:
            # Fetch articles based on the query and category
            results = fetch_data_from_db_or_api(conn, user_query, None if category == "All" else category)
            conn.close()
            
            # Display results or fallback responses
            if results:
                st.write(f"Here are the top results for **'{user_query}'** in **{category}**:")
                for title, description, url, published_at in results:
                    st.markdown(f"### {title}")
                    st.write(description)
                    st.markdown(f"[Read more]({url})")
                    st.write(f"*Published at: {published_at}*")
            else:
                log_unanswered_query(user_query)  # Log unanswered queries
                st.write(f"No relevant data found for **'{user_query}'**.")
                st.write("Try these topics instead:")
                st.markdown("- **Criminal law**")
                st.markdown("- **Corporate law**")
                st.markdown("- **Constitutional law**")
                st.markdown("- **Human rights**")
                st.markdown("- **Environmental law**")
                st.write("Alternatively, check out these resources:")
                st.markdown("- [Government Laws Portal](https://www.legislation.gov)")
                st.markdown("- [UN Human Rights](https://www.ohchr.org)")
                st.markdown("- [Legal Articles](https://www.law.com)")

# Main function
if __name__ == "__main__":
    chatbot_interface()
