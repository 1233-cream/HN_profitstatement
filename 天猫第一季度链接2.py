import pandas as pd 
import numpy as np 
import pymysql 



conn=pymysql.connect(
    host='localhost',
    database='yipin_2020',
    user='root',
    password='root'
    )
cursor=conn.cursor()


sql=('''select 
sum(a.`收入金额`),
sum(a.`支出金额`),
a.`业务基础订单号`,
b.`原始单号`,
b.`物流方式`,
b.`物流单号`,
b.`交易名`
from 
`yipin_01-04` a 
join sellscount b
on a.`业务基础订单号`=b.`原始单号` 
where a.`业务基础订单号` is not null 
and a.`业务基础订单号`!=""
group by a.`业务基础订单号`
''')
cursor.execute(sql)
results_orderno_alone=cursor.fetchall()
head=['收入总金额','支出总金额','业务基础订单号','原始单号','物流方式','物流单号','交易名']
df_res_alone=pd.DataFrame(results_orderno_alone,columns=head)
print(len(df_res_alone))

df_res_alone.to_csv(r'C:\Users\LYX\Desktop\测试文件夹\res_alone.csv',encoding='GBK',header=head,index=None)
