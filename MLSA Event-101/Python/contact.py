from tkinter import *
from tkinter.messagebox import *
import sqlite3
from tkinter import ttk

# Insert new contact
def insert():
    n = name.get()
    p = phone.get()
    m = mail.get()
    if n != "" and p != "" and m != "":
        con = sqlite3.connect('data.db')
        c = con.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS contact (name TEXT, phone TEXT, mail TEXT)')
        try:
            c.execute("INSERT INTO contact(name, phone, mail) VALUES (?, ?, ?)", (n, p, m))
            con.commit()
            showinfo('Insert', 'Successfully inserted')
        except Exception as e:
            showerror("Error", f"Something went wrong: {str(e)}")
        con.close()
    else:
        showerror("Invalid Data", "Some fields are empty, check again!")

# Delete contact
def dele():
    n = name.get()
    if n != "":
        con = sqlite3.connect('data.db')
        c = con.cursor()
        c.execute("DELETE FROM contact WHERE name=?", (n,))
        con.commit()
        if c.rowcount > 0:
            showinfo('Deleted', 'Successfully Deleted')
        else:
            showerror("Invalid Data", "No such name found!")
        con.close()
    else:
        showwarning('Warning', 'Please enter a name to delete!')

# Open delete window
def delete():
    top = Toplevel()
    top.title("DELETE DATA")
    Label(top, text="Enter the name to delete").grid(row=0, columnspan=4)
    Entry(top, width=30, textvariable=name).grid(row=2, columnspan=2)
    Button(top, text="Delete", command=dele).grid(row=4, columnspan=4)

# Open add window
def add():
    top = Toplevel()
    top.title("ADD DATA")
    
    Label(top, text="NAME :-").grid(row=1)
    Label(top, text="MOBILE :-").grid(row=2)
    Label(top, text="E-MAIL :-").grid(row=3)

    Entry(top, width=30, textvariable=name).grid(row=1, column=1)
    Entry(top, width=30, textvariable=phone).grid(row=2, column=1)
    Entry(top, width=30, textvariable=mail).grid(row=3, column=1)

    Button(top, text="Submit", command=insert).grid(row=4, columnspan=2)

# Placeholder for update functionality
def update():
    showinfo('Sorry', 'This feature is not available yet')

# Main window setup
root = Tk()
root.title("Contact Application with SQLite")
root.geometry("700x500")

# Tkinter variables
name = StringVar()
phone = StringVar()
mail = StringVar()

# Title bar
f = Frame(root, height=50)
f.pack(fill=X, side=TOP)
Label(f, text="Contact Application", bg="white", fg="red", font=("Arial", 16)).pack(fill=X)

# Buttons
f2 = Frame(root, height=100, bg="black")
f2.pack(fill=X, side=TOP)

Button(f2, text="DELETE", command=delete).grid(row=1, column=3, sticky=N, padx=80)
Button(f2, text="+ADD", command=add).grid(row=1, column=4, sticky=N, padx=50)
Button(f2, text="UPDATE", command=update).grid(row=1, column=5, sticky=N, padx=100)

# Treeview
f3 = Frame(root, height=200, bg="blue")
f3.pack(fill=X)

tree = ttk.Treeview(f3)
tree["columns"] = ("one", "two")
tree.column("#0", width=210, minwidth=270, stretch=NO)
tree.column("one", width=210, minwidth=200, stretch=NO)
tree.column("two", width=250, minwidth=230, stretch=NO)

tree.heading("#0", text="Name", anchor=W)
tree.heading("one", text="Mobile Number", anchor=W)
tree.heading("two", text="Mail Id", anchor=W)

# Load existing data
con = sqlite3.connect('data.db')
c = con.cursor()
c.execute('CREATE TABLE IF NOT EXISTS contact (name TEXT, phone TEXT, mail TEXT)')
r = c.execute("SELECT * FROM contact")
for row in r:
    tree.insert('', 'end', text=row[0], values=(row[1], row[2]))
con.close()

tree.pack(side=TOP, fill=X)

root.resizable(0, 0)
root.mainloop()
