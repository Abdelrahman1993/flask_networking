from __main__ import app
from flask_marshmallow import Marshmallow
ma = Marshmallow(app)

class SubnetSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'address', 'vlan_id')


subnet_schema = SubnetSchema()
subnets_schema = SubnetSchema(many=True)