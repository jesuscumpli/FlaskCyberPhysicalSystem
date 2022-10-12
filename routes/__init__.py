from flask import Blueprint

routes = Blueprint('routes', __name__)

'''
Add routes python files
'''

from .userRoutes import *
from .homeRoutes import *
from .deviceRoutes import *