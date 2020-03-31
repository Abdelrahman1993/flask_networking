from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import ipaddress


app = Flask(__name__)

#database settings
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'crud.sqlite')


#app routes
import routes.subnet_routes
import routes.vlan_routes
import routes.ip_routes



if __name__ == '__main__':
    app.run(debug=True)
