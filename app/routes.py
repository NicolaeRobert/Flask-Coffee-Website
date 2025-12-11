from flask import Blueprint, session, render_template, request, flash
from .utils import get_cursor,get_connection,get_orders
from argon2 import PasswordHasher

#Here we create the instance od the blueprint called main 
main=Blueprint('main',__name__)

#We create an object of the PasswordHasher class in order to hash the password
ph=PasswordHasher()

#The route of the home page
@main.route('/')
def home():
    logged="user_id" in session
    return render_template("home.html", account_show=logged)

#The route of the about us page
@main.route('/about_us')
def about_us():
    logged="user_id" in session
    return render_template("about_us.html", account_show=logged)

#The route of the product page
@main.route('/products')
def products():
    logged="user_id" in session

    mycursor=get_cursor()

    mycursor.execute('SELECT stock FROM products')
    dark_coffee,nespreso_beens,brew,capsules=mycursor.fetchall()

    print(dark_coffee,nespreso_beens,brew,capsules)

    mycursor.close()

    return render_template("products.html", account_show=logged, dark_coffee=dark_coffee[0], nespreso_beens=nespreso_beens[0], brew=brew[0], capsules=capsules[0])

#The route of the user page
@main.route('/user_page',methods=["GET","POST"])
def user_page():
    #The two cases, when we have a get request or a post request
    if request.method=='GET':
        #Here I treat the case in witch the user is not connected and tries to enter the user page through the url
        if session:
            #Get the data about orders from the database
            orders_data=get_orders()

            return render_template("user_page.html",username=session['username'],orders=orders_data)
        else:
            flash("You must be connected to enter the user page","error")
            return render_template("login.html")
    elif request.method=='POST':
        #Get the connection, the cursor to make queries to the database and get the id from the session
        conn=get_connection()
        mycursour=get_cursor()
        id=session['user_id']
        #Check to see from what form we came and make the changes accordingly
        if 'new_username' in request.form:
            #Here we change the username in the database, commit the connection(commit the changes), end the cursor then return a comfirmation page

            new_username=request.form['new_username']
            mycursour.execute('UPDATE USERS SET username=%s WHERE id=%s',(new_username,id))

            conn.commit()
            mycursour.close()

            session['username']=new_username

            return render_template("comfirmation_for_user_page.html",message='username')
        
        elif 'new_password' in request.form:
            #Here we change the password in the database, commit the connection(commit the changes), end the cursor then return a comfirmation page

            new_password=ph.hash(request.form['new_password'])
            mycursour.execute('UPDATE USERS SET password=%s WHERE id=%s',(new_password,id))

            conn.commit()
            mycursour.close()

            return render_template("comfirmation_for_user_page.html",message='password')
