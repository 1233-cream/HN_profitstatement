import pandas as pd 
import numpy as np

def read_test(month,apartment='总公司',shop='全店铺'):
    reader=pd.read_excel(r'C:\Users\LYX\Desktop\八月\利润表\df_res.xlsx',sheet_name='明细表')
    reader['月份']=reader['所属日期'].apply(lambda x:str(x)[5:7] )
    reader=reader[reader['月份']==month]
    if apartment=='总公司':
        grouped=reader.groupby(['费用所属部门','费用所属店铺','一级科目','二级科目'],as_index=False)
        df=grouped.agg(np.sum)
        df_json=df.to_json(orient='records')
    return df_json