from flask import Blueprint, redirect, render_template, url_for, session, request
from .utils import get_connection, get_cursor, delete_old_webhooks
from flask_mailman import EmailMessage
from . import mail
import stripe
import os
from pprint import pprint

stripe_implementation=Blueprint('stripe',__name__)

stripe.api_key=os.getenv("SECRET_KEY_STRIPE")

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

@stripe_implementation.route("/webhook_payment_failed", methods=["POST"])
def webhook_failed():
    
    delete_old_webhooks(False)

    body=request.data
    stripe_signature=request.headers.get('Stripe-Signature')

    endpoint_secret=os.getenv("ENDPOINT_SECRET_FAIL")

    try:
        event=stripe.Webhook.construct_event(
            body,
            stripe_signature,
            endpoint_secret
        )
    except ValueError:
        return 'Invalid payload',400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature',400
    
    conn=get_connection()
    mycursor=get_cursor()

    mycursor.execute(
        "SELECT id FROM webhook_fail WHERE id=%s",
        (event['id'],)
    )

    id=mycursor.fetchone()

    if id==None and event['type']=="payment_intent.payment_failed":
        
        mycursor.execute(
            'INSERT INTO webhook_fail (id,email) VALUES (%s,%s)',
            (event['id'],event['receipt_email'])
        )

        conn.commit()

        message_for_payment_failure=EmailMessage(
            subject="Nesso - Payment Failed",
            body="""
                The payment process failed. Try again!
                In case that this happen again please contact us!
            """,
            from_email=os.getenv("EMAIL"),
            to=[event["receipt_email"]],
            reply_to=[os.getenv("EMAIL")]
        )

        message_for_payment_failure.send()

    mycursor.close()

    return "OK",200

@stripe_implementation.route('/webhook_payment_success', methods=["POST"])
def webhook_succeeded():

    delete_old_webhooks(True)

    body=request.data
    stripe_signature=request.headers.get('Stripe-Signature')
    endpoint_secret=os.getenv("ENDPOINT_SECRET_SUCCESS")

    try:
        event=stripe.Webhook.construct_event(
            body,
            stripe_signature,
            endpoint_secret
        )
    except ValueError:
        return 'Invalid payload',400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature',400
    
    conn=get_connection()
    mycursor=get_cursor()

    mycursor.execute(
        "SELECT id FROM webhook_success WHERE id=%s",
        (event["id"],)
    )
    id=mycursor.fetchone()
    
    if id==None and event['type']=='payment_intent.succeeded':
        
        for key in session["cart"]:
            session["cart"][key]=0

        mycursor.execute(
            "INSERT INTO webhook_success (id,email) VALUES (%s,%s)",
            (event['id'],"roby36474@gmail.com")
        )

        conn.commit()

        comfirmation_message=EmailMessage(
            subject='Nesso - Payment Comfirmation',
            body='The payment was successful. Thank you for choosing out products!',
            from_email=os.getenv('EMAIL'),
            to=["roby36474@gmail.com"],
            reply_to=[os.getenv('EMAIL')]
        )

        comfirmation_message.send()

    
    mycursor.close()

    return 'OK',200
