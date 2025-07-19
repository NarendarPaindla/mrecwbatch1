# real_time_recommender.py
# Streamlit Real-Time Telugu Movie Recommendation Engine (no sklearn)
# Dependencies: pip install streamlit pandas requests lxml

import streamlit as st
import pandas as pd
import os
import requests
import math
import re
from collections import defaultdict, Counter

@st.cache_data(show_spinner=False)
def generate_telugu_movies_csv():
    """
    Scrape Wikipedia by year for Telugu films (1931–present) and save CSV.
    """
    movies = []
    current_year = pd.Timestamp.now().year
    for year in range(1931, current_year + 1):
        url = f"https://en.wikipedia.org/wiki/List_of_Telugu_films_of_{year}"
        try:
            tables = pd.read_html(url)
            df_year = next((t for t in tables if 'Title' in t.columns), None)
            if df_year is None:
                continue
            for title in df_year['Title'].dropna().astype(str):
                movies.append({'title': title.strip(), 'year': year})
        except Exception:
            continue
    df = pd.DataFrame(movies).drop_duplicates(subset='title').reset_index(drop=True)
    df.to_csv('telugu_movies.csv', index=False)
    return df

@st.cache_data(show_spinner=False)
def load_data():
    """
    Load CSV if exists; otherwise generate via scraping.
    Normalize columns to ensure 'title' and 'year' exist.
    """
    csv_path = 'telugu_movies.csv'
    if not os.path.exists(csv_path):
        df = generate_telugu_movies_csv()
    else:
        df = pd.read_csv(csv_path)
        # Strip whitespace from column names
        df.columns = [col.strip() for col in df.columns]
        # Rename common variants to 'title' and 'year'
        if 'title' not in df.columns:
            if 'Title' in df.columns:
                df.rename(columns={'Title': 'title'}, inplace=True)
            else:
                st.error("CSV file is missing a 'title' column. Please regenerate the CSV.")
                st.stop()
        if 'year' not in df.columns:
            if 'Year' in df.columns:
                df.rename(columns={'Year': 'year'}, inplace=True)
            else:
                df['year'] = pd.NA
    return df


def tokenize(text):
    """
    Simple word tokenizer: lowercase alphanumeric tokens.
    """
    return re.findall(r"\b\w+\b", text.lower())

@st.cache_data(show_spinner=False)
def build_tfidf_docs(corpus):
    """
    Build TF-IDF representation for each document (title+year).
    """
    N = len(corpus)
    df_count = defaultdict(int)
    tokenized = []
    # Document Frequencies
    for doc in corpus:
        tokens = tokenize(doc)
        tokenized.append(tokens)
        for tok in set(tokens):
            df_count[tok] += 1
    # Inverse Document Frequencies
    idf = {tok: math.log((N + 1) / (df_count[tok] + 1)) + 1 for tok in df_count}
    # TF-IDF per document
    tfidf_docs = []
    for tokens in tokenized:
        tfidf = {}
        counts = Counter(tokens)
        total = len(tokens)
        for tok, cnt in counts.items():
            tf = cnt / total
            tfidf[tok] = tf * idf.get(tok, 0.0)
        tfidf_docs.append(tfidf)
    return tfidf_docs


def cosine_sim(d1, d2):
    """
    Cosine similarity between two TF-IDF dicts.
    """
    common = set(d1.keys()) & set(d2.keys())
    num = sum(d1[k] * d2[k] for k in common)
    denom = math.sqrt(sum(v * v for v in d1.values())) * math.sqrt(sum(v * v for v in d2.values()))
    return num / denom if denom else 0.0


def main():
    st.set_page_config(page_title="Telugu Movie Recommender", layout='wide')
    st.title("🎬 Real-Time Telugu Movie Recommendation Engine")
    st.markdown(
        "No external ML libraries—scrapes Wikipedia for all Telugu films, normalizes columns, then recommends similar titles live."
    )

    df = load_data()
    # Combine title and year for better context
    corpus = (df['title'] + ' ' + df['year'].astype(str).fillna('')).tolist()
    tfidf_docs = build_tfidf_docs(corpus)

    num_recs = st.sidebar.slider("Number of recommendations", 1, 10, 5)
    selected = st.sidebar.selectbox("Choose a Telugu movie", df['title'].tolist())

    if selected:
        idx = df.index[df['title'] == selected][0]
        v1 = tfidf_docs[idx]
        sims = [cosine_sim(v1, v2) for v2 in tfidf_docs]
        scored = sorted(enumerate(sims), key=lambda x: x[1], reverse=True)
        top_idxs = [i for i, score in scored if i != idx][:num_recs]
        recommendations = df['title'].iloc[top_idxs].tolist()

        st.subheader("Recommended Telugu Movies")
        cols = st.columns(num_recs)
        for col, rec in zip(cols, recommendations):
            col.write(f"**{rec}**")

    if st.sidebar.button("Download Telugu Movies CSV"):
        with open('telugu_movies.csv', 'rb') as f:
            st.sidebar.download_button(
                label="Download CSV",
                data=f,
                file_name="telugu_movies.csv",
                mime="text/csv"
            )

if __name__ == '__main__':
    main()
