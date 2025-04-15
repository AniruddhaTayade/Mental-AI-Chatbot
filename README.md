# Mental Health Chatbot

## Overview
This mental health assistant Flask-based web application designed to provide a safe and engaging platform for a person to discuss their mental health. It uses cutting-edge natural language processing (NLP) models to facilitate meaningful conversations, summarize chats, and analyze user sentiment. The chatbot ensures user data privacy and supports personalized interactions by tailoring responses based on user-provided information.

---

## Features
- **User Authentication**: Secure signup, login, and logout functionalities.
- **Personalized Chat**: Custom responses based on user-provided likes, dislikes, and preferences.
- **Sentiment Analysis**: Analyzes chat sentiment to detect alarming content.
- **Chat Summarization**: Summarizes conversations using pre-trained NLP models.
- **Session Management**: Allows users to view and save chat history.
- **Session Analysis**: Summarizes user chat sessions and flags potential concerns.

---

## Technologies Used
- **Backend**: Flask
- **Database**: SQLite
- **NLP Models**: Hugging Face Transformers (Summarization, Sentiment Analysis)
- **Authentication**: Flask-Login
- **Frontend**: Jinja2 Templates, HTML, CSS
- **Environment Management**: dotenv
- **AI API**: Google Gemini API (via `google.generativeai`)

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- Flask
- SQLite
- Hugging Face Transformers library
- Google Gemini API access

### Installation Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/AniruddhaTayade/Mental-AI-Chatbot
   cd Mental-AI-Chatbot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file to configure environment variables:
   ```
   SECRET_KEY=<your-secret-key>
   GOOGLE_API_KEY=<your-google-api-key>
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```bash
   python app.py
   ```

6. Open the application in your browser at:
   ```
   http://127.0.0.1:PORT/
   ```

---

## Application Routes

| Route                  | Method | Description                                     |
|------------------------|--------|-------------------------------------------------|
| `/`                    | GET    | Homepage                                       |
| `/signup`              | GET/POST | User signup page                              |
| `/login`               | GET/POST | User login page                               |
| `/logout`              | GET    | Logs out the user                              |
| `/chat`                | GET    | Chat interface for logged-in users            |
| `/send_message`        | POST   | Handles user messages and returns bot responses |
| `/end_chat`            | POST   | Summarizes and saves chat history             |
| `/dashboard`           | GET    | User dashboard displaying session details     |
| `/mood-zone`           | GET    | Mood-specific resources page                  |
| `/users`               | GET    | Admin view of all registered users            |
| `/get_user_sessions`   | GET    | Retrieves all chat sessions for the current user |
| `/session_summary/<id>`| GET    | Summarizes a specific user session            |

---

## Key Components

### User Management
- Implements user authentication via `flask_login`.
- Stores user data, preferences, and credentials securely in an SQLite database.

### Chat Functionality
- Handles user messages and generates responses using the Google Gemini API.
- Summarizes chats with Hugging Face's `summarization` pipeline.
- Analyzes sentiment to flag alarming content using Hugging Face's `sentiment-analysis` pipeline.

### Session Management
- Saves chat sessions to the database (`ChatHistory` model).
- Provides users with a summary and sentiment analysis of their past sessions.
- Flags sessions containing potentially alarming content.

### Mood Zone
- Dynamic pages for specific moods, providing targeted resources and activities.

---

## Models
- **User**: Stores user details such as username, password, preferences, and favorites.
- **ChatHistory**: Logs chat content, timestamps, and associated user IDs.

---

## Example `.env` File
```env
SECRET_KEY=your-random-secret-key
GOOGLE_API_KEY=your-google-api-key
```

---

## Future Enhancements
- Integration with a professional mental health support service.
- Multi-language support.
- Improved natural language understanding for nuanced conversations.
- Advanced mood-based content recommendations.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for discussion.

---

## Acknowledgements
- [Hugging Face Transformers](https://huggingface.co/transformers/)
- [Flask](https://flask.palletsprojects.com/)
- [Google Gemini API](https://cloud.google.com/)

