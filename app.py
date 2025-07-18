# The code for database configuration and general route structure is adapted from the CS340 Flask starter code and module walkthroughs.
# All route logic and SQL queries are entirely our own work with the following exception:
    # Parameterized SQL query structure based on Flask module guide videos
    # Database error handling:
        # Date: 08/05/24
        # Adapted from the docmentation at:
        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-errors-integrityerror.html

from flask import Flask, render_template, request, redirect, json
import os
from dotenv import load_dotenv
from flask_mysqldb import MySQL

load_dotenv()

PORT = os.getenv('PORT')

# Configuration - this module copied from the starter code
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = os.getenv('DB_NAME')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD') 
app.config['MYSQL_DB'] = os.getenv('DB_NAME')
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Route for home page
@app.route("/")
def root():
    return render_template("main.j2")


# Routes for Enforcers page
@app.route('/add_enforcer', methods=["POST", "GET"])
def add_enforcer():
    # Query to populate the display table
    query_Enforcers = 'SELECT enforcerID, firstName, lastName, startDate, rankName FROM Enforcers LEFT JOIN Ranks ON Enforcers.rankID=Ranks.rankID ORDER BY enforcerID;'
    # Query to polulate the select Ranks dropdown  
    query_Ranks = 'SELECT rankID, rankName FROM Ranks;'

    # Execute all queries and store json
    cur = mysql.connection.cursor()
    cur.execute(query_Enforcers)
    enforcers = cur.fetchall()
    cur.execute(query_Ranks)
    ranks = cur.fetchall()

    # Handles add new enforcer form request
    if request.method == "POST":
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        startDate = request.form.get('startDate')
        rankID = request.form.get('rankID')
        if rankID == "None":
             rankID = None

        # Insert query for add new enforcer
        query_Add_Enforcer = f"INSERT INTO Enforcers (firstName, lastName, startDate, rankID) VALUES (%s, %s, %s, %s);"
        try:
            cur.execute(query_Add_Enforcer, (firstName, lastName, startDate, rankID,))
            mysql.connection.commit()
            print("Enforcer added.")
        except mysql.connection.IntegrityError as err:
                print("Error: {}".format(err))
        return redirect('add_enforcer')


    return render_template("add_enforcer.j2", enforcers=enforcers, ranks=ranks)

@app.route('/delete_enforcer/<int:enforcerID>')
def delete_enforcer(enforcerID):
    # Query to delete enforcer entry with selected ID
    query_Delete_Enforcer = "DELETE FROM Enforcers WHERE enforcerID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_Delete_Enforcer, (enforcerID,))
    mysql.connection.commit()
    return redirect('/add_enforcer')

@app.route('/update_enforcer/<int:enforcerID>', methods=["POST", "GET"])
def update_enforcer(enforcerID):
    cur = mysql.connection.cursor()
    if request.method == "GET":
        # Query to populate form with current enforcer attributes
        query_Enforcer_selected = 'SELECT enforcerID, firstName, lastName, startDate, Ranks.rankID, rankName FROM Enforcers LEFT JOIN Ranks ON Ranks.rankID=Enforcers.rankID WHERE enforcerID = %s;' % (enforcerID)
        cur.execute(query_Enforcer_selected)
        enforcer = cur.fetchall()
        # Query to populate ranks select dropdown
        query_Ranks = 'SELECT * FROM Ranks;'
        cur.execute(query_Ranks)
        ranks = cur.fetchall()
        # Render the page if the request is a GET
        return render_template("update_enforcer.j2", enforcer=enforcer, ranks=ranks)
    # Handles update enforcer form request
    elif request.method == "POST":
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        startDate = request.form.get('startDate')
        rankID = request.form.get('rankID')
        if rankID == "None":
             rankID = None
        # Query to update efnrocer attributes
        query_Update_Enforcer = "UPDATE Enforcers SET Enforcers.firstName = %s, Enforcers.lastName = %s, Enforcers.startDate = %s, Enforcers.rankID = %s WHERE Enforcers.enforcerID = %s;"
        try:
            print(firstName, lastName, startDate, rankID, enforcerID)
            cur.execute(query_Update_Enforcer, (firstName, lastName, startDate, rankID, enforcerID))
            mysql.connection.commit()
        except mysql.connection.IntegrityError as err:
                print("Error: {}".format(err))
        return redirect('../add_enforcer')

# Routes for Clients page
@app.route('/add_client', methods=["POST", "GET"])
def add_client():
    cur = mysql.connection.cursor()

    if request.method == "GET":
            # Query to polulate the Client table
            query_Clients = 'SELECT * FROM Clients;'
            cur.execute(query_Clients)
            clients = cur.fetchall()
            return render_template("add_client.j2", clients=clients)

    if request.method == "POST":
            # Query inputs from form, then add row to database
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            inGoodStanding = request.form.get('inGoodStanding')
            query_Add_Client = "INSERT INTO Clients (firstName, lastName, inGoodStanding) VALUES (%s, %s, %s);"
            try:
                cur.execute(query_Add_Client, (firstName, lastName, inGoodStanding))
                mysql.connection.commit()
            except mysql.connection.IntegrityError as err:
                  print("Error: {}".format(err))
            return redirect('add_client')
    
    

@app.route('/update_client/<int:clientID>', methods=["POST", "GET"])
def update_client(clientID):
    cur = mysql.connection.cursor()
    if request.method == "GET":
        query_Client_selected = 'SELECT * FROM Clients WHERE clientID = %s;' % (clientID)
        cur.execute(query_Client_selected)
        client = cur.fetchall()
        # Render the page if the request is a GET
        return render_template("update_client.j2", client=client)
    elif request.method == "POST":
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        inGoodStanding = request.form.get('inGoodStanding')
        query_Update_Client = "UPDATE Clients SET Clients.firstName = %s, Clients.lastName = %s, Clients.inGoodStanding = %s WHERE Clients.clientID = %s;"
        try:
            cur.execute(query_Update_Client, (firstName, lastName, inGoodStanding, clientID))
            mysql.connection.commit()
        except:
            print("Error: ")
        return redirect('../add_client')


@app.route('/delete_client/<int:clientID>', methods=["POST", "GET"])
def delete_client(clientID):
    # Query to delete Client entry with selected ID
    query_Delete_Client = "DELETE FROM Clients WHERE clientID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_Delete_Client, (clientID,))
    mysql.connection.commit()
    return redirect('../add_client')


# Routes for enforcers_has_clients page
@app.route('/enforcers_has_clients', methods=["POST", "GET"])
def enforcers_has_clients():  
    # Query to populate the display table
    query_EnforcersHasClients = 'SELECT enforcerHasClientID, Enforcers.firstName, Enforcers.lastName, Clients.firstName, Clients.lastName FROM EnforcersHasClients INNER JOIN Enforcers ON EnforcersHasClients.enforcerID=Enforcers.enforcerID INNER JOIN Clients ON EnforcersHasClients.clientID=Clients.clientID ORDER BY enforcerHasClientID;'
    # Query to polulate the select client dropdown  
    query_Clients = 'SELECT clientID, firstName, lastName FROM Clients;'
    # Query to polulate the select enforcer dropdown 
    query_Enforcers = 'SELECT enforcerID, firstName, lastName FROM Enforcers;'

    # Execute all queries and store json
    cur = mysql.connection.cursor()
    cur.execute(query_EnforcersHasClients)
    enforcer_has_clients = cur.fetchall()
    cur.execute(query_Clients)
    clients = cur.fetchall()
    cur.execute(query_Enforcers)
    enforcers = cur.fetchall()
    # print(enforcer_has_clients, clients, enforcers)

    # Handles add new enforcer_has_client form request
    if request.method == "POST":
            clientID = request.form.get('assign_client')
            enforcerID = request.form.get('assign_enforcer')

            # Insert query for add new enforcers_has_client 
            query_Add_Assignment = "INSERT INTO EnforcersHasClients (enforcerID, clientID) VALUES (%s, %s);"
            try:
                cur.execute(query_Add_Assignment, (enforcerID, clientID))
                mysql.connection.commit()
                print("Client assigned.")
            except mysql.connection.IntegrityError as err:
                  print("Error: {}".format(err))
            return redirect('enforcers_has_clients')
    
    return render_template("enforcers_has_clients.j2", enforcers=enforcers, clients=clients, enforcer_has_clients=enforcer_has_clients)

@app.route('/delete_assignment/<int:enforcerHasClientID>')
def delete_assignment(enforcerHasClientID):
    # Query to delete enforcer_has_client entry with selected ID
    query_Delete_Assignment = "DELETE FROM EnforcersHasClients WHERE enforcerHasClientID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_Delete_Assignment, (enforcerHasClientID,))
    mysql.connection.commit()

    return redirect('/enforcers_has_clients')

@app.route('/edit_assignment/<int:id>', methods=["POST", "GET"])
def edit_assignment(id):
    # Setup queries for Clients, Enforcers and the Selected relationship to edit.
    query_Clients = 'SELECT clientID, firstName, lastName FROM Clients;'
    query_Enforcers = 'SELECT enforcerID, firstName, lastName FROM Enforcers;'
    query_EnforcersHasClients_selected = "SELECT * FROM EnforcersHasClients WHERE enforcerHasClientID = %s;" % (id)

    # Perform the queries to get the necessary information from the db to render the page
    cur = mysql.connection.cursor()
    cur.execute(query_Clients)
    clients = cur.fetchall()
    cur.execute(query_Enforcers)
    enforcers = cur.fetchall()
    cur.execute(query_EnforcersHasClients_selected)
    selection = cur.fetchall()
    if request.method == "GET":
        # Render the page if the request is a GET
        return render_template("enforcers_has_clients_update.j2", enforcers=enforcers, clients=clients, selection=selection)
    elif request.method == "POST":
        # Perform the update in the database with the values supplied by the user if the request is a POST
        clientID = request.form.get('assign_client')
        enforcerID = request.form.get('assign_enforcer')
        query_Update_Assignment = f"UPDATE EnforcersHasClients SET EnforcersHasClients.clientID = {clientID}, EnforcersHasClients.enforcerID = {enforcerID} WHERE EnforcersHasClients.enforcerHasClientID = {id};"
        # If an illegal set of values is given this will catch the database error.
        try:
            cur.execute(query_Update_Assignment)
            mysql.connection.commit()
        except mysql.connection.IntegrityError as err:
                  print("Error: {}".format(err))
        return redirect('/enforcers_has_clients')


# Routes for Locations page
@app.route('/add_location', methods=["POST", "GET"])
def add_location():
    cur = mysql.connection.cursor()
    # Query to populate the clients select dropdown
    query_Clients = 'SELECT clientID, firstName, lastName FROM Clients;'
    cur.execute(query_Clients)
    clients = cur.fetchall()
    # Query to populate the locations display table
    query_Business_Locations = 'SELECT businessID, streetAddress, cityName, stateName, zipCode, Clients.firstName, Clients.lastName FROM BusinessLocations JOIN Clients ON BusinessLocations.ownerID = Clients.clientID;'
    cur.execute(query_Business_Locations)
    locations = cur.fetchall()

    # Handles the new location form request
    if request.method == "POST":
            clientID = request.form.get('assign_owner')
            streetAddress = request.form.get('streetAddress')
            stateName = request.form.get('stateName')
            cityName = request.form.get('cityName')
            zipCode = request.form.get('zipCode')

            # Insert query for add new location 
            query_Add_Location = "INSERT INTO BusinessLocations (ownerID, streetAddress, cityName, stateName, zipCode) VALUES (%s, %s, %s, %s, %s);"
            try:
                cur.execute(query_Add_Location, (clientID, streetAddress, stateName, cityName, zipCode))
                mysql.connection.commit()
                print("Client assigned.")
            except mysql.connection.IntegrityError as err:
                  print("Error: {}".format(err))
            return redirect('/add_location')
    
    return render_template("add_location.j2", locations=locations, clients=clients)

@app.route('/delete_location/<int:businessID>')
def delete_location(businessID):
    # Query to delete location entry with selected ID
    query_Delete_Location = "DELETE FROM BusinessLocations WHERE businessID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_Delete_Location, (businessID,))
    mysql.connection.commit()
    return redirect('/add_location')

# Routes for Loans page
@app.route('/add_loan', methods=["POST", "GET"])
def add_loan():
    # Query to populate loan display table
    query_Loans = '(SELECT loanID, firstName, lastName, originationAmount, originationDate, interestRate, paymentDue FROM Loans INNER JOIN Clients ON Loans.clientID=Clients.clientID ORDER BY loanID) AS Loans'
    query_amountCollected = '(SELECT loanID, SUM(amountCollected) AS amountPaid FROM Collections GROUP BY loanID) AS collectionSum'
    query_amountPaid = f'(SELECT Loans.loanID, Loans.originationAmount - collectionSum.amountPaid AS principalRemaining FROM {query_amountCollected} INNER JOIN Loans ON Loans.loanID=collectionSum.loanID) AS amountPaid'
    query_combineLoansPaid = f'SELECT Loans.loanID, interestRate, originationAmount, originationDate, firstName, lastName, paymentDue, principalRemaining FROM {query_Loans} LEFT JOIN {query_amountPaid} ON Loans.loanID=amountPaid.loanID;'
    # Query to populate client select dropdown
    query_Clients = 'SELECT clientID, firstName, lastName FROM Clients;'
    
    
    # Executes all queries and stores json
    cur = mysql.connection.cursor()
    cur.execute(query_combineLoansPaid)
    loans = cur.fetchall()
    cur.execute(query_Clients)
    clients = cur.fetchall()

    #Handles add new loan form request
    if request.method == "POST":
            originationAmount = request.form.get('originationAmount')
            interestRate = request.form.get('interestRate')
            dueDate = request.form.get('paymentDue')
            clientID = request.form.get('assign_loan')

            # Insert query for add new loan
            query_Add_Location = "INSERT INTO Loans (clientID, originationAmount, principalRemaining, originationDate, interestRate, paymentDue) VALUES (%s, %s, %s, NOW(), %s, %s);"
            try:
                cur.execute(query_Add_Location, (clientID, originationAmount, originationAmount, interestRate, dueDate))
                mysql.connection.commit()
                print("Loan added.")
            except mysql.connection.IntegrityError as err:
                  print("Error: {}".format(err))
            return redirect('/add_loan')

    return render_template("add_loan.j2", loans=loans,  clients=clients)

@app.route('/delete_loan/<int:loanID>')
def delete_loan(loanID):
    # Query to delete loan entry with selected ID
    query_Delete_Loan = "DELETE FROM Loans WHERE loanID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_Delete_Loan, (loanID,))
    mysql.connection.commit()
    return redirect('/add_loan')

# Routes for Collections page
@app.route('/add_collection', methods=["POST", "GET"])
def add_collection():
    cur = mysql.connection.cursor()
    # Query to populate locations select dropdown
    query_Business_Locations = 'SELECT * FROM BusinessLocations;'
    cur.execute(query_Business_Locations)
    locations = cur.fetchall()
    # Query to populate enforcers select dropdown
    query_Enforcers = 'SELECT * FROM Enforcers;'
    cur.execute(query_Enforcers)
    enforcers = cur.fetchall()
    # Query to populate loans select dropdown
    query_Loans = 'SELECT * FROM Loans INNER JOIN Clients ON Clients.clientID=Loans.clientID;'
    cur.execute(query_Loans)
    loans = cur.fetchall()
    # Query to populate collections display table
    query_Collections = 'SELECT * FROM Collections INNER JOIN BusinessLocations ON Collections.businessID=BusinessLocations.businessID INNER JOIN Enforcers ON Enforcers.enforcerID=Collections.enforcerID;'
    cur.execute(query_Collections)
    collections = cur.fetchall()

    # Handles collections form add request
    if request.method == "POST":
            enforcerID = request.form.get('select_enforcer')
            loanID = request.form.get('select_loan')
            businessID = request.form.get('select_location')
            amountCollected = request.form.get('amount_collected')
            # Insert query for add new collection
            query_Add_Collection = "INSERT INTO Collections (enforcerID, loanID, businessID, amountCollected, dateOfCollection) VALUES (%s, %s, %s, %s, NOW());"
            try:
                cur.execute(query_Add_Collection, (enforcerID, loanID, businessID, amountCollected))
                mysql.connection.commit()
                print("Loan added.")
            except mysql.connection.IntegrityError as err:
                  print("Error: {}".format(err))
            return redirect('/add_collection')

    return render_template("add_collection.j2", collections=collections, loans=loans, enforcers=enforcers, locations=locations)

@app.route('/delete_collection/<int:collectionID>')
def delete_collection(collectionID):
    # Query to delete collection entry with selected ID
    query_Delete_Collection = "DELETE FROM Collections WHERE collectionID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_Delete_Collection, (collectionID,))
    mysql.connection.commit()
    return redirect('/add_collection')

# Routes for Ranks page
@app.route('/add_rank', methods=["POST", "GET"])
def add_rank():
    cur = mysql.connection.cursor()
    # Query to populate ranks display table
    query_Ranks = 'SELECT * FROM Ranks ORDER BY rankID;'
    cur.execute(query_Ranks)
    ranks = cur.fetchall()

    # Handles ranks form add request
    if request.method == "POST":
            rankName = request.form.get('rankName')
            # Insert query to add new rank
            query_Add_Rank = "INSERT INTO Ranks (rankName) VALUES (%s);"
            try:
                 cur.execute(query_Add_Rank, (rankName,))
                 mysql.connection.commit()
            except mysql.connection.IntegrityError as err:
                  print("Error: {}".format(err))
            return redirect('/add_rank')
    return render_template("add_rank.j2", ranks=ranks)

@app.route('/delete_rank/<int:rankID>')
def delete_rank(rankID):
    # Query to delete rank entry with selected ID
    query_Delete_Rank = "DELETE FROM Ranks WHERE rankID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query_Delete_Rank, (rankID,))
    mysql.connection.commit()

    return redirect('../add_rank')

# Listener - this module copied from the starter code
if __name__ == "__main__":
    port = int(os.environ.get('PORT', PORT))
    
    app.run(port=port) 