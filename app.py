import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import google.generativeai as genai
from dotenv import load_dotenv
from models import db, User
from config import model
from models import ChatHistory
from transformers import pipeline

from datetime import datetime
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # Ensure to use a secure secret key in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"  # Redirect here if a user is not logged in

# Load user callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



@app.route("/")
def index():
    return render_template("homepage.html", user=current_user)

@app.route("/chat", methods=["GET"])
@login_required
def chat():
    
    return render_template("chat.html")

summarizer = pipeline("summarization", device=0)
sentiment_analyzer = pipeline("sentiment-analysis", device=0)

@app.route("/send_message", methods=["POST"])
@login_required
def send_message():
    user_message = request.get_json().get("message")

    if not user_message:
        return jsonify({"response": "No message provided"}), 400
    
    # Get the bot response
    bot_response = get_chatbot_response(user_message)

    # Accumulate messages in session
    if 'chat_log' not in session:
        session['chat_log'] = []

    session['chat_log'].append(f"User: {user_message}")
    session['chat_log'].append(f"Bot: {bot_response}")

    return jsonify({"response": bot_response})

@app.route("/end_chat", methods=["POST"])
@login_required
def end_chat():
    # Retrieve the accumulated chat log from the session
    chat_log = session.get('chat_log', [])

    if not chat_log:
        return jsonify({"message": "No chat history to save."}), 400
    
    # Combine the chat log into a single string
    chat_content = "\n".join(chat_log)

    # Run summary analysis on the chat
    summary = summarizer(chat_content, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
    sentiment = sentiment_analyzer(chat_content)[0]

    # Check if the chat contains alarming content
    alarming = False
    if sentiment['label'] == 'NEGATIVE' and sentiment['score'] > 0.9:
        alarming = True

    # Save the chat session to the ChatHistory model
    new_chat = ChatHistory(
        user_id=current_user.id,
        chat_content=chat_content,
        timestamp=datetime.utcnow()
    )
    db.session.add(new_chat)
    db.session.commit()

    # Clear the chat log from session after saving
    session.pop('chat_log', None)

    # Return summary and alarming flag
    return jsonify({
        "summary": summary,
        "sentiment": sentiment,
        "alarming": alarming
    })
# Function to send user input to the Gemini API and get a response
def get_chatbot_response(user_input):
    # Collect user information for personalization
    user_info = f"""
    User's Name: {current_user.name}
    Likes: {', '.join(current_user.likes)}
    Dislikes: {', '.join(current_user.dislikes)}
    Favorite Sports: {', '.join(current_user.favorite_sports)}
    Favorite Songs: {', '.join(current_user.favorite_songs)}
    """

    # Prepend the user information to the user input
    full_input = user_info + "\nUser says: " + user_input

    # Start a chat session without context
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [full_input],
            }
        ]
    )

    # Send the user input and get the response
    response = chat_session.send_message(full_input)

    # Extract and return the model's response text
    return response.text

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        age = request.form["age"]
        likes = request.form.getlist("likes")  # Assuming likes is a multiple-choice input
        dislikes = request.form.getlist("dislikes")  # Assuming dislikes is a multiple-choice input
        favorite_sports = request.form.getlist("favorite_sports")  # Assuming sports is a multiple-choice input
        favorite_songs = request.form.getlist("favorite_songs")  # Assuming songs is a multiple-choice input

        new_user = User(
            username=username,
            password=password,
            name=name,
            age=age,
            likes=", ".join(likes),  # Convert list to a comma-separated string
            dislikes=", ".join(dislikes),  # Convert list to a comma-separated string
            favorite_sports=", ".join(favorite_sports),  # Convert list to a comma-separated string
            favorite_songs=", ".join(favorite_songs)  # Convert list to a comma-separated string
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Signup successful! You can now log in.", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash("Username already exists. Please choose a different one.", "danger")
            print(e)  # Print exception for debugging
    
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            login_user(user)
            session["username"] = user.username
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password. Please try again.", "danger")

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", username=current_user.username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/mood-zone')
def mood_zone():
    return render_template('mood_zone.html')

@app.route('/mood/<mood_name>')
def mood_page(mood_name):
    return render_template(f'moods/{mood_name}.html')

@app.route("/users")
def view_users():
    users = User.query.all()  # Query all users from the database
    return render_template("user.html", users=users)  # Render a template to display users

@app.route('/save_chat', methods=['POST'])
@login_required
def save_chat():
    try:
        data = request.get_json()
        user_message = data.get("message")
        bot_response = get_chatbot_response(user_message)

        # Save chat history in the database
        chat_history = ChatHistory(
            user_id=current_user.id,
            chat_content=f"User: {user_message}\nBot: {bot_response}",
            timestamp=datetime.utcnow()
        )

        db.session.add(chat_history)
        db.session.commit()

        return jsonify({"response": bot_response}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_user_sessions', methods=['GET'])
@login_required
def get_user_sessions():
    try:
        # Query chat history for the current user
        user_sessions = ChatHistory.query.filter_by(user_id=current_user.id).order_by(ChatHistory.timestamp.desc()).all()

        if not user_sessions:
            return jsonify({"message": "No chat history found"}), 404

        # Format session data
        session_data = [
            {
                "id": session.id,
                "timestamp": session.timestamp,
                "chat_content": session.chat_content
            }
            for session in user_sessions
        ]

        return jsonify({"sessions": session_data}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/session_summary/<int:user_id>', methods=['GET'])
@login_required
def session_summary(user_id):
    # Ensure the user is viewing their own session or is authorized
    if current_user.id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    # Query the chat history for the user from the database
    sessions = ChatHistory.query.filter_by(user_id=user_id).all()

    if not sessions:
        return jsonify({'message': 'No chat history found for this user.'}), 404

    summaries = []

    # Summarize and analyze each session
    for session in sessions:
        chat_content = session.chat_content
        summary = summarizer(chat_content, max_length=150, min_length=30, do_sample=False)[0]['summary_text']
        sentiment = sentiment_analyzer(chat_content)[0]

        alarming = False
        # If sentiment is negative and score is higher than a threshold, flag it as alarming
        if sentiment['label'] == 'NEGATIVE' and sentiment['score'] > 0.9:
            alarming = True

        # Add the summary, sentiment, alarming flag, and timestamp to the response
        summaries.append({
            'summary': summary,
            'sentiment': {
                'label': sentiment['label'],
                'score': sentiment['score']
            },
            'alarming': alarming,
            'timestamp': session.timestamp
        })

    # Return the list of session summaries
    return jsonify({'summaries': summaries})
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)

