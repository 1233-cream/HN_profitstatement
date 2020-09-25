import pandas as pd 


def files_read(file_path,chunkSize=100000,skiprows=0,colname=[]):
    file_path=file_path
    chunks=[]
    chunksrows=0
    try:
        reader=pd.read_csv(file_path,skiprows=skiprows,iterator=True,chunksize=chunkSize,low_memory=False)
        for chunk in reader:
            chunks.append(chunk.loc[:,['店铺','物流单号']])
            chunksrows+=chunkSize
            print('已完成{}行数据导入'.format(chunksrows))
        df=pd.concat(chunks,ignore_index=True)
    except:
        reader=pd.read_csv(file_path,skiprows=skiprows,iterator=True,chunksize=chunkSize,low_memory=False)
        for chunk in reader:
            chunks.append(chunk)
            chunksrows+=chunkSize
            print('已完成{}行数据导入'.format(chunksrows))
        df=pd.concat(chunks,ignore_index=True)
    #df=df.dropna(axis=0,subset=['发生时间'])
    print(df.shape)
    print(df.columns)
    return df

file_path_sellsdetail=r'C:\Users\LYX\Desktop\八月\八月销售明细(成交时间)\August\august_all.csv'
file_path_ytexpress=r'C:\Users\LYX\Desktop\yt\续重费.csv'

df_sellsdetail=files_read(file_path_sellsdetail)
df_sellsdetail2=df_sellsdetail.loc[:,['店铺','物流单号']]
df_ytexpress=files_read(file_path_ytexpress)
result=pd.merge(df_sellsdetail2,df_ytexpress,how='right',left_on='物流单号',right_on='运单号码')
result=result.drop_duplicates('运单号码')


print(result.shape)
result.to_csv(r'C:\Users\LYX\Desktop\yt_detail.csv')
