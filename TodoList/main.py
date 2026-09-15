from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


app = Flask(__name__)


# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CONFIGURE TABLE
class TodoPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task: Mapped[str] = mapped_column(String(250), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    result = db.session.execute(db.select(TodoPost))
    todos = result.scalars().all()

    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add_todo():
    new_todo = TodoPost(
        task=request.form["task"]
    )

    db.session.add(new_todo)
    db.session.commit()

    return redirect(url_for("home"))


@app.route("/complete/<int:todo_id>")
def complete(todo_id):
    todo = db.get_or_404(TodoPost, todo_id)

    todo.completed = not todo.completed

    db.session.commit()

    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = db.get_or_404(TodoPost, todo_id)

    db.session.delete(todo)
    db.session.commit()

    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True, port=5003)
