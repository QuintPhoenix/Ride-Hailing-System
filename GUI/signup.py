from tkinter import *
from tkinter.ttk import *
import rider, driver
import oracledb

con = oracledb.connect(
    user="c##kevin",
    password="manager",
    dsn="localhost:49703/xe")

cur = con.cursor()


root = Tk()
root.title("Sign Up Window")
root.geometry("500x300")
style = Style()
style.configure("W.TButton",font=("Arial", 13, "bold"), foreground="green")

def login():
    phone=phone_var.get()
    password = password_var.get()
    pass_length = len(password)
    global rows
    if drive_or_user.current() == 1:
        cur.execute('select * from rider where PHONE_NUM='+phone)
        rows = cur.fetchall()
        
    else:
        cur.execute('select * from driver where PHONE_NUM='+phone)
        rows = cur.fetchall()
    
    if((len(phone) == 10 and pass_length>0) and len(rows) != 0 and rows[0][1]==password and rows[0][4]==phone):
        Success_Label.place(x=170, y=220)
        
        if(drive_or_user.current() == 1):
            root.destroy()
            rider.riderWindow(rows[0][0])
            
        else:
            root.destroy()
            driver.driverWindow(rows[0][0])    
            
           
    else: 
        Error_Label.place(x=170,y=220)

phone_var = StringVar()
password_var = StringVar()

head_Label = Label(root, text="Login", font=("Arial", 25, "bold"))
head_Label.place(x=200, y=10)
n = StringVar()
drive_or_user = Combobox(root, width = 27, textvariable = n) 
drive_or_user["values"] = ("Driver", "Rider")
drive_or_user.place(x=10, y=50)

Email_Label = Label(root, text="Phone Number: ", font=("Arial", 13))
Email_Label.place(x=10, y=80)
Email_Entry = Entry(root, textvariable=phone_var,font=("Arial", 13))
Email_Entry.place(x=180, y=80)

Error_Label = Label(root, text="Login error! Check email/password", font=("Arial", 10), foreground="red")
Success_Label = Label(root, text="Login Sucessful", font=("Arial", 10), foreground="green")

Password_Label = Label(root, text="Password: ", font=("Arial", 13))
Password_Label.place(x=10, y=130)
Password_Entry = Entry(root, textvariable=password_var, font=("Arial", 13), show="*")
Password_Entry.place(x=180, y=130)

submit_button = Button(root, text="Login", style="W.TButton", command=login)
submit_button.place(x=180, y=180)
root.mainloop()

