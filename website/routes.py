from website import app, db, bcrypt
from flask import render_template, flash, url_for, redirect
from website.forms import RegistrationForm, LoginForm
from website.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required

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
    return render_template("threads.html", threads=threads, title="Threads")


@app.route("/about")
def aboutpage():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def registerpage():
    if current_user.is_authenticated:
        return redirect(url_for("homepage"))
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
    if current_user.is_authenticated:
        return redirect(url_for("homepage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for("homepage"))
        else:
            flash(f"Login Unsuccessful. Please check email or password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logoutpage():
    logout_user()
    return redirect(url_for("homepage"))


@app.route("/account")
@login_required
def accountpage():
    return render_template("account.html", title="Account")


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Post": Post}
