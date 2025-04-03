import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
import mysql.connector

# Database connection function
def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="chandru212k",
            port="3306",
            database="my_database", # Change this to your actual database name
            auth_plugin = "mysql_native_password"
        )
        return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Database Connection Error", f"Error connecting to the database: {e}")
        return None

# Save function to insert data into the database
def save_data():
    # Collect form data
    name = name_entry.get()
    place = place_var.get()
    degrees = []
    gender = gender_var.get()
    years_of_experience = experience_entry.get()
    about_experience = experience_text.get("1.0", tk.END).strip()

    # Collecting degrees based on checkboxes
    if hsc_var.get():
        degrees.append("HSC")
    if sslc_var.get():
        degrees.append("SSLC")
    if diploma_var.get():
        degrees.append("Diploma")
    if mca_var.get():
        degrees.append("MCA")

    degree_string = ', '.join(degrees)

    # Validate form data
    if not (name and place and degree_string and gender and years_of_experience and about_experience):
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    db = connect_db()
    if db is None:
        return

    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO user_info (name, place, degree, gender, years_of_experience, about_experience) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (name, place, degree_string, gender, years_of_experience, about_experience)
        )
        db.commit()
        messagebox.showinfo("Success", "Data saved successfully!")
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error saving data: {e}")
    finally:
        if db.is_connected():
            db.close()

# Function to display saved data
def display_data():
    db = connect_db()
    if db is None:
        return

    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM  my_db3.user_info")
        records = cursor.fetchall()

        new_window = tk.Toplevel(root)
        new_window.title("Saved User Information")
        new_window.config(bg="#f0f0f0")

        for index, record in enumerate(records):
            tk.Label(new_window,
                     text=f"Name: {record[1]}, Place: {record[2]}, Degree: {record[3]}, Gender: {record[4]}, "
                          f"Years: {record[5]}, About: {record[6]}",
                     bg="#f0f0f0", font=("Arial", 10)).pack(pady=5)

    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error retrieving data: {e}")
    finally:
        if db.is_connected():
            db.close()

# Main form to input user information
def open_user_info_form():
    global name_entry, place_var, hsc_var, sslc_var, diploma_var, mca_var, gender_var, experience_entry, experience_text

    # Clear the login window
    for widget in root.winfo_children():
        widget.destroy()

    root.title("User Information Form")
    root.geometry("500x600")
    root.configure(bg="skyblue")

    # About Me Label
    tk.Label(root, text="ABOUT ME", bg="skyblue", font=("Arial", 14)).grid(row=0, column=0, columnspan=2, pady=10)

    # Name Field
    tk.Label(root, text="Name:", bg="skyblue", font=("Arial", 12)).grid(row=1, column=0, sticky="w")
    name_entry = tk.Entry(root)
    name_entry.grid(row=1, column=1, padx=10, pady=5)

    # Place Dropdown
    tk.Label(root, text="Place:", bg="skyblue", font=("Arial", 12)).grid(row=2, column=0, sticky="w")
    place_var = tk.StringVar()
    place_dropdown = ttk.Combobox(root, textvariable=place_var)
    place_dropdown['values'] = ("Chennai", "Salem")
    place_dropdown.grid(row=2, column=1, padx=10, pady=5)

    # Degree Checkboxes
    tk.Label(root, text="Degree:", bg="skyblue", font=("Arial", 12)).grid(row=3, column=0, sticky="w")
    hsc_var = tk.IntVar()
    sslc_var = tk.IntVar()
    diploma_var = tk.IntVar()
    mca_var = tk.IntVar()
    tk.Checkbutton(root, text="HSC", variable=hsc_var, bg="skyblue").grid(row=3, column=1, sticky="w")
    tk.Checkbutton(root, text="SSLC", variable=sslc_var, bg="skyblue").grid(row=4, column=1, sticky="w")
    tk.Checkbutton(root, text="Diploma", variable=diploma_var, bg="skyblue").grid(row=5, column=1, sticky="w")
    tk.Checkbutton(root, text="MCA", variable=mca_var, bg="skyblue").grid(row=6, column=1, sticky="w")

    # Gender Radio Buttons
    tk.Label(root, text="Gender:", bg="skyblue", font=("Arial", 12)).grid(row=7, column=0, sticky="w")
    gender_var = tk.StringVar(value="Male")
    tk.Radiobutton(root, text="Male", variable=gender_var, value="Male", bg="skyblue").grid(row=7, column=1, sticky="w")
    tk.Radiobutton(root, text="Female", variable=gender_var, value="Female", bg="skyblue").grid(row=8, column=1, sticky="w")

    # Experience Entry
    tk.Label(root, text="Years of Experience:", bg="skyblue", font=("Arial", 12)).grid(row=9, column=0, sticky="w")
    experience_entry = tk.Entry(root)
    experience_entry.grid(row=9, column=1, padx=10, pady=5)

    # About Your Experience
    tk.Label(root, text="About Your Experience:", bg="skyblue", font=("Arial", 12)).grid(row=10, column=0, sticky="w")
    experience_text = scrolledtext.ScrolledText(root, width=40, height=5)
    experience_text.grid(row=11, column=0, columnspan=2, padx=10, pady=10)

    # Buttons
    tk.Button(root, text="Save", command=save_data, bg="#32cd32", font=("Arial", 12)).grid(row=12, column=0, padx=10, pady=10)
    tk.Button(root, text="Show Saved Data", command=display_data, bg="#1e90ff", font=("Arial", 12)).grid(row=12, column=1, padx=10, pady=10)

# Login function
def login():
    username = entry_username.get()
    password = entry_password.get()

    if username == "chandru" and password == "chandru212k":
        messagebox.showinfo("Login Success", "Welcome!")
        open_user_info_form()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# Main login window
root = tk.Tk()
root.title("Login Page")
root.geometry("500x400")

# Username and Password fields
tk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
entry_username = tk.Entry(root)
entry_username.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
entry_password = tk.Entry(root, show="*")
entry_password.grid(row=1, column=1, padx=10, pady=10)

# Login Button
tk.Button(root, text="Login", command=login, bg="sky blue").grid(row=2, columnspan=2, pady=10)

root.mainloop()






































































