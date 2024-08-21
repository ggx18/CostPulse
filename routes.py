from flask import Flask, render_template,Response, request, redirect, url_for, session, flash
import pandas as pd
from forms import StructureForm, ResourceForm, DriverDataForm, DestinationValueForm
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from config import create_db_connection

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn, cursor = create_db_connection()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):  # Assuming password is the third field
            session['logged_in'] = True
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    
    return render_template('login.html')





@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Hash the password using the default method (pbkdf2:sha256)
        hashed_password = generate_password_hash(password)
        
        conn, cursor = create_db_connection()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()
        
        flash('Signup successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('signup.html')



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    conn, cursor = create_db_connection()
    cursor.execute("SELECT COUNT(*) FROM structures")
    count = cursor.fetchone()[0]
    # print("count: ", count)
    cursor.close()
    conn.close()
    return render_template('index.html', count = count)

@app.route('/costplan')
@login_required
def costplan():
    conn, cursor = create_db_connection()
    cursor.execute("SELECT * FROM costplan")
    costplans = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('costplan.html', costplans=costplans)

######################################################## STRUCTURES #####################################################

@app.route('/structures')
@login_required
def structures():
    conn, cursor = create_db_connection()
    cursor.execute("SELECT * FROM structures")
    structures = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('structures.html', structures=structures)

@app.route('/delete_structure/<int:slno>', methods=['POST'])
@login_required
def delete_structure(slno):
    conn, cursor = create_db_connection()
    cursor.execute("DELETE FROM structures WHERE slno = ?", (slno))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('structures'))

@app.route("/addstructure")
@login_required
def addstructure():
    return render_template("/addstructure.html")

@app.route('/add_structure', methods=['POST'])
@login_required
def add_structure():

    form = StructureForm(request.form)
    if request.method == "POST" and form.validate():
        # sl_no = request.form['slno']    
        str_id = request.form['strid']
        str_name = request.form['strname']
        parent_id = request.form['parentid']    
        parent_name = request.form['parentname']
        conn, cursor = create_db_connection()
        cursor.execute("INSERT INTO structures (strid, strname, parentid ,parentname) VALUES (?, ?, ? ,?)", 
                       (str_id, str_name, parent_id, parent_name))
        cursor.commit()
        conn.close()
        return redirect(url_for('structures'))

@app.route('/edit_structure/<int:slno>', methods=['GET', 'POST'])
@login_required
def edit_structure(slno):
    conn, cursor = create_db_connection()
    
    # Corrected line to pass slno as a tuple
    cursor.execute("SELECT * FROM structures WHERE slno = ?", (slno,))
    structure = cursor.fetchone()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        str_id = request.form['strid']
        str_name = request.form['strname']
        parent_id = request.form['parentid']
        parent_name = request.form['parentname']

        conn, cursor = create_db_connection()
        cursor.execute("UPDATE structures SET strid = ?, strname = ?, parentid = ?, parentname = ? WHERE slno = ?",
                       (str_id, str_name, parent_id, parent_name, slno))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('structures'))

    return render_template('edit_structure.html', structure=structure)


############################################ RESOURCES ##############################

@app.route('/resources')
@login_required
def resources():
    conn, cursor = create_db_connection()
    cursor.execute("SELECT * FROM resources")
    resources = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('resources.html', resources=resources)

@app.route('/delete_resource/<int:slno>', methods=['POST'])
@login_required
def delete_resource(slno):
    conn, cursor = create_db_connection()
    cursor.execute("DELETE FROM resources WHERE slno = ?", (slno))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('resources'))

@app.route("/addresource")
@login_required
def addresource():
    return render_template("/addresource.html")

@app.route('/add_resource', methods=['POST'])
@login_required
def add_resource():

    form = ResourceForm(request.form)
    if request.method == "POST" and form.validate():

        parent_id = request.form['parentid']
        parent_name = request.form['parentname']
        resource_id = request.form['resourceid']
        resource_name = request.form['resourcename']
        resource_amount = request.form['resourceamount']

        conn, cursor = create_db_connection()
        cursor.execute("INSERT INTO resources (parentid, parentname, resourceid, resourcename, resourceamount) VALUES (?, ?, ?, ?, ?)", 
                       (parent_id, parent_name, resource_id, resource_name, resource_amount))
        cursor.commit()
        conn.close()
        return redirect(url_for('resources'))
    
@app.route('/edit_resource/<int:slno>', methods=['GET', 'POST'])
@login_required
def edit_resource(slno):
    conn, cursor = create_db_connection()
    
    cursor.execute("SELECT * FROM resources WHERE slno = ?", (slno,))
    resource = cursor.fetchone()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        parent_id = request.form['parentid']
        parent_name = request.form['parentname']
        resource_id = request.form['resourceid']
        resource_name = request.form['resourcename']
        resource_amount = request.form['resourceamount']
        plan_id = request.form['planid']

        conn, cursor = create_db_connection()
        cursor.execute("UPDATE resources SET parentid = ?, parentname = ?, resourceid = ?, resourcename = ?, resourceamount = ?, planid = ? WHERE slno = ?",
                       (parent_id, parent_name, resource_id, resource_name, resource_amount, plan_id, slno))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('resources'))

    return render_template('edit_resource.html', resource=resource)


        

######################################################## DRIVER DATA ##############################################3

@app.route('/driverdata')
@login_required
def driverdata():
    conn, cursor = create_db_connection()
    cursor.execute("SELECT * FROM driverdata")
    driverdatas = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('driverdata.html', driverdatas=driverdatas)

@app.route('/delete_driverdata/<int:slno>', methods=['POST'])
@login_required
def delete_driverdata(slno):
    conn, cursor = create_db_connection()
    cursor.execute("DELETE FROM driverdata WHERE slno = ?", (slno))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('driverdata'))

@app.route("/adddriverdata")
@login_required
def adddriverdata():
    return render_template("/adddriverdata.html")

@app.route('/add_driverdata', methods=['POST'])
@login_required
def add_driverdata():

    form = DriverDataForm(request.form)
    if request.method == "POST" and form.validate():

        parent_id = request.form['parentid']    
        parent_name = request.form['parentname']
        resource_id = request.form['resourceid']
        resource_name = request.form['resourcename']
        resource_amount = request.form['resourceamount']
        driver_id = request.form['driverid']

        conn, cursor = create_db_connection()
        cursor.execute("INSERT INTO driverdata (parentid, parentname, resourceid, resourcename, resourceamount, driverid) VALUES (?, ?, ?, ?, ?, ?)", 
                       (parent_id, parent_name, resource_id, resource_name, resource_amount, driver_id))
        
        conn.commit()
        conn.close()
        return redirect(url_for('driverdata'))
    
@app.route('/edit_driverdata/<int:slno>', methods=['GET', 'POST'])
@login_required
def edit_driverdata(slno):
    conn, cursor = create_db_connection()
    
    cursor.execute("SELECT * FROM driverdata WHERE slno = ?", (slno,))
    driverdata = cursor.fetchone()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        parent_id = request.form['parentid']
        parent_name = request.form['parentname']
        resource_id = request.form['resourceid']
        resource_name = request.form['resourcename']
        resource_amount = request.form['resourceamount']
        driver_id = request.form['driverid']

        conn, cursor = create_db_connection()
        cursor.execute("UPDATE driverdata SET parentid = ?, parentname = ?, resourceid = ?, resourcename = ?, resourceamount = ?, driverid = ? WHERE slno = ?",
                       (parent_id, parent_name, resource_id, resource_name, resource_amount, driver_id, slno))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('driverdata'))

    return render_template('edit_driverdata.html', driverdata=driverdata)

    

    ############################################ DESTINATION VALUES ################################################


################################################################### DESTINATION VALUES ###################################################

@app.route('/destinationvalues')
@login_required
def destinationvalues():
    conn, cursor = create_db_connection()
    cursor.execute("SELECT * FROM destinationvalues")
    destinationvalues = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('destinationvalues.html', destinationvalues=destinationvalues)

@app.route('/delete_destinationvalue/<int:slno>', methods=['POST'])
@login_required
def delete_destinationvalue(slno):
    conn, cursor = create_db_connection()
    cursor.execute("DELETE FROM destinationvalues WHERE slno = ?", (slno,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('destinationvalues'))

@app.route("/adddestinationvalue")
@login_required
def adddestinationvalue():
    return render_template("adddestinationvalue.html")

@app.route('/add_destinationvalue', methods=['POST'])
@login_required
def add_destinationvalue():

    form = DestinationValueForm(request.form)
    if request.method == "POST":

        driver_id = request.form['driverid']
        resource_id = request.form['resourceid']
        destination_account = request.form['destinationaccount']
        driver_qty_unit = request.form['driverqtyunit']

        conn, cursor = create_db_connection()
        cursor.execute("INSERT INTO destinationvalues (driverid, resourceid, destinationaccount, driverqtyunit ) VALUES (?, ?, ?, ?)", 
                       (driver_id, resource_id, destination_account, driver_qty_unit))
        
        conn.commit()
        conn.close()
        return redirect(url_for('destinationvalues'))
    
@app.route('/edit_destinationvalue/<int:slno>', methods=['GET', 'POST'])
@login_required
def edit_destinationvalue(slno):
    conn, cursor = create_db_connection()
    
    cursor.execute("SELECT * FROM destinationvalues WHERE slno = ?", (slno,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        driver_id = request.form['driverid']
        resource_id = request.form['resourceid']
        destination_account = request.form['destinationaccount']
        driver_qty_unit = request.form['driverqtyunit']
        plan_id = request.form['planid']

        conn, cursor = create_db_connection()
        cursor.execute("UPDATE destinationvalues SET driverid = ?, resourceid = ?, destinationaccount = ?, driverqtyunit = ?, planid = ? WHERE slno = ?",
                       (driver_id, resource_id, destination_account, driver_qty_unit, plan_id, slno))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('destinationvalues'))

    return render_template('edit_destinationvalue.html', data=data)


@app.route('/cleanthefile', methods=['GET', 'POST'])
def cleanthefile():
    if request.method == 'POST':
        csv_file = request.files['csv_file']
        if csv_file:
            # Read CSV data using pandas
            if csv_file.filename.endswith('.csv'):
                # Read CSV file
                df = pd.read_csv(csv_file)
            elif csv_file.filename.endswith('.xlsx'):
                # Read Excel file
                df = pd.read_excel(csv_file)
            else:
                return "Unsupported file type", 400
            
            
            # Final file column count
            column_count = df.shape[1]
            
            # Final file row count
            row_count = df.shape[0]
            
            # Initialize rule counts
            rule_counts = {
                'column_count': column_count,
                'row_count': row_count
            }

            return render_template('cleanthefile.html', rule_counts=rule_counts)
    return render_template('cleanthefile.html')




######################################### SQLITE ##########################################################

# from config import Config
# from models import db, Student

# app = Flask(__name__)
# app.config.from_object(Config)

# db.init_app(app)

# @app.route('/students')
# def display_students():
#     students = Student.query.all()
#     return render_template('students.html', students=students)

# # Initialize the database
# with app.app_context():
#     db.create_all()

####################################################################################################