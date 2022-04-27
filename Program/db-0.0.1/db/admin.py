from db.__config import admin,flushadmin

def add(username:str,password:str)->bool:
    if username in admin:
        return False
    admin[username]=password
    flushadmin()
    return True

def check(username:str,password:str)->bool:
    return username in admin and admin[username]==password

def remove(username:str)->None:
    if username in admin:
        del admin[username]
        flushadmin()
