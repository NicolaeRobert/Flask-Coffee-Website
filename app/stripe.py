from flask import Blueprint, redirect, render_template, url_for, session, request
from .utils import get_connection, get_cursor, delete_old_webhooks
from flask_mailman import EmailMessage
from . import mail
import stripe
import os
from pprint import pprint

#Create the blueprint for the stripe implementation
stripe_implementation=Blueprint('stripe',__name__)

#Get the stripe secret key that we receive in the sandbox
stripe.api_key=os.getenv("SECRET_KEY_STRIPE")

#The route to redirect the user to stripe
@stripe_implementation.route('/redirect_to_stripe')
def redirect_to_stripe():

    #Here we create the objects bought parameter that we will pass to line_items
    objects_bought=[]
    #Iterate through the cart
    for key in session["cart"]:
        #Check to see if the current element was added
        if session['cart'][key]!=0:
            #Add the object to the parameter
            env_string=key.upper()
            objects_bought.append(
                {
                    "price": os.getenv(env_string),
                    "quantity": session['cart'][key]
                }
            )

    #Create the checkout session
    checkout=stripe.checkout.Session.create(
        line_items=objects_bought,#The object bought with the quantities
        mode="payment",#The mode set to payment
        success_url=url_for('stripe.success', _external=True),#The page where stripe redirects after everything was completed
        cancel_url=url_for('stripe.cancel', _external=True)#The page where stripe redirect if the user cancels
    )

    #Redirect to the checkout stripe page
    return redirect(checkout.url)
    
#The page where stripe redirects after everything was completed
@stripe_implementation.route('/success')
def success():
    return render_template('success_page.html')

#The page where stripe redirect if the user cancels
@stripe_implementation.route('/cancel')
def cancel():
    return render_template('cancel_page.html')

#The webhook that is being called if a payment failed
@stripe_implementation.route("/webhook_payment_failed", methods=["POST"])
def webhook_failed():

    #Delete old wekhook that have more that 7 days
    delete_old_webhooks(False)

    #Get the body od the request along with a parameter from the header
    body=request.data
    stripe_signature=request.headers.get('Stripe-Signature')

    #Get the endpoint secret from .env file(we have received it when we created the webhook)
    endpoint_secret=os.getenv("ENDPOINT_SECRET_FAIL")

    #Here we create the object received
    try:
        event=stripe.Webhook.construct_event(
            body,
            stripe_signature,
            endpoint_secret
        )
    #This error means that we had a problem with the body(payload)
    except ValueError:
        return 'Invalid payload',400
    #This error means that we had a problem with the stripe signature, the parameter from the header
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature',400
    
    #Here we get the connection and the cursor for the database
    conn=get_connection()
    mycursor=get_cursor()

    #See if we already processed the call(stripe sends multiple calls)
    mycursor.execute(
        "SELECT id FROM webhook_fail WHERE id=%s",
        (event['id'],)
    )
    id=mycursor.fetchone()

    #If we didn't process the call, do it here
    if id==None and event['type']=="payment_intent.payment_failed":
        
        #Insert the id and email into the database to consider it processed for the next calls
        mycursor.execute(
            'INSERT INTO webhook_fail (id,email) VALUES (%s,%s)',
            (event['id'],event['receipt_email'])
        )

        #Commit the changes
        conn.commit()

        #Create a message of failure for the user 
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

        #Send the message
        message_for_payment_failure.send()

    #Close the cursor connection
    mycursor.close()

    #Return 200 OK, because if we got here everything went great
    return "OK",200

@stripe_implementation.route('/webhook_payment_success', methods=["POST"])
def webhook_succeeded():

    #Delete old wekhook that have more that 7 days 
    delete_old_webhooks(True)

    #Get the body od the request along with a parameter from the header
    body=request.data
    stripe_signature=request.headers.get('Stripe-Signature')

    #Get the endpoint secret from .env file(we have received it when we created the webhook)
    endpoint_secret=os.getenv("ENDPOINT_SECRET_SUCCESS")

    #Here we create the object received
    try:
        event=stripe.Webhook.construct_event(
            body,
            stripe_signature,
            endpoint_secret
        )
    #This error means that we had a problem with the body(payload)
    except ValueError:
        return 'Invalid payload',400
    #This error means that we had a problem with the stripe signature, the parameter from the header
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature',400
    
    #Here we get the connection and the cursor for the database
    conn=get_connection()
    mycursor=get_cursor()

    #See if we already processed the call(stripe sends multiple calls)
    mycursor.execute(
        "SELECT id FROM webhook_success WHERE id=%s",
        (event["id"],)
    )
    id=mycursor.fetchone()
    
    #If we didn't process the call, do it here
    if id==None and event['type']=='payment_intent.succeeded':
        
        #Now that the payment was completet we can empty the cart
        for key in session["cart"]:
            session["cart"][key]=0

        #Add the id and the email in the database to consider it processed for next calls
        mycursor.execute(
            "INSERT INTO webhook_success (id,email) VALUES (%s,%s)",
            (event['id'],"roby36474@gmail.com")
        )

        #Commit the changes
        conn.commit()

        #Create the cmfirmation email
        comfirmation_message=EmailMessage(
            subject='Nesso - Payment Comfirmation',
            body='The payment was successful. Thank you for choosing out products!',
            from_email=os.getenv('EMAIL'),
            to=["roby36474@gmail.com"],
            reply_to=[os.getenv('EMAIL')]
        )

        #Send the email
        comfirmation_message.send()

    #Close the cursor
    mycursor.close()

    #Return 200 OK, because if we got here everything went great
    return 'OK',200
