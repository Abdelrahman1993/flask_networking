# from __main__ import app
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy(app)


# class Subnet(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     address = db.Column(db.String(18))
#     vlan_id = db.Column(db.Integer, nullable=True)
#     reserved_ips = db.relationship('ReservedIP', backref='subnet', lazy=True)

#     def __init__(self, name, address, vlan_id):
#         self.name = name
#         self.address = address
#         self.vlan_id = vlan_id


# class ReservedIP(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     ip_address = db.Column(db.String(15), nullable=False)
#     subnet_id = db.Column(db.Integer, db.ForeignKey('subnet.id'),
#                           nullable=False)

#     def __init__(self, ip_address, subnet_id):
#         self.ip_address = ip_address
#         self.subnet_id = subnet_id