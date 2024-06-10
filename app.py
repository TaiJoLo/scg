from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
import re
from datetime import datetime
from datetime import date
from datetime import timedelta
import mysql.connector
from mysql.connector import FieldType
import connect
app = Flask(__name__)
app.secret_key = 'flash'

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, 
                                         password=connect.dbpass, 
                                         host=connect.dbhost, 
                                         database=connect.dbname, 
                                         autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/sites")
def listsites():
    connection = getCursor()
    sql_query = """ 
        SELECT * FROM sites;
    """
    connection.execute(sql_query)
    sitelist = connection.fetchall()
    return render_template("sitelist.html", sitelist=sitelist)

@app.route("/campers", methods=['GET', 'POST'])
def campers():
    if request.method == "GET":
        return render_template("datepickercamper.html", currentdate=datetime.now().date())
    else:
        campDate = request.form.get('campdate')
        connection = getCursor()
        sql_query = """
            SELECT bookings.booking_id, bookings.booking_date, sites.site_id, bookings.occupancy, customers.firstname, customers.familyname, customers.email, customers.phone 
            FROM bookings 
            JOIN sites ON site = site_id 
            INNER JOIN customers ON customer = customer_id 
            WHERE booking_date = %s;
        """
        connection.execute(sql_query, (campDate,))
        camperList = connection.fetchall()
        return render_template("camperlist.html", camperlist=camperList)

@app.route("/booking", methods=['GET', 'POST'])
def booking():
    if request.method == "GET":
        return render_template("datepicker.html", currentdate=datetime.now().date())
    else:
        bookingNights = request.form.get('bookingnights')
        bookingDate = request.form.get('bookingdate')
        occupancy = request.form.get('occupancy')

        if not bookingDate:
            flash('Booking date is required.')
            return redirect(url_for('booking'))

        try:
            firstNight = date.fromisoformat(bookingDate)
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.')
            return redirect(url_for('booking'))

        lastNight = firstNight + timedelta(days=int(bookingNights))
        connection = getCursor()
        sql_query1 = """ 
            SELECT * FROM customers;
        """
        connection.execute(sql_query1)
        customerList = connection.fetchall()
        sql_query2 = """
            SELECT * FROM sites 
            WHERE occupancy >= %s 
            AND site_id NOT IN 
            (SELECT site 
             FROM bookings 
             WHERE booking_date BETWEEN %s AND %s);
        """
        connection.execute(sql_query2, (occupancy, firstNight, lastNight))
        siteList = connection.fetchall()
        return render_template("bookingform.html", customerlist=customerList, bookingdate=bookingDate, sitelist=siteList, bookingnights=bookingNights, occupancy=occupancy)

@app.route("/booking/add", methods=['POST'])
def makebooking():
    customer_id = request.form.get('customer')
    site_id = request.form.get('site')
    bookingDate = request.form.get('bookingdate')
    bookingNights = int(request.form.get('bookingnights'))
    occupancy = int(request.form.get('occupancy'))

    try:
        start_date = date.fromisoformat(bookingDate)
    except ValueError:
        flash('Invalid date format. Please use YYYY-MM-DD.')
        return redirect(url_for('booking'))

    connection = getCursor()

    sql_query1 = """
        INSERT INTO bookings (booking_date, customer, site, occupancy)
        VALUES (%s, %s, %s, %s);
    """
    for night in range(bookingNights):
        booking_night_date = start_date + timedelta(days=night)
        connection.execute(sql_query1, (booking_night_date, customer_id, site_id, occupancy))

    sql_query2 = """
        SELECT firstname, familyname 
        FROM customers 
        WHERE customer_id = %s
    """
    connection.execute(sql_query2, (customer_id,))
    customer = connection.fetchone()
    fname = customer[0]
    sname = customer[1]

    return render_template('success.html', message='Booking successfully added!', customer_id=customer_id, fname=fname, sname=sname, site_id=site_id, booking_date=bookingDate, booking_nights=bookingNights, occupancy=occupancy)

@app.route("/search_customer", methods=['GET', 'POST'])
def search_customer():
    if request.method == "GET":
        return render_template("search_customer.html")
    else:
        search_term = request.form.get('search_term')
        connection = getCursor()

        sql_query = """
            SELECT * FROM customers
            WHERE customer_id LIKE %s OR firstname LIKE %s OR familyname LIKE %s OR email LIKE %s OR phone LIKE %s
        """
        connection.execute(sql_query, (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"))
        customerList = connection.fetchall()

        return render_template("search_result.html", customerlist=customerList, search_term=search_term)

@app.route("/customeredit")
def editcustomer():
    id = request.args.get("id")
    connection = getCursor()
    sql_query = """
        SELECT * FROM customers WHERE customer_id=%s;
    """
    connection.execute(sql_query, (id,))
    customer = connection.fetchone()
    return render_template("customerform.html", customer=customer)

@app.route("/customerupdate", methods=["POST"])
def updatecustomer():
    id = request.form.get("id")
    fname = request.form.get("customerfname")
    sname = request.form.get("customersname")
    email = request.form.get("customeremail")
    phone = request.form.get("customerphone")
    connection = getCursor()
    sql_query = """
        UPDATE customers 
        SET firstname=%s, familyname=%s, email=%s, phone=%s 
        WHERE customer_id=%s
    """
    connection.execute(sql_query, (fname, sname, email, phone, id))
    
    return render_template("success.html", message="Customer successfully updated!", customer_id=id, fname=fname, sname=sname, email=email, phone=phone)

@app.route("/customeradd", methods=["POST"])
def addcustomer():
    fname = request.form.get("customerfname")
    sname = request.form.get("customersname")
    email = request.form.get("customeremail")
    phone = request.form.get("customerphone")
    connection = getCursor()
    
    sql_query1 = """
        INSERT INTO customers (firstname, familyname, email, phone)
        VALUES (%s, %s, %s, %s)
    """
    connection.execute(sql_query1, (fname, sname, email, phone))

    sql_query2 = """
        SELECT LAST_INSERT_ID()
    """
    connection.execute(sql_query2)
    customer_id = connection.fetchone()[0]
    
    return render_template("success.html", message="Customer successfully added!", customer_id=customer_id, fname=fname, sname=sname, email=email, phone=phone)

@app.route("/customerlist")
def customerlist():
    connection = getCursor()
    sql_query = """
        SELECT customer_id, firstname, familyname, email, phone 
        FROM customers
    """
    connection.execute(sql_query)
    customerList = connection.fetchall()
    return render_template("search_result.html", customerlist=customerList)

@app.route("/customersummary")
def customersummary():
    customer_id = request.args.get("id")
    connection = getCursor()

    query = """
        SELECT 
            c.customer_id, 
            CONCAT(c.firstname, ' ', c.familyname) AS name,
            COUNT(b.booking_date) AS total_nights,
            AVG(b.occupancy) AS average_occupancy
        FROM 
            customers c
        LEFT JOIN 
            bookings b ON c.customer_id = b.customer
        WHERE 
            c.customer_id = %s
        GROUP BY 
            c.customer_id, c.firstname, c.familyname
    """
    connection.execute(query, (customer_id,))
    customer_summary = connection.fetchone()

    return render_template("customer_summary.html", customer_summary=customer_summary)
