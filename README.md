# AI Auto Correction Tool

# 🚀 AI Auto-Correction App | Pinnacle Labs Internship

During my internship at **Pinnacle Labs**, I developed an **AI-powered Auto-Correction App** that helps users enhance their writing by automatically fixing grammar, spelling, and stylistic errors. The app combines rule-based and generative AI to provide accurate, real-time corrections.

---

## 🛠 Technologies Used

* **Streamlit** — Interactive app interface
* **Google Generative AI (Gemini API)** — Advanced language corrections
* **TextBlob** — Grammar and spelling checks
* **LanguageTool** — Rule-based grammar validation
* **NLTK** — Natural language processing
* **Pandas / NumPy** — Data handling
* **Dotenv** — Secure API key management

---

## 💡 Features

✅ Real-time grammar and spelling correction
✅ Suggestions for improved clarity and style
✅ Uses **Gemini API** for advanced language model support
✅ Simple, interactive **Streamlit** UI
✅ Secure API key handling with `.env`

---

## ⚙️ Installation

📌 **Clone the repository**

```bash
git clone https://github.com/your-username/ai-auto-correction-app.git
cd ai-auto-correction-app
```

📌 **Install dependencies**

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit>=1.22.0
pip install pandas>=1.5.3
pip install numpy>=1.24.2
pip install language-tool-python>=2.7.0
pip install textblob>=0.17.1
pip install nltk>=3.8.1
pip install python-dotenv>=1.0.0
pip install google-generativeai>=0.5.0
```

📌 **Set up environment variables**

Create a `.env` file in the project directory:

```env
GEMINI_API_KEY=your_gemini_api_key
```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

* Open the browser link provided in your terminal
* Enter or paste text to see corrections

---

## 💡 Future Improvements

* Add support for multiple languages
* Suggest tone adjustments (formal/informal)
* Provide detailed grammar explanations
