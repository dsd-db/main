import initializate
import db

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

db.admin.check('qwq','123abc\');insert into admin(username,email,password) values(\'hack\',\'1\',\'hack\')')
assert db.admin.add('hack','hack')==True
db.admin.remove('hack')

db.admin.remove('admin')

assert db.admin.check('admin','123456')==False
assert db.admin.check('admin','12345678')==False

db.admin.remove('a2')
db.admin.remove('a3')
db.admin.remove('a4')
db.admin.remove('a5')

print('OK')
