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

# Photography booking submission route
@app.route('/submit_photography_booking', methods=['POST'])
def submit_photography_booking():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    zip_code = request.form['zip']
    package_type = request.form['packageType']
    extra_photos = "Yes" if 'extraPhotos' in request.form else "No"
    rush_delivery = "Yes" if 'rushDelivery' in request.form else "No"

    # Package details
    package_details = {
        # Standard Photography
        "silver": "10 professionally edited photos<br>Social media-optimized versions",
        "gold": "20 professionally edited photos<br>Social media-optimized versions<br>Two unique locations",
        "platinum": "35+ professionally edited photos<br>Social media-optimized versions<br>Up to three locations<br>Priority editing (deliver within 5 days)",

        # Film Photography
        "SilverFilm": "Low-resolution social media photos<br>20-mile travel radius<br>$0.75/mile for extra distance",
        "GoldFilm": "High-resolution images<br>5 (4x6) print photos<br>60-mile travel radius<br>$0.75/mile for extra distance",
        "PlatinumFilm": "Low & high-resolution social media photos<br>5 (4x6) print photos<br>10 instant film prints<br>100-mile travel radius<br>$0.75/mile for extra distance<br>No rush delivery or extra edits available",

        # Roller Packages
        "photoRoller": "Dynamic rolling shots of a single car<br>Includes 10+ high-resolution photos<br>Rush delivery and extra edits available",
        "videoRoller": "Cinematic rolling video (60 seconds min)<br>Edited for social media<br>Additional footage or extended edits available<br>Rush delivery and extra edits available",
        "eliteRoller": "Both rolling photos and cinematic videos<br>Discounted rate<br>Extended video length or additional photos optional<br>Rush delivery and extra edits available",

        # Shadow Packages
        "Shadow": "Action shots of the car on the track or at the event<br>Photos of pit lane and garages<br>3-5 dynamic photos of your car in action<br>Rush delivery and extra edits available",
        "goldShadow": "Everything in Shadow Package<br>Exclusive staged photos on the track (if permitted)<br>Driver portraits included<br>10+ dynamic action shots<br>Rush delivery and extra edits available",
        "platinumShadow": "Everything in Gold Shadow Package<br>Full professional video coverage of the car in action<br>Driver mic-up for onboard audio capture<br>Custom highlight reels for social media or promotional use<br>Rush delivery and extra edits available",

        # Business Packages
        "businesspackage": "Professional vehicle photos<br>High-res and web-optimized versions<br>Optional video walkthroughs<br>Price varies depending on desired content",
        "trackeventpackage": "Full event coverage: crowd, cars, facilities<br>Highlight reels for promotion<br>Social media-ready posts<br>Price varies depending on desired content"
    }

    # Package prices
    package_prices = {
        # Standard Photography
        "silver": 150,
        "gold": 250,
        "platinum": 400,

        # Film Photography
        "SilverFilm": 225,
        "GoldFilm": 300,
        "PlatinumFilm": 400,

        # Roller Packages
        "photoRoller": 200,
        "videoRoller": 300,
        "eliteRoller": 450,

        # Shadow Packages
        "shadow": 200,
        "goldShadow": 400,
        "platinumShadow": 650,

        # Business Packages
        "businesspackage": 500,
        "trackeventpackage": 1500
    }

    total_price = package_prices[package_type]
    if extra_photos == "Yes":
        total_price += 10
    if rush_delivery == "Yes":
        total_price += 75

    # Email content
    email_body = f"""
    <html>
        <body>
            <h2>New Photography Booking</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Email:</strong> {email}</p>
            <p><strong>Phone:</strong> {phone}</p>
            <p><strong>Zip Code:</strong> {zip_code}</p>
            <p><strong>Package:</strong> {package_type.capitalize()} - ${package_prices[package_type]}</p>
            <p><strong>Package Details:</strong> {package_details[package_type]}</p>
            <p><strong>Add-Ons:</strong></p>
            <ul>
                <li>Extra Photos: {extra_photos}</li>
                <li>Rush Delivery: {rush_delivery}</li>
            </ul>
            <h3>Total Price: ${total_price}</h3>
        </body>
    </html>
    """

    try:
        send_email(f"Photography Booking from {name}", email_body)
        return redirect('/thank_you')
    except Exception as e:
        print(f"Error sending email: {e}")
        return "An error occurred while processing your booking. Please try again later.", 500

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

@app.route('/about_us')
def about_you():
    return render_template('about_us.html')

# route for about us

# Car of the Month route
@app.route('/car_of_the_month')
def car_of_the_month():
    months = [
        {"name": "November", "image": "November.jpg"},
        {"name": "December", "image": "December.jpg"},
        {"name": "January", "image": "January.jpg"},
        {"name": "February", "image": "February.jpg"},
        {"name": "March", "image": "March.jpg"},
        {"name": "April", "image": "April.jpg"},
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

@app.route('/events')
def events():
    return render_template('event_calendar.html')

@app.route('/photography')
def photography():
    return render_template('photography.html')

if __name__ == '__main__':
    app.run(debug=True)
