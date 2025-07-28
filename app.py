import os
import stripe
from flask import Flask, render_template, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.route('/')
def index():
    return render_template('index.html', public_key=os.getenv("STRIPE_PUBLIC_KEY"))

@app.route('/create-checkout-session/<amount>')
def create_checkout_session(amount):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f'Offre à {amount}€',
                    },
                    'unit_amount': int(amount) * 100,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        return redirect(session.url, code=303)
    except Exception as e:
        return str(e)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/cancel')
def cancel():
    return render_template('cancel.html')

if __name__ == '__main__':
    app.run(debug=True)
