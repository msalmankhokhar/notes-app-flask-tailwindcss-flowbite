from flask import Flask, render_template, request, redirect, flash, session, g
from sqlalchemy import or_
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime
from database_manager import connection_URI
from svg import svg

app = Flask(__name__)
app.secret_key = 'ali_muthal_don'

# Setting up databse connection
sql_server_URI = f'mssql+pyodbc:///?odbc_connect={connection_URI}Encrypt=no'
app.config["SQLALCHEMY_DATABASE_URI"] = sql_server_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
database = SQLAlchemy(app)

# Creating Database models
class Note(database.Model):
    serial_number = database.Column(database.Integer, primary_key=True)
    title = database.Column(database.String(200), nullable=False)
    desc = database.Column(database.String(500), nullable=False)
    user = database.Column(database.String(150), nullable=False)
    
    def __repr__(self) -> str:
        return f"{self.serial_number} - {self.title}"

class User(database.Model):
    email = database.Column(database.String(150), primary_key=True)
    name = database.Column(database.String(70), nullable=False)
    password = database.Column(database.String(70), nullable=True)

# Creating database tables
with app.app_context():
    database.create_all()

@app.before_request
def add_theme_color():
    g.svg = svg

def getNotesList(email:str) -> list:
    with app.app_context():
        user_notes = Note.query.filter_by(user=email).all()
        notesList = [ { 'serial_number' : note.serial_number, 'title' : note.title, 'desc' : note.desc } for note in user_notes ]
        return notesList

@app.route('/theme', methods=['GET'])
def theme():
    darkTheme = request.args.get('value')
    if darkTheme == 'true':
        session.update({ 'theme' : True })
        return { 'theme' : True }
    else:
        session.pop('theme')
        return { 'theme' : False }

@app.route('/', methods = [ 'GET'])
def index():
    if 'user' in session:
        user = User.query.filter_by(email=session.get('user')).first()
        if user:
            notesList = getNotesList(user.email)
            return render_template('index.html', user = user, notesList=notesList)
        else:
            session.pop('user')
            return redirect('/login')
    else:
        return redirect('/login')
    
@app.route('/search')
def search():
    if 'user' in session:
        user = session.get('user')
        searchInput = request.args.get('search')
        searchResultNotes = Note.query.filter(or_( Note.title.contains(searchInput), Note.desc.contains(searchInput) ), Note.user==user).all()
        if len(searchResultNotes) > 0:
            return render_template('search.html', notesList = searchResultNotes, searchInput=searchInput)
        else:
            flash('No search results found for your query', 'danger')
            return redirect('/')
    else:
        return redirect('/login')
    

@app.route('/login', methods = [ 'GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user:
            if user.password == password:
                session['user'] = user.email
                flash('Log in successfull', 'success')
                return redirect('/')
            else:
                flash('Wrong Password. Please try again', 'warning')
                return redirect('/login')
        else:
            flash('No account exists with this email', 'warning')
            return redirect('/login')

@app.route('/signup', methods = [ 'GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        new_user = User(name=name, email=email, password=password)
        database.session.add(new_user)
        database.session.commit()
        flash('Account created successfully. Please Log in now', 'success')
        return redirect('/login')

# api endpoint to load and display user notes on the frontend
@app.route('/api/notes', methods=['GET'])
def get_notes():
    user = request.args.get('user')
    notesList = getNotesList(user)
    return { 'notes' : notesList }

# endpoint to add a new note
@app.route('/add_note', methods=['POST'])
def add_note():
    if 'user' in session:
        last_serial_num = len(Note.query.all())
        user = session.get('user')
        title = request.form.get('title')
        desc = request.form.get('desc')
        new_note = Note(title=title, desc=desc, user=user, serial_number=last_serial_num+1)
        database.session.add(new_note)
        database.session.commit()
        flash('New Note added in database', 'success')
        return redirect('/')
    else:
        return redirect('/login')
    
# endpoint to edit a note
@app.route('/edit_note/<string:serial_number>', methods=['POST'])
def edit_note(serial_number):
    if 'user' in session:
        user = session.get('user')
        title = request.form.get('title')
        desc = request.form.get('desc')
        selected_note = Note.query.filter_by(user=user, serial_number=serial_number).first()
        selected_note.title = title
        selected_note.desc = desc
        database.session.commit()        
        flash('Changes saved', 'success')
        return redirect('/')
    else:
        return redirect('/login')
    
# endpoint to delete a note
@app.route('/del_note/<string:serial_number>', methods=['GET'])
def delete_note(serial_number):
    if 'user' in session:
        user = session.get('user')
        selected_note = Note.query.filter_by(user=user, serial_number=serial_number).first()
        database.session.delete(selected_note)
        database.session.commit()
        flash('Note has been deleted', 'success')
        return redirect('/')
    else:
        return redirect('/login')
    
# endpoint to log out
@app.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        session.pop('user')
        flash('You have been logged out', 'success')
        return redirect('/')
    else:
        return redirect('/login')
    


if __name__=="__main__":
    app.run(host='0.0.0.0', debug=True, port=80)