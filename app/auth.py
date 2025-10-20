from flask import Blueprint, session, redirect, url_for, render_template, request, flash
from argon2 import PasswordHasher
from flask_mailman import EmailMessage
from .utils import get_connection, get_cursor, create_session,check_pass
from . import mail

#Here we create the instance of the blueprint called auth
auth_var=Blueprint('auth',__name__)

#We create an object of the PasswordHasher class in order to hash the password
ph=PasswordHasher()

#The root of the register page(here we accept both get and post method)
@auth_var.route('/register', methods=["GET", "POST"])
def register():
    #If the method is get we simply render the page, else we create the message, add the account, create the session and send the email. Then we return a confirmation page.
    if request.method=="GET":
        return render_template("register.html")
    elif request.method=="POST":

        #The input
        username=request.form['username']
        email=request.form['email']
        password=request.form["password"]

        #The hassed password
        hashed_password=ph.hash(password)

        #The connection and the cursor to the database

        conn=get_connection()
        mycursor=get_cursor()

        #Here we check if you already have an account with this email and if we have we redirect to the login page and flash a message
        mycursor.execute('SELECT id FROM USERS WHERE email=%s',(email,))
        result=mycursor.fetchone()
        if result is not None:
            flash('You already have an account. Log in here.', "error")
            return redirect(url_for('auth.login'))

        #Here we register the user and send an email of confirmation

        #The message
        account_created_message=EmailMessage(
            subject="Nesso: account created",
            body="Congratulations! Your account has been created succesfully.",
            from_email="programminguse985@gmail.com",
            to=[request.form['email']],
            reply_to=["programminguse985@gmail.com"]
        )

        
        #The user is added into the database
        mycursor.execute(
            'INSERT INTO USERS (username,email,password) VALUES (%s,%s,%s)',
            (username,email,hashed_password)
        )
        conn.commit()
        
        #The session is created here
        mycursor.execute('SELECT id FROM USERS WHERE email=%s',(email,))
        id=mycursor.fetchone()
        create_session(username,id[0])

        #The email of comfirmation is sent here
        account_created_message.send()

        #Close the current cursor
        mycursor.close()

        return redirect(url_for("auth.confirmation"))


#The login root. Here we also accept both get and post methods
@auth_var.route('/login', methods=["GET", "POST"])
def login():
    #If the method is get we render the login page, else we create a session if the account is valid and if it's not we show a flash message and redirect to the register page in order for an account to be created.
    if request.method=="GET":
        return render_template("login.html")
    elif request.method=="POST":

        #The input necessary for the connection
        email=request.form["email"]
        password=request.form["password"]

        #Database connection and cursor
        conn=get_connection()
        mycursor=get_cursor()

        mycursor.execute('SELECT password FROM USERS WHERE email=%s',(email,))
        result=mycursor.fetchone()
        if result is None:
            mycursor.close()
            flash("You don't have an account! Create one here.",'error')
            return redirect(url_for('auth.register'))
        
        if check_pass(result[0],password):
            mycursor.execute('SELECT username,id FROM USERS WHERE email=%s',(email,))
            result=mycursor.fetchone()
            mycursor.close()
            create_session(result[0],result[1])
            return redirect(url_for('main.home'))
        else:
            mycursor.close()
            flash("Wrong password! Try connecting again.",'error')
            return redirect(url_for('auth.login'))


#We log out the person by crearing the session and redirect them to the home page
@auth_var.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))

#The confirmation page used in the register page when the account has been successfully created
@auth_var.route('/confirmation')
def confirmation():
    return render_template("confirmation_registration.html")
