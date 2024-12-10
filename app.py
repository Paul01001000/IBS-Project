from flask import Flask, render_template, request, redirect

from database_0 import Database

db = Database()
app = Flask(__name__)

@app.route("/")
def root():
    return redirect("login")

@app.route("/login")
def login():
    db.log_out
    return render_template("login.html")

@app.route("/main", methods = ["POST"])
def main():
    if not db.get_user:
        redirect("login")
    res = request.form
    if db.verify_user(res["name"],res["password"]):
        return render_template("main.html", 
                                name = res["name"])
    else:
        return redirect("login")
    

@app.route("/register", methods = ["POST"])
def register():
    res = request.form
    if not res:
        return render_template("register.html")
    user_data = {k:"" for k in db.USER_HEADERS}
    user_data["Username"] = res["name"]
    user_data["Password"] = res["password"]
    if db.create_new_user(user_data):
        return redirect("login")
    else:
        return render_template("register.html")
    
@app.route("/patienten", methods = ["POST"])
def clients():
    client_data = db.get_clients_json
    return render_template("clients.html",clients=client_data)
    


if __name__ == "__main__":
    app.run()