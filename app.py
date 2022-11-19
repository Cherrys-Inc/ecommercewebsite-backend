import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI")

db = SQLAlchemy(app)

from flask_migrate import Migrate
from models import *

Migrate(app, db)


@app.route('/add', methods=['POST'])
@cross_origin()
def create():
    user = User()
    json_data = request.get_json(force=True)
    user.userName = json_data['userName']
    user.email = json_data['email']
    user.firebase_uid = json_data['uid']
    user.mobile = json_data['mobile']
    db.session.add(user)
    db.session.commit()
    return "Record added"


@app.route('/getdata', methods=['GET'])
def get_data():
    uid = request.args.get('uid')
    print(uid)
    user_data = User.query.filter_by(firebase_uid=uid).one()
    user_found = user_data.to_json()
    return jsonify(user_found)


if __name__ == '__main__':
    app.run(debug=True)
