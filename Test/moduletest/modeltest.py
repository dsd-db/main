import os

import db
from initializate import rd

b=db.model.getBase()
m=open(b,'rb').read()

b2=rd('mdl')
assert b2!=b
m2=open(b2,'rb').read()

db.model.setBase(b2)
assert os.path.exists(b2)
assert os.path.exists(b)

b3=db.model.getBase()
assert b3==b
assert b3!=b2
m3=open(b3,'rb').read()
assert m3==m2

print('OK')
