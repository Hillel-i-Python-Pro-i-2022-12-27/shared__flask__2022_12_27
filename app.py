from flask import Flask
from webargs import fields
from webargs.flaskparser import use_args

from application.generate_humans import generate_humans

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run()
