from flask import Flask,request,jsonify,render_template
#import dingtalk_data as dt
import json 
import werkzeug 
import os
import sys 
from express_recount_copy import express_recount
import numpy
import decimal 
#重写MyEncoder
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        elif isinstance(obj,decimal.Decimal):
            return float(obj)
        else:
            return super(MyEncoder, self).default(obj)

app=Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/hello')
def hello():
    return 'Hello World'

    
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
      f.save(os.path.join( os.path.split(sys.argv[0])[0],'temp_file',f.filename))
      dic_result=express_recount(os.path.join( os.path.split(sys.argv[0])[0],'temp_file',f.filename))
      return json.dumps({
          'code':"1",
          'data':dic_result,
          'msg':'succee'
          },cls=MyEncoder)   


@app.route('/reader',methods=['POST'])
def reader():
    from df_test import read_test
    data=json.loads(request.get_data(as_text=True))
    month_select=data['month']
    apartment_select=data['apartment']
    shop_select=data['shop']
    df_json=read_test(month_select,apartment_select)
    return df_json

@app.route('/return',methods=['GET','POST'])
def reback():
    data=json.loads(request.get_data(as_text=True))
    return data['name']

@app.route('/proformance',methods=['POST'])
def proformance():
    pass


if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()
    #app.run()
    