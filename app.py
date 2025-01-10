from flask import Flask,render_template,request,flash,redirect,url_for
from db_scripts import DataBaseManager
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from dotenv import load_dotenv
load_dotenv()
import os
from datetime import datetime

db = DataBaseManager('todo.db')

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'loginuser'

app.secret_key = os.getenv('SECRET_KEY')

class User(UserMixin):
    def __init__(self,id,login,password):
        self.id= id
        self.login = login
        self.password = password

    

@login_manager.user_loader
def load_user(user_id):
    db_user = db.get_user(user_id)
    if db_user:
        return User(db_user[0],db_user[2],db_user[1])
    return None

@app.route("/")  # Вказуємо url-адресу для виклику функції
def index():
    return render_template("home.html")     




@app.route("/current")
@login_required
def currenttodos():
    todos = db.get_all_todos(current_user.id)
    return render_template("currenttodos.html",todos = todos)

@app.route("/completed")
@login_required
def completed():
    todos = db.get_all_todos(current_user.id)
    return render_template("completed.html",todos = todos)
    
@app.route("/todo/new",methods=["GET","POST"])
@login_required
def new_article():
    if request.method == 'POST':
        important = 'on' if request.form.get('important') else 'off'
        db.add_article(request.form['title'],request.form['text'],current_user.id,important)
        flash('Завдання додано','alert-success')

    return render_template('newtodo.html')



@app.route('/todo/<int:id>',methods=["GET","POST"])
@login_required
def viewtodo(id):
    if request.method == 'POST':
        db.save_article(request.form['title'],request.form['memo'],id)
    todo = db.get_article(id)
    return render_template("viewtodo.html",todo=todo)



@app.route('/todo/delete/<int:id>', methods=["POST"])
@login_required 
def deletetodo(id): 
    db.delete_todo(id) 
    return redirect(url_for('currenttodos'))

@app.route('/todo/complete/<int:id>', methods=["POST"]) 
@login_required
def completetodo(id): 
    current_datetime = datetime.now()
    db.complete_todo(request.form['completed'],current_datetime.strftime('%Y-%m-%d %H:%M:%S'),id) 
    return redirect(url_for('currenttodos'))


    
@app.route("/signup",methods=["GET","POST"])
def signupuser():
    if request.method == 'POST':
        if request.form['password1'] == request.form['password2']:
            
            if db.createuser(request.form['username'],request.form['password1']):
                flash('Користувача зареєстровано','alert-success')
            else:
                flash("Ім'я користувача вже зайняте",'alert-danger')
        else:
            flash('Паролі повинні співпадати','alert-danger')

    
    return render_template('signupuser.html')

@app.route("/login",methods=["GET","POST"])
def loginuser():
    if request.method == 'POST':
            user_db=db.check_user(request.form['username'],request.form['password'])
            if user_db:
                user = User(user_db[0],user_db[2],user_db[1])
                login_user(user)
                return redirect(url_for('currenttodos'))
            else:
                flash("Неправильний логін або пароль",'alert-danger')
    
    return render_template('login.html')

@app.route("/logout",methods=["GET","POST"])
@login_required
def logoutuser():
    logout_user()
    return redirect(url_for('index'))




if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()