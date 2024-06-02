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

# Route for searching customers
@app.route("/search_customer", methods=['GET', 'POST'])
def search_customer():
    # If the request method is GET, render the search form
    if request.method == "GET":
        return render_template("search_customer.html")
    else:
        # Extract the search term from the form
        search_term = request.form.get('search_term')

        # Establish database connection
        connection = getCursor()

        # Perform a SQL query to search for customers with partial matches
        query = """
            SELECT * FROM customers
            WHERE customer_id LIKE %s OR firstname LIKE %s OR familyname LIKE %s OR email LIKE %s OR phone LIKE %s
        """
        # Use wildcards to match any part of the name
        connection.execute(query, (f"%{search_term}%",f"%{search_term}%", f"%{search_term}%",f"%{search_term}%",f"%{search_term}%"))
        customer_list = connection.fetchall()

        # Render the results on the same page
        return render_template("search_result.html", customer_list=customer_list, search_term=search_term)

@app.route("/customeredit")
def editcustomer():
    id = request.args.get("id")
    connection = getCursor()
    connection.execute("SELECT * FROM customers WHERE customer_id=%s;",(id,))
    customer = connection.fetchone()
    return render_template("customerform.html", customer = customer)

@app.route("/customerupdate", methods=["POST"])
def updatecustomer():
    id = request.form.get("id")
    fname = request.form.get("customerfname")
    sname = request.form.get("customersname")
    email = request.form.get("customeremail")
    phone = request.form.get("customerphone")
    connection = getCursor()
    connection.execute("UPDATE customers SET firstname=%s, familyname=%s, email=%s, phone=%s WHERE customer_id=%s;",(fname,sname,email,phone,id))
    return redirect("/search_customer")

@app.route("/customeradd", methods=["POST"])
def addcustomer():
    # Extract data from the form
    fname = request.form.get("customerfname")
    sname = request.form.get("customersname")
    email = request.form.get("customeremail")
    phone = request.form.get("customerphone")
    
    # Establishing database connection
    connection = getCursor()
    
    # Insert new customer data into the database
    sql_query = """
        INSERT INTO customers (firstname, familyname, email, phone)
        VALUES (%s, %s, %s, %s)
    """
    connection.execute(sql_query, (fname, sname, email, phone))

    # Get the ID of the newly added customer
    connection.execute("SELECT LAST_INSERT_ID()")
    customer_id = connection.fetchone()[0]
    
    # Render the success page with a message
    return render_template("success.html", message="Customer successfully added!", customer_id=customer_id,fname=fname,sname=sname,email=email,phone=phone)
