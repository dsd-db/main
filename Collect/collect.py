import os
import pandas as pd
data=pd.ExcelFile("./acs_downstair_01.xlsx").parse('Sheet1')
n=len(data)
conf='./acs_downstair_01.conf'
if os.path.exists(conf):
    i=int(open(conf,'r').read())
else:
    i=0
open(conf,'w').write(str((i+1)%n))
ans=[str(i) for i in data.iloc[i]]
print(','.join(ans))
