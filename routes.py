from flask import Flask,render_template, redirect, request,flash,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from cryptography.fernet import Fernet
from flask_bcrypt import Bcrypt

app = Flask(__name__)

key=b'zHkzFtBbF7iAC_LGYWT8iQzP9gt2NFi8TVYAZdamgNY='

app.config['MYSQL_USER']='1gHwgAeSYz'
app.config['MYSQL_PASSWORD']='jxlT9gsWiu'
app.config['MYSQL_HOST']='remotemysql.com'
app.config['MYSQL_DB']='1gHwgAeSYz'
# app.config['MYSQL_CURSORCLASS']= 'DictCursor'

mysql = MySQL(app)
bcrypt=Bcrypt(app)

@app.route('/')
def index():
    return redirect('/home')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=='POST':
        data=request.form
        email=data.get('email')
        name=data.get('name')
        password=data.get('password1')
        passwordHash=bcrypt.generate_password_hash(password)
        
        try:
            cur= mysql.connection.cursor()
            print('Connection Successful!')
            try: 
                cur.execute("""SELECT * FROM clients""")
                clientData=cur.fetchall()
                mysql.connection.commit() 
                # id=len(clientData)+2
                # print(id)
                print("fetched id")
                cur.execute("""INSERT INTO clients (email, password) VALUES (%s,%s)""",(email,passwordHash,))
                mysql.connection.commit() 
                print("executed insertion")          
                cur.close()
                print('Cursor closed')
                return redirect('/login')
            except:
                print('Unable to close cursor')
                return "unable to close cursor"
        except:
            print('Connection Failed!')
            return "connection failed"
    return render_template("signup.html")
    
        # try:
        #     cur= mysql.connection.cursor()
        #     print('Connection Successful!')
            
        #     cur.ececute("""SELECT * FROM clients""")
        #     user = cur.fetchall()
        #     mysql.connection.commit()
        #     id=5
        #     print("fetched id")
        #     cur.execute("""INSERT INTO clients ( id,email, password) VALUES (%s,%s,%s)""",(id,cemail,cpassword,))
        #     print("executed insertion")
        #     mysql.connection.commit()           
        #     cur.close()
        #     print('Cursor closed')
        #     return redirect('/login')
        # except:
        #     print('unable to connect')

        #return redirect('/login')

        #INSERT INTO `clients` (`id`, `email`, `password`) VALUES ('1', 'kapil@gmail.com', 'kapil'), ('2', 'vaya@gmail.com', 'vaya');



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
            cur.execute("""SELECT * FROM clients where email=%s""",(email,))
            clientData=cur.fetchall()
            print(clientData)
            print(clientData[0][2])
            print(password)
            if(bcrypt.check_password_hash(clientData[0][2],password)):
                session['id']=clientData[0][0]
                session['email']=clientData[0][1]
                return redirect('/')
            else:
                return "invalid password"
        except:
            print('Connection Failed!')
    return render_template("login.html")
    

            # if(cur.execute('''SELECT password FROM `clients` where email=email''')):
            #     pwd=cur.fetchall()
            # else:
            #     print("error in query")
            # if(pwd):
            #     if(pwd==password):
            #         return redirect('/')
            #     else:
            #         flash('invlaid password',category='error')

@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
    if 'id' in session:
        session.pop('id')  
    return redirect('/login') 


@app.route('/home',methods=['POST','GET'])
def home():
    if 'id' not in session:
        print("not signed in")
        return redirect('/login')
    else:
        print(session['id'])
        if request.method=='POST':
            data=request.form
            topic=data.get('Topic')
            desc=data.get('description')
            fernet=Fernet(key)
            message=fernet.encrypt(desc.encode('utf-8'))
            id=session['id']
            print(id,topic, message)
        #password2=data.get('password2')
            try:
                cur= mysql.connection.cursor()
                print('Connection Successful!')
                try: 
                    cur.execute("""INSERT INTO messages ( id,title, description) VALUES (%s,%s,%s)""",(id,topic,message,))
                    mysql.connection.commit() 
                    print("executed insertion")          
                    cur.close()
                    print('Cursor closed')
                    return redirect('/home')
                except:
                    print('Unable to close cursor')
                    return "unable to close cursor"
            except:
                print('Connection Failed!')
                return "connection failed"

        else:
            try:
                cur= mysql.connection.cursor()
                print('Connection Successful!')
                try: 
            #email='kapil@gmail.com'
                    cur.execute("""Select * from clients""")
            # cur.execute("""Select * from clients where email=%s""",(email,))
                    mysql.connection.commit() 
                    user=cur.fetchall()
                    id=user[1][0]
                    print(id)
                    cur.execute("""Select * from messages where id=%s""",(id,))
                    messages=cur.fetchall()
                    mysql.connection.commit()
                    #print(messages[0][2])

                    newmess=[]
                    fernet=Fernet(key)
                    for i in range(len(messages)):
                        print(messages[i][2])
                        mess=fernet.decrypt(messages[i][2].encode()).decode()
                        print(mess)
                        newmess.insert(i,mess)
                    for i in newmess:
                        print(i)
                    cur.close()
                    print('Cursor closed')
            #messages=["this is message 1","this is message 2"]
                    return render_template('home.html',messages=newmess)
                except:
                    print('Unable to close cursor')
                    return "unable to close cursor"
            except:
                print('Connection Failed!')
                return "connection failed"

    
    

@app.route('/decrypt')
def decrypt():
    return render_template("decryption.html")

if __name__=='__main__':
    app.secret_key="super secret key"
    app.run(debug=True)