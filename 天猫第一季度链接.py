import pymysql
import pandas as pd 
import numpy as np 


conn=pymysql.connect(
    host='localhost',
    user='root',password='root',
    database='tm_firstseason_link'
)

#创建游标
cursor=conn.cursor()

#查询表字段名
sql='select column_name from information_schema.`columns` where table_name=\'yipin_01-03_sellsdetail\''
cursor.execute(sql)
filedname=cursor.fetchall()
filednames=[]
for  f in filedname:
    filednames.append(f[0])
print('表中的字段名包含:{}'.format(filednames))

#查询多订单号订单
FiledName='原始单号,订单编号,交易名'
Condition='length(原始单号)>18'
# FiledName=input("请输入需要查询的字段名,使用英文逗号分隔 : ")
# Condition=input("请输入Having条件 : ")
sql='select distinct {0} from `yipin_01-03_sellsdetail` having {1}'.format(FiledName,Condition)
cursor.execute(sql)
orderNO=cursor.fetchall()
orderNOs_csv=[]
# orderNOs=[]
for no in orderNO:
    nos=no[0].split(',',-1)
    for i in nos:
        # orderNOs.append(i)
        orderNOs_csv.append((i,no[1],no[2]))
print(len(orderNOs_csv))

#输出拆分后的原始单号到csv文件
head=FiledName.split(',',-1)
df_orderNOs=pd.DataFrame(orderNOs_csv,columns=head)
df_orderNOs.to_csv(r'C:\Users\LYX\Desktop\测试文件夹\orderNos.csv',mode='w',header=True,index=None,encoding='gbk')

head2=FiledName.split(',',-1)
df_orderNOs_123=pd.DataFrame(orderNO,columns=head2)
df_orderNOs_123.to_csv(r'C:\Users\LYX\Desktop\测试文件夹\orderNos_123.csv',mode='w',header=True,index=None,encoding='gbk')

#对多个单号的订单再次查询
# sql='select * from yipin_accountcount where 基础业务订单号 in {0}'.format(orderNOs)
# cursor.execute(sql)

cursor.close 
conn.close 
