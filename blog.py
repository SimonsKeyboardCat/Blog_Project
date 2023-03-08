from flask import Flask, url_for, request
from flask import render_template
import requests
import smtplib


my_email = "YOUR_EMAIL@gmail.com"
my_password = "YOUR_PASSWORD"

app = Flask(__name__)

url = "https://api.npoint.io/139b49f33729ed6e6cd8"
response = requests.get(url)
posts = response.json()
print(posts)


@app.route("/")
def index():
    return render_template('index.html', name="home", all_posts=posts)


@app.route("/home")
def home():
    return render_template('index.html', name="home", all_posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', name="about")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(my_email, my_password)
        connection.sendmail(my_password, my_email, email_message)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)
