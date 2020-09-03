#!/usr/bin/env python
# coding: utf-8

# In[16]:


import pandas as pd

data = {'year':[2000,2001,2002,2001,2002],'value':[1.5,1.7,3.6,2.4,2.9]}

frame = pd.DataFrame(data)
print(frame)
print('='*20)
def testfunc(x, str):  #第一个参数代表该函数处理的每一个元素，第二个参数args是传入的参数
    print (x, str)


frame['year'].apply(testfunc, args = ('ok',)) #('ok',)表示一个参数
print ('=============' )

frame


# In[1]:


import pandas as pd 

df_salary=pd.read_excel(r'C:\Users\LYX\Desktop\花名册(1).xlsx',sheet_name=2)
df_salary.shape


# In[2]:


df_salary.head(5)


# In[3]:


import pandas as pd 
df_detail=pd.read_excel(r'C:\Users\LYX\Desktop\花名册(1).xlsx',sheet_name=0)
df_detail.shape


# In[8]:


df_attendance=pd.read_excel(r'C:\Users\LYX\Desktop\花名册(1).xlsx',sheet_name=1)
df_attendance.shape


# In[9]:


print(df_salary.columns)
print(df_detail.columns)
print(df_attendance.columns)


# In[35]:


df_new=pd.merge(df_salary.loc[:,['姓名','职务']],df_detail.loc[:,['姓名', '职位', '工号', '身份证号', '手机号', '入职时间', '转正时间', '离职时间', '试用期',
       '薪资待遇', '加班时薪', '餐补标准', '全勤标准']],how='left',left_on='姓名',right_on='姓名')
df_new=pd.merge(df_new,df_attendance.loc[:,['考勤月份','姓名','休息天数', '出勤', '补助工作日天数',
       '加班时长(小时)', '请假', '休息在岗', '年假', '计薪天数', '借支', '其他', '日报未交', '迟到 ', '缺卡' ]],how='outer',on='姓名')
df_new.dropna(axis=0,how='any',subset=['姓名'],inplace=True)
df_new.reset_index()
df_new.columns


# In[ ]:


def att_salary(att_day,basic_salry,month_day,)


# In[33]:


df_new.to_excel(r'C:\Users\LYX\Desktop\测试工资表.xlsx')
print('success')
df_new.head

