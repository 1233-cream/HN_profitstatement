from flask import Flask,request,jsonify,render_template
#import dingtalk_data as dt
import json 
import werkzeug 
import os
from express_recount_copy import express_recount
import numpy

#重写MyEncoder
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        # elif isinstance(obj,decimal):
        #     return float(obj)
        else:
            return super(MyEncoder, self).default(obj)

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def helloworld():
    return 'Hello World!'


@app.route('/doge')
def doge():
    return '你是狗崽子吗!'


# @app.route('/fee_test')
# def fee_test():
#     df=dt.df_read('test_feedetail.csv')
#     a=[]
#     for i in df.iloc[2:5,2]:
#         a.append(i) 
#     tuple_a={
#         'code':1,
#         'data':a,
#         'msg':'success'
#     }
#     return tuple_a


@app.route('/test',methods=['POST'])
def post_data():
    #print('hh')
    # data1=json.loads(request.get_data())
    postdata = int(request.form['id'])+666
    #file = request.files['file']
    recognize_info = {'id': postdata}
    return jsonify(recognize_info), 201

#form信息传递
@app.route('/student')
def student():
    return render_template("student.html")

@app.route('/result',methods=['GET','POST'])
def result():
    if request.method=='POST':
        result=request.form 
        return render_template('result.html',result=result)
    
@app.route('/upload')
def upload_file():
   return render_template('upload.html')

#文件的接受和保存
@app.route('/uploader',methods=['GET','POST'])
def uploader():
   if request.method == 'POST':
      f = request.files['file']
      f.save(os.path.join( r'D:/代码库/temp_files/',f.filename))
      dic_result=express_recount(os.path.join( r'D:/代码库/temp_files/',f.filename))
      return json.dumps(dic_result,cls=MyEncoder)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9000,debug=True)