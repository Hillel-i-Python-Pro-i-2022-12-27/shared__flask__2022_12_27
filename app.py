from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/hello")
def hello_123():  # put application's code here
    return "Hello 123!"


@app.route("/hi/<name>")
def hello_by_name(name: str = "Jack"):  # put application's code here
    return f"Hello {name}!"


if __name__ == "__main__":
    app.run()
