import db
from initializate import DEFAULT_USERNAME,DEFAULT_PASSWORD

assert db.admin.add(DEFAULT_USERNAME,DEFAULT_PASSWORD)==False
assert db.admin.add(DEFAULT_USERNAME,'qwq')==False

assert db.admin.add('admin','123456')==True
assert db.admin.add('admin','123456')==False
assert db.admin.add('admin','12345678')==False
assert db.admin.add('a2','123456')==True
assert db.admin.add('a3','123456')==True
assert db.admin.add('a4','123456')==True
assert db.admin.add('a5','123456')==True

db.admin.remove('admin')
db.admin.remove('a2')
db.admin.remove('a3')
db.admin.remove('a4')
db.admin.remove('a5')

def f(username,password):
    try:
        db.admin.add(username,password)
    except ValueError:
        pass
    else:
        assert ValueError==None


f('admin','')
f('','123456')
f('admin','\n')
f('.','123456')
f('admin','a'*99)
f('a'*99,'123456')

print('OK')
