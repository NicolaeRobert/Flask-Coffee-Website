from flask import Blueprint, request, render_template, flash, url_for, jsonify
from .utils import get_cursor, get_connection
from datetime import datetime,timedelta
from flask_mailman import EmailMessage
from argon2 import PasswordHasher
from . import mail
import jwt
import os

#Initialize the password hasher object
ph=PasswordHasher()

#Create the bluprint
pass_change=Blueprint("pass",__name__)

#The route where the user sends the email and is being sent a message with the url that contains a token that gives him acces to that page
@pass_change.route('/redirect_and_token_creation',methods=["GET","POST"])
def redirect_and_token_creation():
    #If the request is get we simply allow him to send as an email that represents his account
    if request.method=="GET":
        return render_template("get_email.html")
    #If the request is post we check the email, create a JWT and send the url where he can change the password
    elif request.method=="POST":
        #Get the email from the form
        email=request.form['email']

        #Get the cursor that allows as to perform queries to the database
        mycursor=get_cursor()
        mycursor.execute("SELECT id FROM users WHERE email=%s", (email,))

        #Here we get the id of the user and close the connection
        id=mycursor.fetchone()
        mycursor.close()

        #If the user has no id, it means that he/she doesn't exists, case in with we announce them
        if id==None:
            flash("There is no accout with this email! Go to register to create one or introduce a valid email.","error")
            return render_template("get_email.html")
        
        #Create the payload that represents the info in the JWT, and then create the JWT itself
        payload={
            "sub":str(id),
            "email":email,
            "exp":datetime.now()+timedelta(minutes=5)
        }
        token=jwt.encode(payload,os.getenv('SECRET'),algorithm='HS256')

        #The url that we send to the user
        url_for_email_message="http://127.0.0.1:5000/"+url_for('pass.change_password_with_email',token=token)

        #The body of the email
        body=f"""
        You're receiving this e-mail because you or someone else has requested a password reset for your user account at .

        Click the link below to reset your password:
        {url_for_email_message}

        If you did not request a password reset you can safely ignore this email.
        """

        #The email is being created here
        email_message=EmailMessage(
            subject="Change password Nesso account",
            body=body,
            from_email='u1447448204@gmail.com',
            to=[email],
            reply_to=['u1447448204@gmail.com']
        )

        #We send the email
        email_message.send()

        #Return a confirmation to the user that everything went great and the email has been sent
        return render_template("comfirmation_password_change_with_email.html",message="The email has been sent. You have 5 minutes to change the password.")


#The route for the url that we send in the email
@pass_change.route('/change_password_with_email',methods=["GET","POST"])
def change_password_with_email():
    #If the method is GET check the authenticity of the token. If it is the one that we sent and it isn't expired allow the unser to acces it, otherwise don't
    if request.method=="GET":
        token=request.args["token"]
        try:
            payload=jwt.decode(token,os.getenv("SECRET"),"HS256")
            return render_template("change_password_with_email.html",token=token)
        except jwt.ExpiredSignatureError:
            return render_template("comfirmation_password_change_with_email.html",message="The time allowed to change the password has expired. Please retake the process.")
        except jwt.InvalidTokenError:
            return render_template("comfirmation_password_change_with_email.html",message="The token is not valid.")
    #If the method is POST check the autenticity of the token, and do the rest of the thing explained below
    elif request.method=="POST":

        #Here we take the token from the url and check it's autenticity and expiery date
        token=request.args["token"]
        try:
            payload=jwt.decode(token,os.getenv("SECRET"),"HS256")
        except jwt.ExpiredSignatureError:
            return render_template("comfirmation_password_change_with_email.html",message="The time allowed to change the password has expired. Please retake the process.")
        except jwt.InvalidTokenError:
            return render_template("comfirmation_password_change_with_email.html",message="The token is not valid.")
        
        #Here we hash the password given by the user
        password=ph.hash(request.form["new_password"])

        #Get the connection and the cursor for the database access
        conn=get_connection()
        mycursor=get_cursor()

        #Change the password in the database
        mycursor.execute(
            "UPDATE users SET password=%s WHERE email=%s",
            (password,payload['email'])
        )
        
        #Commit the connection for the changes to be permanent and close the cursor
        conn.commit()
        mycursor.close()
        
        #Return a confirmation message that everything went great
        return render_template("comfirmation_password_change_with_email.html",message="The password has been changed seccessfully.")
    