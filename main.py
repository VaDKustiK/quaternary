from flask import Flask, render_template, request
from flask_babel import Babel

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

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Process form data (validate, save user, etc.)
        ...
    return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Sidebar (index page)
@app.route("/submit")
def submit():
    return render_template("submit.html")

if __name__ == '__main__':
    app.run(debug=True)