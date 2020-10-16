import pandas as pd 
import numpy as np

reader=pd.read_csv(r'C:\Users\LYX\Desktop\阿里销售明细2.csv')

alist=['义乌市海纳日用品有限公司','余姚市聚邦电器有限公司','金华市净腾卫浴洁具有限公司']
blist=['将驰电子商务','新团日用百货有限公司']

df=reader[reader['店铺'].isin(alist+blist)]
df=df.loc[:,['店铺','业务员','分摊后应收合计']]
df['业务员']=df['业务员'].astype('str')

def seller(shopname,seller):
    if shopname in alist:
        if seller in ['009','010']:
            k=seller
        else:
            k='none'
    elif shopname in blist:
        if seller in ['006','013']:
            k=seller
        else:
            k='none'
    else:
        pass
    return k
df['业务员']=df.apply(lambda x:seller(x['店铺'],x['业务员']),axis=1)

def sgroup(shopname):
    if shopname  in alist:
        return 'A'
    elif shopname in blist:
        return 'B'
    else:
        return 'Others'
df['组']=df['店铺'].apply(lambda x: sgroup(x))

grouped=df.groupby(['组','店铺','业务员'],as_index=False)
result=grouped.agg(np.sum)
#print(result.shape)

#提成金额计算
grouped1=result.groupby(['组','业务员'],as_index=False)
result2=grouped1.agg(np.sum)
def pushmoney_base(result2,group,seller):
    if seller!='none':
        # grouped1=result.groupby(['组','业务员'],as_index=False)
        # result2=grouped1.agg(np.sum)
        # print(result2)
        pbase1=result2[(result2['业务员']==seller)&(result2['组']==group)].iloc[0,2]
        pbase2=result2[(result2['业务员']=='none')&(result2['组']==group)].iloc[0,2]
        pbase3=result2[(result2['业务员']!=(seller or 'none'))&(result2['组']==group)].iloc[0,2]
        pbase=(pbase1*0.7+pbase3*0.3+pbase2/2)-300000
    #     print('base1:{},base2:{},base3:{},base:{}'.format(base1,base2,base3,base))
    else:
        pbase=0
    #print(base)
    return pbase 
result2['提成基数']=result2.apply(lambda x: pushmoney_base(result2,x['组'],x['业务员']),axis=1)
result2=result2[result2['业务员']!='none'].drop(columns=['分摊后应收合计'])
dic_seller={
    '006':'章小利',
    '013':'张若',
    '009':'彭丝',
    '010':'周双'
}
def dict1(seller):
    return dic_seller[seller]
#计算提成金额并将业务员代码修改为业务员姓名
result2['业务员']=result2['业务员'].apply(lambda x :dict1(x))

#录入绩效
def proformance(seller):
    proformance=float(input('请输入{}的绩效(%):'.format(seller)))
    if proformance==0:
        proformance=100
    return proformance
result2['绩效']=result2.apply(lambda x: proformance(x['业务员']),axis=1)
result2['提成金额']=round(result2['提成基数']*5/1000*result2['绩效']/100,0)
result=result.rename({'分摊后应收合计':'销售额'},axis=1)

writer=pd.ExcelWriter(r'C:\Users\LYX\Desktop\result.xlsx')
result.to_excel(writer,sheet_name='总览',index=False)
result2.to_excel(writer,sheet_name='提成表',index=False)

writer.save()
writer.close()

#print(result)
