"""
Job Application Submission Project.
Author : Sharvari D 17-01-2026 Developed Script

"""
from datetime import datetime
from flask import Flask, render_template, request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail,Message
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
#dkuv ntug bjlm ygqj


app = Flask(__name__)

app.config["SECRET_KEY"] = "myapplication123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = "sharvari0823@gmail.com"
app.config["MAIL_PASSWORD"] = "dkuvntugbjlmygqj"

mail = Mail(app)
db = SQLAlchemy(app)

class Form(db.Model):
    """
    Create Table Form in SQLALCHEMY
    """
    id = db.Column(db.Integer,primary_key = True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(100))

@app.route("/",methods = ["GET","POST"])
def index():
    """
    Handle Form Request For Get and post method
    :return: Message in case of post
    """
    if request.method == "POST":
        logger.info(f"{request.method}")
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date = request.form["date"]
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        occupation = request.form["occupation"]

        form = Form(first_name = first_name, last_name = last_name, email = email,date = date_obj , occupation = occupation)
        db.session.add(form)
        db.session.commit()
        logger.info("inserted into db", first_name)

        flash(f"{first_name}, Form is submitted successfully","success")

        message_body = f"Thank You {first_name}!\n Your application has been saved successfully"
        message = Message(subject="Application Submission", sender=app.config["MAIL_USERNAME"], recipients= [email], body = message_body)
        mail.send(message)
        logger.info(f"mail sent successfully on {email}")


    return render_template("index.html")

if __name__ == "__main__":
    logger.info("Script Started")
    with app.app_context():
        db.create_all()

    app.run(debug=True)

