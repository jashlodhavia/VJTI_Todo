# VJTI_Todo
API  round for workindia



- Clone this repo on your desktop
- Open command line/terminal in your machine

- Run the command ``` python app.py ``` 

- Open a browser(Chrome, firefox etc)

- Go to "http://localhost:5000"

- To sign up as an agent go to "http://localhost:5000/app/agent"

- To authenticate and login go to "http://localhost:5000/app/agent/auth"

- To create a todo go to "http://localhost:5000/app/agent/sites?agent_id=<yourid>"

- To see the list of your todos go to "http://localhost:5000/app/sites/list?agent_id = <yourid>"

- Please note that the app is connected to a local MySQL database, just change the details in the db.yaml file and connect the app to your local mysql database with the following tables already created.

```
create table users(id int NOT NULL auto_increment, agent_id varchar(20) unique, password varchar(500), primary key (id));
create table notes(id int not null auto_increment, agent_id varchar(20), title varchar(100), description varchar(1000), category varchar(50), due_date date, primary key(id))
```
