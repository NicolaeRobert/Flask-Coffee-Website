from flask import session, g
from argon2 import PasswordHasher
import mysql.connector
import os

#Here we will have all the neccesary funtions for the app

#Here we check if the password is correct or not
def check_pass(p1,p2):
    #We create an object of the PasswordHasher class in order to hash the password
    ph=PasswordHasher()

    try:
        return ph.verify(p1,p2)
    except:
        return False
    
#Here is the two fuctions we gives the connection and the cursor to the database
def get_connection():
    if not hasattr(g,'conn'):
        g.conn=mysql.connector.connect(
            host='localhost',
            user='root',
            password=os.getenv("DB_PASS"),
            database='coffee_shop'
        )
    return g.conn

def get_cursor():
    conn=get_connection()
    return conn.cursor()

#Here we define the function that will close the connection to the database
def close_connections(exception):
    conn=g.pop('conn',None)
    if conn is not None:
        conn.close()


#Here we create the session
def create_session(username, id):
    session.permanent=True
    session["user_id"]=id
    session["username"]=username
