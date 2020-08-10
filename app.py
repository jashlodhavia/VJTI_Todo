from flask import Flask, render_template, request, redirect, jsonify
from flask_mysqldb import MySQL
import yaml
import hashlib

app = Flask(__name__)

# Configure db
db = yaml.load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def home():
    return redirect('/app/agent')

@app.route('/app/agent', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        agent_id = userDetails['agent_id']
        password = userDetails['password']
        cur = mysql.connection.cursor()

        encrypted_pass = hashlib.md5(password.encode())
        encrypted_pass = encrypted_pass.hexdigest()

        cur.execute("INSERT INTO users(agent_id, password) VALUES(%s, %s)",(agent_id, encrypted_pass))
        mysql.connection.commit()
        cur.close()


        return jsonify({"status": "account Created","status_code":200})

    return render_template('signup.html')


@app.route('/app/agent/auth', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # Fetch form data
        userDetails = request.form
        agent_id = userDetails['agent_id']
        password = userDetails['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT password from users where agent_id = %s", [agent_id])
        passw = cur.fetchone()
        cur.close()

        encrypted_pass = hashlib.md5(password.encode())
        encrypted_pass = encrypted_pass.hexdigest()

        if passw == None:
        	return jsonify({"status" : "Agent not registered. Please register"})


        if encrypted_pass == passw[0]:
        	is_logged = True
        	agent_logged = agent_id
        	return jsonify({"status": "success","agent_id": agent_id, "status_code":200})

        else:
        	return jsonify({"status": "failure", "status_code":401})

    return render_template('login.html')

@app.route('/app/sites', methods=['GET', 'POST'])
def create_note():
	if request.method == 'POST':
		agent_id = request.args.get('agent_id')
		cur = mysql.connection.cursor()
		cur.execute("SELECT * from users where agent_id = %s", [agent_id])
		num_row = cur.fetchone()

		if num_row == None:
			return jsonify({"status": "Please register the agent"})

		notes = request.form
		title = notes['title']
		description = notes['description']
		category = notes['category']
		due_date = notes['due_date']

		

		cur.execute("INSERT INTO notes(agent_id, title, description, category, due_date) VALUES(%s, %s, %s, %s, %s)", (agent_id ,title, description, category, due_date))
		mysql.connection.commit()
		cur.close()

		return jsonify({"status":"success", "status_code":200})

	return render_template('create_note.html')

@app.route('/app/sites/list', methods=['GET'])
def get_todo():

	agent_id = request.args.get('agent_id')
	cur = mysql.connection.cursor()

	cur.execute("SELECT title,description,category,due_date from notes where agent_id = %s order by due_date",  [agent_id])
	todos = cur.fetchall()

	todo_list = []
	for todo in todos:
		todo_list.append(todo)

	return jsonify(todo_list)



app.run(debug=True);