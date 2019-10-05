# TODO: Make this not terrible.  Following a tutorial.  Clearly this is not secure.
from werkzeug.security import safe_str_cmp
from user import User

# note: these are placeholders for database info
users = [
    User(1, 'putty', 'PuttyPass')
]

username_mapping = {u.username: u for u in users} # set comprehension (new to me now)
userid_mapping = {u.id: u for u in users}


#Note, this allows is to use tokens to validate user for each request made.
def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)