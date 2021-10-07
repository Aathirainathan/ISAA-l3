from flask import Flask,render_template, redirect, request,flash

app = Flask(__name__)

@app.route('/')
def home():
    if(False):
        return redirect('/signup')
    return render_template("home.html")


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        data=request.form
        email=data.get('email')
        name=data.get('name')
        password=data.get('password1')
        password2=data.get('password2')
        return redirect('/login')
    return render_template("signup.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        data=request.form
        return redirect('/')
    return render_template("login.html")

if __name__=='__main__':
    app.run(debug=True)