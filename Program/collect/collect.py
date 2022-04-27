import os
import pandas as pd
DIR='~/collect'
DIR=os.path.abspath(os.path.expanduser(DIR))
NAME='1'
XLSX=os.path.join(DIR,'%s.xlsx'%NAME)
CONF=os.path.join(DIR,'%s.conf'%NAME)

data=pd.ExcelFile(XLSX).parse('Sheet1')
n=len(data)
i=int(open(CONF,'r').read())
open(CONF,'w').write(str((i+1)%n))
ans=[str(i) for i in data.iloc[i]]
print(','.join(ans))
