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





# endpoint to add vlan to subnet
@app.route("/subnets/<id>/vlan", methods=["POST"])
# endpoint to update subnet with new vlan
@app.route("/subnets/<id>/vlan", methods=["PUT"])
def subnet_update(id):
    subnet = Subnet.query.get(id)
    vlan_id = request.json.get('vlan_id', None)
    if vlan_id >=1 and vlan_id<=1001:
        subnet.vlan_id = vlan_id
        db.session.commit()
        return subnet_schema.jsonify(subnet)
    return "vlan id must be 1:1001 "


# endpoint to delete vlan
@app.route("/subnets/<id>/vlan", methods=["DELETE"])
def vlan_delete(id):
    subnet = Subnet.query.get(id)
    subnet.vlan_id = None
    db.session.commit()
    return subnet_schema.jsonify(subnet)


# endpoint to reserve ip given the subnet
@app.route("/subnets/<id>/ips", methods=["POST"])
def reserve_ip(id):
    ip_address = request.json['ip']
    subnet = Subnet.query.get(id)

    #check if ip is not in the subnet and not already reserved 
    if ipaddress.ip_address(ip_address) in ipaddress.ip_network(subnet.address) and not any(ip.ip_address == ip_address for ip in subnet.reserved_ips):
        #check if ip is not net address and not brodcast address
        if ip_address != subnet.address.split('/')[0] and ip_address != str(ipaddress.IPv4Network(subnet.address).broadcast_address).split('/')[0]:
            ip = ReservedIP(ip_address, id)
            subnet.reserved_ips.append(ip)
            db.session.add(subnet)
            db.session.commit()
            return reservedIP_schema.jsonify(ip)

    return "Invalid ip for the subnet or already reserved"


# endpoint to free ip from the subnet
@app.route("/subnets/<id>/ips", methods=["DELETE"])
def free_ip(id):
    ip_address = request.json['ip_address']
    subnet = Subnet.query.get(id)

    if subnet:
        for index, item in enumerate(subnet.reserved_ips):
            if item.ip_address == ip_address:
                db.session.delete(subnet.reserved_ips[index])
                db.session.commit()
                return "deleted"
                break

    return "Not found"




#Get details regarding an IP. (parent Subnet, free/used)
# # endpoint to get ip info
@app.route("/subnets/ip", methods=["GET"])
def info_ip():
    
    ip_address = request.json['ip_address']
    ip_address_reserv = ReservedIP.query.filter_by(ip_address=ip_address).first() 
    if ip_address_reserv:
        return jsonify({
            "ip_address" : ip_address,
             "free" : False,
             "subnet" : subnet_schema.dump(ip_address_reserv.subnet)
        })
    else:
        return "free ip address"



        # "subnet mask" : ipaddress.IPv4Address(subnet.address).netmask()

    # return jsonify({
    #     "address" : subnet.address,
    #     "name" : subnet.name,
    #     "vlan_id" : subnet.vlan_id,
    #     "ips" : reservedIPs_schema.dump(subnet.reserved_ips)
    # })



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
