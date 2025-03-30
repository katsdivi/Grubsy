import sys
import os

# Make sure your project folder is in sys.path
sys.path.insert(0, '/home/yourusername/fastapi_app')

from app import app
from starlette.middleware.wsgi import WSGIMiddleware

application = WSGIMiddleware(app)

