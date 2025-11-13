from flask import Blueprint, redirect, render_template, session, request, url_for
from google_auth_oauthlib.flow import Flow
from .utils import get_connection, get_cursor, create_session
from flask_mailman import EmailMessage
from . import mail
import os
import requests

#Here I create the blueprint for the google oauth2 connection
auth_with_google=Blueprint('auth_g',__name__)

#The configuration taken from the google console
client_config={
    "web":
        {"client_id":os.getenv("CLIENT_ID"),#The client id that is stored in the .env file and loaded as an environment variable
         "project_id":"coffee-shop-flask",
         "auth_uri":"https://accounts.google.com/o/oauth2/auth",
         "token_uri":"https://oauth2.googleapis.com/token",
         "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
         "client_secret":os.getenv("CLIENT_SECRET"),#The client secret that is stored in the .env file and loaded as an environment variable
         "redirect_uris":["http://127.0.0.1:5000/callback"]
         }
}

#The route that redirects to the google page for the user to connect
@auth_with_google.route("/redirect_to_google")
def redirect_to_google():
    #The flow object that does allmost all the things in the OAuth2 process to connect with google
    #Here we create it and specify the info from the console, the info that we want to get and where to send the code
    flow=Flow.from_client_config(
        client_config=client_config,
        scopes=["openid","https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/userinfo.profile"],
        redirect_uri='http://127.0.0.1:5000/callback'
    )
    
    #The authorization url for the google page and a parameter called state to prevent others from faking the callback from google
    #We temporarely store the state in the session to use it for verification later
    authorization_url,state=flow.authorization_url()
    session["state"]=state

    #Send the user to the google page to authentificate
    return redirect(authorization_url)

#The callback route, where google send the code
@auth_with_google.route("/callback")
def callback():
    #Recreate the flow object and give it the state parameter for the authomatic verification
    flow=Flow.from_client_config(
        client_config=client_config,
        scopes=["openid","https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/userinfo.profile"],
        redirect_uri='http://127.0.0.1:5000/callback',
        state=session["state"]
    )

    #Fetch the tokens
    flow.fetch_token(authorization_response=request.url)
    
    #Getting the tokens received via the credentials object
    credentials=flow.credentials
    token=credentials.token

    #Make a get request to the google userifo endpoint and get the basic info about the user
    user_info=requests.get(
        "https://openidconnect.googleapis.com/v1/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    ).json()

    #Delete the state parameter from the session
    session.pop('state',None)

    #Get the cpnnection and the cursor to the database
    conn=get_connection()
    mycursor=get_cursor()

    #Make a query to see if the user authentificated by google already has an account
    mycursor.execute(
        "SELECT username,id FROM users WHERE email=%s",
        (user_info["email"],)
    )

    #Get the results of the query
    results=mycursor.fetchone()

    #Here we treat the case where the user doesn't have an account, case in witch we create one for it
    if results==None:
        #Insert the user in the database, get the info for the session and commit the connection to the database for the changes to be permanent
        mycursor.execute(
            "INSERT INTO users (username,email,created_with) VALUES (%s,%s,%s)",(user_info["name"],user_info["email"],'google')
        )

        mycursor.execute(
            "SELECT username,id FROM users WHERE email=%s",
            (user_info["email"],)
        )

        results=mycursor.fetchone()
        conn.commit()

        #Create the message and use the mail object imported from the __init__ file to send
        account_created_message=EmailMessage(
            subject='Nesso: account created',
            body='Congratulations! Your account has been created succesfully.',
            from_email='u1447448204@gmail.com',
            to=[user_info['email']],
            reply_to=['u1447448204@gmail.com']
        )

        account_created_message.send()


    #Create the session and close the cursor
    create_session(results[0],results[1])
    mycursor.close()

    #Redirect to the home page, once the user is authenticated
    return redirect(url_for('main.home'))

