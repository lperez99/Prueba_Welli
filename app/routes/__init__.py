from flask import Blueprint

# Create a blueprint for the routes
api = Blueprint('api', __name__)

# Import routes
from .loan_routes import *
from .purchase_routes import *
from .inventory_routes import *