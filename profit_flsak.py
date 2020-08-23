from flask import Flask 
import dingtalk_data as dt


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
    for i in df.iloc[:,1]:
        a=a.append.i 
    return a





if __name__ == '__main__':
    app.run(debug=True)