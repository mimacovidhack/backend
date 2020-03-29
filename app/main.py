from flask import Flask, escape, request
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

app = Flask(__name__)
port = int(os.getenv('PORT', 3000))

cred = credentials.Certificate({
        "type": "service_account",
        "project_id": os.getenv('PROJECT_ID'),
        "private_key_id": os.getenv('PRIVATE_KEY_ID'),
        "private_key": os.getenv('PRIVATE_KEY').replace('\\n', '\n'),
        "client_email": os.getenv('CLIENT_EMAIL'),
        "client_id": os.getenv('CLIENT_ID'),
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://accounts.google.com/o/oauth2/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": os.getenv('CLIENT_CERT_URL')
})


#cred = credentials.Certificate('../../mima-covid-hack-firebase-adminsdk-uxltg-1fc30b3a52.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/test-data', methods=['POST'])
def add_test_data():
    data = request.json
    doc_ref = db.collection(u'test-data').add(data)
    #doc_ref.set(data)

    return {'id': data}, 200

@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes_ref = db.collection(u'heroes')
    heroes = heroes_ref.stream()
    all_heroes = [{**{'id': hero.id}, **hero.to_dict()} for hero in heroes_ref.stream()]
    
    return jsonify(all_heroes), 200

@app.route('/heroes', methods=['POST'])
def add_hero():
    data = request.json
    heroes_ref = db.collection(u'heroes').add(data)

    return {'id': data}, 200

@app.route('/volunteers', methods=['GET'])
def get_volunteers():
    volunteers_ref = db.collection(u'volunteers')
    all_volunteers = [{**{'id': volunteer.id}, **volunteer.to_dict()} for volunteer in volunteers_ref.stream()]
    
    return jsonify(all_volunteers), 200

@app.route('/volunteers', methods=['POST'])
def add_volunteer():
    data = request.json
    doc_ref = db.collection(u'volunteers').add(data)

    return {'id': data}, 200

@app.route('/professions', methods=['POST'])
def add_hero():
    data = request.json
    heroes_ref = db.collection(u'professions').add(data)

    return {'id': data}, 200
    

app.run(host='0.0.0.0', port=port)
