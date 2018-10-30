from flask import Flask,render_template,url_for,request,redirect

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('test.html')

@app.route('/posttest',methods = ['POST'])
def posttest():
    print(request.form.getlist('ch'))
    return "ok"


if __name__ == '__main__':
    app.run(debug=True)
