# 🧠 Mental Health AI Chatbot

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.x-black?style=flat&logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue?style=flat&logo=sqlite)
![HuggingFace](https://img.shields.io/badge/NLP-HuggingFace-yellow?style=flat&logo=huggingface)
![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-orange?style=flat&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

> A secure, full-stack mental health assistant built with Flask, featuring real-time AI conversation,
> NLP-powered sentiment analysis, and enterprise-grade security features.

---

## 🔐 Security Features

This project was built with a cybersecurity-first approach:

- **CSRF Protection** — All forms protected against cross-site request forgery
- **Input Validation** — Server-side sanitization on all user inputs
- **Secure Session Management** — Encrypted session tokens with expiry
- **Audit Logging** — All user actions and flagged sessions are logged
- **Email-based 2FA** — Two-factor authentication on login
- **Password Hashing** — Credentials stored using secure hashing (never plaintext)
- **Environment Variables** — All secrets managed via `.env`, never hardcoded

---

## ✨ Key Features

- **AI Conversation** — Personalized responses powered by Google Gemini API tailored to user likes, dislikes, and preferences
- **Sentiment Analysis** — Real-time detection of alarming or distressing content using Hugging Face
- **Chat Summarization** — Automatic session summaries using pre-trained NLP models
- **Mood Zone** — Dynamic mood-based resource pages with targeted activities
- **Session Dashboard** — Full history of past conversations with sentiment scores and flagged content
- **User Authentication** — Secure signup, login, and logout via Flask-Login

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Flask (Python) |
| Database | SQLite |
| AI / NLP | Google Gemini API, Hugging Face Transformers |
| Authentication | Flask-Login |
| Frontend | Jinja2, HTML5, CSS3 |
| Security | CSRF, 2FA, Input Validation, Audit Logs, Secure Sessions |

---

## 📁 Project Structure

```
Mental-AI-Chatbot/
├── app.py                  # Main Flask application & routes
├── models.py               # User & ChatHistory database models
├── templates/              # Jinja2 HTML templates
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── chat.html
│   ├── dashboard.html
│   └── mood_zone.html
├── static/                 # CSS, JS, assets
├── requirements.txt
├── .env.example
└── README.md
```

---

## 📡 API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Homepage |
| `/signup` | GET/POST | User registration |
| `/login` | GET/POST | User login with 2FA |
| `/logout` | GET | Logout |
| `/chat` | GET | Main chat interface |
| `/send_message` | POST | Send message, get AI response |
| `/end_chat` | POST | Summarize and save session |
| `/dashboard` | GET | User session dashboard |
| `/mood-zone` | GET | Mood-based resource pages |
| `/users` | GET | Admin view of all users |
| `/get_user_sessions` | GET | Retrieve all sessions for current user |
| `/session_summary/<id>` | GET | View specific session summary |

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.8+
- Google Gemini API key
- Hugging Face Transformers library

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/AniruddhaTayade/Mental-AI-Chatbot
cd Mental-AI-Chatbot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
SECRET_KEY=your-random-secret-key
GOOGLE_API_KEY=your-google-api-key

# 4. Initialize the database
flask db init
flask db migrate
flask db upgrade

# 5. Run the application
python app.py
```

Open in browser: `http://127.0.0.1:PORT/`

---

## 🗄️ Database Models

**User**
- Stores username, hashed password, preferences, likes, dislikes, and favorites
- Linked to all chat sessions via user ID

**ChatHistory**
- Logs full chat content, timestamps, sentiment scores, and associated user ID
- Flags sessions containing potentially alarming content for review

---

## 🔮 Future Enhancements

- Integration with licensed mental health support services
- Multi-language NLP support
- Advanced mood-based content recommendation engine
- Mobile-responsive UI overhaul
- Real-time crisis detection and escalation alerts

---

## 👤 Contributor

**Aniruddha Tayade**
[LinkedIn](https://www.linkedin.com/in/aniruddhatayade/) | [GitHub](https://github.com/AniruddhaTayade)

---

## 📄 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Flask](https://flask.palletsprojects.com/)
- [Google Gemini API](https://ai.google.dev/)
