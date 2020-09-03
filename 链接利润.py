import pandas as pd 
import numpy as np 
import pymysql

#读取目标文件
df=pd.read_csv(r'C:\Users\LYX\Desktop\data_222.csv')
print(df.shape)
list_originalorderno=df.loc[:,['订单编号','原始单号']]
list1=[]
for row in list_originalorderno.iterrows():
    orders=row[1][1].split(',',-1)
    for i in orders:
        list1.append((row[1][0],i))

print(df.columns.values) 
print(len(list1)) 
df_list1=pd.DataFrame(list1,columns=['订单编号','原始单号'],index=None)
#df_list1.to_csv(r'C:\Users\LYX\Desktop\data_333.csv')
conn3=pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='sellsdetail'
)
# sql_goods='select 订单编号,原始单号 from sellsdetail where 交易名 regexp \'卫生间置物架免打孔厕所洗手间洗漱台用品浴室收纳架洗澡间壁挂式\''

#生成已结算的订单的支付宝账单
conn=pymysql.connect(
    host='localhost',
    user='root',password='root',
    database='yipin_2020'
)
cur=conn.cursor()
#sql_blank='update yipin_alipay_july set `业务基础订单号`=replace(`业务基础订单号`,\'	\',\'\')'

#cur.execute(sql_blank)
#conn.commit()
#list_selection='|'.join(list1)
sql='select `业务基础订单号`,`业务描述`,`收入金额`,`支出金额` from yipin_alipay_july where `业务基础订单号` in {0} '.format(tuple(df_list1.loc[:,'原始单号']))

cur.execute(sql)  #创建游标

res=cur.fetchall()

df_res=pd.DataFrame(res)

head=['业务基础订单号','业务描述','收入金额','支出金额']

df_res.columns=head
#df_res.to_csv(r'C:\Users\LYX\Desktop\测试文件夹\0809.csv')
grouped1=df_res.groupby('业务基础订单号',as_index=False).agg(np.sum)
grouped1.to_csv(r'C:\Users\LYX\Desktop\测试文件夹\s\goruped1.csv')
#grouped_res=df_res.groupby('业务描述',as_index=False).agg(np.sum)
#grouped_res.to_csv(r'C:\Users\LYX\Desktop\测试文件夹\0809.csv')  
sql_set='set global max_allowed_packet = 1024*1024*1024;'

#生成已结算订单货品及成本明细表
conn2=pymysql.connect(
    host='localhost',
    user='root',
    password='root',
    database='sellsdetail'
)
cur2=conn2.cursor()   #创建游标

order_list=df_list1.loc[:,'订单编号']
select_list=['订单编号','原始单号','订单类型','订单状态','货品编号','品名','规格','物流单号','数量','分摊后应收合计']
try:
    del a
except:
    pass
a=''
a=','.join(select_list)

sql='select {1} from july_tm where `订单编号` in {0} '.format(tuple(order_list),a)
cur.execute(sql_set)
conn.commit()
cur2.execute(sql)

res=cur2.fetchall()

df_res2=pd.DataFrame(res)
df_res2.columns=select_list
df_res2.to_csv(r'C:\Users\LYX\Desktop\测试文件夹\s\df_res2.csv')
grouped2=df_res2.loc[:,['订单类型','订单状态','货品编号','品名','规格','数量']].groupby(['订单类型','订单状态','货品编号','品名','规格'],as_index=False).agg(np.sum) 
grouped2.to_csv(r'C:\Users\LYX\Desktop\测试文件夹\s\goruped2.csv')


cur.close
cur2.close
conn.close
conn2.close