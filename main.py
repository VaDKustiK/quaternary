import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_babel import Babel
from sqlalchemy.orm import Session
from tools.models.init_db import engine, SessionLocal, init_db
from tools.models.issue import Issue
from werkzeug.security import generate_password_hash
from tools.models.user import User
from dotenv import load_dotenv
from flask import session
from werkzeug.security import check_password_hash
from functools import wraps
from datetime import datetime, timezone, timedelta

app = Flask(__name__)

load_dotenv()
app.secret_key = os.getenv("SECRET_KEY")

# Configuration for Babel (i18n)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ru']

babel = Babel()

def get_locale():
    lang = request.args.get('lang')
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        return lang
    return request.accept_languages.best_match(app.config['BABEL_SUPPORTED_LOCALES'])


babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_locale():
    return {'get_locale': get_locale}


init_db()  # creating tables once before running the app

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("You need to log in", "warning")
            return redirect(url_for("index"))
        db = SessionLocal()
        user = db.query(User).get(session["user_id"])
        if not user or not user.is_admin:
            flash("Access denied", "danger")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    session = SessionLocal()
    latest_issue = session.query(Issue).order_by(Issue.year.desc(), Issue.id.desc()).first()
    return render_template('index.html', latest_issue=latest_issue)


@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]
    session_db = SessionLocal()
    user = session_db.query(User).filter_by(email=email).first()

    if user and check_password_hash(user.password_hash, password):
        session["user_id"] = user.id
        session["user_name"] = user.name
        session["is_admin"] = user.is_admin
        flash("Successfully logged in!", "success")

        return redirect(request.referrer or url_for("index"))
    else:
        flash("Invalid email or password", "danger")
        return redirect(request.referrer or url_for("index"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "success")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if password != confirm_password:
            flash("Passwords do not match", "danger")
            return render_template("register.html")

        session = SessionLocal()
        existing_user = session.query(User).filter_by(email=email).first()
        if existing_user:
            flash("Email already registered", "danger")
            return render_template("register.html")

        user = User(
            name=name,
            surname=surname,
            email=email,
            password_hash=generate_password_hash(password)
        )

        session.add(user)
        session.commit()
        flash("Account created successfully! You can now log in.", "success")
        return redirect(url_for("index"))

    return render_template("register.html")


@app.route("/password_reset")
def password_reset():
    return render_template("password_reset.html")


@app.route("/profile")
def profile():
    return render_template("profile.html")


# Navbar
@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/issues')
def archive():
    session = SessionLocal()
    issues = session.query(Issue).order_by(Issue.year.desc()).all()

    grouped_issues = {}
    for issue in issues:
        grouped_issues.setdefault(issue.year, []).append(issue)

    return render_template('archive.html', grouped_issues=grouped_issues)


@app.route('/issues/<int:issue_id>')
def issue_detail(issue_id):
    session = SessionLocal()
    issue = session.query(Issue).get(issue_id)
    if not issue:
        return "Issue not found", 404

    return render_template('issue_detail.html', issue=issue)


# Sidebar (index page)
@app.route("/submit")
def submit():
    return render_template("submit.html")


# Admin panel
@app.route("/admin")
@admin_required
def admin_panel():
    return render_template("admin/admin_panel.html")


@app.before_request
def update_last_seen():
    if "user_id" in session:
        db = SessionLocal()
        user = db.query(User).get(session["user_id"])
        if user:
            user.last_seen = datetime.now(timezone.utc)
            db.commit()


@app.route("/admin/online")
@admin_required
def iframe_online():
    db = SessionLocal()
    active_threshold = datetime.now(timezone.utc) - timedelta(minutes=5)
    active_users = db.query(User).filter(User.last_seen >= active_threshold).count()
    return render_template("admin/online.html", active_users=active_users)


@app.route("/admin/users")
@admin_required
def admin_users():
    q = request.args.get("q", "")
    filter_admin = request.args.get("filter_admin")
    sort = request.args.get("sort", "newest")
    db = SessionLocal()
    query = db.query(User)

    if q:
        query = query.filter(
            (User.name.ilike(f"%{q}%")) |
            (User.surname.ilike(f"%{q}%")) |
            (User.email.ilike(f"%{q}%"))
        )

    if filter_admin == "true":
        query = query.filter(User.is_admin == True)
    elif filter_admin == "false":
        query = query.filter(User.is_admin == False)

    if sort == "oldest":
        query = query.order_by(User.created_at.asc())
    else:
        query = query.order_by(User.created_at.desc())

    users = query.all()
    return render_template("admin/users.html", users=users, q=q, filter_admin=filter_admin, sort=sort)


@app.route("/admin/issues")
@admin_required
def admin_issues():
    db = SessionLocal()
    issues = db.query(Issue).order_by(Issue.year.desc()).all()
    return render_template("admin/issues.html", issues=issues)


if __name__ == '__main__':
    app.run(debug=True)