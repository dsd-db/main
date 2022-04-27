import os

from initializate import rd
import db

b=db.model.getBase()
assert os.path.exists(b)

b2=rd('mdl')
assert b2!=b
assert os.path.exists(b2)

db.model.setBase(b2)
assert not os.path.exists(b2)
assert os.path.exists(b)

b3=db.model.getBase()
assert b3==b
assert b3!=b2

print('OK')
