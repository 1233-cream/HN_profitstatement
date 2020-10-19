import pandas as pd 
import decimal
import math
import numpy as np 
import os
import sys 
def express_recount(file_path):
    reader=pd.read_csv(file_path,chunksize=100000,iterator=True)

    #print('读取完成')
    chunks=[]
    for chunk in reader:
        chunks.append(chunk)
    df=pd.concat(chunks,ignore_index=True)
    #print(df.columns)
    df=df.dropna(how='all')
    tariff=pd.read_csv(os.path.join(os.path.split(sys.argv[0])[0],'data','price_express.csv'),index_col=0)
    special_area=['海南省','新疆维吾尔自治区','西藏自治区']
    def con_cost(weight,city):
        con_fee=0
        if city not in special_area:
            if weight<=3:
                con_fee=0
            else:
                con_fee=tariff.loc[city,'续重费']*weight
        else:
            con_fee=tariff.loc[city,'续重费']*weight
        con_fee=decimal.Decimal.from_float(con_fee).quantize(decimal.Decimal('0.000'))
        return con_fee 

    df['续重费']=df.apply(lambda x:con_cost(x['计费重量（kg）'],x['计费省份']),axis=1)
    #print('续重费计算完成')
    def surcharges(weight,city):
        surcharge=0
        if city=='北京':
            surcharge=0.8+int(weight)*0.5
        if city=='上海':
            surcharge=0.5+int(weight)*0.2
        surcharge=decimal.Decimal.from_float(surcharge).quantize(decimal.Decimal('0.000'))
        return surcharge


    df['附加费2']=df.apply(lambda x:surcharges(x['计费重量（kg）'],x['计费省份']),axis=1)
    #print('附加费计算完成')


    df['超重派送费2']=df.apply(lambda x:decimal.Decimal.from_float(x['计费重量（kg）']*0.1).\
        quantize(decimal.Decimal('0.000')) if x['计费重量（kg）']>2 else 0,axis=1)
    #print(df['超重派送费2'].dtypes)
    #print('超重派送费计算完成')


    sum_xzf=df['续重费'].sum()
    sum_fjf=df['附加费2'].sum()
    sum_psf=df['超重派送费2'].sum()
    count_avg=df[(df['计费重量（kg）']<=3)&(df['计费省份'].\
        map(lambda x : x not in ['海南省','新疆维吾尔自治区','西藏自治区']))].loc[:,'计费重量（kg）'].count()
    mean_avg=df[(df['计费重量（kg）']<=3)&(df['计费省份'].\
        map(lambda x : x not in ['海南省','新疆维吾尔自治区','西藏自治区']))].loc[:,'计费重量（kg）'].mean()
    avg_cost=round((mean_avg-0.4)*count_avg,2)

    # sum_xzf=float(sum_xzf)
    # sum_fjf=float(sum_fjf)
    # sum_psf=float(sum_psf)
    # count_avg=float(count_avg)
    # mean_avg=float(mean_avg)
    # avg_cost=float(avg_cost)


    dic_result={
        '续重费':sum_xzf,
        '附加费':sum_fjf,
        '超重派送费':sum_psf,
        '均重件数':count_avg,
        '平均重量':mean_avg,
        '超均重费':avg_cost
    }
    return dic_result
# print('续重费:{}\n附加费:{}\n超重派送费:{}'.format(sum_xzf,sum_fjf,sum_psf))
# print('均重件共{}件,平均重量为{}\n超均重费为{}'.format(count_avg,mean_avg,avg_cost))
