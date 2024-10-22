from flask import Flask, render_template, request

app = Flask(__name__)
@app.route("/")
def login():
    return render_template("login.html")

@app.route("/main", methods = ["POST"])
def main():
    res = request.form
    print(res["password"])
    return render_template("main.html", 
                           name = res["name"])

if __name__ == "__main__":
    app.run()