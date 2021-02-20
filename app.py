from flask import Flask,session,request,render_template
import psycopg2
import time 
app=Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
db='postgres://kmehjunwelbxem:3a5bd15721c4b183a610f35e1228e8c3cfb1173010a07d43f7d215dde7f03b20@ec2-3-210-23-22.compute-1.amazonaws.com:5432/d33g4onqiumn8h'
conn=psycopg2.connect(db)
print(conn)
cursor=conn.cursor()
print(cursor)
@app.route('/',methods=["GET","POST"])
def home():
    if request.method=='POST':
        email1=request.form['email']
        password=request.form['password']
        email=(email1,password)
        cursor.execute('select student_email,student_phone from "App_students"')
        account=cursor.fetchall() 
        if email in account:
            cursor.execute('SELECT * FROM "App_students" where "student_email"=%s',(email1,))
            account_details=cursor.fetchall()
            print(account_details)
            cursor.execute('select * from "App_exam"')
            exam=cursor.fetchall()
            cursor.execute('select student_name from "App_students"')
            name=cursor.fetchall()
            cursor.execute('select * from "App_college"')
            other_details=cursor.fetchall()
            print(other_details)
            return render_template('student.html',exam=exam,account_details=account_details,name=name,other_details=other_details)
        else:
            msg = 'Incorrect username/password!'
            return render_template('base.html',msg=msg)
    return render_template('base.html')

@app.route('/ready',methods=["GET","POST"])
def views():
    return render_template('index.html')

@app.route('/mainpage',methods=["GET","POST"])
def views1():
    # t = 18000
    # while t: 
    #     mins, secs = divmod(t, 60) 
    #     timer = '{:02d}:{:02d}'.format(mins, secs) 
        
    #     time.sleep(1) 
    #     t -= 1
    cursor.execute('SELECT * FROM "App_students"')
    account_details=cursor.fetchall()
    cursor.execute('SELECT * FROM "App_questions"')
    account_details1=cursor.fetchall()
    return render_template('quiz.html',account_details=account_details,account_details1=account_details1)
if __name__ == "__main__":
    app.run(debug=True)
