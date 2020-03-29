from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import ipaddress


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'crud.sqlite')

from models import db,Subnet,ReservedIP


ma = Marshmallow(app)

class SubnetSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'address', 'vlan_id')


subnet_schema = SubnetSchema()
subnets_schema = SubnetSchema(many=True)


########################################################



class ReservedIPSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'ip_address', 'subnet_id')


reservedIP_schema = ReservedIPSchema()
reservedIPs_schema = ReservedIPSchema(many=True)


# endpoint to create new subnet
@app.route("/subnets", methods=["POST"])
def add_subnet():
    name = request.json['name']
    address = request.json['address']
    vlan_id = request.json.get('vlan_id', None)
    subnet = Subnet(name, address, vlan_id)

    db.session.add(subnet)
    db.session.commit()

    return subnet_schema.jsonify(subnet)

#not required




import routes.subnet_routes
import routes.vlan_routes
import routes.ip_routes



if __name__ == '__main__':
    app.run(debug=True)
