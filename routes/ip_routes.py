from __main__ import app
from models.subnet import Subnet,db
from models.reserved_ip import ReservedIP
from __main__ import subnets_schema,subnet_schema
from __main__ import reservedIPs_schema,reservedIP_schema
from flask import Flask, request, jsonify
import ipaddress


# endpoint to reserve ip given the subnet
@app.route("/subnets/<id>/ips", methods=["POST"])
def reserve_ip(id):
    ip_address = request.json['ip_address']
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
