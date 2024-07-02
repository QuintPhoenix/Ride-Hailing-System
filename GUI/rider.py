from tkinter import *
from tkinter.ttk import *
import oracledb
import time
con = oracledb.connect(
    user="c##kevin",
    password="manager",
    dsn="localhost:49703/xe")

cur = con.cursor()
cur.execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'")

def getTrips(userid):
    cur.execute('select count(*) from trip where rider_id='+str(userid))
    rows = cur.fetchone()
    return str(rows[0])

def getStatus(tripid):
    cur.execute('select status from trip where trip_id='+str(tripid))
    rows = cur.fetchone()
    return str(rows[0])

def getAmount(userid):
    cur.execute('select sum(fare) from trip where rider_id='+str(userid))
    rows = cur.fetchone()
    return str(rows[0])

def getDriverDetails(userid):
    cur.execute('select name,phone_num from trip,driver where rider_id='+str(userid)+"and trip.driver_id=driver.user_id order by trip.start_time desc")
    rows = cur.fetchall()
    if(rows):
        name = rows[0][0]
        phone_num = rows[0][1]
    else:
        name = "NIL"
        phone_num = "NIL"
    return "\nName - "+name+"\nPhone Number - "+phone_num

def lastTripLocation(userid):
    cur.execute('select drop_loc from trip where rider_id='+str(userid))
    rows = cur.fetchall()
    if(rows):
        return str(rows[0][0])
    else:
        return "NIL"

def createTrip(start_loc,end_loc,userid):
    argumentss = [int(1),str(start_loc),str(end_loc),int(userid),int(1)]
    cur.callproc('insert_trip',argumentss)
    con.commit()
    cur.execute('select max(trip_id) from trip where rider_id='+str(userid))
    trip_id = cur.fetchone()
    cur.callproc('assign_driver',[int(trip_id[0])])
    con.commit()
        
def riderWindow(userid):
    win2 = Tk()
    win2.geometry("600x600")
    win2.title("Rider Page")

    style = Style()

    style.configure("W.TButton", font=("Arial", 17), foreground="blue", bd="4")

    def bookRide():
        if(pickupLoc_Entry.get() == "" and DropLoc_Entry.get() == ""):
            return True
        createTrip(pickupLoc_Entry.get(),DropLoc_Entry.get(),userid)
        cur.execute('select max(trip_id) from trip where rider_id='+str(userid))
        tripid=cur.fetchone()
        status_label.config(text="Status :- "+getStatus(tripid[0]),foreground="green")
        return True

    AnalyticsFrame = LabelFrame(win2).pack(expand='yes', fill='both')
    headLabel_AnalyticsFrame = Label(AnalyticsFrame, text="Analytics", font=("Arial", 25))
    headLabel_AnalyticsFrame.place(x=250, y=15)

    field1_var, field2_var, field3_var, field4_var = StringVar(),StringVar(),StringVar(),StringVar()
    num_drivers = str(StringVar())

    Label1 = Label(AnalyticsFrame, text="Trips taken till now :- " + getTrips(userid), font=("Arial", 13))
    Label1.place(x=50, y=100)
    Label2 = Label(AnalyticsFrame, text="Amount paid till now :- " + getAmount(userid) +" Rs.", font=("Arial", 13))
    Label2.place(x=320, y=100)
    Label3 = Label(AnalyticsFrame, text="Last Trip Driver Details :- " + getDriverDetails(userid), font=("Arial", 13))
    Label3.place(x=50, y=200)
    Label4 = Label(AnalyticsFrame, text="Last Trip Drop-off Pincode - " + lastTripLocation(userid), font=("Arial", 13))
    Label4.place(x=320, y=200)

    RideBookingFrame = LabelFrame(win2).pack(expand="yes", fill="both")
    headLabel_BookingFrame = Label(RideBookingFrame, text="Book A Ride", font=("Arial", 25))
    headLabel_BookingFrame.place(x=225, y=320)
    pickupLoc_Label = Label(RideBookingFrame, text="Pick Up Location", font=("Arial", 13))
    pickupLoc_Label.place(x=25, y=400)
    pickupLoc_Entry = Entry(RideBookingFrame, font=("Arial", 14))
    pickupLoc_Entry.place(x=160, y=400)
    dropLoc_Label = Label(RideBookingFrame, text="Drop Location", font=("Arial", 13))
    dropLoc_Label.place(x=25, y=475)
    DropLoc_Entry = Entry(RideBookingFrame, font=("Arial", 14))
    DropLoc_Entry.place(x=160, y=475)
    rideBookingButton = Button(RideBookingFrame, text="Book a Ride", command=bookRide, style="W.TButton")
    rideBookingButton.place(x=425, y=435)
    status_label = Label(RideBookingFrame, text="Status :- ", font=("Arial", 13))
    status_label.place(x=375, y=535)
    
    win2.mainloop()

