from werkzeug.security import safe_str_cmp # Safe string compare that works on old versions of python
    # if user and safe_str_cmp(user.password, password): # comparing two strings, return True if equal
from models.user import UserModel

#
# deleted users list (replaced with .db file)
# deleted username_mapping and userid_mapping methods (replaced with class method in user.py)
#

def authenticate(username, password):
    #user = username_mapping.get(username, None)
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    # return userid_mapping.get(user_id, None)
    return UserModel.find_by_id(user_id)