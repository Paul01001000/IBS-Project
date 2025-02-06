import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
import os
import calendar
import datetime
import csv

# File paths
USER_FILE = 'users.csv'
CLIENT_FILE = 'client_database.csv'
THERAPISTS_FILE = "therapists.csv"
APPOINTMENTS_FILE = "appointments.csv"

# Headers for the client database CSV
CLIENT_HEADERS = ["Patienten ID", "Vor & Nachname", "Telefonnummer", "Handynummer", "Adresse",
                  "Name vom Doktor", "Name vom Pfleger", "Versicherung", "Versicherungsnummer",
                  "Geschlecht", "Rezept Details", "Beschwerde"]

# Initialize user and client database files if they don't exist
if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["Username", "Password", "Firstname", "Lastname", "Date_of_Birth"]).to_csv(USER_FILE, index=False)

if not os.path.exists(CLIENT_FILE):
    pd.DataFrame(columns=CLIENT_HEADERS).to_csv(CLIENT_FILE, index=False)

# Function for the login system
def login():
    username = entry_username.get()
    password = entry_password.get()
    users = pd.read_csv(USER_FILE)
    if ((users['Username'] == username) & (users['Password'] == password)).any():
        messagebox.showinfo("Success", f"Welcome, {username}!")
        open_main_menu()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Function to handle registration
def register():
    register_window = tk.Toplevel(window)
    register_window.title("Register New User")

    labels = ["Username", "Password", "Firstname", "Lastname", "Date_of_Birth"]
    entries = {}

    for i, label in enumerate(labels):
        tk.Label(register_window, text=label).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(register_window, show="*" if label == "Password" else None)
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[label] = entry

    def save_user():
        user_data = {label: entry.get() for label, entry in entries.items()}
        if all(user_data.values()):
            users = pd.read_csv(USER_FILE)
            if user_data["Username"] in users['Username'].values:
                messagebox.showerror("Error", "Username already exists.")
            else:
                users = pd.concat([users, pd.DataFrame([user_data])], ignore_index=True)
                users.to_csv(USER_FILE, index=False)
                messagebox.showinfo("Success", "User registered successfully.")
                register_window.destroy()
        else:
            messagebox.showerror("Error", "All fields are required.")

    tk.Button(register_window, text="Register", command=save_user).grid(row=len(labels), column=1, pady=10)

# Function to open the main menu
def open_main_menu():
    window.withdraw()
    menu_window = tk.Toplevel()
    menu_window.title("Main Menu")

    def open_client_database():
        menu_window.destroy()
        manage_client_database()

    def open_appointment_manager():
        menu_window.destroy()
        manage_appointments()

    def exit_system():
        menu_window.destroy()
        window.destroy()  # Closes the main login window, effectively ending the program

    tk.Label(menu_window, text="Funktionsauswahl", font=("Arial", 16)).pack(pady=20)
    tk.Button(menu_window, text="Patienten Datenbank", command=open_client_database).pack(pady=10)
    tk.Button(menu_window, text="Terminverwaltung", command=open_appointment_manager).pack(pady=10)

    # Add the Exit System button
    tk.Button(menu_window, text="Exit System", command=exit_system, bg="red", fg="white").pack(pady=10)

# Client database management
def manage_client_database():
    client_window = tk.Toplevel()
    client_window.title("Patienten Datenbank")
    client_window.geometry("1000x700")
    entry_fields = {}

    # Create entry fields for adding a client
    for idx, header in enumerate(CLIENT_HEADERS):
        tk.Label(client_window, text=header).grid(row=idx, column=0, padx=5, pady=5)
        entry = tk.Entry(client_window)
        entry.grid(row=idx, column=1, padx=5, pady=5)
        entry_fields[header] = entry

    def add_client():
        data = {header: entry_fields[header].get() for header in CLIENT_HEADERS}
        if all(data.values()):
            df = pd.read_csv(CLIENT_FILE)
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            df.to_csv(CLIENT_FILE, index=False)
            messagebox.showinfo("Erfolgreich", "Patient wurde hinzugefügt.")
        else:
            messagebox.showwarning("Warnung", "Alle Felder müssen ausgefüllt sein.")

    def view_all_clients():
        df = pd.read_csv(CLIENT_FILE)
        view_window = tk.Toplevel(client_window)
        view_window.title("Alle Patienten")

        tree = ttk.Treeview(view_window, columns=CLIENT_HEADERS, show='headings')
        for header in CLIENT_HEADERS:
            tree.heading(header, text=header)
            tree.column(header, width=120)
        for _, row in df.iterrows():
            tree.insert("", "end", values=list(row))
        tree.pack(fill=tk.BOTH, expand=True)

    def view_specific_client():
        def search_client():
            client_name = search_entry.get()
            if not client_name:
                messagebox.showwarning("Warnung", "Bitte geben Sie einen gültigen Namen an.")
                return

            df = pd.read_csv(CLIENT_FILE)
            client = df[df["Vor & Nachname"] == client_name]
            if client.empty:
                messagebox.showerror("Fehler", f"Kein Eintrag mit dem Namen: {client_name}")
            else:
                search_result_window = tk.Toplevel(client_window)
                search_result_window.title("Patienten Details")
                tree = ttk.Treeview(search_result_window, columns=CLIENT_HEADERS, show='headings')
                for header in CLIENT_HEADERS:
                    tree.heading(header, text=header)
                    tree.column(header, width=120)
                for _, row in client.iterrows():
                    tree.insert("", "end", values=list(row))
                tree.pack(fill=tk.BOTH, expand=True)

        search_window = tk.Toplevel(client_window)
        search_window.title("Suche Patienten via Name")
        tk.Label(search_window, text="Geben Sie den Namen an:").pack(pady=5)
        search_entry = tk.Entry(search_window)
        search_entry.pack(pady=5)
        tk.Button(search_window, text="Suche", command=search_client).pack(pady=10)

    def delete_client():
        def confirm_delete():
            client_name = delete_entry.get()
            if not client_name:
                messagebox.showwarning("Warnung", "Geben Sie bitte einen gültigen Namen an.")
                return

            df = pd.read_csv(CLIENT_FILE)
            if client_name not in df["Vor & Nachname"].values:
                messagebox.showerror("Fehler", f"Kein Eintrag mit dem Namen: {client_name}")
            else:
                df = df[df["Vor & Nachname"] != client_name]
                df.to_csv(CLIENT_FILE, index=False)
                messagebox.showinfo("Erfolgreich", f"Patient mit dem Namen {client_name} wurde gelöscht.")
                delete_window.destroy()

        delete_window = tk.Toplevel(client_window)
        delete_window.title("Lösche Patienten")
        tk.Label(delete_window, text="Geben Sie den zu löschenden Namen an:").pack(pady=5)
        delete_entry = tk.Entry(delete_window)
        delete_entry.pack(pady=5)
        tk.Button(delete_window, text="Löschen", command=confirm_delete).pack(pady=10)

    def update_client():
        def search_for_update():
            client_name = update_search_entry.get()
            if not client_name:
                messagebox.showwarning("Warnung", "Bitte geben Sie einen gültigen Namen an.")
                return

            df = pd.read_csv(CLIENT_FILE)
            client = df[df["Vor & Nachname"] == client_name]
            if client.empty:
                messagebox.showerror("Fehler", f"Kein Eintrag mit dem Namen: {client_name}")
                return

            client_data = client.iloc[0]

            update_fields = {}
            for idx, header in enumerate(CLIENT_HEADERS):
                tk.Label(update_window, text=header).grid(row=idx + 1, column=0, padx=5, pady=5)
                entry = tk.Entry(update_window)
                entry.insert(0, client_data[header])
                entry.grid(row=idx + 1, column=1, padx=5, pady=5)
                update_fields[header] = entry

            def save_updates():
                updated_data = {header: update_fields[header].get() for header in CLIENT_HEADERS}
                if all(updated_data.values()):
                    # Update the specific client's data in the DataFrame
                    df.loc[df["Vor & Nachname"] == client_name, :] = updated_data.values()
                    df.to_csv(CLIENT_FILE, index=False)
                    messagebox.showinfo("Erfolgreich", "Patienteninformationen wurden aktualisiert.")
                    update_window.destroy()
                else:
                    messagebox.showwarning("Warnung", "Alle Felder müssen ausgefüllt sein.")

            tk.Button(update_window, text="Speichern", command=save_updates).grid(row=len(CLIENT_HEADERS) + 2, column=0, columnspan=2, pady=10)

        update_window = tk.Toplevel(client_window)
        update_window.title("Patienteninformationen aktualisieren")
        tk.Label(update_window, text="Geben Sie den Namen an:").grid(row=0, column=0, padx=5, pady=5)
        update_search_entry = tk.Entry(update_window)
        update_search_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(update_window, text="Suche", command=search_for_update).grid(row=0, column=2, padx=5, pady=5)

    # Buttons for managing the database
    tk.Button(client_window, text="Patienten hinzufügen", command=add_client).grid(row=len(CLIENT_HEADERS), column=0, pady=10)
    tk.Button(client_window, text="Sieh alle Patienten", command=view_all_clients).grid(row=len(CLIENT_HEADERS), column=1, pady=10)
    tk.Button(client_window, text="Sieh Patienten via Name", command=view_specific_client).grid(row=len(CLIENT_HEADERS) + 1, column=0, pady=10)
    tk.Button(client_window, text="Aktualisiere Patienteninformationen", command=update_client).grid(row=len(CLIENT_HEADERS) + 1, column=1, pady=10)
    tk.Button(client_window, text="Lösche einen Patienten", command=delete_client).grid(row=len(CLIENT_HEADERS) + 2, column=0, pady=10)

    # Button to close the window and return to the menu
    tk.Button(client_window, text="Zurück zum Menü", command=lambda: [client_window.destroy(), open_main_menu()]).grid(row=len(CLIENT_HEADERS) + 3, column=0, columnspan=2, pady=10)

# Appointment management
# Load therapists from file
def load_therapists():
    if os.path.exists(THERAPISTS_FILE):
        with open(THERAPISTS_FILE, "r") as file:
            return [line.strip() for line in file.readlines()]
    return ["Genereller Therapeut"]

# Save therapists to file
def save_therapists():
    with open(THERAPISTS_FILE, "w") as file:
        for therapist in therapists:
            file.write(therapist + "\n")

# Load appointments from file
def load_appointments():
    if os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                therapist = row["therapist"]
                date = row["date"]
                time = row["time"]
                if therapist not in appointments:
                    appointments[therapist] = {}
                if date not in appointments[therapist]:
                    appointments[therapist][date] = {}
                appointments[therapist][date][time] = {
                    "client_name": row["client_name"],
                    "type": row["type"],
                }

# Save appointments to file
def save_appointments():
    with open(APPOINTMENTS_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["therapist", "date", "time", "client_name", "type"])
        writer.writeheader()
        for therapist, dates in appointments.items():
            for date, times in dates.items():
                for time, details in times.items():
                    writer.writerow({
                        "therapist": therapist,
                        "date": date,
                        "time": time,
                        "client_name": details["client_name"],
                        "type": details["type"],
                    })

# Initialize data
appointments = {}
therapists = load_therapists()
load_appointments()

# View daily overview
def view_daily_overview():
    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    
    overview_window = tk.Toplevel(window)  # Changed from calendar_window to window
    overview_window.title("Daily Overview")
    overview_window.geometry("400x600")

    tk.Label(overview_window, text=f"Termine für {today}", font=("Arial", 14)).pack(pady=10)

    # Create a scrollable frame for the overview
    container = tk.Frame(overview_window)
    container.pack(fill="both", expand=True)

    canvas = tk.Canvas(container)
    scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Display appointments for all therapists for the current day
    found_appointments = False
    for therapist, dates in appointments.items():
        if today in dates:
            tk.Label(scrollable_frame, text=f"Therapeut: {therapist}", font=("Arial", 12, "bold")).pack(pady=5)
            for time, details in sorted(dates[today].items()):
                tk.Label(
                    scrollable_frame,
                    text=f"{time} - {details['client_name']} ({details['type']})",
                    font=("Arial", 10)
                ).pack(anchor="w", padx=20)
                found_appointments = True

    if not found_appointments:
        tk.Label(scrollable_frame, text="Heute noch keine Termine", font=("Arial", 10)).pack(pady=20)

    tk.Button(overview_window, text="Close", command=overview_window.destroy).pack(pady=10)

# Appointment management system
def manage_appointments():
    calendar_window = tk.Toplevel()
    calendar_window.title("Terminverwaltung")
    calendar_window.geometry("500x600")

    selected_therapist = tk.StringVar(value=therapists[0])

    def add_therapist():
        def save_therapist():
            name = therapist_entry.get().strip()
            if not name:
                messagebox.showwarning("Warnung", "Name darf nicht leer sein.")
                return
            if name in therapists:
                messagebox.showwarning("Warnung", "Therapeut existiert bereits.")
                return

            therapists.append(name)
            save_therapists()
            therapist_menu["menu"].add_command(label=name, command=tk._setit(selected_therapist, name))
            therapist_window.destroy()
            messagebox.showinfo("Erfolg", f"Therapeut '{name}' erfolgreich hinzugefügt.")

        therapist_window = tk.Toplevel(calendar_window)
        therapist_window.title("Therapeut anlegen")
        tk.Label(therapist_window, text="Enter Therapeut Name:").pack(pady=10)
        therapist_entry = tk.Entry(therapist_window)
        therapist_entry.pack(pady=5)
        tk.Button(therapist_window, text="Save", command=save_therapist).pack(pady=10)

    def open_timetable(year, month, day):
        date = f"{year}-{month:02d}-{day:02d}"
        therapist = selected_therapist.get()

        timetable_window = tk.Toplevel()
        timetable_window.title(f"Zeitplan für {therapist} vom {date}")
        timetable_window.geometry("400x600")

        # Create a scrollable frame
        container = tk.Frame(timetable_window)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        segments = []
        times = []

        # Generate 24-hour timetable with 30-minute segments
        for hour in range(24):
            for minute in (0, 30):
                time_label = f"{hour:02d}:{minute:02d}"
                times.append(time_label)

        selected_segments = set()

        def toggle_selection(idx):
            if idx in selected_segments:
                selected_segments.remove(idx)
                segments[idx].config(bg="white", text=times[idx])
            else:
                selected_segments.add(idx)
                segments[idx].config(bg="lightblue")

        def save_appointment():
            if not selected_segments:
                messagebox.showwarning("Fehler", "Keine Zeiten ausgewählt.")
                return

            client_name = client_entry.get().strip()
            appointment_type = appointment_type_var.get()

            if not client_name:
                messagebox.showwarning("Warnung", "Patientenname muss ausgefüllt sein.")
                return

            if appointment_type not in ["Klinik", "Hausbesuch"]:
                messagebox.showwarning("Warnung", "Wähle einen Termintypen.")
                return

            # Save appointment
            if therapist not in appointments:
                appointments[therapist] = {}
            if date not in appointments[therapist]:
                appointments[therapist][date] = {}

            for idx in selected_segments:
                if times[idx] in appointments[therapist][date]:
                    messagebox.showerror("Fehler", f"Zeit {times[idx]} ist bereits verbucht.")
                    return
                appointments[therapist][date][times[idx]] = {
                    "client_name": client_name,
                    "type": appointment_type,
                }

                # Update timetable slot appearance
                color = "green" if appointment_type == "Klinik" else "blue"
                segments[idx].config(bg=color, text=f"{times[idx]}\n{client_name}")

            save_appointments()
            messagebox.showinfo("Erfolgreich", "Termin wurde gespeichert.")
            timetable_window.destroy()

        def delete_appointment():
            if therapist not in appointments or date not in appointments[therapist]:
                messagebox.showerror("Fehler", "Keine Termine zum Löschen vorhanden.")
                return

            for idx in selected_segments:
                time = times[idx]
                if time in appointments[therapist][date]:
                    del appointments[therapist][date][time]
                    segments[idx].config(bg="white", text=times[idx])

            save_appointments()
            messagebox.showinfo("Erfolg", "Ausgewählte Termine wurden gelöscht.")

        def update_appointment():
            if not selected_segments:
                messagebox.showwarning("Fehler", "Keine Zeiten ausgewählt.")
                return

            client_name = client_entry.get().strip()
            appointment_type = appointment_type_var.get()

            if not client_name:
                messagebox.showwarning("Warnung", "Patientenname muss ausgefüllt sein.")
                return

            if appointment_type not in ["Klinik", "Hausbesuch"]:
                messagebox.showwarning("Warnung", "Wähle einen Termintypen.")
                return

            for idx in selected_segments:
                time = times[idx]
                if time in appointments[therapist][date]:
                    appointments[therapist][date][time]["client_name"] = client_name
                    appointments[therapist][date][time]["type"] = appointment_type

                    color = "green" if appointment_type == "Klinik" else "blue"
                    segments[idx].config(bg=color, text=f"{time}\n{client_name}")

            save_appointments()
            messagebox.showinfo("Erfolg", "Termine wurden aktualisiert.")

        # Display timetable
        tk.Label(scrollable_frame, text=f"Zeitplan für {therapist} am {date}", font=("Arial", 14)).pack(pady=10)

        for idx, time_label in enumerate(times):
            segment = tk.Button(scrollable_frame, text=time_label, width=20, height=2, bg="white", relief="solid",
                                command=lambda idx=idx: toggle_selection(idx))

            # Pre-color booked slots
            if therapist in appointments and date in appointments[therapist] and time_label in appointments[therapist][date]:
                appt = appointments[therapist][date][time_label]
                color = "green" if appt["type"] == "Klinik" else "blue"
                segment.config(bg=color, text=f"{time_label}\n{appt['client_name']}")

            segment.pack(pady=2)
            segments.append(segment)

        # Appointment details input
        tk.Label(timetable_window, text="Patientenname:").pack(pady=5)
        client_entry = tk.Entry(timetable_window, width=40)
        client_entry.pack(pady=5)

        tk.Label(timetable_window, text="Termintyp:").pack(pady=5)
        appointment_type_var = tk.StringVar()
        appointment_type_menu = tk.OptionMenu(timetable_window, appointment_type_var, "Klinik", "Hausbesuch")
        appointment_type_menu.pack(pady=5)

        # Buttons
        tk.Button(timetable_window, text="Speicher Termin", command=save_appointment).pack(pady=10)
        tk.Button(timetable_window, text="Lösche Termine", command=delete_appointment).pack(pady=10)
        tk.Button(timetable_window, text="Aktualisiere Termine", command=update_appointment).pack(pady=10)

        # Close button
        tk.Button(timetable_window, text="Schließen", command=timetable_window.destroy).pack(pady=10)

    def create_calendar(year, month):
        cal_frame = tk.Frame(calendar_window)
        cal_frame.pack()

        # Clear previous calendar if any
        for widget in cal_frame.winfo_children():
            widget.destroy()

        # Month and year label with navigation buttons
        nav_frame = tk.Frame(cal_frame)
        nav_frame.grid(row=0, column=0, columnspan=7, pady=10)

        def switch_month(direction):
            nonlocal current_year, current_month
            current_month += direction
            if current_month > 12:
                current_month = 1
                current_year += 1
            elif current_month < 1:
                current_month = 12
                current_year -= 1
            create_calendar(current_year, current_month)

        tk.Button(nav_frame, text="<", command=lambda: switch_month(-1)).grid(row=0, column=0, padx=5)
        tk.Label(nav_frame, text=f"{calendar.month_name[month]} {year}", font=("Arial", 16)).grid(row=0, column=1, columnspan=5)
        tk.Button(nav_frame, text=">", command=lambda: switch_month(1)).grid(row=0, column=6, padx=5)

        # Weekday labels
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(cal_frame, text=day, font=("Arial", 10)).grid(row=1, column=i, padx=5, pady=5)

        # Days in the current month
        for row, week in enumerate(calendar.monthcalendar(year, month), start=2):
            for col, day in enumerate(week):
                if day != 0:
                    tk.Button(
                        cal_frame,
                        text=str(day),
                        command=lambda d=day: open_timetable(year, month, d)
                    ).grid(row=row, column=col, padx=5, pady=5)

    # Initialize the calendar with current date
    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    create_calendar(current_year, current_month)

    # Therapist selector and add button
    tk.Label(calendar_window, text="Therapeuten auswählen:", font=("Arial", 12)).pack(pady=10)
    therapist_menu = tk.OptionMenu(calendar_window, selected_therapist, *therapists)
    therapist_menu.pack(pady=5)
    tk.Button(calendar_window, text="Therapeuten hinzufügen", command=add_therapist).pack(pady=10)

    # View daily overview button
    tk.Button(calendar_window, text="Sieh dir die heutigen Termine an", command=view_daily_overview).pack(pady=10)

    # Back to main menu button
    tk.Button(calendar_window, text="Zurück zum Menü", command=lambda: [calendar_window.destroy(), open_main_menu()]).pack(pady=10)

# Login window
window = tk.Tk()
window.title("Login / Registrierung")
window.geometry("300x200")

tk.Label(window, text="Benutzername").grid(row=0, column=0, padx=10, pady=5)
entry_username = tk.Entry(window)
entry_username.grid(row=0, column=1, padx=10, pady=5)

tk.Label(window, text="Passwort").grid(row=1, column=0, padx=10, pady=5)
entry_password = tk.Entry(window, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=5)

tk.Button(window, text="Login", command=login).grid(row=2, column=0, pady=10)
tk.Button(window, text="Registrierung", command=register).grid(row=2, column=1, pady=10)

window.mainloop()

