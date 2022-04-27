import os

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

ADMIN='admin.db'
ADMIN=os.path.join(DIR,ADMIN)

DEVICE='device.db'
DEVICE=os.path.join(DIR,DEVICE)

if __name__=='__main__':
    print(DIR)
    print(BASE)
    print(DEVICE)
    print(MODEL)
    print(CALIBRATION)
    print(ADMIN)
    print(DEVICE)
