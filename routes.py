from flask import Flask,render_template, redirect, request,flash
from flask_mysqldb import MySQL
import MySQLdb.cursors


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
            #cur.execute("""INSERT INTO clients (id, email, password) VALUES (3,'kiran@gmail.com','kiran');""")
            #mysql.connection.commit()           
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
    return "done"

# @app.route('/')
# def home():
#     if(True):
#         return redirect('/signup')
#     return render_template("home.html")


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        data=request.form
        cemail=data.get('email')
        cname=data.get('name')
        cpassword=data.get('password1')
        password2=data.get('password2')

        try:
            cur= mysql.connection.cursor()
            print('Connection Successful!')
                
            try: 
                cur.ececute("""SELECT * FROM clients""")
                user = cur.fetchall()
                id=len(user)+1
                print("fetched id")
                cur.execute("""INSERT INTO clients ( id,email, password) VALUES (%s,%s,%s);""",(id,cemail,cpassword,))
                print("executed insertion")
                mysql.connection.commit()           
                cur.close()
                print('Cursor closed')
                return redirect('/login')
            except:
                print('Unable to close cursor')

        except:
            print('unable to connect')
        #return redirect('/login')

        #INSERT INTO `clients` (`id`, `email`, `password`) VALUES ('1', 'kapil@gmail.com', 'kapil'), ('2', 'vaya@gmail.com', 'vaya');
    return render_template("signup.html")



@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        data=request.form
        email=data.get('email')
        print(email)
        password=data.get('password')
        print(password)
        try:
            cur= mysql.connection.cursor()
            print('Connection Successful!')
            #return redirect('/')
            cur.execute('SELECT password FROM clients where email=%s;',(email,))
            pwd=cur.fetchone()
            print(pwd[0])
            print(password)
            if(pwd[0]==password):
                return redirect('/')
            else:
                return "invalid password"
        except:
            print('Connection Failed!')
        
            # if(cur.execute('''SELECT password FROM `clients` where email=email''')):
            #     pwd=cur.fetchall()
            # else:
            #     print("error in query")
            # if(pwd):
            #     if(pwd==password):
            #         return redirect('/')
            #     else:
            #         flash('invlaid password',category='error')
        
    return render_template("login.html")

@app.route('/home')
def home():
    try:
        cur= mysql.connection.cursor()
        print('Connection Successful!')

        try: 
            email='kapil@gmail.com'
            cur.execute("""Select * from clients where email=%s""",(email,))
            user=cur.fetchall()
            mysql.connection.commit() 
            id=user[0][0]
            print(id)
            cur.execute("""Select * from messages where id=%s""",(id,))
            messages=cur.fetchall()
            mysql.connection.commit()
            for i in messages:
                print(i[1])          
            cur.close()
            print('Cursor closed')
            #messages=["this is message 1","this is message 2"]
            return render_template('home.html',messages=messages)
        except:
            print('Unable to close cursor')
            return "unable to close cursor"
    except:
        print('Connection Failed!')
        return "connection failed"
    

if __name__=='__main__':
    app.secret_key="super secret key"
    app.run(debug=True)