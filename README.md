<h1>JustiFi - Legal News Chatbot</h1>

## Overview
The **Legal News Chatbot** is an AI-powered application that allows users to access the latest legal news, court decisions, legal trends, and more. The chatbot retrieves data from the **NewsAPI** and stores it in a **PostgreSQL** database. It uses **Natural Language Processing (NLP)** to provide users with relevant information based on their queries. The chatbot is hosted on **Streamlit**, allowing users to interact with it via a simple web interface.


## Features
- Fetches the latest legal news articles using the **NewsAPI**.
- Stores news data in a **PostgreSQL database**.
- Allows users to ask questions about specific cases, legal trends, or recent news.
- Chatbot responses are powered by **Natural Language Processing (NLP)**.
- Hosted on **Streamlit** for easy access and interaction.

## Installations

### Prerequisites

- **Python 3.8+**
- **PostgreSQL Database** (locally set up or remote)
- **Streamlit**
- **NewsAPI Key** (sign up at [NewsAPI](https://newsapi.org/))

### Steps to Set Up

**Step 1: Clone the repository**<br>

git clone https://github.com/your-username/legal-news-chatbot.git<br>

cd legal-news-chatbot

**Step 2: Install dependencies** <br>
   
pip install -r requirements.txt<br>

**Step 3: Set up PostgreSQL database**<br>

 *1.* Create a database in PostgreSQL (either locally or on a remote server).<br>
 
 *2.* Set up the necessary tables to store news data (you can refer to the SQL schema in the repository).<br>
 
 *3.* Update the connection details in the config.py file:<br>
 - Host: "localhost" or the remote host IP<br>
 - Database name: "your_database_name"<br>
 - Username: "your_postgres_username"<br>
 - Password: "your_postgres_password"<br>

 **Step 4: Add your NewsAPI key**<br>
 
 *1.* Sign up at https://newsapi.org/ and get your API key.<br>
 
 *2.* Insert your API key in the config.py file in the relevant field.<br>
 
**Step 5: Run the application**<br>
streamlit run app.py <br>


## Usage
Once the app is up and running, you can interact with the chatbot via the Streamlit interface. Here are some example questions you can ask:
- General Legal News: "What are the latest legal news updates?"
- Case-Specific Inquiries: "Can you find news about [specific case name]?"
- Legal Topics: "What are the latest updates on intellectual property law?"
- Lawyer or Firm Information: "What are the latest news about [lawyer name]?"
- Court Decisions or Laws: "What recent court decisions have impacted [specific area of law]?"
- Region-Specific Legal News: "What’s the latest legal news in [location]?"
- Legal Trends or Events: "What are the legal trends this year?"

## Contributing
- Fork the repository.
- Create a new branch for your changes.
- Commit your changes.
- Push your changes to your forked repository.
- Create a pull request to the main repository.

## Acknowledgments
- **NewsAPI** for providing access to real-time news articles.
- **Streamlit** for creating a seamless interface for the chatbot.
- **PostgreSQL** for providing a robust database solution.
