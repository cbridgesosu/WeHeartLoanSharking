from flask import Flask, render_template, request, redirect
import os
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv('PORT')

# temporary data until DB implemented
enforcers = [
    {
        "enforcerID": 1,
        "firstName": "Sergei",
        "lastName": None,
        "startDate": "1990-01-01"
    },
    {
        "enforcerID": 2,
        "firstName": "Elena",
        "lastName": "Stark",
        "startDate": "2015-08-22"
    },
    {
        "enforcerID": 3,
        "firstName": "Georg",
        "lastName": "Rulin",
        "startDate": "2007-02-27"
    }
]

clients = [
    {
         "clientID": 1,
        "firstName": "Jon",
        "lastName": "Snow",
        "inGoodStanding": True,
        "loansRemaining": 100000
    },
    {
        "clientID": 2,
        "firstName": "Cersei",
        "lastName": "Lannister",
        "inGoodStanding": False,
        "loansRemaining": 150000
    },
    {
        "clientID": 3,
        "firstName": "Ned",
        "lastName": "Stark",
        "inGoodStanding": False,
        "loansRemaining": 55000
    }
]

enforcer_has_clients = [
    {
        'enforcerClientID': 1,
        'enforcerID': 1,
        'clientID': 3
    },
    {
        'enforcerClientID': 2,
        'enforcerID': 2,
        'clientID': 1
    },
    {
        'enforcerClientID': 3,
        'enforcerID': 3,
        'clientID': 3
    },
    {
        'enforcerClientID': 4,
        'enforcerID': 2,
        'clientID': 3
    },
]

# Configuration

app = Flask(__name__)


# Routes 

@app.route("/")
def root():
    return render_template("main.j2")

@app.route('/add_enforcer', methods=["POST", "GET"])
def add_enforcer():
    if request.method == "POST":
            print("Enforcer added.")
            enforcers.append({"firstName": request.form.get("firstName"), 
                              "lastName": request.form.get("lastName"), 
                              "startDate": request.form.get("startDate")})
    return render_template("add_enforcer.j2", enforcers=enforcers)

@app.route('/add_client', methods=["POST", "GET"])
def add_client():
    if request.method == "POST":
            print("Client added.")
            clients.append({"firstName": request.form.get("firstName"), 
                              "lastName": request.form.get("lastName"), 
                              "inGoodStanding": True,
                              "loansRemaining": 0})
    return render_template("add_client.j2", clients=clients)

@app.route('/assign_client', methods=["POST", "GET"])
def assign_client():
    if request.method == "POST":
            print("Client assigned.")
    return render_template("assign_client.j2", enforcers=enforcers, clients=clients, enforcer_has_clients=enforcer_has_clients)

@app.route('/test')
def test():
    return render_template("test.j2")


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', PORT))
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port) 