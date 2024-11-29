from flask import Flask, render_template, request
from prototype import *
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        date = request.form["date"]
        time = request.form["time"]
        time = str(date)+"-"+str(time)
        email = request.form["email"]
        booking = add_booking(time, email)
        return render_template("book.html", booking=booking)
    return render_template("book.html", booking=None)

@app.route("/my_bookings", methods=["GET", "POST"])
def my_bookings():
    if request.method == "POST":
        email = request.form["email"]
        bookings = show_my_bookings(email)
        return render_template("my_bookings.html", bookings=bookings)
    return render_template("my_bookings.html", bookings=None)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/show_all_bookings", methods=["GET"])
def display_bookings():
    bookings = show_all_bookings()  # Anta att denna funktion returnerar data snarare än att printa direkt
    return render_template("show_all_bookings.html", bookings=bookings)

if __name__ == "__main__":
    app.run(debug=True)

