import pandas as pd 

df_salary=pd.read_excel(r'C:\Users\LYX\Desktop\花名册(1).xlsx',sheet_name=2)
df_detail=pd.read_excel(r'C:\Users\LYX\Desktop\花名册(1).xlsx',sheet_name=0)
df_attendance=pd.read_excel(r'C:\Users\LYX\Desktop\花名册(1).xlsx',sheet_name=1)

# print(df_salary.columns)
# print(df_detail.columns)
# print(df_attendance.columns)

df_new=pd.merge(df_salary.loc[:,['姓名','职务']],df_detail.loc[:,['姓名', '职位', '工号', '身份证号', '手机号', '入职时间', '转正时间', '离职时间', '试用期',
       '薪资待遇', '加班时薪', '餐补标准', '全勤标准']],how='left',left_on='姓名',right_on='姓名')
df_new=pd.merge(df_new,df_attendance.loc[:,['考勤月份','姓名','休息天数', '出勤', '补助工作日天数',
       '加班时长(小时)', '请假', '休息在岗', '年假', '计薪天数', '借支', '其他', '日报未交', '迟到 ', '缺卡' ]],how='outer',on='姓名')
df_new.dropna(axis=0,how='any',subset=['姓名'],inplace=True)
df_new.reset_index()

def att_salary(att_day,probation_salary,basic_salry,s_month,emtry_day):
       if month()



df_new.to_excel(r'C:\Users\LYX\Desktop\测试工资表.xlsx')
print('success')
