from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key='india'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='hr_erp_db'

mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contact')
def contactus():
    return render_template('contactus.html')

@app.route('/reg')
def registrationpage():
    return render_template('registration.html')

@app.route('/success',methods=['POST'])
def successpage():
    n = request.form['txtName']
    m = request.form['txtMobile']

    return "<h1>Welcome : "+n +" Mobile: "+m

@app.route('/square')
def square():
    return render_template('square.html')

@app.route('/result',methods=['POST'])
def result():
    n = int(request.form['txtNumber'])
    z = n*n
    return "Square is : "+str(z)

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')

@app.route('/admindashboard',methods=['post'])
def admindashboard():
    u = request.form['txtUsername']
    p = request.form['txtPassword']

    if(u=="admin" and p=="super"):
        session["name"] = "Ram"         # Session Variable Created
        session["login"] = u
        return render_template('admin_dashboard.html')

    else:
        msg = "Invalid Username and Password."
        return render_template('adminlogin.html',message = msg)


@app.route('/admin_addemp')
def admin_addemp():
    return render_template('admin_addemp.html')

@app.route('/admin_showemp')
def admin_showemp():
    # Database Connection Open
    cur = mysql.connection.cursor()
    # Query Specification
    cur.execute('select empid,empname,designation from registration')

    emplist = cur.fetchall()

    return render_template('admin_showemp.html',recordlist=emplist)


@app.route('/admin_searchemp')
def admin_searchemp():
    return render_template('admin_searchemp.html')

@app.route('/save',methods=['post'])
def save():
    i = request.form['txtEmpID']
    n = request.form['txtName']
    e = request.form['txtEmailID']
    m = request.form['txtMobile']
    d = request.form['txtDesignation']
    s = request.form['txtSalary']

    #Database Connection Open
    cur = mysql.connection.cursor()

    #Query Specification
    cur.execute('insert into registration(empid,empname,email,mobile,designation,salary) values(%s,%s,%s,%s,%s,%s)',(i,n,e,m,d,s))

    #Transaction Save/commit
    mysql.connection.commit()
    #Database Connection Close
    cur.close()
    return render_template('admin_reg_success.html')



@app.route('/admin_emp_profile')
def admin_emp_profile():
    id = request.args.get('eid')
    cur = mysql.connection.cursor()
    cur.execute('select empid,empname,email,mobile,designation,salary from registration where empid='+id)
    emplist = cur.fetchall()
    return render_template('admin_emp_profile.html',recordlist=emplist)


@app.route('/admin_emp_update',methods=['post'])
def admin_emp_update():
    i = request.form['txtEmpID']
    n = request.form['txtName']
    e = request.form['txtEmailID']
    m = request.form['txtMobile']
    d = request.form['txtDesignation']
    s = request.form['txtSalary']

    # Database Connection Open
    cur = mysql.connection.cursor()

    # Query Specification
    cur.execute('update registration set empname=%s,email=%s,mobile=%s,designation=%s,salary=%s where empid=%s',(n,e,m,d,s,i,))

    # Transaction Save/commit
    mysql.connection.commit()
    # Database Connection Close
    cur.close()

    return render_template('admin_emp_update_success.html')



@app.route('/admin_emp_delete')
def admin_emp_delete():
    i = request.args.get('id')

    # Database Connection Open
    cur = mysql.connection.cursor()
    # Query Specification
    cur.execute('delete from registration where empid=%s',(i,))
    # Transaction Save/commit
    mysql.connection.commit()
    # Database Connection Close
    cur.close()

    return render_template('admin_emp_delete_success.html')



@app.route('/admin_emp_searchprocess',methods=['post'])
def admin_emp_searchprocess():
    n = request.form['txtName']
    print(n)
    cur = mysql.connection.cursor()
    q = "Select * from registration where empname like '" +n+ "%'"
    print(q)
    cur.execute(q)
    emplist=cur.fetchall()
    cur.close()
    return render_template('admin_emp_searchresult.html',recordlist=emplist)

@app.route('/logout')
def logout():
    session["name"]=None
    return render_template("adminlogin.html")


app.run(debug=True)

# app.run(host='0.0.0.0',port=120)

