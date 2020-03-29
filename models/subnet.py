from __main__ import app
from flask_sqlalchemy import SQLAlchemy
from models.reserved_ip import ReservedIP,db




class Subnet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    address = db.Column(db.String(18))
    vlan_id = db.Column(db.Integer, nullable=True)
    reserved_ips = db.relationship('ReservedIP', backref='subnet', lazy=True)

    def __init__(self, name, address, vlan_id):
        self.name = name
        self.address = address
        self.vlan_id = vlan_id