from __main__ import app
from models import Subnet
from __main__ import subnets_schema,subnet_schema
from __main__ import reservedIPs_schema
from flask import Flask, request, jsonify
import ipaddress
from models import db

# endpoint to show all subnets
@app.route("/subnets", methods=["GET"])
def get_subnets():
    all_subnets = Subnet.query.all()
    result = subnets_schema.dump(all_subnets)
    return jsonify(result)

#Get details regarding a subnet. (VLAN ID, network IP, subnet mask, utilization percentage, subnet name)
# endpoint to get subnet info
@app.route("/subnets/<id>", methods=["GET"])
def info_subnet(id):
    subnet = Subnet.query.get(id)
    network = ipaddress.ip_network(subnet.address)
    subnet_mask = network.netmask
    num_of_addresses = network.num_addresses-2
    num_of_reserved = len(subnet.reserved_ips)

    return jsonify({
        "address" : subnet.address,
        "name" : subnet.name,
        "vlan_id" : subnet.vlan_id,
        "subnet mask" : str(subnet_mask),
        "utilization" : int(num_of_reserved*100/num_of_addresses)

    })


# endpoint to get subnet ips
@app.route("/subnets/<id>/ips", methods=["GET"])
def info_subnet_ips(id):
    subnet = Subnet.query.get(id)
    result = reservedIPs_schema.dump(subnet.reserved_ips)
    return jsonify(result)
    #return subnet_schema.jsonify(subnet)



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