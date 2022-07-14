from flask import Flask, request, make_response
from config_end import config_end
from functools import wraps

app = Flask(__name__)

def auth_required(f):
    @wraps(f)
    def decorated (*args, **kwargs):
        auth = request.authorization
        if auth and auth.username == 'funcionaria1' and auth.password == '1234':
            return f(*args, **kwargs)
        return make_response ('Login/senha incorretos!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
    return decorated



@app.route ('/')
def index():
    if request.authorization and request.authorization.username == 'username'and request.authorization.password == 'password':
        return '<h1>Você está logado :D !</h1>'
    return make_response ('Login/senha incorretos!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

