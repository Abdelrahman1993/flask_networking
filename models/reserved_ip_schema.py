from __main__ import app
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)



class ReservedIPSchema(ma.Schema):
    class Meta:
        fields = ('id', 'ip_address', 'subnet_id')


reservedIP_schema = ReservedIPSchema()
reservedIPs_schema = ReservedIPSchema(many=True)

