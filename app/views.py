from datetime import datetime
import os
from flask import request
from flask import send_from_directory

from app import app
from flask import render_template,jsonify
from models import FINANCIAL_ACCOUNT

@app.route("/")
def index():
    #form = TodoForm()
    #todos = Todo.objects.order_by('-time')
    return  render_template("index.html")

@app.route("/list_account")
def list_account():
    finances = FINANCIAL_ACCOUNT.query.all()
    return jsonify(status="success",finances=[finance.tojson() for finance in finances])

# @app.route('/add',methods=["POST",])
# def add():
#     form = TodoForm(request.form)
#     if form.validate():
#         content = form.content.data
#         todo = Todo(content=content,time=datetime.now())
#         todo.save()
#     todos = Todo.objects.order_by('-time')
#     return render_template("index.html",todos=todos, form=form)
#
# @app.route('/done/<string:todo_id>')
# def done(todo_id):
#     form = TodoForm()
#     todo = Todo.objects.get_or_404(id=todo_id)
#     todo.status = 1
#     todo.save()
#     todos = Todo.objects.order_by('-time')
#     return render_template("index.html", todos=todos, form=form)
#
# @app.route('/undone/<string:todo_id>')
# def undone(todo_id):
#     form = TodoForm()
#     todo = Todo.objects.get_or_404(id=todo_id)
#     todo.status = 0
#     todo.save()
#     todos = Todo.objects.order_by('-time')
#     return render_template("index.html", todos=todos, form=form)
#
# @app.route('/delete/<string:todo_id>')
# def delete(todo_id):
#     form = TodoForm()
#     todo = Todo.objects.get_or_404(id=todo_id)
#     todo.delete()
#     todos = Todo.objects.order_by('-time')
#     return render_template("index.html", todos=todos, form=form)

#@app.route('/favicon.ico')
#def favicon():
#    return send_from_directory(os.path.join(app.root_path, 'static'),
#                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.')