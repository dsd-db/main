import os

import db

b=db.model.getBase()
assert os.path.exists(b)

print('OK')
