from flask import render_template, redirect, url_for, request
from . import main
# from forms import CategoryForm,TaskForm
# from .. import Category,Task

@main.route("/",methods=['GET','POST'])
def index():
	return render_template("index.html")

# @main.route("/add_category",methods=['GET','POST'])
# def add_category():
# 	form = CategoryForm()
# 	name = None
# 	if form.validate_on_submit():
# 		name = form.name.data
# 		form.name.data = ''
# 		db.session.add(Category(name=name))
# 		db.session.commit()
# 	return render_template('category_form.html', form=form, name=name)

# @main.route("/add_task",methods=['GET','POST'])
# def add_task():
# 	name = None
# 	category = None
# 	priority = None
# 	form = TaskForm()
# 	form.getChoices()

# 	if form.validate_on_submit():
# 		name = form.name.data
# 		category = form.category.data
# 		priority = form.priority.data
# 		if priority == "p1":
# 			priority_name = "HIGH"
# 		elif priority == "p2":
# 			priority_name = "NORMAL"
# 		else:
# 			priority_name = "LOW"

# 		form.name.data = ''
# 		db.session.add(Task(category=category, name=name, priority=priority_name))
# 		db.session.commit()
# 	return render_template('task_form.html', form=form, name=name, priority=priority, category=category)

# @main.route("/view_tasks",methods=['GET','POST'])
# def view_tasks():
# 	tasks = {"Task1":{"Category":"c2","Priority":"Low"}, "Task2":{"Category":"c1","Priority":"High"}, "Task3":{"Category":"c3","Priority":"Medium"}}
# 	res = Task.query.all()
# 	tasks = {}
# 	for item in res:
# 		tasks[item.name] = {"Category":item.category, "Priority":item.priority}
# 	new = False
# 	if len(tasks) == 0:
# 		new = True
# 	return render_template('view_tasks.html', tasks=tasks, new=new)