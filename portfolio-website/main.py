from flask import Flask, render_template,request
import requests
import smtplib

my_email = "appbrewerytester781@gmail.com"
password = "vdnw aanr iptr adzi"

posts = requests.get("https://api.npoint.io/674f5423f73deab1e9a7").json()
app = Flask(__name__)

@app.route('/')
def get_all_posts():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("../../Portfolio/Portfolio-Website/templates/about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # Encrypts the connection
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs="appbrewerytester781@yahoo.com",
                msg=f"Subject:Hello\n\n"
                    f"Name: {data['name']}\n"
                    f"Email: {data['email']}\n"
                    f"Phone: {data['phone']}\n"
                    f"Message: {data['message']}"
            )
            print("Email sent!")

        return render_template("../../Portfolio/Portfolio-Website/templates/contact.html", successful=True)
    return render_template("../../Portfolio/Portfolio-Website/templates/contact.html", successful=False)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("../../Portfolio/Portfolio-Website/templates/post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)