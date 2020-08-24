import pandas as pd 
import datetime as dt 
import numpy as np 

#读取费用明细文件
def df_read(filename):
    files_path=r'C:\Users\LYX\Desktop\测试文件夹\\'
    feedetail=filename
    df_original=pd.read_csv(files_path+feedetail,skip_blank_lines=True)
    df=df_original.dropna(how='all')           #清空空行
    df=df[df.审批状态=='完成'].reset_index()   #重置index
    df['审批编号']=df['审批编号'].astype(str)   #转换'审批编号'数据类型
    return df 