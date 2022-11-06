from flask import Blueprint
import sys
sys.path.append("/opt/controlSystem")

routes = Blueprint('routes', __name__)

'''
Add routes python files
'''

from .userRoutes import *
from .homeRoutes import *
from .deviceRoutes import *
from .logsDeviceRoutes import *
from .logsUsersRoutes import *
from .operationsRoutes import *