from flask import Flask, render_template, request, redirect
from flask_mail import Mail, Message
import tkinter as tk
from tkinter import ttk


def submit():
    global email, password
    email = email_entry.get()
    password = password_entry.get()

    with open("credentials.txt", "w") as f:
        f.write(email + "\n")
        f.write(password + "\n")


root = tk.Tk()
root.title("Login")

# Create and position email label and entry
email_label = ttk.Label(root, text="Email:")
email_label.grid(column=0, row=0, padx=(20, 10), pady=(20, 5), sticky=tk.W)
email_entry = ttk.Entry(root)
email_entry.grid(column=1, row=0, padx=(10, 20), pady=(20, 5))

# Create and position password label and entry
password_label = ttk.Label(root, text="Password:")
password_label.grid(column=0, row=1, padx=(20, 10), pady=5, sticky=tk.W)
password_entry = ttk.Entry(root, show="*")
password_entry.grid(column=1, row=1, padx=(10, 20), pady=5)

# Create and position submit button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(column=1, row=2, padx=(10, 20), pady=(5, 20))

root.mainloop()

app = Flask(__name__)


def get_credentials():
    with open("credentials.txt", "r") as f:
        email = f.readline().strip()
        password = f.readline().strip()

    return email, password

email, password = get_credentials()

app.config['MAIL_SERVER'] = 'smtp-mail.outlook.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = email
app.config['MAIL_PASSWORD'] = password

mail = Mail(app)

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

@app.route('/success')
def success():
    return 'Data received. You will be contacted with pricing soon.'

def read_qual_data():
    lender_data = [
        {
            "lender_name": "Ken.Fox@acralending.com",
            "min_loan_amt": 100000,
            "min_prop_value": 100000,
            "LTV": 90,
            "credit_score": 575,
            "season": 0,
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
            "season": 0,
        },
        {
            "lender_name": "alex@greenboxloans.com",
            "min_loan_amt": 150000,
            "min_prop_value": None,
            "LTV": 70,
            "credit_score": 680,
            "season": 0,
        },
        {
            "lender_name": "jcalderon@homexmortgage.com",
            "min_loan_amt": 100000,
            "min_prop_value": 150000,
            "LTV": 80,
            "credit_score": 600,
            "season": 0,
        },
        {
            "lender_name": "jcraft@lsmortgage.com",
            "min_loan_amt": 125000,
            "min_prop_value": 0,
            "LTV": 80,
            "credit_score": 620,
            "season": 3,
        },
        {
            "lender_name": "acureton@oaktreefunding.com",
            "min_loan_amt": 100000,
            "min_prop_value": 0,
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
            "season": 0,
        },
    ]
    return lender_data




def calculate_ltv(loan_amount, property_value):
    return (loan_amount / property_value) * 100



def match_lenders(loan_amount, property_value, credit_score):
    ltv = calculate_ltv(loan_amount, property_value)
    matched_lenders = []

    for lender in read_qual_data():
        if ltv <= lender["max_ltv"] and credit_score >= lender["min_credit_score"]:
            matched_lenders.append(lender)

    return matched_lenders



def process_form_data(form_data):
    loan_amount = float(form_data["loan_amount"])
    property_value = float(form_data["property_value"])
    credit_score = int(form_data["credit_score"])

    matched_lenders = match_lenders(loan_amount, property_value, credit_score)
    return matched_lenders


def send_email(matched_lenders, form_data):
    subject = "Price Quote Request for VHL"

    with mail.connect() as conn:
        for lender in matched_lenders:
            msg = Message(subject,
                          recipients=[lender["lender_name"]],
                          sender=app.config['MAIL_USERNAME'])
            msg.html = render_template('outbound.html', form_data=form_data)
            conn.send(msg)

if __name__ == '__main__':
    app.run(debug=True)
