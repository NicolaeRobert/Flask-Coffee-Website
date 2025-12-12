from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from .utils import are_elements_in_cart

#Create the blueprint for the routes that take care of the buying process
buy_product=Blueprint("buy",__name__)

#The route for buying a dark coffee product
@buy_product.route("/buy_dark_coffee", methods=["POST"])
def buy_dark_coffee():
    #If the user is connected, a product can be bought, and it will be added in the session['cart']
    is_connected="user_id" in session
    if is_connected==True:
        quantity=int(request.form["nr_of_products"])
        session["cart"]["dark_coffee"]+=quantity

        return redirect(url_for('main.products'))
    
    #If the user is not connected we redirect them to the page where they can choose a way to connect or create an account
    flash("You have to be connected in order to buy something","error")
    return redirect(url_for('auth.choose_login_method'))

#The route for changing the number of dark coffee products in the cart
@buy_product.route("/change_dark_coffee", methods=["POST"])
def change_dark_coffee():
    #Get the number that the user wants, change it in the session['cart'] and then redirect back to the page
    quantity=int(request.form["nr_of_products"])
    session["cart"]["dark_coffee"]=quantity

    return redirect(url_for('buy.cart'))

#The route to delete the dark coffee products from the cart
@buy_product.route("/delete_dark_coffee", methods=["POST"])
def delete_dark_coffee():
    #Delete them by setting the quantity of that product to 0, then redirect back to the page
    session["cart"]["dark_coffee"]=0

    return redirect(url_for('buy.cart'))

#The route to buy a nespreso beens product
@buy_product.route("/buy_nespreso_beens", methods=["POST"])
def buy_nespreso_beens():
    #If the user is connected, a product can be bought, and it will be added in the session['cart']
    is_connected="user_id" in session
    if is_connected==True:
        quantity=int(request.form["nr_of_products"])
        session["cart"]["nespreso_beens"]+=quantity

        return redirect(url_for('main.products'))
    
    #If the user is not connected we redirect them to the page where they can choose a way to connect or create an account
    flash("You have to be connected in order to buy something","error")
    return redirect(url_for('auth.choose_login_method'))

#The route to changing the number of nespreso beens products in the cart
@buy_product.route("/change_nespreso_beens", methods=["POST"])
def change_nespreso_beens():
    #Get the number that the user wants, change it in the session['cart'] and then redirect back to the page
    quantity=int(request.form["nr_of_products"])
    session["cart"]["nespreso_beens"]=quantity

    return redirect(url_for('buy.cart'))

#The route for deleting the nespreso beens products from the cart
@buy_product.route("/delete_nespreso_beens", methods=["POST"])
def delete_nespreso_beens():
    #Delete them by setting the quantity of that product to 0, then redirect back to the page
    session["cart"]["nespreso_beens"]=0

    return redirect(url_for('buy.cart'))

#The route to buy a brew product
@buy_product.route("/buy_brew", methods=["POST"])
def buy_brew():
    #If the user is connected, a product can be bought, and it will be added in the session['cart']
    is_connected="user_id" in session
    if is_connected==True:
        quantity=int(request.form["nr_of_products"])
        session["cart"]["brew"]+=quantity

        return redirect(url_for('main.products'))
    
    #If the user is not connected we redirect them to the page where they can choose a way to connect or create an account
    flash("You have to be connected in order to buy something","error")
    return redirect(url_for('auth.choose_login_method'))

#The route to change the number of brew products in the cart
@buy_product.route("/change_brew", methods=["POST"])
def change_brew():
    #Get the number that the user wants, change it in the session['cart'] and then redirect back to the page
    quantity=int(request.form["nr_of_products"])
    session["cart"]["brew"]=quantity

    return redirect(url_for('buy.cart'))

#The route to delete the brew products from the cart
@buy_product.route("/delete_brew", methods=["POST"])
def delete_brew():
    #Delete them by setting the quantity of that product to 0, then redirect back to the page
    session["cart"]["brew"]=0

    return redirect(url_for('buy.cart'))

#The route to buy capsules products
@buy_product.route("/buy_capsules", methods=["POST"])
def buy_capsules():
    #If the user is connected, a product can be bought, and it will be added in the session['cart']
    is_connected="user_id" in session
    if is_connected==True:
        quantity=int(request.form["nr_of_products"])
        session["cart"]["capsules"]+=quantity

        return redirect(url_for('main.products'))
    
    #If the user is not connected we redirect them to the page where they can choose a way to connect or create an account
    flash("You have to be connected in order to buy something","error")
    return redirect(url_for('auth.choose_login_method'))

#The route to change the number of capsules products in the cart
@buy_product.route("/change_capsules", methods=["POST"])
def change_capsules():
    #Get the number that the user wants, change it in the session['cart'] and then redirect back to the page
    quantity=int(request.form["nr_of_products"])
    session["cart"]["capsules"]=quantity

    return redirect(url_for('buy.cart'))

#The route to delete the capsules products in the cart
@buy_product.route("/delete_capsules", methods=["POST"])
def delete_capsules():
    #Delete them by setting the quantity of that product to 0, then redirect back to the page
    session["cart"]["capsules"]=0

    return redirect(url_for('buy.cart'))

#The route that redirects to the cart page
@buy_product.route("/cart")
def cart():
    #Check if there is a session(it means that the user is connected)
    account_show="user_id" in session
    if(account_show==True):
        #Get a bool saying if there are elements in the cart
        is_empty=are_elements_in_cart()
        #Return the cart page with the 2 parameters from above plus the number added in the cart for each product
        return render_template("cart.html", account_show=account_show,is_empty=is_empty,dark_coffee=str(session["cart"]["dark_coffee"]),nespreso_beens=str(session["cart"]["nespreso_beens"]),brew=str(session["cart"]["brew"]),capsules=str(session["cart"]["capsules"]))
    #Return the same page, but transmit only one parameter, that means that the user is not connected
    return render_template("cart.html", account_show=account_show)