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

@app.route("/main", methods = ["GET","POST"])
def main():
    if not db.get_user:
        redirect("login")

    if request.method == "GET":
        return render_template("main.html", 
                                name = db.get_user)
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
    
@app.route("/patienten", methods = ["GET"])
def clients():
    if not db.get_user:
        return redirect("login")
    client_data = db.get_clients_json
    return render_template("clients.html",clients=client_data)
    
@app.route("/patient", methods = ["GET"])
def client():
    if not db.get_user:
        return redirect("login")
    res = request.args
    db.set_client(int(res["row"]))
    this_client_data = db.get_client_json
    return render_template("client_setting.html",client=this_client_data)

@app.route("/patienten_neu", methods = ["POST"])
def new_client():
    if not db.get_user:
        return redirect("login")
    res = request.form
    if not res:
        return render_template("register_user.html")
    db.create_new_client(res)
    return redirect("patienten")

@app.route("/patienten_delete")
def delete_client():
    db.delete_client()
    db.set_client(None)
    return redirect("patienten")

@app.route("/patienten_update",methods = ["POST"])
def update_client():
    res = request.form
    db.update_client(res)
    return redirect("patient?row=" + str(db.get_client))


if __name__ == "__main__":
    app.run()