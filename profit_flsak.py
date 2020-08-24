from flask import Flask,request,jsonify 
import dingtalk_data as dt
import json 

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False

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


@app.route('/test',methods=['POST'])
def post_data():
    #print('hh')
    data1=json.loads(request.get_data())
    postdata = data1['id']+'321'
    #file = request.files['file']
    recognize_info = {'id': postdata}
    return jsonify(recognize_info), 201


if __name__ == '__main__':
    app.run(debug=True)