# Required imports
import csv
import os
import json
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="")

# CORS origin handler
cors = CORS(app, resources={r"/banks/*": {"origins": "*"}})
auth = HTTPBasicAuth()

# Postgres config setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://sibsinxgxxlliw:4b5b0ed3b371dbc7b94b5aa4ca10a8c46613b0ab3dddaa018dc1cbb96e3c0920@ec2-23-21-122-141.compute-1.amazonaws.com:5432/d2ivg4cvnakno7'

db = SQLAlchemy(app)


# Auth verifier
@auth.get_password
def get_password(username):
    if username == 'testuser':
        return 'secretfyle'
    return None


# Unauthorized error handler
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'status': 403, 'error': 'Unauthorized access'}), 403)


# Data not found error handler
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'status': 404, 'error': 'Not found'}), 404)


# Function to convert response into a list of objects
def extractRows(result):
    # If no rows were returned in the result, return an empty list
    if result.returns_rows == False:
        bank = []
    # Convert the response to a plain list of dicts
    else:
        bank = [dict(row.items()) for row in result]
    return bank


@app.route('/banks', methods=['GET'])
# @auth.login_required  # auth checker for this route
def get_tasks():
    # Initializing variables
    ifsc = request.args.get('ifsc')
    name = request.args.get('name')
    city = request.args.get('city')

    # Getting details based on IFSC code
    if ifsc:
        ifsc = ifsc.upper()

        # Quering database for IFSC match
        result = db.session.execute(
            "select * from Branches inner join Banks on Banks.id = Branches.bank_id where Branches.ifsc = :ifsc", {"ifsc": ifsc})
        bank = extractRows(result)

        if len(bank) == 0:
            abort(404)
        else:
            bank = {
                'status': 200,
                'count': len(bank),
                'banks': bank
            }

    # Getting details based on Name and City
    elif name or city:
        print "******Entered name and city**********"
        bank = []
        try:
            # Exact match
            if name and city:
                city = city.upper()
                name = name.upper()
                result = db.session.execute(
                    "select * from Branches inner join Banks on Banks.id = Branches.bank_id where Banks.name = :name and Branches.city = :city limit 200", {"name": name, "city": city})
                bank = extractRows(result)

            elif len(city) and (name is None or len(name) == 0):
                city = city.upper()
                result = db.session.execute(
                    "select * from Branches inner join Banks on Banks.id = Branches.bank_id where Branches.city = :city limit 200", {"city": city})
                bank = extractRows(result)

            elif len(name) and (city is None or len(city) == 0):
                name = name.upper()
                result = db.session.execute(
                    "select * from Branches inner join Banks on Banks.id = Branches.bank_id where Branches.name = :name limit 200", {"name": name})
                bank = extractRows(result)

            # Partial matching if there is no exact match
            if len(bank) == 0:
                if name and city:
                    city = city.upper()
                    name = name.upper()
                    result = db.session.execute("select * from Branches inner join Banks on Banks.id = Branches.bank_id where Banks.name like :name and Branches.city like :city limit 200", {
                                                "name": "%"+name+"%", "city": "%"+city+"%"})
                    bank = extractRows(result)

                elif len(city) and (name is None or len(name) == 0):
                    city = city.upper()
                    result = db.session.execute(
                        "select * from Branches inner join Banks on Banks.id = Branches.bank_id where Branches.city like :city limit 200", {"city": "%"+city+"%"})
                    bank = extractRows(result)
                    print type(bank)
                    print len(bank)

                elif len(name) and (city is None or len(city) == 0):
                    name = name.upper()
                    result = db.session.execute(
                        "select * from Branches inner join Banks on Banks.id = Branches.bank_id where Branches.name like :name limit 200", {"name": "%"+name+"%"})
                    bank = extractRows(result)

        except NameError as e:
            print e
        if len(bank) == 0:
            abort(404)
        else:
            bank = {
                'status': 200,
                'count': len(bank),
                'banks': bank
            }
    return jsonify(bank)

if __name__ == '__main__':
    app.run(debug=True)
