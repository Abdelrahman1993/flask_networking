from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Subnet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    address = db.Column(db.String(19))
    vlsm = db.Column(db.Integer)
    vlan_id = db.Column(db.Integer, nullable=False)

    def __init__(self, name, address, vlsm, vlan_id):
        self.name = name
        self.address = address
        self.vlsm = vlsm
        self.vlan_id = vlan_id


class SubnetSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'address', 'vlsm', 'vlan_id')


subnet_schema = SubnetSchema()
subnets_schema = SubnetSchema(many=True)


# endpoint to create new subnet
@app.route("/subnets", methods=["POST"])
def add_subnet():
    name = request.json['name']
    address = request.json['address']
    vlsm = request.json['vlsm']
    vlan_id = request.json.get('vlan_id', 1)
    subnet = Subnet(name, address, vlsm, vlan_id)

    db.session.add(subnet)
    db.session.commit()

    return subnet_schema.jsonify(subnet)


# endpoint to show all users
@app.route("/subnets", methods=["GET"])
def get_subnets():
    all_subnets = Subnet.query.all()
    result = subnets_schema.dump(all_subnets)
    return jsonify(result)


# endpoint to delete subnet
@app.route("/subnets/<id>", methods=["DELETE"])
def subnet_delete(id):
    subnet = Subnet.query.get(id)

    if(subnet):
        db.session.delete(subnet)
        db.session.commit()
        return subnet_schema.jsonify(subnet)
    else:
        return "subnet not found"


# endpoint to add vlan to subnet
@app.route("/subnets/<id>/vlan", methods=["POST"])
# endpoint to update subnet with new vlan
@app.route("/subnets/<id>/vlan", methods=["PUT"])
def subnet_update(id):
    subnet = Subnet.query.get(id)
    subnet.vlan_id = request.json.get('vlan_id', None)

    db.session.commit()
    return subnet_schema.jsonify(subnet)


# endpoint to delete vlan
@app.route("/subnets/<id>/vlan", methods=["DELETE"])
def vlan_delete(id):
    subnet = Subnet.query.get(id)
    subnet.vlan_id = None
    db.session.commit()
    return subnet_schema.jsonify(subnet)


# # endpoint to show all users
# @app.route("/users", methods=["GET"])
# def get_user():
#     all_users = User.query.all()
#     result = users_schema.dump(all_users)
#     return jsonify(result)


# # endpoint to get user detail by id
# @app.route("/users/<id>", methods=["GET"])
# def user_detail(id):
#     user = User.query.get(id)
#     return user_schema.jsonify(user)


# # endpoint to update user
# @app.route("/users/<id>", methods=["PUT"])
# def user_update(id):
#     user = User.query.get(id)
#     username = request.json['username']
#     email = request.json['email']

#     user.email = email
#     user.username = username

#     db.session.commit()
#     return user_schema.jsonify(user)
# # endpoint to delete user
# @app.route("/users/<id>", methods=["DELETE"])
# def user_delete(id):
#     user = User.query.get(id)
#     db.session.delete(user)
#     db.session.commit()
#     return user_schema.jsonify(user)
if __name__ == '__main__':
    app.run(debug=True)
