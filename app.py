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
            email="kapil@gmail.com"
            # cur.execute("""Select * from clients where email=%s""",(email,))
            # user=cur.fetchall()
            # mysql.connection.commit() 
            # for i in user:
            #     print(i[2])    
            id=1
            cur.execute("""Select * from messages where id=%s""",(id,))
            messages=cur.fetchall()
            mysql.connection.commit()
            for i in messages:
                print(i[1])          
            cur.close()      
            print('Cursor closed')
        except:
            print('Unable to close cursor')
    except:
        print('Connection Failed!')
    return "done"
    

@app.route('/signup',methods=['POST','GET'])
def signup():
   return signup



@app.route('/login',methods=['POST','GET'])
def login():
    return login


if __name__=='__main__':
    app.secret_key="super secret key"
    app.run(debug=True)