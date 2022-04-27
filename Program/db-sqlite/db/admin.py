import re
import sqlite3

from db.__config import ADMIN

con=sqlite3.connect(ADMIN)
cur=con.cursor()
cur.execute('create table if not exists admin(username varchar(64) primary key,email varchar(1024),password varchar(1024))')
con.commit()

def add(username:str,password:str)->bool:
    cur.execute('select 1 from admin where username=?',(username,))
    s=cur.fetchone()
    if s:
        return False

    if not username:
        raise ValueError('username is empty')
    if not password:
        raise ValueError('password is empty')
    if len(username)>40:
        raise ValueError('username is too long')
    if len(password)>40:
        raise ValueError('password is too long')
    if not all(ord(c)<128 for c in username):
        raise ValueError('username contains non-ascii characters')
    if not all(ord(c)<128 for c in password):
        raise ValueError('password contains non-ascii characters')
    if not re.match('^\w+$',username):
        raise ValueError('username is invalid')
    if not re.match('^\S+$',password):
        raise ValueError('password is invalid')

    cur.execute('insert into admin(username,email,password) values(?,?,?)',(username,None,password))
    con.commit()
    return True

def check(username:str,password:str)->bool:
    cur.execute('select password from admin where username=?',(username,))
    s=cur.fetchone()
    if not s or s[0]!=password:
        return False
    else:
        return True

def remove(username:str)->None:
    cur.execute('delete from admin where username=?',(username,))
    con.commit()
