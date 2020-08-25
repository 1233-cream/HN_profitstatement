import pandas as pd 


#读取目标文件
df=pd.read_csv(r'C:\Users\LYX\Desktop\data_222.csv')
print(df.shape)
list_originalorderno=df.loc[:,'原始单号']
list1=[]
for order in list_originalorderno:
    orders=order.split(',',-1)
    for i in orders:
        list1.append(i)

print(df.columns.values) 
print(len(list1)) 
df_list1=pd.DataFrame(list1,columns=['原始单号'],index=None)
df_list1.to_csv(r'C:\Users\LYX\Desktop\data_333.csv')

import pymysql 

conn=pymysql.connect(
    host='localhost',
    user='root',password='root',
    database='yipin_2020'
)