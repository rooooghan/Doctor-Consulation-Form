
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

db = mysql.connector.connect(host="localhost",user="root",password="root",database="miniproject")

cursor = db.cursor()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/doc_dashboard')
def doc_dashboard():
    return render_template('doc_dashboard.html')

@app.route('/medicalform',methods=['GET','POST'])
def medicalform():
    if request.method=='POST':
        username = request.form['uname']
        name = request.form['fname']
        address = request.form['add']
        age = request.form['age']
        phoneno = request.form['phno']
        description=request.form['additional_info']
        symptoms = request.form.getlist('symptoms')
        sym=','.join(map(str,symptoms))
        start_date=request.form['start_date']
        cursor.execute('INSERT INTO med_details VALUES(%s,%s,%s,%s,%s,%s,%s,%s)', (username,name,address,age,phoneno,description,sym,start_date))
        db.commit()
        return render_template('pat_dashboard.html')
    return render_template('medicalform.html')


@app.route('/patientdetails')
def patientdetails():
    cursor.execute('SELECT patient_username,patient_name,age,description,symptoms,startdate FROM med_details')
    data = cursor.fetchall()
    return render_template('patientdetails.html',data=data)

@app.route('/providecons',methods=['GET','POST'])
def providecons():
    if request.method=='POST':
        username=request.form['uname']
        medicines=request.form['medicines_prescribed']
        do_n_dont=request.form['dos-and-donts']
        next_date=request.form['next-consultation-date']
        cursor.execute('INSERT INTO consultation VALUES(%s,%s,%s,%s)', (username,medicines,do_n_dont,next_date))
        db.commit()
        return render_template('patientdetails.html')
    return render_template('providecons.html')


@app.route('/pat_dashboard')
def pat_dashboard():
    return render_template('pat_dashboard.html')

@app.route('/clogin',method=['GET','POST'])
def clogin():
    if request.method == 'POST':
        # process the form data
        name = request.form['name']
        password = request.form['password']
        username = request.form['username']
        cursor.execute('SELECT * FROM patientreg WHERE patient_name=%s AND patient_username=%s AND patient_pass=%s',(name,username,password))
        
        s=cursor.fetchall()
        if len(s)==1:
            cursor.execute('SELECT medicines,do_n_dont,next_date FROM consultation WHERE patient_username=%s',(username) )
            data=cursor.fetchall()
            return render_template('viewcons.html',data=data)
        else:
            return render_template('clogin.html')
    return render_template('clogin.html')

@app.route('/dsignup', methods=['GET', 'POST'])
def dsignup():
    if request.method == 'POST':
        # process the form data
        name = request.form['name']
        password = request.form['password']
        username = request.form['username']
        # save the user to the database
        cursor.execute('INSERT INTO doctorreg VALUES(%s,%s,%s)', (name, password,username))
        db.commit()
        return redirect(url_for('doc_dashboard'))
    return render_template('dsignup.html')

@app.route('/psignup', methods=['GET', 'POST'])
def psignup():
    if request.method == 'POST':
        # process the form data
        name = request.form['name']
        password = request.form['password']
        username = request.form['username']
        # save the user to the database
        cursor.execute('INSERT INTO patientreg VALUES(%s,%s,%s)',(name,password,username))
        db.commit()
        return redirect(url_for('pat_dashboard'))
    return render_template('psignup.html')

@app.route('/dlogin', methods=['GET', 'POST'])
def dlogin():
    if request.method == 'POST':
        # process the form data
        name = request.form['name']
        password = request.form['password']
        username = request.form['username']
        cursor.execute('SELECT * FROM doctorreg  WHERE doctor_name=%s AND doctor_username=%s AND doctor_pass=%s',(name,username,password))
        r=cursor.fetchall()
        if len(r)==1:
            return redirect(url_for('patientdetails'))
        else:
            return redirect(url_for('dlogin'))
        # check if the user exists in the database
        # if yes, log them in and redirect to the dashboard
        # if not, show an error message
    return render_template('dlogin.html')

@app.route('/plogin', methods=['GET', 'POST'])
def plogin():
    if request.method == 'POST':
        # process the form data
        name = request.form['name']
        password = request.form['password']
        username = request.form['username']
        cursor.execute('SELECT * FROM patientreg WHERE patient_name=%s AND patient_username=%s AND patient_pass=%s',(name,username,password))
        
        s=cursor.fetchall()
        if len(s)==1:
            return redirect(url_for('medicalform'))
        else:
            return redirect(url_for('plogin'))
    return render_template('plogin.html')

if __name__ == '__main__':
    app.run(debug=True)
