import db
from initializate import DEFAULT_USERNAME,DEFAULT_PASSWORD

assert db.admin.check(DEFAULT_USERNAME,DEFAULT_PASSWORD)==True

assert db.admin.check('qwq','123abc')==False
assert db.admin.check('admin','123456')==False

assert db.admin.add('admin','123456')==True
assert db.admin.add('admin','123456')==False
assert db.admin.add('admin','12345678')==False
assert db.admin.add('a2','123456')==True
assert db.admin.add('a3','123456')==True
assert db.admin.add('a4','123456')==True
assert db.admin.add('a5','123456')==True

assert db.admin.check('qwq','123abc')==False
assert db.admin.check('admin','123456')==True
assert db.admin.check('admin','12345678')==False

db.admin.remove('admin')

assert db.admin.check('admin','123456')==False
assert db.admin.check('admin','12345678')==False

db.admin.remove('a2')
db.admin.remove('a3')
db.admin.remove('a4')
db.admin.remove('a5')

print('OK')
