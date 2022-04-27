import os
import json

DIR='~/data/'
DIR=os.path.abspath(os.path.expanduser(DIR))

BASE='base.mdl'
BASE=os.path.join(DIR,BASE)

DEVICE='device'
DEVICE=os.path.join(DIR,DEVICE)

MODEL='device.mdl'
MODEL=os.path.join(DEVICE,'%s',MODEL)

CALIBRATION='calibration'
CALIBRATION=os.path.join(DEVICE,'%s',CALIBRATION)

_ADMIN='admin.json'
_ADMIN=os.path.join(DIR,_ADMIN)
if os.path.exists(_ADMIN):
    admin=json.load(open(_ADMIN,'rb'))
else:
    admin=dict()
def flushadmin()->None:
    with open(_ADMIN,'w') as f:
        f.write(json.dumps(admin,skipkeys=True,ensure_ascii=False,indent=4,sort_keys=True))

_DEVICE='device.json'
_DEVICE=os.path.join(DIR,_DEVICE)
if os.path.exists(_DEVICE):
    device=json.load(open(_DEVICE,'rb'))
else:
    device=dict()
def flushdevice()->None:
    with open(_DEVICE,'w') as f:
        f.write(json.dumps(device,skipkeys=True,ensure_ascii=False,indent=4,sort_keys=True))
