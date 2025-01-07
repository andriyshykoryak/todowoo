from flask import Flask,render_template,request,flash,redirect,url_for
from db_scripts import DataBaseManager
from dotenv import load_dotenv
load_dotenv()
import os


db = DataBaseManager('todo.db')
currentuser = 1

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

@app.route("/")  # Вказуємо url-адресу для виклику функції
def index():
    return render_template("home.html")     




@app.route("/current")
def currenttodos():
    todos = db.get_all_todos(currentuser)
    return render_template("currenttodos.html",todos = todos)
    
@app.route("/todo/new",methods=["GET","POST"])
def new_article():
    if request.method == 'POST':
        db.add_article(request.form['title'],request.form['text'],1,request.form['important'])
        flash('Завдання додано','alert-success')

    return render_template('newtodo.html')


@app.route('/todo/<int:id>',methods=["GET","POST"])
def viewtodo(id):
    if request.method == 'POST':
        db.save_article(request.form['title'],request.form['memo'],id)
    todo = db.get_article(id)
    return render_template("viewtodo.html",todo=todo)



@app.route('/todo/delete/<int:id>', methods=["POST"]) 
def deletetodo(id): 
    db.delete_todo(id) 
    return redirect(url_for('currenttodos'))

@app.route('/todo/complete/<int:id>', methods=["POST"]) 
def completetodo(id): 
    db.complete_todo(request.form['completed'],id) 
    return redirect(url_for('currenttodos'))

if __name__ == "__main__":
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()