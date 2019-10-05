# TODO: Make this not terrible.  Following a tutorial.  Clearly this is not secure.
from werkzeug.security import safe_str_cmp
from user import User

#Note, this allows is to use tokens to validate user for each request made.
def authenticate(username, password):
    user = User.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_by_id(user_id)