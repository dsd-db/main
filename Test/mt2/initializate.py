import os
import uuid
import shutil
import random

# N=10000000
N=65536

TMP='~/tmp'
TMP=os.path.abspath(os.path.expanduser(TMP))
if os.path.exists(TMP):
    shutil.rmtree(TMP)
os.makedirs(TMP)

DIR='~/data/'
DIR=os.path.abspath(os.path.expanduser(DIR))

BASE='base.mdl'
BASE=os.path.join(DIR,BASE)

DEVICE='device'
DEVICE=os.path.join(DIR,DEVICE)

# MODEL='device.mdl'
# MODEL=os.path.join(DEVICE,'%s',MODEL)

# CALIBRATION='calibration'
# CALIBRATION=os.path.join(DEVICE,'%s',CALIBRATION)

_set=set()
def r()->str:
    i=random.randint(1,N)
    while i in _set:
        i=random.randint(1,N)
    _set.add(i)
    return str(i)

def rd(x:str=None)->str:
    if x=='id' or x=='uuid':
        s=str(uuid.uuid4())
    elif x=='email' or x=='mail':
        s=r()+'@gov.cn'
    elif x=='mdl' or x=='model':
        s=os.path.join(TMP,r()+'.mdl')
        with open(s,'w') as f:
            f.write('model:%s\n'%s)
    else:
        s=os.path.join(TMP,r(),'')
        os.makedirs(s)
        for i in range(1,7):
            with open(os.path.join(s,'%d.csv'%i),'w') as f:
                f.write('%s,%d\n'%(s,i))
    return s

def g(s,c=-1):
    l=len(s)
    if c==-1:
        if l<=1:
            return ''
        n=random.randint(0,l-1)
        return s[:n]+s[n+1:]
    else:
        if l<1:
            return c
        n=random.randint(0,l)
        return s[:n]+c+s[n:]
