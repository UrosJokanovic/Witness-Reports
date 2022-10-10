from genericpath import exists
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from models import create_file_reports, get_reports
import os, json
from requests import get


app = Flask(__name__)



@app.route('/')
def start():
    # removing witness.json file every time I start app for testing purposes
    if exists("witness.json"):
        os.remove("witness.json")
    return redirect(url_for('index'))

@app.route('/home', methods=['GET', 'POST'])
def index():

    pn    = True # checks if phone number is valid or possible
    tn    = True # checks if title name is in fbi db
    cn    = 1    # message before first input of title name and phone number
    match = True # checks if locations by number and ip adress match

    if request.method == 'GET':
        pass

    if request.method == 'POST':
        
        # getting country code from ip adress of a client
        ip           = get('https://api.ipify.org').content.decode('utf8')
        url          = 'http://ipwho.is/{}'.format(ip)
        req          = get(url)
        ip_info      = json.loads(req.text)
        country_code = ip_info['country_code']

        title      = request.form.get('title')
        number     = request.form.get('number')
        pn, tn, cn, match = create_file_reports(title, "+" + number, country_code)
    

    witness_reports = get_reports() # witness_reports of the list of titles

    return render_template('index.html', witness_reports = witness_reports, phoneNumberValid = pn, titleValid = tn, beforeFirstInput = cn, match = match)


# Preview of FBI MOST WANTED DB Cases
@app.route('/allreports', methods=['GET'])
def all_reports():

    return get_reports()


if __name__ == '__main__':
    app.run(port=8080, debug=True, use_reloader=True)