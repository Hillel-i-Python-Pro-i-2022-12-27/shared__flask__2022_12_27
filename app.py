from flask import Flask, Response
from webargs import fields
from webargs.flaskparser import use_args

from application.generate_humans import generate_humans
from application.services.create_table import create_table
from application.services.db_connection import DBConnection

app = Flask(__name__)


@app.route("/users/create")
@use_args({"name": fields.Str(required=True), "age": fields.Int(required=True)}, location="query")
def users__create(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO users (name, age) VALUES (:name, :age);",
                {"name": args["name"], "age": args["age"]},
            )

    return "Ok"


@app.route("/users/read-all")
def users__read_all():
    with DBConnection() as connection:
        users = connection.execute("SELECT * FROM users;").fetchall()

    return "<br>".join([f'{user["pk"]}: {user["name"]} - {user["age"]}' for user in users])


@app.route("/users/read/<int:pk>")
def users__read(pk: int):
    with DBConnection() as connection:
        user = connection.execute(
            "SELECT * " "FROM users " "WHERE (pk=:pk);",
            {
                "pk": pk,
            },
        ).fetchone()

    return f'{user["pk"]}: {user["name"]} - {user["age"]}'


@app.route("/users/update/<int:pk>")
@use_args({"age": fields.Int(), "name": fields.Str()}, location="query")
def users__update(
    args,
    pk: int,
):
    with DBConnection() as connection:
        with connection:
            name = args.get("name")
            age = args.get("age")
            if name is None and age is None:
                return Response(
                    "Need to provide at least one argument",
                    status=400,
                )

            args_for_request = []
            if name is not None:
                args_for_request.append("name=:name")
            if age is not None:
                args_for_request.append("age=:age")

            args_2 = ", ".join(args_for_request)

            connection.execute(
                "UPDATE users " f"SET {args_2} " "WHERE pk=:pk;",
                {
                    "pk": pk,
                    "age": age,
                    "name": name,
                },
            )

    return "Ok"


@app.route("/users/delete/<int:pk>")
def users__delete(pk):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "DELETE " "FROM users " "WHERE (pk=:pk);",
                {
                    "pk": pk,
                },
            )

    return "Ok"


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/hi/<name>/<int:age>")
@app.route("/hi/<name>")
@app.route("/hi")
def hello_by_name_and_age(name: str = "Jack", age: int = 10):  # put application's code here
    return f"Hello {name}! You are {age} years old!"


@app.route("/hello")
@use_args({"name": fields.Str(missing="Bob"), "age": fields.Int(missing=20)}, location="query")
def hello_by_webargs(args):
    name = args["name"]
    age = args["age"]
    return f"Hello {name}! You are {age} years old!"


@app.route("/humans")
@use_args({"amount": fields.Int(missing=10)}, location="query")
def generate_humans_(args):
    amount = args["amount"]

    humans = generate_humans(amount=amount)

    temp_ = "".join(
        f"<li>" f"<span>{human.name}</span>" f"<span> - </span>" f"<span>{human.age}</span>" f"</li>"
        for human in humans
    )

    return f"<ol>{temp_}</ol>"


# HTML tags

# div
# p
# span

# ul
# ol
# li

# hr

# br

# a

# form
# input
# button

# h1, h2, h3, h4, h5, h6

create_table()

if __name__ == "__main__":
    app.run()
