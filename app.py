from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import ipaddress


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'crud.sqlite')

# from models import Subnet,ReservedIP
from models.subnet import Subnet
from models.reserved_ip import ReservedIP


ma = Marshmallow(app)

class SubnetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'vlan_id')


subnet_schema = SubnetSchema()
subnets_schema = SubnetSchema(many=True)


########################################################



class ReservedIPSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ip_address', 'subnet_id')


reservedIP_schema = ReservedIPSchema()
reservedIPs_schema = ReservedIPSchema(many=True)






import routes.subnet_routes
import routes.vlan_routes
import routes.ip_routes



if __name__ == '__main__':
    app.run(debug=True)
