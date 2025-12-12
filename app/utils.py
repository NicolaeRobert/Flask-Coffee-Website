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
    session["cart"]={
        "dark_coffee": 0,
        "nespreso_beens": 0,
        "brew": 0,
        "capsules": 0
    }

#Returns true if there is any element in the cart, or false otherwise
def are_elements_in_cart():
    for key in session["cart"]:
        if session["cart"][key]!=0:
            return True
    return False

#Here we get all the orders that a user has done and order them in a useful way for working with them
def get_orders():
    #Here I get the connection and the cursor for executing queries to the database
    conn=get_connection()
    mycursor=get_cursor()

    #Here I check how may orders does the user have
    mycursor.execute('SELECT COUNT(*) FROM ORDERS WHERE id_user=%s',(session['user_id'],))
    nr_of_orders=mycursor.fetchone()
    nr_of_orders=nr_of_orders[0]#To keep the value of the tuple

    #Check if there are any orders, else return an empty dictionary
    if nr_of_orders==0:
        return {}

    #Here I execute the query and bring all the orders of the user from the database to the code
    mycursor.execute('''
    SELECT id_order,date,delivered,total,id_prod,quantity FROM ORDERS
    INNER JOIN ITEMS_ORDER ON ORDERS.ID=ITEMS_ORDER.ID_ORDER
    WHERE ORDERS.id_user=%s
    ORDER BY ORDERS.ID DESC
    ''',(session['user_id'],))
    result=mycursor.fetchall()

    mycursor.close()

    #Here I set the data brought from the database in a better format
    dictionary={}
    dictionary[nr_of_orders]=[]
    dictionary[nr_of_orders].append(result[0])

    for data in result[1:]:
        if dictionary[nr_of_orders][0][0]==data[0]:
            dictionary[nr_of_orders].append(data)
        else:
            nr_of_orders-=1
            dictionary[nr_of_orders]=[]
            dictionary[nr_of_orders].append(data)

    #Return the data in a format of dictionary{nr_of_order:[(info_item1),(info_intem2),...],...}
    return dictionary

#This funtion deletes payment success/failed webhooks older that 7 days
def delete_old_webhooks(witch_one):
    # !!! IMPORTANT !!! If witch_one is true we delete the ones from payment success table, if it is false delete the one from payment failed 

    #Get the connection and the cursor
    conn=get_connection()
    mycursor=get_cursor()


    if witch_one==True:
        #Make the deletion process for the payment success
        mycursor.execute(
            "DELETE FROM webhook_success WHERE session_date < DATE_SUB(NOW(), INTERVAL 7 DAY)"
        )
    else:
        #Make the deletion process for the payment failed
        mycursor.execute(
            "DELETE FROM webhook_fail WHERE session_date < DATE_SUB(NOW(), INTERVAL 7 DAY)"
        )

    #Commit the connection and close the cursor
    conn.commit()
    mycursor.close()