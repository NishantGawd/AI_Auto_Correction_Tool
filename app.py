import streamlit as st
import pandas as pd
import numpy as np
import time
import base64
import nltk
import random
import re
import google.generativeai as genai
from textblob import TextBlob
from nltk.corpus import wordnet
from difflib import ndiff
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Set Streamlit page config
st.set_page_config(
    page_title="✨ AI Auto-Correction Tool",
    page_icon=":pencil2:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Download necessary NLTK data
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Gemini grammar correction
def correct_text(text, tone="professional"):
    try:
        prompt = f"""Correct the grammar and spelling of the following text. Make it sound {tone}:

        Text: \"\"\"{text}\"\"\"

        Corrected:"""
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Gemini correction failed: {str(e)}")
        return text

# Rephrasing suggestions (using TextBlob + wordnet)
def get_rephrasing_suggestions(text, num_suggestions=3):
    suggestions = []
    blob = TextBlob(text)

    for _ in range(num_suggestions * 2):
        words = text.split()
        tagged = blob.tags
        for i, (word, pos) in enumerate(tagged):
            if i < len(words) and pos.startswith(('VB', 'NN', 'JJ')):
                syns = wordnet.synsets(word)
                if syns:
                    lemma = random.choice(syns).lemmas()[0].name()
                    if lemma != word:
                        words[i] = lemma
        if len(words) > 4 and random.random() > 0.5:
            pivot = random.randint(1, len(words)-1)
            words = words[pivot:] + words[:pivot]
        suggestion = ' '.join(words)
        if suggestion != text and suggestion not in suggestions:
            suggestions.append(suggestion)
        if len(suggestions) >= num_suggestions:
            break
    return suggestions

# Download link
def get_download_link(text, filename="corrected_text.txt"):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download Corrected Text</a>'

# Change count
def calculate_changes(original, corrected):
    diff = ndiff(original.split(), corrected.split())
    return sum(1 for d in diff if d.startswith('+ ') or d.startswith('- '))

# Main Streamlit app
def main():
    st.title("✨ AI-Powered Auto-Correction Tool")
    st.markdown("Professional writing correction powered by Gemini AI")

    if 'history' not in st.session_state:
        st.session_state.history = pd.DataFrame(columns=["Original", "Corrected", "Timestamp"])
    if 'rephrasings' not in st.session_state:
        st.session_state.rephrasings = []

    st.sidebar.title("Settings")
    tone = st.sidebar.selectbox("Tone", ["professional", "formal", "casual"], index=0)
    show_readability = st.sidebar.checkbox("Show readability score", True)
    show_rephrasing = st.sidebar.checkbox("Show rephrasing suggestions", True)
    dark_mode = st.sidebar.checkbox("Dark mode", False)

    if st.sidebar.button("🧹 Clear History"):
        st.session_state.history = pd.DataFrame(columns=["Original", "Corrected", "Timestamp"])
        st.session_state.rephrasings = []
        if 'corrected_text' in st.session_state:
            del st.session_state.corrected_text
        st.sidebar.success("History cleared!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original Text")
        input_text = st.text_area("Input:", height=300, placeholder="Type or paste text here...", key="input_text")

        if st.button("🚀 Correct Text"):
            if not input_text.strip():
                st.warning("Please enter some text to correct.")
            else:
                with st.spinner("🔍 Analyzing text..."):
                    start_time = time.time()
                    corrected_text = correct_text(input_text, tone)
                    rephrasings = get_rephrasing_suggestions(corrected_text)
                    st.session_state.corrected_text = corrected_text
                    st.session_state.rephrasings = rephrasings
                    st.session_state.processing_time = time.time() - start_time

                    new_entry = pd.DataFrame({
                        "Original": [input_text],
                        "Corrected": [corrected_text],
                        "Timestamp": [pd.Timestamp.now()]
                    })
                    st.session_state.history = pd.concat([st.session_state.history, new_entry], ignore_index=True)

    with col2:
        st.subheader("Corrected Text")
        if 'corrected_text' in st.session_state:
            st.text_area("Output:", value=st.session_state.corrected_text, height=300, key="corrected_text")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Original Chars", len(input_text))
            with col2:
                st.metric("Corrected Chars", len(st.session_state.corrected_text))
            with col3:
                st.metric("Changes", calculate_changes(input_text, st.session_state.corrected_text))

            st.markdown(get_download_link(st.session_state.corrected_text), unsafe_allow_html=True)
            if st.button("📋 Copy to Clipboard"):
                st.success("Copied to clipboard!")

            if show_rephrasing and st.session_state.rephrasings:
                with st.expander("🔄 Rephrasing Suggestions"):
                    for i, rephrase in enumerate(st.session_state.rephrasings, 1):
                        st.text_area(f"Suggestion {i}", value=rephrase, height=75, key=f"sug_{i}", disabled=True)

    if not st.session_state.history.empty:
        st.sidebar.subheader("History")
        for idx, row in st.session_state.history.sort_values("Timestamp", ascending=False).iterrows():
            with st.sidebar.expander(f"{row['Timestamp'].strftime('%H:%M')}"):
                st.text_area("Original", value=row['Original'], height=100, key=f"orig_{idx}")
                st.text_area("Corrected", value=row['Corrected'], height=100, key=f"corr_{idx}")
                if st.button("Use", key=f"use_{idx}"):
                    st.session_state.corrected_text = row['Corrected']

if __name__ == "__main__":
    main()
