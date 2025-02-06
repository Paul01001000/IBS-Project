from flask import Flask, render_template, request, redirect

from database_0 import Database

import webbrowser

ROOT = "./Database/"
db = Database(ROOT)
app = Flask(__name__,template_folder = "./templates")

@app.route("/")
def root():
    return redirect("login")

@app.route("/login")
def login():
    db.log_out
    return render_template("login.html")

@app.route("/main", methods = ["GET","POST"])
def main():
    if db.get_user:
        return render_template("main.html", 
                                name = db.get_user)
    res = request.form
    if res:
        if db.verify_user(res["name"],res["password"]):
            return render_template("main.html", 
                                name = res["name"])
    return redirect("login")
    

@app.route("/register", methods = ["POST"])
def register():
    res = request.form
    if not res:
        return render_template("register.html")
    if res["Password"] != res["Password_rep"]:
        return render_template("register.html")
    if "" in res.values():
        return render_template("register.html")
    user_data = {k:res[k] for k in db.USER_HEADERS}
    if db.create_new_user(user_data):
        return redirect("login")
    else:
        return render_template("register.html")
    
@app.route("/patienten", methods = ["GET"])
def clients():
    if not db.get_user:
        return redirect("login")
    client_data = db.get_clients_json
    return render_template("clients.html",
                           clients=client_data)
    
@app.route("/patient", methods = ["GET"])
def client():
    if not db.get_user:
        return redirect("login")
    res = request.args
    db.set_client(int(res["row"]))
    this_client_data = db.get_client_json
    return render_template("client_setting.html",
                           client=this_client_data)

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

@app.route("/termine", methods = ["GET"])
def appointments():
    if not db.get_user:
        return redirect("login")
    appointment_data = db.get_appointments_json
    return render_template("appointments.html",
                           appointments=appointment_data,
                           therapist_list=db.get_all_therapists)
    
@app.route("/termin", methods = ["GET"])
def appointment():
    if not db.get_user:
        return redirect("login")
    res = request.args
    db.set_appointment(int(res["row"]))
    this_appointment_data = db.get_appointment_json
    return render_template("appointment_setting.html",
                           appointment=this_appointment_data,
                           therapist_list=db.get_all_therapists)

@app.route("/termin_neu", methods = ["POST"])
def new_appointment():
    if not db.get_user:
        return redirect("login")
    res = request.form
    if not res:
        return render_template("create_appointment.html",therapist_list=db.get_all_therapists)
    db.create_new_appointment(res)
    return redirect("termine")

@app.route("/appointment_delete")
def delete_appointment():
    db.delete_appointment()
    db.set_appointment(None)
    return redirect("termine")

@app.route("/termin_update",methods = ["POST"])
def update_appointment():
    res = request.form
    db.update_appointment(res)
    return redirect("termin?row=" + str(db.get_appointment))

@app.route("/date_and_therapist", methods = ["POST"])
def set_values():
    res = request.form
    db.set_date(res["Datum"])
    db.set_therapist(res["Therapeut"])
    return redirect("termine")



if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000/login")
    app.run()