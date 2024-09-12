from app import db, datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False, unique=False)
    dp = db.Column(db.String(50), nullable=False, unique=False, default="default.jpg")

    def __repr__(self):
        return f"User({self.username!r}, {self.email!r}, {self.dp!r})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=False)
    content = db.Column(db.String(1000), nullable=False, unique=False)
    date = db.Column(db.DateTime, nullable=False, unique=False, default=datetime.utcnow)

    def __repr__(self):
        return f"Post(title={self.title}, date={self.date})"
