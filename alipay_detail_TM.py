import pandas as pd 
import os
import numpy as np 
import re 
#大数据分块读取方法
def readcsv(file_path,name,chunk_size=100000):
    try:
        df=pd.read_csv(file_path,header=4,iterator=True,low_memory=False,chunksize=chunk_size)
        print('读取成功')
    except:
        df=pd.read_csv(file_path,header=4,iterator=True,low_memory=False,chunksize=chunk_size,encoding='gbk')
        print('读取成功')

    chunks=[]
    i=0

    #区分c类店铺与天猫店铺的账单
    for chunk in df:
        if '业务描述' in chunk.columns :
            chunks.append(chunk.reindex().loc[:,['业务描述','收入金额（+元）','支出金额（-元）']])
        else:
            def match_obj(text,reges_str=r"\d{0,5}[a-zA-Z\u4e00-\u9fa5]+\d{0,5}[a-zA-Z\u4e00-\u9fa5]+"):
                try:
                    k=re.findall(reges_str, text)[0]
                except:
                    k=''
                # finally:
                #     print('text:',text,'k:',k)
                return k 
            chunk['业务描述']=[match_obj(x) for x in chunk['备注']]
            chunks.append(chunk.reindex().loc[:,['业务描述','收入金额（+元）','支出金额（-元）']])
        i+=1
        print('完成第{}个区块添加'.format(i))
    
    df_result=pd.concat(chunks,ignore_index=True)
    

    return df_result




input_path=r'C:\Users\LYX\Desktop\九月\9月账单'
for root,dirs,files in os.walk(input_path,topdown=True):   #输入文件夹路径
    df_count=pd.DataFrame()
    for name in files:
#         print(name)
        file_path=os.path.join(root,name)
        if '汇总' in file_path or 'zip' in file_path:
            continue 
        print(file_path)

        # try:
        exec('''df_{0}=readcsv(file_path,name)
print(\'df_{0}\',\'success\')
grouped_{0}=df_{0}.groupby(['业务描述'],as_index=False)
grouped_{0}=grouped_{0}.agg(np.sum)
df_count=df_count.append(grouped_{0})
print(type(df_count))'''.format(name.split(".",-1)[0]))
        # except:
        #     print(name+'文件格式或编码错误')
    print('Next')
    try:
        df_count=df_count.groupby(['业务描述']).agg(np.sum)
        df_count.to_csv(r'C:\Users\LYX\Desktop\九月\newdirs\{0}.csv'.format(os.path.split(root)[1]),encoding='gbk')   #输出文件路径
        print('输出{0}成功'.format(os.path.split(root)[1]))
    except:
        print('输出{0}失败'.format(os.path.split(root)[1]))

print('='*50)