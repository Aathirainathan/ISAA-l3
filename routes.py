from flask import Flask,render_template, redirect, request,flash
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_USER']='1gHwgAeSYz'
app.config['MYSQL_PASSWORD']='jxlT9gsWiu'
app.config['MYSQL_HOST']='remotemysql.com'
app.config['MYSQL_DB']='1gHwgAeSYz'
# app.config['MYSQL_CURSORCLASS']= 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    try:
        cur= mysql.connection.cursor()
        print('Connection Successful!')
        try:            
            cur.close()
            print('Cursor closed')
        except:
            print('Unable to close cursor')
    except:
        print('Connection Failed!')


    # cur.execute('''CREATE TABLE example (id INTEGER)''')
    # cur.execute('''Insert into example(1)''')
    # mysql.connection.commit()

    # cur.execute('''Select * from example''')
    # results=cur.fetchall()
    # print(results)
    # return str(results[0][0])


    return 'Done!'

# @app.route('/')
# def home():
#     if(False):
#         return redirect('/signup')
#     return render_template("home.html")


# @app.route('/signup',methods=['POST','GET'])
# def signup():
#     if request.method=='POST':
#         data=request.form
#         email=data.get('email')
#         name=data.get('name')
#         password=data.get('password1')
#         password2=data.get('password2')
#         return redirect('/login')
#     return render_template("signup.html")

# @app.route('/login',methods=['POST','GET'])
# def login():
#     if request.method=='POST':
#         data=request.form
#         return redirect('/')
#     return render_template("login.html")

if __name__=='__main__':
    app.run(debug=True)