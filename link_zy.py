import pandas as pd 
import numpy as np 

#读取三个文件:支付宝账单,网店管家销售明细,快递账单

def file_read(file_path,col_list=[],skiprows=0,header=0,chunkSize=100000):
    reader=pd.read_csv(file_path,low_memory=False,iterator=True,skiprows=skiprows,chunksize=chunkSize,delimiter=',',header=header)
    chunks=[]
    if len(col_list)==0:
        for chunk in reader:
            chunks.append(chunk)
            # print(chunk.columns) 
            print('写入')
    else:
        for chunk in reader:
            chunks.append(chunk.loc[:,col_list])
            print('写入选定字段')
    
    df=pd.concat(chunks,ignore_index=True)
    df=df.dropna(how='all')
    df=df.reset_index()
    print(df.columns)
    return df

file_path_sellsdetail=r'C:\Users\LYX\Desktop\链接文件夹\july_sellsdetail.csv'
file_path_alipay=r'C:\Users\LYX\Desktop\链接文件夹\july_alipay.csv'
df_sellsdetail=file_read(file_path_sellsdetail,col_list=['店铺','订单编号','原始单号','物流单号','货品编号','数量','应收合计分摊','成本','交易名'])
df_alipay=file_read(file_path_alipay,skiprows=4,header=0,col_list=['账务流水号','收入金额（+元）','支出金额（-元）','业务描述','业务基础订单号'])  

print(df_sellsdetail.shape,df_alipay.shape) 

grouped_alipay=df_alipay.groupby(['账务流水号','业务基础订单号'])
grouped_alipay=grouped_alipay.agg(np.sum)

grouped_alipay.to_csv(r'C:\Users\LYX\Desktop\链接文件夹\out.csv')