import os
from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
import re

app = Flask(__name__)
# DO NOT CHANGE ANY OF THIS CODE
# function to get email credentials from the file credentials.txt
def get_credentials():
    with open("credentials.txt", "r") as f:
        email = f.readline().strip()
        password = f.readline().strip()

    return email, password
#  global variables for email and password that use the flask mail library to send emails

# DO NOT CHANGE ANY OF THIS CODE
email, password = get_credentials()

app.config['MAIL_SERVER'] = 'smtp-gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] = password

mail = Mail(app)

# DO NOT CHANGE ANY OF THIS CODE
# directing the flask app to the index.html (form) file and rendering it
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = {
            key: request.form[key] for key in request.form.keys()
        }

        matched_lenders = process_form_data(form_data)

        send_email(matched_lenders, form_data)

        return redirect('/success')
    return render_template('index.html')

# DO NOT CHANGE ANY OF THIS CODE
# This is the text that will display once the user submits the form
@app.route('/success')
def success():
    return 'Data received. You will be contacted with pricing soon.'

# IF CHANGES NEED TO BE MADE OR LENDERS ADDED. COPY A SECTION AND EDIT THE VALUES MUST INCLUDE {}
#  This function takes the form data and matches it to the lenders in the lender_data list
def read_qual_data():
    lender_data = [
        {
            "lender_name": "Ken.Fox@acralending.com",
            "min_loan_amt": 100000,
            "min_prop_value": 100000,
            "LTV": 90,
            "credit_score": 575,
            "season": None,
        },
        {
            "lender_name": "Bret.Chard@carringtonms.com",
            "min_loan_amt": 100000,
            "min_prop_value": None,
            "LTV": 80,
            "credit_score": 660,
            "season": 6,
        },
        {
            "lender_name": "Clark.Knoblock@ChangeWholesale.com",
            "min_loan_amt": 100000,
            "min_prop_value": 100000,
            "LTV": 80,
            "credit_score": 680,
            "season": None,
        },
        {
            "lender_name": "alex@greenboxloans.com",
            "min_loan_amt": 150000,
            "min_prop_value": None,
            "LTV": 70,
            "credit_score": 680,
            "season": None,
        },
        {
            "lender_name": "jcalderon@homexmortgage.com",
            "min_loan_amt": 100000,
            "min_prop_value": 150000,
            "LTV": 80,
            "credit_score": 600,
            "season": None,
        },
        {
            "lender_name": "jcraft@lsmortgage.com",
            "min_loan_amt": 125000,
            "min_prop_value": None,
            "LTV": 80,
            "credit_score": 620,
            "season": 3,
        },
        {
            "lender_name": "acureton@oaktreefunding.com",
            "min_loan_amt": 100000,
            "min_prop_value": None,
            "LTV": 80,
            "credit_score": 620,
            "season": 6,
        },
        {
            "lender_name": "eserdinsky@thelender.com",
            "min_loan_amt": 70000,
            "min_prop_value": 83000,
            "LTV": 80,
            "credit_score": 620,
            "season": None,
        },
    ]
    return lender_data


# DO NOT CHANGE ANY OF THIS CODE
# this function calculates the loan to value ratio based on the info from the form
def calculate_ltv(loan_amount, property_value):
    return (loan_amount / property_value) * 100

# DO NOT CHANGE ANY OF THIS CODE
# this function identifies the lenders that match the form data
def match_lenders(loan_amount, property_value, credit_score):
    ltv = calculate_ltv(loan_amount, property_value)
    matched_lenders = []

    for lender in read_qual_data():
        if ltv <= lender["LTV"] and credit_score >= lender["credit_score"]:
            matched_lenders.append(lender)

    return matched_lenders

# DO NOT CHANGE ANY OF THIS CODE
# this function processes the form data and matches it to the data in the lender_data list
def process_form_data(form_data):
    credit_score_clean = re.sub(r'\D', '', form_data["credit_score"])
    credit_score = int(credit_score_clean)
    loan_amount = float(form_data["loan_amount"])
    property_value = float(form_data["property_value"])
    credit_score = int(form_data["credit_score"])

    matched_lenders = match_lenders(loan_amount, property_value, credit_score)
    return matched_lenders
# DO NOT CHANGE ANY OF THIS CODE
# this function uses the outbound.html file as a template, populates it with the form data and sends it to the matched lenders
def send_email(matched_lenders, form_data):
    subject = "Price Quote Request for VHL"

    with mail.connect() as conn:
        for lender in matched_lenders:
            msg = Message(subject,
                          recipients=[lender["lender_name"]],
                          sender=app.config['MAIL_USERNAME'])
            msg.html = render_template('outbound.html', form_data=form_data)
            conn.send(msg)


# DO NOT CHANGE ANY OF THIS CODE
if __name__ == '__main__':
    app.run(debug=True)
