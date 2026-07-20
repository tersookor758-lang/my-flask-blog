from .auth import *
from .posts import *
from .profiles import *
from routes.routes_auth_ import auth

app.register_blueprint(auth)