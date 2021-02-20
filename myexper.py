import pandas as pd
from pandas import DataFrame
value={'19': 'ID', '20': '32bits', '21': '16', '22': '7', '23': 'TCP'}
df1=list(value.values())
df2=list(value.keys())
df3=[df1,df2]
print(df3)
df = DataFrame (df3,['answers','question_id']).transpose()
df['student_id']=9
df=df.to_string(index=False)
print(df)
 