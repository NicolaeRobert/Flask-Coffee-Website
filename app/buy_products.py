from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from .utils import are_elements_in_cart

buy_product=Blueprint("buy",__name__)

@buy_product.route("/buy_dark_coffee", methods=["POST"])
def buy_dark_coffee():
    is_connected="user_id" in session
    if is_connected==True:
        quantity=int(request.form["nr_of_products"])
        session["cart"]["dark_coffee"]+=quantity

        return redirect(url_for('main.products'))
    
    flash("You have to be connected in order to buy something","error")
    return redirect(url_for('auth.choose_login_method'))

@buy_product.route("/change_dark_coffee", methods=["POST"])
def change_dark_coffee():
    quantity=int(request.form["nr_of_products"])
    session["cart"]["dark_coffee"]=quantity

    return redirect(url_for('buy.cart'))

@buy_product.route("/delete_dark_coffee", methods=["POST"])
def delete_dark_coffee():
    session["cart"]["dark_coffee"]=0

    return redirect(url_for('buy.cart'))

@buy_product.route("/buy_nespreso_beens", methods=["POST"])
def buy_nespreso_beens():
    is_connected="user_id" in session
    if is_connected==True:
        quantity=int(request.form["nr_of_products"])
        session["cart"]["nespreso_beens"]+=quantity

        return redirect(url_for('main.products'))
    
    flash("You have to be connected in order to buy something","error")
    return redirect(url_for('auth.choose_login_method'))

@buy_product.route("/change_nespreso_beens", methods=["POST"])
def change_nespreso_beens():
    quantity=int(request.form["nr_of_products"])
    session["cart"]["nespreso_beens"]=quantity

    return redirect(url_for('buy.cart'))

@buy_product.route("/delete_nespreso_beens", methods=["POST"])
def delete_nespreso_beens():
    session["cart"]["nespreso_beens"]=0

    return redirect(url_for('buy.cart'))

@buy_product.route("/buy_brew", methods=["POST"])
def buy_brew():
    is_connected="user_id" in session
    if is_connected==True:
        quantity=int(request.form["nr_of_products"])
        session["cart"]["brew"]+=quantity

        return redirect(url_for('main.products'))
    
    flash("You have to be connected in order to buy something","error")
    return redirect(url_for('auth.choose_login_method'))

@buy_product.route("/change_brew", methods=["POST"])
def change_brew():
    quantity=int(request.form["nr_of_products"])
    session["cart"]["brew"]=quantity

    return redirect(url_for('buy.cart'))

@buy_product.route("/delete_brew", methods=["POST"])
def delete_brew():
    session["cart"]["brew"]=0

    return redirect(url_for('buy.cart'))

@buy_product.route("/buy_capsules", methods=["POST"])
def buy_capsules():
    is_connected="user_id" in session
    if is_connected==True:
        quantity=int(request.form["nr_of_products"])
        session["cart"]["capsules"]+=quantity

        return redirect(url_for('main.products'))
    
    flash("You have to be connected in order to buy something","error")
    return redirect(url_for('auth.choose_login_method'))

@buy_product.route("/change_capsules", methods=["POST"])
def change_capsules():
    quantity=int(request.form["nr_of_products"])
    session["cart"]["capsules"]=quantity

    return redirect(url_for('buy.cart'))

@buy_product.route("/delete_capsules", methods=["POST"])
def delete_capsules():
    session["cart"]["capsules"]=0

    return redirect(url_for('buy.cart'))

@buy_product.route("/cart")
def cart():
    account_show="user_id" in session
    if(account_show==True):
        is_empty=are_elements_in_cart()
        return render_template("cart.html", account_show=account_show,is_empty=is_empty,dark_coffee=str(session["cart"]["dark_coffee"]),nespreso_beens=str(session["cart"]["nespreso_beens"]),brew=str(session["cart"]["brew"]),capsules=str(session["cart"]["capsules"]))
    return render_template("cart.html", account_show=account_show)