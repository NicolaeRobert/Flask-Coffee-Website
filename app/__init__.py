from flask import Flask
from datetime import timedelta
from flask_mailman import Mail
from dotenv import load_dotenv
import os
from .utils import close_connections

load_dotenv()

mail=Mail()

def create_app():

    #We create the instance of the app(called app), add a secret key for the session and set a lifetime for the session
    app=Flask(__name__)
    app.secret_key=os.getenv("APP_SECRET_KEY")
    app.permanent_session_lifetime=timedelta(minutes=30)

    #We configure the app for sending the email(SMTP server, the port, the sender's email, the password, the encription and the default sender)
    app.config["MAIL_SERVER"]="smtp.gmail.com"
    app.config["MAIL_PORT"]=465
    app.config["MAIL_USERNAME"]=os.getenv("EMAIL")
    app.config["MAIL_PASSWORD"]=os.getenv("MAIL_PASSWORD")
    app.config["MAIL_USE_TLS"]=False
    app.config["MAIL_USE_SSL"]=True
    app.config["MAIL_DEFAULT_SENDER"]=os.getenv("EMAIL")

    #We configure the mail instance so that we can use it in the other blueprints
    mail.init_app(app)

    #Here we register the blueprint called main
    from .routes import main
    app.register_blueprint(main)

    #Here we register the blueprint called auth
    from .auth import auth_var
    app.register_blueprint(auth_var)

    #Here we register the bluprint for google connection
    from .google_auth import auth_with_google
    app.register_blueprint(auth_with_google)

    #Here we register the blueprint for the password change with email
    from .change_password_with_email import pass_change
    app.register_blueprint(pass_change)

    #Here we register the blueprint for the part that takes care of the buying process
    from .buy_products import buy_product
    app.register_blueprint(buy_product)

    #Here I set the close_connection function to automatically execute at the end of every request to end the connection to the database
    app.teardown_appcontext(close_connections)

    #Here the object of the app is being returned
    return app