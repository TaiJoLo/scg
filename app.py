from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import re
from datetime import datetime
from datetime import date
from datetime import timedelta
import mysql.connector
from mysql.connector import FieldType
import connect

app = Flask(__name__)

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/sites")
def listsites():
    connection = getCursor()
    connection.execute("SELECT * FROM sites;")
    sitelist = connection.fetchall()
    print(sitelist)
    return render_template("sitelist.html", sitelist = sitelist)  

@app.route("/campers", methods=['GET','POST'])
def campers():
    if request.method == "GET":
        return render_template("datepickercamper.html", currentdate = datetime.now().date())
    else:
        campDate = request.form.get('campdate')
        connection = getCursor()
        connection.execute("SELECT bookings.booking_id,bookings.booking_date,sites.site_id,sites.occupancy ,customers.firstname,customers.familyname,customers.email, customers.phone FROM bookings join sites on site = site_id inner join customers on customer = customer_id where booking_date= %s;",(campDate,))
        camperList = connection.fetchall()
        print(camperList)
        return render_template("datepickercamper.html", camperlist = camperList)

@app.route("/booking", methods=['GET','POST'])
def booking():
    if request.method == "GET":
        return render_template("datepicker.html", currentdate = datetime.now().date())
    else:
        bookingNights = request.form.get('bookingnights')
        bookingDate = request.form.get('bookingdate')
        occupancy = request.form.get('occupancy')
        firstNight = date.fromisoformat(bookingDate)

        lastNight = firstNight + timedelta(days=int(bookingNights))
        connection = getCursor()
        connection.execute("SELECT * FROM customers;")
        customerList = connection.fetchall()
        connection.execute("select * from sites where occupancy >= %s AND site_id not in (select site from bookings where booking_date between %s AND %s);",(occupancy,firstNight,lastNight))
        siteList = connection.fetchall()
        return render_template("bookingform.html", customerlist = customerList, bookingdate=bookingDate, sitelist = siteList, bookingnights = bookingNights, occupancy = occupancy)    

@app.route("/booking/add", methods=['POST'])
def makebooking():
    # Extracting data from the form
    customer_id = request.form.get('customer')
    site_id = request.form.get('site')
    bookingDate = request.form.get('bookingdate')
    bookingNights = int(request.form.get('bookingnights'))
    occupancy = int(request.form.get('occupancy'))

    # Parsing the booking start date
    start_date = date.fromisoformat(bookingDate)

    # Establishing database connection
    connection = getCursor() 

    # Inserting booking data for each night of the booking
    sql_query = """
        INSERT INTO bookings (booking_date, customer, site,occupancy)
        VALUES (%s, %s, %s, %s);
    """
    for night in range(bookingNights):
        booking_night_date = start_date + timedelta(days=night)
        connection.execute(sql_query, (booking_night_date, customer_id, site_id, occupancy))

    # Redirecting to a success page
    return redirect('/success')

# Success route to confirm booking addition
@app.route("/success")
def success():
    return "Booking successfully added!"


