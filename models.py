from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    likes = db.Column(db.String(200), nullable=True)
    dislikes = db.Column(db.String(200), nullable=True)
    favorite_sports = db.Column(db.String(200), nullable=True)
    favorite_songs = db.Column(db.String(200), nullable=True)

    # Define relationship to ChatHistory
    chat_history = db.relationship('ChatHistory', backref='user', lazy=True)

    # Flask-Login properties
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id

    def __repr__(self):
        return f"<User {self.username}>"

class ChatHistory(db.Model):
    __tablename__ = 'chat_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Foreign key linking to User
    chat_content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ChatHistory user_id={self.user_id}, timestamp={self.timestamp}>"

