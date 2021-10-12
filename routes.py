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

mysql = MySQL(app)
bcrypt=Bcrypt(app)

@app.route('/')
def index():
    return redirect('/home')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if 'id' in session:
        return redirect('/home')
    else:
        if request.method=='POST':
            email=request.form.get('email')
            name=request.form.get('name')
            password=request.form.get('password1')
            passwordHash=bcrypt.generate_password_hash(password)
            
            try:
                cur= mysql.connection.cursor()
                print('Connection Successful!')
                try: 
                    cur.execute("""INSERT INTO clients (email, password) VALUES (%s,%s)""",(email,passwordHash,))
                    mysql.connection.commit()        
                    cur.close()
                    flash('Signup Successful')
                    return redirect('/login')
                except:
                    flash('Signup Unsuccessful. Try Again!',category='error')
            except:
                flash('Failed to connect to the database. Try again!',category='error')
        return render_template("signup.html")


@app.route('/login',methods=['POST','GET'])
def login():
    if 'id' in session:
        return redirect('/home')
    else:
        if request.method=='POST':
            email=request.form.get('email')
            password=request.form.get('password')
            try:
                cur= mysql.connection.cursor()
                print('Connection Successful!')
                cur.execute("""SELECT * FROM clients where email=%s""",(email,))
                clientData=cur.fetchall()
                if(bcrypt.check_password_hash(clientData[0][2],password)):
                    session['id']=clientData[0][0]
                    session['email']=clientData[0][1]
                    flash('Login Successful',category='success')
                    return redirect('/home')
                else:
                    flash('Invalid Email/Password! Try again!',category='error' )
            except:
                flash('Failed to connect to the database. Try again!',category='error')
        return render_template("login.html")


@app.route('/home',methods=['POST','GET'])
def home():
    if 'id' not in session:
        flash('Login to Continue!',category='error')
        return redirect('/login')
    else:
        if request.method=='POST':
            topic=request.form.get('Topic')
            description=request.form.get('Description')
            fernet=Fernet(key)
            message=fernet.encrypt(description.encode('utf-8'))
            id=session['id']
            try:
                cur= mysql.connection.cursor()
                print('Connection Successful!')
                try: 
                    cur.execute("""INSERT INTO messages ( id,title, description) VALUES (%s,%s,%s)""",(id,topic,message,))
                    mysql.connection.commit() 
                    cur.close()
                    flash('Successfully Encrypted and Stored in the Database!','success')
                    return redirect('/home')
                except:
                    flash('Error Occured While Storing in the Database. Try again!','error')
            except:
                flash('Failed to connect to the database. Try again!',category='error')

        else:
            try:
                cur= mysql.connection.cursor()
                print('connection successful')
                try:
                    cur.execute("""Select * from messages where id=%s""",(session['id'],))
                    messages=cur.fetchall()
                    mysql.connection.commit()
                    cur.close()
                    return render_template('home.html',messages=messages)
                except:
                    flash('Unable to Fetch Messages!','error')
            except:
               flash('Failed to connect to the database. Try again!',category='error')

    


@app.route('/decrypt/<topic>/<message>')
def decrypt(topic,message):
    
    fernet=Fernet(key)
    decryptedMessage=fernet.decrypt(message.encode()).decode()
    
    return render_template("decryption.html",topic=topic,encryptedMessage=message,decryptedMessage=decryptedMessage)


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
    if 'id' in session:
        session.pop('id')  
    return redirect('/login') 

if __name__=='__main__':
    app.secret_key="super_secret_key"
    app.run(debug=True)


#match pwd and confirm pwd
# required fields in signup login all