from flask import Flask,render_template

app = Flask(__name__)

@app.route("/")  # Вказуємо url-адресу для виклику функції
def index():
    return render_template("home.html")     


if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()