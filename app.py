from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# PayPal email address for payment
PAYPAL_EMAIL = "cure.auto.services@gmail.com"

# Membership pricing rates
YEARLY_RATES = {"silver": 300, "gold": 600, "platinum": 1000}
MONTHLY_RATES = {tier: rate / 12 for tier, rate in YEARLY_RATES.items()}

# Calculate membership price based on the start and end dates
def calculate_membership_price(start_date, end_date, tier):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    duration = (end.year - start.year) * 12 + (end.month - start.month)
    if duration % 12 == 0:
        return YEARLY_RATES[tier]
    else:
        return duration * MONTHLY_RATES[tier]

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Modifications route - Coming Soon Page
@app.route('/modifications')
def modifications():
    return render_template('comingsoon.html')

# Membership route - Coming Soon Page
@app.route('/membership')
def membership():
    return render_template('comingsoon.html')

# Detailing route
@app.route('/detailing', methods=['GET'])
def detailing():
    return render_template('detailing.html')

# Detailing booking submission route
@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    service_type = request.form['serviceType']
    service_prices = {"interior": 150, "exterior": 100, "both": 250}
    base_price = service_prices.get(service_type, 0)

    wax = "Yes" if 'wax' in request.form else "No"
    tire_dressing = "Yes" if 'tireDressing' in request.form else "No"
    clay_bar = "Yes" if 'clayBar' in request.form else "No"
    paint_sealant = "Yes" if 'paintSealant' in request.form else "No"

    total_price = base_price
    if wax == "Yes":
        total_price += 40
    if tire_dressing == "Yes":
        total_price += 20
    if clay_bar == "Yes":
        total_price += 50
    if paint_sealant == "Yes":
        total_price += 75

    message_content = f"""
    <html>
        <body>
            <h2>New Detailing Service Booking</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Phone:</strong> {phone}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Service Type:</strong> {service_type.title()}</p>
            <p><strong>Waxing:</strong> {wax}</p>
            <p><strong>Tire Dressing:</strong> {tire_dressing}</p>
            <p><strong>Clay Bar Treatment:</strong> {clay_bar}</p>
            <p><strong>Paint Sealant:</strong> {paint_sealant}</p>
            <h3>Total Price: ${total_price:.2f}</h3>
            <p>Thank you for your booking!</p>
        </body>
    </html>
    """

    send_email("New Detailing Booking", message_content)
    return redirect('/thank_you')

# Send email function
def send_email(subject, body):
    sender_email = "cure.auto.services@gmail.com"
    receiver_email = "cure.auto.services@gmail.com"
    password = "sumhrzdgfmgrfvxn"  # Use an app-specific password for better security

    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = receiver_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Thank you route
@app.route('/thank_you')
def thank_you():
    return render_template('thank_you.html')

# Car of the Month route
@app.route('/car_of_the_month')
def car_of_the_month():
    months = [
        {"name": "November", "image": "November.jpg"},
        {"name": "December", "image": "december.jpg"},
        {"name": "January", "image": None},
        {"name": "February", "image": None},
        {"name": "March", "image": None},
        {"name": "April", "image": None},
        {"name": "May", "image": None},
        {"name": "June", "image": None},
        {"name": "July", "image": None},
        {"name": "August", "image": None},
        {"name": "September", "image": None},
        {"name": "October", "image": None}
    ]
    return render_template('car_of_the_month.html', months=months)

# Easter egg game route
@app.route('/easter_egg_game')
def easter_egg_game():
    return render_template('easter_egg_game.html')

if __name__ == '__main__':
    app.run(debug=True)
@app.route('/events')
def events():
    return render_template('event_calendar.html')
