
import pandas as pd 

def proportion(file_path,sheet_name='Sheet1'):
    df_sndcount=pd.read_excel(file_path,encoding='gbk',sheet_name=sheet_name)
    df_sc=df_sndcount.loc[:,['店铺名','金华仓订单量','义乌仓订单量']]
    df_sc.loc[df_sc['义乌仓订单量'].isnull(),'义乌仓订单量']=0
    df_sc['总单量']=df_sc[['金华仓订单量','义乌仓订单量']].apply(lambda x:x['金华仓订单量']+x['义乌仓订单量'],axis=1)

    df_sc=df_sc.drop(df_sc[df_sc.总单量==0].index)
    sum_sc=df_sc['总单量'].sum()
    sum_sc_yw=df_sc['义乌仓订单量'].sum()
    sum_sc_jh=df_sc['金华仓订单量'].sum()
    print(sum_sc,sum_sc_yw,sum_sc_jh)

    df_sc['金华仓分摊比例']=df_sc.apply(lambda x:x['金华仓订单量']/sum_sc_jh,axis=1)
    df_sc['义乌仓分摊比例']=df_sc.apply(lambda x:x['义乌仓订单量']/sum_sc_yw,axis=1)
    df_sc['总公司分摊比例']=df_sc.apply(lambda x:x['总单量']/sum_sc,axis=1)
    # df_sc['部门内部分摊比例']=df_sc.apply(lambda  x:x['总单量']/df_sc[df_sc['部门']==x['部门']].loc[:,'总单量'].sum(),axis=1)
    return df_sc 

def department(file_path,sheet_name='Sheet1'):
    df_read=pd.read_excel(file_path,encoding='gbk',sheet_name=sheet_name)
    df_dpt=df_read.loc[:,['部门','店铺名','店铺编号']]

    return df_dpt 

def feedetail(file_path,sheet_name='Sheet1'):
    df_read=pd.read_excel(file_path,sheet_name=sheet_name,encoding='gbk')
    df_read['所属日期']=pd.to_datetime(df_read['所属日期'])
    print(df_read['所属日期'].dtype)
    df_fdl=df_read[(df_read['审批结果']=='同意')&(df_read['审批状态']=='完成')&(df_read['记账金额（元）'].notnull())].\
        loc[:,['审批编号','摘要','记账金额（元）','费用所属部门','费用所属店铺','一级科目',
    '二级科目','三级科目','所属日期']]
    df_fdl=df_fdl[(df_fdl['所属日期'].map(lambda x:x.strftime('%m'))=='09')]
    return df_fdl 

file_path_proportion=r'C:\Users\LYX\Desktop\九月\利润表\发货单量表.xlsx'
file_path_department=r'C:\Users\LYX\Desktop\八月\利润表准备文件夹\部门_店铺.xlsx'
file_path_feedetail=r'C:\Users\LYX\Desktop\九月钉钉数据.xlsx'
df_fdl=feedetail(file_path_feedetail,sheet_name='数据汇总')
df_sc=proportion(file_path_proportion,sheet_name='Sheet3')
df_dpt=department(file_path_department,sheet_name='数据段1')

# print(df_fdl.columns) 

df_sc=df_sc.merge(df_dpt,how='left',left_on='店铺名',right_on='店铺名')
df_sc['部门内部分摊比例']=df_sc.apply(lambda  x:x['总单量']/df_sc[df_sc['部门']==x['部门']].loc[:,'总单量'].sum(),axis=1)

df_fdl=df_fdl.merge(df_dpt,how='left',left_on='费用所属店铺',right_on='店铺编号')
df_fdl['部门']=df_fdl.apply(lambda x:x['费用所属部门'] if x['费用所属部门']!='店铺专属,不分摊' else x['部门'],axis=1)

df_res=pd.DataFrame(columns=df_fdl.columns)

k=df_fdl.shape[0]
i=0
for date,rows in df_fdl.iterrows():
    mon=rows['记账金额（元）']
    if rows['费用所属部门']=='店铺专属,不分摊':
        rows['费用所属部门']=rows['部门']
        df_res.loc[df_res.shape[0]]=rows
    elif rows['费用所属部门']=='总公司':
        for date2,rows2 in df_sc.iterrows():
            rows['记账金额（元）']=mon*rows2['总公司分摊比例']
            rows['费用所属店铺']=rows2['店铺编号']
            rows['费用所属部门']=rows2['部门']
            df_res.loc[df_res.shape[0]]=rows
    elif rows['费用所属部门']=='金华仓': 
        for date2,rows2 in df_sc.iterrows():
            rows['记账金额（元）']=mon*rows2['金华仓分摊比例']
            rows['费用所属店铺']=rows2['店铺编号']
            rows['一级科目']='5602-管理费用'
            rows['二级科目']='5602004-仓储费用'
            rows['三级科目']='5602004001-金华仓仓储费用'
            rows['费用所属部门']=rows2['部门']
            df_res.loc[df_res.shape[0]]=rows
    elif rows['费用所属部门']=='义乌仓': 
        for date2,rows2 in df_sc.iterrows():
            rows['记账金额（元）']=mon*rows2['义乌仓分摊比例']
            rows['费用所属店铺']=rows2['店铺编号']
            rows['一级科目']='5602-管理费用'
            rows['二级科目']='5602004-仓储费用'
            rows['三级科目']='5602004001-义乌仓仓储费用'
            rows['费用所属部门']=rows2['部门']
            df_res.loc[df_res.shape[0]]=rows
    else:
        for date2,rows2 in df_sc[df_sc['部门']==rows['费用所属部门']].iterrows():
            rows['记账金额（元）']=mon*rows2['部门内部分摊比例']
            rows['费用所属店铺']=rows2['店铺编号']
            rows['费用所属部门']=rows2['部门']
            df_res.loc[df_res.shape[0]]=rows
    i+=1
    if i%10==0:
        print('已完成{0}%'.format(round(i/k*100,2)))

#调整数字方向
df_res['记账金额（元）']=df_res.apply(lambda x:x['记账金额（元）'] if x['二级科目'] in\
     ['5001001-营业收入','5401002-退货'] else x['记账金额（元）']*(-1) ,axis=1)



df_fdl.to_excel(r'C:\Users\LYX\Desktop\九月\利润表\df_fdl.xlsx',encoding='gbk',index=None)
df_sc.to_excel(r'C:\Users\LYX\Desktop\九月\利润表\df_sc.xlsx',encoding='gbk',index=None)
df_res.to_excel(r'C:\Users\LYX\Desktop\九月\利润表\df_res.xlsx',encoding='gbk',index=None)