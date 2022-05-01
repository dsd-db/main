import os
import sys
import random

import db
from initializate import rd,BASE

if len(sys.argv)==1:
    COUNT=128
else:
    COUNT=int(sys.argv[1])

for _ in range(COUNT):
    if not _&255:
        print('db.model',_)
    i=random.randint(0,1)
    if i==0:
        b=db.model.getBase()
        assert b==BASE
        assert os.path.exists(BASE)
    else:
        b=rd('mdl')
        assert b!=BASE
        assert os.path.exists(b)
        db.model.setBase(b)
        assert os.path.exists(b)
        assert os.path.exists(BASE)

print('OK')
