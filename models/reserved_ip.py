from __main__ import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class ReservedIP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False)
    subnet_id = db.Column(db.Integer, db.ForeignKey('subnet.id'),
                          nullable=False)

    def __init__(self, ip_address, subnet_id):
        self.ip_address = ip_address
        self.subnet_id = subnet_id