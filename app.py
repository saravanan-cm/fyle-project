# Required imports
import csv
import json
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS

app = Flask(__name__, static_url_path="")
# CORS origin handler
cors = CORS(app, resources={r"/banks/*": {"origins": "*"}})
auth = HTTPBasicAuth()

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


# Bank data loader
with open("bank_data.json") as file:
    banks = json.load(file)
    temp = []
    for i in banks:
        temp.append(i)
    banks = temp


@app.route('/banks', methods=['GET'])
@auth.login_required  # auth checker for this route
def get_tasks():
    # Initializing variables
    ifsc = request.args.get('ifsc')
    name = request.args.get('name')
    city = request.args.get('city')

    # Getting details based on IFSC code
    if ifsc:
        ifsc = ifsc.lower()
        # Quering database for IFSC match
        bank = filter(lambda t: t['ifsc'].lower() == ifsc, banks)
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
            for x in range(0, len(banks)):
                if len(name) and len(city):
                    if banks[x]['bank_name'].lower() == name.lower() and banks[x]['city'].lower() == city.lower():
                        bank.append(banks[x])
                elif len(name) == 0 and len(city):
                    if banks[x]['city'].lower() == city.lower():
                        bank.append(banks[x])
                elif len(city) == 0 and len(name):
                    if banks[x]['bank_name'].lower() == name.lower():
                        bank.append(banks[x])

            # Partial matching if there is no exact match
            if len(bank) == 0:
                for x in range(0, len(banks)):
                    if len(name) and len(city):
                        if banks[x]['bank_name'].lower().find(name.lower()) != -1 and banks[x]['city'].lower().find(city.lower()) != -1:
                            bank.append(banks[x])
                    elif len(name) == 0 and len(city):
                        if banks[x]['city'].lower().find(city.lower()) != -1:
                            bank.append(banks[x])
                    elif len(city) == 0 and len(name):
                        if banks[x]['bank_name'].lower().find(name.lower()) != -1:
                            bank.append(banks[x])
        except NameError:
            print 'Name Error'
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
