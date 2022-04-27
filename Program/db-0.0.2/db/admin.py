import sqlite3

from db.__config import ADMIN

con=sqlite3.connect(ADMIN)
cur=con.cursor()
cur.execute('create table if not exists admin(username varchar(64) primary key,email varchar(1024),password varchar(1024))')
con.commit()

def add(username:str,password:str)->bool:

    # if username in admin:
    #     return False
    cur.execute('select 1 from admin where username=?',(username,))
    s=cur.fetchone()
    if s:
        return False

    # admin[username]=password
    cur.execute('insert into admin(username,email,password) values(?,?,?)',(username,None,password))

    # flushadmin()
    con.commit()

    return True

def check(username:str,password:str)->bool:
    # return username in admin and admin[username]==password
    cur.execute('select password from admin where username=?',(username,))
    s=cur.fetchone()
    if not s or s[0]!=password:
        return False
    else:
        return True

def remove(username:str)->None:
    # if username in admin:
    #     del admin[username]
    #     flushadmin()
    cur.execute('delete from admin where username=?',(username,))
    con.commit()
