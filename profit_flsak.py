from flask import Flask 
import dingtalk_data as dt
import json 

app=Flask(__name__)

@app.route('/')
def helloworld():
    return 'Hello World!'


@app.route('/doge')
def doge():
    return '你是狗崽子吗!'


@app.route('/fee_test')
def fee_test():
    df=dt.df_read('test_feedetail.csv')
    a=[]
    for i in df.iloc[2:5,2]:
        a.append(i) 
    tuple_a={
        'code':1,
        'data':a,
        'msg':'success'
    }
    return tuple_a





if __name__ == '__main__':
    app.run(debug=True)