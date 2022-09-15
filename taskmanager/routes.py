from flask import render_template, request, redirect, url_for
from taskmanager import app, db
from taskmanager.models import Category, Task


# Displays list of tasks created by user
@app.route("/")
def home():
    tasks = list(Task.query.order_by(Task.id).a())
    return render_template("tasks.html", tasks=tasks)


# Displays the list of categories created by user
@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)


# This does not redirect back to categories route :( bug?
# Is executed when the 'Add Category' button is clicked (categories.html)
@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")


# This function is executed when the 'Edit' button is clicked (categories.html)
@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    # Get chosen category or display '404' error message
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)


# Deletes chosen category, by user, and returns to categories.html
# Is executed when the Delete button is clicked (categories.html)
@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    # Get chosen category or display '404' error message
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    # Redirect to categories route function
    return redirect(url_for("categories"))


# This function is executed when the 'Add Task' button is clicked (tasks.html)
@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=bool(True if request.form.get("is_urgent") else False),
            due_date=request.form.get("due_date"),
            category_id=request.form.get("category_id")
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html", categories=categories)


# This function is executed when the 'Edit' button is clicked (tasks.html)
@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.is_urgent = bool(True if request.form.get("is_urgent") else False)
        task.due_date = request.form.get("due_date")
        task.category_id = request.form.get("category_id")
        db.session.commit()
    return render_template("edit_task.html", task=task, categories=categories)


# This function is executed when the delete button is clicked
@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    # Get chosen task or display '404' error message
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    # Redirect to home route
    return redirect(url_for("home"))