from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
# from flask_restplus import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)
cust_post_args = reqparse.RequestParser()
# print(cust_post_args)
cust_post_args.add_argument("job", type=str, help='Job of the customer')
cust_post_args.add_argument("marital status", type=str, help='marital status of the customer')
# cust_post_args.add_argument("education", type=str, help="education level of the customer")
# cust_post_args.add_argument("contact", type=str, help="contact of the customer")
# cust_post_args.add_argument("month", type=str, help="month when the customer was contacted")
# cust_post_args.add_argument("poutcome", type=str, help="outcome of the customer")
customers = {}

class Prediction(Resource):
    def get(self, cust_id):
        return customers[cust_id]

    def post(self, cust_id):
        # print(request.form['job'])
        args = cust_post_args.parse_args()
        return jsonify({cust_id: args})
        # return {}


api.add_resource(Prediction, "/predict/<int:cust_id>")

if __name__ == "__main__":
    app.run(debug=True)
