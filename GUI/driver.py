from tkinter import *
from tkinter.ttk import *
import oracledb
import time
con = oracledb.connect(
    user="c##kevin",
    password="manager",
    dsn="localhost:49703/xe")

cur = con.cursor()
global current_status
def getTrips(userid):
    cur.execute('select count(*) from trip where driver_id='+str(userid))
    rows = cur.fetchone()
    return str(rows[0])

def getCut(userid):
    cur.execute('select sum(cut) from driver where user_id='+str(userid))
    rows = cur.fetchone()
    return str(rows[0])

def getRating(userid):
    cur.execute('select avg_rating from driver where user_id='+str(userid))
    rows = cur.fetchone()
    return str(rows[0])

def getLastRider(userid):
    cur.execute('select name,phone_num from trip,rider where driver_id='+str(userid)+"and trip.rider_id=rider.user_id order by trip.start_time desc")
    rows = cur.fetchall()
    if(rows):
        name = rows[0][0]
        phone_num = rows[0][1]
    else:
        name = "NIL"
        phone_num = "NIL"
    return "\nName - "+name+"\nPhone Number - "+phone_num

def lastTripLocation(userid):
    cur.execute('select drop_loc from trip where driver_id='+str(userid))
    rows = cur.fetchall()
    if(rows):
        return str(rows[0][0])
    else:
        return "NIL"



            

def driverWindow(userid):
    def finalize(distance,trip_id):
        fare = int(distance)*2
        cut = fare*0.2
        cur.execute("update trip set dist="+str(distance)+",fare="+str(fare)+",status='Completed',rating=4.5 where trip_id="+str(trip_id))
        cur.execute("update driver set cut="+str(cut)+" where user_id="+str(userid))
        cur.callproc("update_trip_end_time",[int(trip_id)])
        con.commit()

    def checkForTrips(userid):
        cur.execute('Select status from trip where driver_id='+str(userid))
        status_list = cur.fetchall()
        for status in status_list :
            print(status)
            if(status[0]=='Alloted'):
                ride_status_label.configure(text='Trip Status - Alloted')
                accept_button["state"] = "normal"
                cancel_button["state"] = "normal"
                
    win1 = Tk()
    win1.geometry("800x600")
    win1.title("Driver Page")

    def accept_ride():
        ride_status_label.configure(text='Trip Status - Started')
        return True

    def cancel_ride():
        ride_status_label.configure(text='Trip Status - Complete')
        cur.execute("Select trip_id from trip where driver_id="+str(userid)+" and status='Alloted'")
        distance=distance_entry.get()
        trip_id_list=cur.fetchone()
        trip_id=trip_id_list[0]
        finalize(distance,trip_id)
        
        

    field1_var, field2_var, field3_var, field4_var,field5_var, field6_var, field7_var, field8_var = StringVar(),StringVar(),StringVar(),StringVar(), StringVar(), StringVar(), StringVar(), StringVar()

    style = Style()
    style.configure("success.TButton", font=("Arial", 15), foreground="green")
    style.configure("danger.TButton", font=("Arial", 15), foreground="red")

    driver_analytics_frame = LabelFrame(win1).pack(expand="yes", fill="both")
    analytics_head_label = Label(driver_analytics_frame, text="Analytics", font=("Arial", 25))
    analytics_head_label.place(x=350, y=5)

    Label1 = Label(driver_analytics_frame, text="Trips Done till now - "+getTrips(userid), font=("Arial", 13))
    Label1.place(x=75, y=50)
    
    Label3 = Label(driver_analytics_frame, text="Cut Pending - " + getCut(userid), font=("Arial", 13))
    Label3.place(x=574, y=50)
    Label4 = Label(driver_analytics_frame, text="Last Rider :- " + getLastRider(userid), font=("Arial", 13))
    Label4.place(x=75, y=150)
    Label2 = Label(driver_analytics_frame, text="Last Drop-off Location :- " + lastTripLocation(userid), font=("Arial", 13))
    Label2.place(x=574, y=150)


    ride_status_var = str(StringVar()) 
    dist_var = str(StringVar())
    fare_var = str(StringVar())
    drop_var = str(StringVar())
    distance_entry_value=StringVar()

    drive_acceptance_frame = LabelFrame(win1).pack(expand="yes", fill="both")
    drive_head_label = Label(drive_acceptance_frame, text="Ride Details", font=("Arial", 25))
    drive_head_label.place(x=335, y=320)
    ride_status_label = Label(drive_acceptance_frame, text="Ride Status: Not Alloted", font=("Arial", 13))
    ride_status_label.place(x=75, y=380)
    accept_button = Button(drive_acceptance_frame, text="Start Ride", command=accept_ride, style="success.TButton")
    accept_button.place(x=75, y=450)
    accept_button["state"] = "disabled"
    cancel_button = Button(drive_acceptance_frame, text="End Ride", command=cancel_ride, style="danger.TButton")
    cancel_button.place(x=575, y=450)
    cancel_button["state"] = "disabled"
    distance_label = Label(drive_acceptance_frame, text="Distance: ", font=("Arial", 13))
    distance_label.place(x=80, y=550)
    distance_entry=Entry(win1, textvariable=distance_entry_value,font=("Arial", 13))
    distance_entry.place(x=160,y=550)
    checkForTrips(userid)
    win1.mainloop()
    