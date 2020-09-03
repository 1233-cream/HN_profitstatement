import pandas as pd 
import numpy as np 


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
#df_list1.to_csv(r'C:\Users\LYX\Desktop\data_333.csv')

import pymysql 

conn=pymysql.connect(
    host='localhost',
    user='root',password='root',
    database='yipin_2020'
)
cur=conn.cursor()
sql_blank='update yipin_alipay_july set `业务基础订单号`=replace(`业务基础订单号`,\'	\',\'\')'
sql='select * from yipin_alipay_july where `业务基础订单号` in {0} group by `yewu'.format(tuple(list1))

cur.execute(sql_blank)
cur.execute(sql)

res=cur.fetchall()

df_res=pd.DataFrame(res)
head=['业务描述','收入金额','支出金额','备注','业务基础订单号']
df_res=df_res.loc[:,head]
grouped_res=df_res.groupby('业务描述',as_index=False).agg(np.sum)
grouped_res.to_csv(r'C:\Users\LYX\Desktop\测试文件夹\0809.csv')
print(df_res.shape)