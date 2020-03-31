
from __main__ import app
from models.subnet import Subnet,db
from models.subnet_schema import subnets_schema,subnet_schema
from models.reserved_ip_schema import reservedIPs_schema
from flask import Flask, request, jsonify
import ipaddress

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