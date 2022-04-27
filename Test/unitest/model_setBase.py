import os

from initializate import rd
import db

b2=rd('mdl')
assert os.path.exists(b2)

db.model.setBase(b2)
assert not os.path.exists(b2)

print('OK')
