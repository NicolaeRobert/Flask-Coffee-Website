from flask import Blueprint, redirect, render_template, url_for, session
from flask_mailman import EmailMessage
from . import mail
import stripe
import os

stripe_implementation=Blueprint('stripe',__name__)

stripe.api_key=os.getenv("SECRET_KEY_STRIPE")
endpoint_secret=os.getenv("ENDPOINT_SECRET")

@stripe_implementation.route('/redirect_to_stripe')
def redirect_to_stripe():
    objects_bought=[]
    for key in session["cart"]:
        if session['cart'][key]!=0:
            env_string=key.upper()
            objects_bought.append(
                {
                    "price": os.getenv(env_string),
                    "quantity": session['cart'][key]
                }
            )

    if len(objects_bought)>0:
        for key in session["cart"]:
            session['cart'][key]=0
        
        checkout=stripe.checkout.Session.create(
            line_items=objects_bought,
            mode="payment",
            success_url=url_for('stripe.success', _external=True),
            cancel_url=url_for('stripe.cancel', _external=True)
        )

        return redirect(checkout.url)
    
    return render_template('cancel_page.html')

@stripe_implementation.route('/success')
def success():
    return render_template('success_page.html')

@stripe_implementation.route('/cancel')
def cancel():
    return render_template('cancel_page.html')

@stripe_implementation.route('/webhook', methods=["POST"])
def webhook():
    pass
