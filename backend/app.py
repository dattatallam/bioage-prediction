import os, sys, json
from flask import Flask, request, render_template, redirect, session, flash, url_for
from werkzeug.security import generate_password_hash

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from config import SECRET_KEY
from db import q, init_db
from fields import GROUPS, CODES
from ml_model.predictor import predict_age

app = Flask(__name__,
            template_folder=os.path.join(ROOT, "frontend", "templates"),
            static_folder=os.path.join(ROOT, "frontend", "static"))
app.secret_key = SECRET_KEY


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
@app.route("/register")
def auth_redirect():
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/calculator", methods=["GET", "POST"])
def calculator():
    result = None
    if request.method == "POST":
        given = {}
        for code in CODES:
            v = request.form.get(code, "").strip()
            if v:
                given[code] = float(v)

        if "BMI" not in given and "weight" in given and "height" in given:
            given["BMI"] = round(given["weight"] / (given["height"] / 100) ** 2, 1)

        bio = predict_age(given)
        age = request.form.get("chronological_age", "").strip()
        gap = round(bio - float(age), 1) if age else None

        user_id = session.get("uid")
        if user_id is None:
            guest = q("SELECT id FROM users WHERE email=%s", ("guest@local",), one=True)
            if guest:
                user_id = guest["id"]
            else:
                user_id = q("INSERT INTO users (name,email,password_hash) VALUES (%s,%s,%s)",
                            ("Guest", "guest@local", generate_password_hash("guest")), commit=True)
            session["uid"] = user_id
            session["name"] = "Guest"

        q("INSERT INTO predictions (user_id,real_age,predicted_age,age_gap,inputs_filled,inputs) VALUES (%s,%s,%s,%s,%s,%s)",
          (user_id, int(age) if age else None, bio, gap, len(given), json.dumps(given)), commit=True)
        result = dict(bio=bio, gap=gap, age=age, used=len(given))
    return render_template("calculator.html", groups=GROUPS, result=result)

@app.route("/history")
def history():
    user_id = session.get("uid")
    if user_id is None:
        rows = []
    else:
        rows = q("SELECT * FROM predictions WHERE user_id=%s ORDER BY id DESC LIMIT 50", (user_id,))
    return render_template("history.html", rows=rows)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
