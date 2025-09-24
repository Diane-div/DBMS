import mysql.connector
from tkinter import *
from tkinter import messagebox


def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="ait123",  
        database="testdb"
    )

def add_user():
    name = entry_name.get()
    email = entry_email.get()
    if name == "" or email == "":
        messagebox.showwarning("Input Error", "Please fill all fields")
        return
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "User added successfully")
    show_users()


def show_users():
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    listbox.delete(0, END)
    for row in rows:
        listbox.insert(END, row)
    con.close()


def on_select(event):
    selected = listbox.get(listbox.curselection())
    entry_id.delete(0, END)
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    entry_id.insert(END, selected[0])
    entry_name.insert(END, selected[1])
    entry_email.insert(END, selected[2])


def update_user():
    user_id = entry_id.get()
    name = entry_name.get()
    email = entry_email.get()
    if user_id == "":
        messagebox.showwarning("Select Record", "Please select a user to update")
        return
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("UPDATE users SET name=%s, email=%s WHERE id=%s", (name, email, user_id))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "User updated successfully")
    show_users()


def delete_user():
    user_id = entry_id.get()
    if user_id == "":
        messagebox.showwarning("Select Record", "Please select a user to delete")
        return
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("DELETE FROM users WHERE id=%s", (user_id,))
    con.commit()
    con.close()
    messagebox.showinfo("Success", "User deleted successfully")
    show_users()


root = Tk()
root.title("User Management")


Label(root, text="ID").grid(row=0, column=0)
entry_id = Entry(root)
entry_id.grid(row=0, column=1)

Label(root, text="Name").grid(row=1, column=0)
entry_name = Entry(root)
entry_name.grid(row=1, column=1)

Label(root, text="Email").grid(row=2, column=0)
entry_email = Entry(root)
entry_email.grid(row=2, column=1)


Button(root, text="Add", command=add_user).grid(row=3, column=0)
Button(root, text="Update", command=update_user).grid(row=3, column=1)
Button(root, text="Delete", command=delete_user).grid(row=3, column=2)
Button(root, text="Refresh", command=show_users).grid(row=3, column=3)


listbox = Listbox(root, width=50)
listbox.grid(row=4, column=0, columnspan=4)
listbox.bind('<<ListboxSelect>>', on_select)


show_users()

root.mainloop()
