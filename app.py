from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from datetime import datetime
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config["SECRET_KEY"] = "d02d98260b25375be94169e74c9751a8"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired(), Length(3, 20)])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(3, 30)])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Account with your email already exists")


class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(3, 30)])
    remember = BooleanField("Remember Me!")
    submit = SubmitField("Login")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    user_image = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User(username={self.username!r}, email={self.email!r}, dp={self.user_image!r})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post(title={self.title!r}, date={self.date_posted!r})"


# dummy data that will be posted into threadspage
threads = [
    {
        "author": "Ali Habib",
        "title": "Blog 1",
        "date_added": "13th August, 2024",
        "content": "This is the 1st blog",
    },
    {
        "author": "Maryam Hayat",
        "title": "Blog 2",
        "date_added": "14th August, 2024",
        "content": "This is the 2nd blog",
    },
    {
        "author": "Abdullah Khan",
        "title": "Blog 3",
        "date_added": "16th August, 2024",
        "content": "This is the 3rd blog",
    },
    {
        "author": "xyz 123",
        "title": "Blog 4",
        "date_added": "16th August, 2024",
        "content": "This is the 4th blog",
    },
]


@app.route("/")
@app.route("/home")
def homepage():
    return render_template("home.html", title="Home")


@app.route("/threads")
def threadspage():
    return render_template("threads.html", threads=threads, title="Threads")


@app.route("/about")
def aboutpage():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def registerpage():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash(f"Account created, you can now log in", "success")
        return redirect(url_for("loginpage"))
    return render_template("register.html", title="Registration", form=form)


@app.route("/login", methods=["GET", "POST"])
def loginpage():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@gmail.com" and form.password.data == "password":
            flash(f"Login Successful", "success")
            return redirect(url_for("threadspage"))
        else:
            flash(f"Login Unsuccessful, please check email or password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post}


if __name__ == "__main__":
    app.run(debug=True)
