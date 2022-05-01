import os
import sys
import random

import db
from initializate import rd,BASE

if len(sys.argv)==1:
    COUNT=128
else:
    COUNT=int(sys.argv[1])

a=open(BASE,'rb').read()

for _ in range(COUNT):
    if not _&255:
        print('db.model',_)
    i=random.randint(0,1)
    if i==0:
        b=db.model.getBase()
        assert b==BASE
        assert a==open(BASE,'rb').read()
    else:
        b=rd('mdl')
        assert a!=open(b,'rb').read()
        a=open(b,'rb').read()
        assert b!=BASE
        db.model.setBase(b)
        assert os.path.exists(BASE)

print('OK')
