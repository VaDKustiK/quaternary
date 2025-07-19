from flask import Flask, render_template, request
from flask_babel import Babel
from sqlalchemy.orm import Session
from tools.archive_scraper import Issue, init_db

app = Flask(__name__)
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/password_reset")
def password_reset():
    return render_template("password_reset.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Process form data (validate, save user, etc.)
        ...
    return render_template("register.html")

# Navbar
@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/issues')
def archive():
    engine = init_db()
    session = Session(bind=engine)

    issues = session.query(Issue).order_by(Issue.year.desc()).all()

    grouped_issues = {}
    for issue in issues:
        grouped_issues.setdefault(issue.year, []).append(issue)

    return render_template('archive.html', grouped_issues=grouped_issues)

@app.route('/issues/<int:issue_id>')
def issue_detail(issue_id):
    engine = init_db()
    session = Session(bind=engine)

    issue = session.query(Issue).get(issue_id)
    if not issue:
        return "Issue not found", 404

    return render_template('issue_detail.html', issue=issue)


# Sidebar (index page)
@app.route("/submit")
def submit():
    return render_template("submit.html")

if __name__ == '__main__':
    app.run(debug=True)