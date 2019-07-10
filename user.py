from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS

import os

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'user.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


# Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.VARCHAR(50), unique=True)
    first_name = db.Column(db.VARCHAR(50), unique=False)
    last_name = db.Column(db.VARCHAR(50), unique=False)
    age = db.Column(db.INT, unique=False)
    gender = db.Column(db.VARCHAR(50), unique=False)

    def __init__(self, email, first_name, last_name, age, gender):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'email', 'first_name', 'last_name', 'age', 'gender')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


# Create endpoint
@app.route("/user", methods=["POST"])
def user_add():
    email = request.json["email"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    age = request.json["age"]
    gender = request.json["gender"]
    new_user = User(email, first_name, last_name, age, gender)

    db.session.add(new_user)
    db.session.commit()

    return user_schema.jsonify(new_user)


# Read endpoint
@app.route("/user", methods=["GET"])
def user_get():
    all_users = User.query.all()
    result = users_schema.dump(all_users)
    return users_schema.jsonify(result.data)


# Find endpoint
@app.route("/user/id=<id>", methods=["GET"])
def user_find_by_id(id):
    user = User.query.get(id)
    return user_schema.jsonify(user)


# Filter endpoint
@app.route("/user/fn=<first_name>", methods=["GET"])
def user_find_by_first_name(first_name):
    user = User.query.filter_by(first_name=first_name).all()
    return users_schema.jsonify(user)


@app.route("/user/ln=<last_name>", methods=["GET"])
def user_find_by_last_name(last_name):
    user = User.query.filter_by(last_name=last_name).all()
    return users_schema.jsonify(user)


@app.route("/user/em=<email>", methods=["GET"])
def user_find_by_email(email):
    user = User.query.filter_by(email=email).all()
    return users_schema.jsonify(user)


@app.route("/user/a=<age>", methods=["GET"])
def user_find_by_age(age):
    user = User.query.filter_by(age=age).all()
    return users_schema.jsonify(user)


@app.route("/user/g=<gender>", methods=["GET"])
def user_find_by_gender(gender):
    user = User.query.filter_by(gender=gender).all()
    return users_schema.jsonify(user)


# Update endpoint
@app.route("/user/id=<id>", methods=["PUT"])
def user_update(id):
    user = User.query.get(id)
    email = request.json["email"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    age = request.json["age"]
    gender = request.json["gender"]

    user.email = email
    user.first_name = first_name
    user.last_name = last_name
    user.age = age
    user.gender = gender

    db.session.commit()
    return user_schema.jsonify(user)


# Delete endpoint
@app.route("/user/id=<id>", methods=["DELETE"])
def user_delete(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user)


if __name__ == '__main__':
    app.run(debug=True)