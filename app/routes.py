from flask import Blueprint, session, render_template

#Here we create the instance od the blueprint called main 
main=Blueprint('main',__name__)

#The roots of the home page
@main.route('/')
def home():
    logged="user_id" in session
    return render_template("home.html", account_show=logged)

#The root of the about us page
@main.route('/about_us')
def about_us():
    return render_template("about_us.html")

#The root of the product page
@main.route('/products')
def products():
    return render_template("products.html")
