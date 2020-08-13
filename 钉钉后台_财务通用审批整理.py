import pandas as pd 
import datetime as dt 
import numpy as np 

#读取费用明细文件
files_path=r'C:\Users\LYX\Desktop\测试文件夹\\'
feedetail='test_feedetail.csv'
df_original=pd.read_csv(files_path+feedetail,skip_blank_lines=True)
df=df_original.dropna(how='all')           #清空空行
df=df[df.审批状态=='完成'].reset_index()   #重置index
df['审批编号']=df['审批编号'].astype(str)   #转换'审批编号'数据类型

print(df.columns)    #打印数据帧字段名
df.所属日期=pd.to_datetime(df.所属日期)   #转化所属时间为datetime


#确定上下界日期
lbound_date=dt.datetime(2020,7,1)   #设置下确界
ubound_date=dt.datetime(2020,7,31)   #设置上确界
df=df[(df.所属日期<=ubound_date)&(df.所属日期>=lbound_date)]   #筛选上下界日期内的明细
#print(lbound_date,ubound_date)
df_shop=df[df.费用所属店铺.notnull()]   #得到属于店铺费用表

#定义isnotin方法
def isnotin(a,b):
    if a in b:
        return False
    else:
        return True
list1=['总公司','店铺专属,不分摊','金华仓','义乌仓']   
df_dpmt=df[(df.费用所属部门.map(lambda x:isnotin(x,list1)))]    #得到属于部门费用
df_comp=df[(df.费用所属部门=='总公司')]  #总公司所属费用
df_warehJH=df[(df.费用所属部门=='金华仓')]   #金华仓所属费用
df_warehYW=df[df.费用所属部门=='义乌仓']   #义乌仓所属费用
#print(df_dpmt)

#打印excel文件
list_df=['df_shop','df_dpmt','df_comp','df_warehJH','df_warehYW']
#循环打印DataFrame
writer=pd.ExcelWriter('C:/Users/LYX/Desktop/测试文件夹/output.xlsx')   # pylint: disable=abstract-class-instantiated
df_original.to_excel(writer,index=0,sheet_name='df_original')
for i in list_df:
    list_shop_groupby=['费用所属部门','费用所属店铺','一级科目','二级科目','三级科目']
    list_others_groupby=['费用所属部门','一级科目','二级科目','三级科目']   #groupby中有空字段无法处理
    #print(i[3:])
    exec("""if '{0}'=='shop':
    list_groupby=list_shop_groupby
else:
    list_groupby=list_others_groupby
grouped_{0}= df_{0}.groupby(list_groupby,as_index=False)

df_out_{0}=grouped_{0}.agg(np.sum)
try:
    df_out_{0}.to_excel(writer,index=0,sheet_name='df_{0}')
    print('{0}打印完成')
except:
    pass
""".format(i[3:]))
writer.save()
writer.close()



#读取店铺列表
file_shoplist='shoplist.csv'
df_shoplist=pd.read_csv(files_path+file_shoplist,index='店铺名')