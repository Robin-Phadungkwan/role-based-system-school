from abc import ABC, abstractmethod
from functools import wraps
from flask import session, make_response
from secretsapp.db import db_connection, has_role
class Rechten:
    def __init__(self,lezen, schrijven, verwijderen, wijzigen,delen):
        self.lezen = lezen
        self.schrijven = schrijven
        self.verwijderen = verwijderen
        self.wijzigen = wijzigen
        self.delen = delen

    def lezen(self):
        return self.lezen

    def schrijven(self):
        return self.schrijven

    def verwijderen(self):
        return self.verwijderen

    def wijzigen(self):
        return self.wijzigen

    def delen(self):
        return self.delen

@abstractmethod   
class Gebruiker(Rechten):
    def __init__(self,username,role):
        self.username = username
        self.role = role

class Admin(Gebruiker):
    def __init__(self,username):
        super().__init__(username,"Admin")

class User(Gebruiker):
    def __init__(self,username):
        super().__init__(username,"User")
    
def get_role(self):
    return self.role

@abstractmethod
def check_permissions(role):
    def decorator(func):
        def wrapper(*args, **kwargs):
            active_user = kwargs.get("user","role")
            if active_user and hasattr(active_user, 'role') and active_user.role == role:
                return func(*args, **kwargs)
            else:
                raise PermissionError
        return wrapper
    return decorator


@abstractmethod
def auth_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            current_user = session.get('user')
            roles = session.get('role')
            if current_user is None or role not in roles:
                return make_response({"msg": "Unauthorized access"}, 403)
            else:
                pass
            return fn(*args, **kwargs)
        return decorated
    return wrapper
            

