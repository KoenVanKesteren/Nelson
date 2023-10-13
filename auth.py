"""

    Opmerkingen:

        - dit is uiteraard niet hoe je authenticatie doet maar voor nu even simpel gehouden

"""
user_database = {
    'gebruiker1': 'wachtwoord1',
    'gebruiker2': 'wachtwoord2'
}


# Decorator-functie voor gebruikersauthenticatie
def authenticate_user(username, password):
    def decorator(func):
        def auth_wrapper(*args, **kwargs):
            if username in user_database and user_database[username] == password:
                return func(*args, **kwargs)
            else:
                return "<p>Unauthorized</p>"

        auth_wrapper.__name__ = func.__name__
        return auth_wrapper
    return decorator