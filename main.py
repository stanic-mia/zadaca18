# guess the secret number - baze vježba

from flask import Flask, render_template, request, make_response, redirect, url_for
import random
from models import User, db

app = Flask(__name__)
# kreiranje tablice u bazi
db.create_all()

@app.route("/", methods=["GET"])
def index():
    email = request.cookies.get("email")

    if email:
        user = db.query(User).filter_by(email=email).first()
    else:
        user = None

    return render_template("index.html", user=user)

@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    number = random.randint(1, 30)

    user = db.query(User).filter_by(email=email).first()

    if not user:
        user = User(name=name, email=email, number=number)
        db.add(user)
        db.commit()

    response = make_response(redirect(url_for("index")))
    response.set_cookie("email", email)

    return response

@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))

    email = request.cookies.get("email")

    user = db.query(User).filter_by(email=email).first()

    if guess == user.number:
        message = "Correst! The secret number is {0}".format(str(guess))

        new_number = random.randint(1, 30)
        user.number = new_number
        db.add(user)
        db.commit()

    elif guess > user.number:
        message = "Try something smaller."
    elif guess < user.number:
        message = "Try something bigger."

    return render_template("result.html", message=message)

if __name__ == "__main__":
    app.run()