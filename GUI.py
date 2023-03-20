import tkinter as tk
from tkinter import ttk


def submit():
    global email, password
    email = email_entry.get()
    password = password_entry.get()

    with open("credentials.txt", "w") as f:
        f.write(email + "\n")
        f.write(password + "\n")


root = tk.Tk()
root.title("Login")

# Create and position email label and entry
email_label = ttk.Label(root, text="Email:")
email_label.grid(column=0, row=0, padx=(20, 10), pady=(20, 5), sticky=tk.W)
email_entry = ttk.Entry(root)
email_entry.grid(column=1, row=0, padx=(10, 20), pady=(20, 5))

# Create and position password label and entry
password_label = ttk.Label(root, text="Password:")
password_label.grid(column=0, row=1, padx=(20, 10), pady=5, sticky=tk.W)
password_entry = ttk.Entry(root, show="*")
password_entry.grid(column=1, row=1, padx=(10, 20), pady=5)

# Create and position submit button
submit_button = ttk.Button(root, text="Submit", command=submit)
submit_button.grid(column=1, row=2, padx=(10, 20), pady=(5, 20))

root.mainloop()
