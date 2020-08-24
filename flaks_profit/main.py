import flask
import json 
#import dingtalk_data as dt 

app=flask.Flask(__name__)
app.config ['JSON_AS_ASCII']=False



@app.route('/test',methods=['POST'])
def respones_post():
    post_data=flask.request.form['shopname']
    file=flask.request.files['files']
    file_name=file.filename
    file_name=file_name[file_name.index('.')+1:]
    recognize_info={'shopname':post_data,'file_name':file_name}
    return flask.jsonify(recognize_info),201



if __name__=='__main__':
    app.run(debug=True)