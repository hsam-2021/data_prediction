from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import json
import os
import util
import numpy as np
import pickle


# Init app
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
basedir = os.path.abspath(os.path.dirname(__file__))
model = pickle.load(open('/data_prediction/server/artifacts/model.pkl', 'rb'))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)



# Customer Class/Model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    job = db.Column(db.String(30))
    marital_status = db.Column(db.String(30))
    education = db.Column(db.String(30))
    contact = db.Column(db.String(15))
    month = db.Column(db.String(30))
    poutcome = db.Column(db.String(30))
    age = db.Column(db.SmallInteger())
    balance = db.Column(db.Integer())
    day = db.Column(db.Integer())
    duration = db.Column(db.Integer())
    campaign = db.Column(db.Integer())
    previous = db.Column(db.Integer())
    housing = db.Column(db.String(10))
    loan = db.Column(db.String(10))

    def __init__(self, job, marital_status, education, contact, month, poutcome, age, balance, day, duration, campaign,
                 previous, housing, loan):
        self.job = job
        self.marital_status = marital_status
        self.education = education
        self.contact = contact
        self.month = month
        self.poutcome = poutcome
        self.age = age
        self.balance = balance
        self.day = day
        self.duration = duration
        self.campaign = campaign
        self.previous = previous
        self.housing = housing
        self.loan = loan


# Customer Schema
class CustomerSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'job', 'marital_status', 'education', 'contact', 'month', 'poutcome', 'age', 'balance', 'day',
            'duration', 'campaign', 'previous', 'housing', 'loan')


# Init schema
customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)


# Create a Customer
@app.route('/customer', methods=['POST'])
def add_customer():
    job = request.json['job']
    marital_status = request.json['marital_status']
    education = request.json['education']
    contact = request.json['contact']
    month = request.json['month']
    poutcome = request.json['poutcome']
    age = request.json['age']
    balance = request.json['balance']
    day = request.json['day']
    duration = request.json['duration']
    campaign = request.json['campaign']
    previous = request.json['previous']
    housing = request.json['housing']
    loan = request.json['loan']

    new_customer = Customer(job, marital_status, education, contact, month, poutcome, age, balance, day, duration,
                            campaign, previous, housing, loan)

    db.session.add(new_customer)
    db.session.commit()

    return customer_schema.jsonify(new_customer)


# Get All Customers
@app.route('/customer', methods=['GET'])
def get_customers():
    all_customers = Customer.query.all()
    result = customers_schema.dump(all_customers)
    return jsonify(result.data)


# Get Single Customers
# @app.route('/customer/<id>', methods=['GET'])
# def get_customer(id):
#     customer = Customer.query.get(id)
#     return customer_schema.jsonify(customer)


# Update a customer
@app.route('/customer/<id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get(id)

    job = request.json['job']
    marital_status = request.json['marital_status']
    education = request.json['education']
    contact = request.json['contact']
    month = request.json['month']
    poutcome = request.json['poutcome']
    age = request.json['age']
    balance = request.json['balance']
    day = request.json['day']
    duration = request.json['duration']
    campaign = request.json['campaign']
    previous = request.json['previous']
    housing = request.json['housing']
    loan = request.json['loan']

    customer.job = job
    customer.marital_status = marital_status
    customer.education = education
    customer.contact = contact
    customer.month = month
    customer.poutcome = poutcome
    customer.age = age
    customer.balance = balance
    customer.day = day
    customer.duration = duration
    customer.campaign = campaign
    customer.previous = previous
    customer.housing = housing
    customer.loan = loan

    db.session.commit()

    return customer_schema.jsonify(customer)


# Delete Customer
@app.route('/customer/<id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get(id)
    db.session.delete(customer)
    db.session.commit()

    return customer_schema.jsonify(customer)


# Get Prediction for a Customer
@app.route('/customer/result', methods=['POST'])
@cross_origin()
def get_customer():
    record = json.loads(request.data)
    #print(record)
    #customer = Customer.query.get(id)
    job = record['job']
    marital_status = record['marital_status']
    education = record['education']
    contact = record['contact']
    month = record['month']
    poutcome = record['poutcome']
    age = record['age']
    balance = record['balance']
    day = record['day']
    duration = record['duration']
    campaign = record['campaign']
    previous = record['previous']
    housing = record['housing']
    loan = record['loan']

    return util.get_predict_customer(job, marital_status, education, contact, month, poutcome, age, balance, day, duration, campaign, previous, housing, loan)
  

# For Loan status prediction

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(30))
    married = db.Column(db.String(6))
    dependent = db.Column(db.String(2))
    education = db.Column(db.String(30))
    selfEmployed = db.Column(db.String(6))
    creditHistory = db.Column(db.Float(7))
    propertyArea = db.Column(db.String(30))
    applicantIncome = db.Column(db.Integer())
    coApplicantIncome = db.Column(db.Integer())
    loanAmount = db.Column(db.Integer())
    loanAmountTerm = db.Column(db.Integer())

    def __init__(self, gender, married, dependent, education, selfEmployed, creditHistory, propertyArea,
                 applicantIncome, coApplicantIncome,
                 loanAmount, loanAmountTerm):
        self.gender = gender
        self.married = married
        self.dependent = dependent
        self.education = education
        self.selfEmployed = selfEmployed
        self.creditHistory = creditHistory
        self.propertyArea = propertyArea
        self.applicantIncome = applicantIncome
        self.coApplicantIncome = coApplicantIncome
        self.loanAmount = loanAmount
        self.loanAmountTerm = loanAmountTerm


# Loan Schema
class LoanSchema(ma.Schema):
    class Meta:
        fields = (
            'id', 'gender', 'married', 'dependent', 'education', 'selfEmployed', 'creditHistory', 'propertyArea',
            'applicantIncome', 'coApplicantIncome',
            'loanAmount', 'loanAmountTerm')


# Init schema
loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)


# Create a Loan
@app.route('/loan', methods=['POST'])
def add_loan():
    gender = request.json['gender']
    married = request.json['married']
    dependent = request.json['dependent']
    education = request.json['education']
    selfEmployed = request.json['selfEmployed']
    creditHistory = request.json['creditHistory']
    propertyArea = request.json['propertyArea']
    applicantIncome = request.json['applicantIncome']
    coApplicantIncome = request.json['coApplicantIncome']
    loanAmount = request.json['loanAmount']
    loanAmountTerm = request.json['loanAmountTerm']

    new_loan = Loan(gender, married, dependent, education, selfEmployed, creditHistory, propertyArea, applicantIncome,
                    coApplicantIncome, loanAmount,
                    loanAmountTerm)

    db.session.add(new_loan)
    db.session.commit()

    return loan_schema.jsonify(new_loan)


# Get All Loans
@app.route('/loan', methods=['GET'])
def get_loans():
    all_loans = Loan.query.all()
    result = loans_schema.dump(all_loans)
    return jsonify(result.data)


# Update a loan
@app.route('/loan/<id>', methods=['PUT'])
def update_loan(id):
    loan = Loan.query.get(id)

    gender = request.json['gender']
    married = request.json['married']
    dependent = request.json['dependent']
    education = request.json['education']
    selfEmployed = request.json['selfEmployed']
    creditHistory = request.json['creditHistory']
    propertyArea = request.json['propertyArea']
    applicantIncome = request.json['applicantIncome']
    coApplicantIncome = request.json['coApplicantIncome']
    loanAmount = request.json['loanAmount']
    loanAmountTerm = request.json['loanAmountTerm']

    loan.gender = gender
    loan.married = married
    loan.dependent = dependent
    loan.education = education
    loan.selfEmployed = selfEmployed
    loan.creditHistory = creditHistory
    loan.propertyArea = propertyArea
    loan.applicantIncome = applicantIncome
    loan.coApplicantIncome = coApplicantIncome
    loan.loanAmount = loanAmount
    loan.loanAmountTerm = loanAmountTerm

    db.session.commit()

    return loan_schema.jsonify(loan)


# Delete Loan
@app.route('/loan/<id>', methods=['DELETE'])
def delete_loan(id):
    loan = Loan.query.get(id)
    db.session.delete(loan)
    db.session.commit()

    return loan_schema.jsonify(loan)


# Get Prediction for a Customer

# model = pickle.load(open('model.pkl', 'rb'))


@app.route('/loan/result', methods=['POST'])
def loan():
    record = json.loads(request.data)
    #print(record)
    # customer = Customer.query.get(id)
    gender = record['gender']
    married = record['married']
    dependent = record['dependent']
    education = record['education']
    selfEmployed = record['selfEmployed']
    creditHistory = record['creditHistory']
    propertyArea = record['propertyArea']
    applicantIncome = record['applicantIncome']
    coApplicantIncome = record['coApplicantIncome']
    loanAmount = record['loanAmount']
    loanAmountTerm = record['loanAmountTerm']

    # gender
    if gender == "Male":
        male = 1
    else:
        male = 0

    # married
    if married == "Yes":
        married_yes = 1
    else:
        married_yes = 0

    # dependents

    if dependent == '1':
        dependent_1 = 1
        dependent_2 = 0
        dependent_3 = 0
    elif dependent == '2':
        dependent_1 = 0
        dependent_2 = 1
        dependent_3 = 0
    elif dependent == '3+':
        dependent_1 = 0
        dependent_2 = 0
        dependent_3 = 1
    else:
        dependent_1 = 0
        dependent_2 = 0
        dependent_3 = 0

    # education
    if education == "Not Graduate":
        not_graduate = 1
    else:
        not_graduate = 0
    # employed

    if selfEmployed == "Yes":
        employed_yes = 1
    else:
        employed_yes = 0
    # Property area

    if propertyArea == "Semi Urban":
        semiurban = 1
        urban = 0
    elif propertyArea == "Urban":
        semiurban = 0
        urban = 1
    else:
        semiurban = 0
        urban = 0

    applicantIncomeLog = np.log(applicantIncome)
    totalIncomeLog = np.log(applicantIncome + coApplicantIncome)
    loanAmountLog = np.log(loanAmount)
    loanAmountTermLog = np.log(loanAmountTerm)

    prediction = model.predict(
        [[creditHistory, applicantIncomeLog, loanAmountLog, loanAmountTermLog, totalIncomeLog, male,
          married_yes, dependent_1, dependent_2, dependent_3, not_graduate, employed_yes,
          semiurban, urban]])		  
    prediction_str = str(prediction)
    prediction_out = prediction_str[prediction_str.find("['")+2:prediction_str.find("]'")-1]
    return str(prediction_out)   


# Run Server
if __name__ == '__main__':

    #app.run(debug=True)
	# Start flask app
	app.run(host="0.0.0.0", port=5000)
