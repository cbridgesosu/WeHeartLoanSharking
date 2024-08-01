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
        "startDate": "1990-01-01",
        "rankID": 1
    },
    {
        "enforcerID": 2,
        "firstName": "Elena",
        "lastName": "Stark",
        "startDate": "2015-08-22",
        "rankID": 2
    },
    {
        "enforcerID": 3,
        "firstName": "Georg",
        "lastName": "Rulin",
        "startDate": "2007-02-27",
        "rankID": "NULL"
    }
]

clients = [
    {
         "clientID": 1,
        "firstName": "Jon",
        "lastName": "Snow",
        "inGoodStanding": True
    },
    {
        "clientID": 2,
        "firstName": "Cersei",
        "lastName": "Lannister",
        "inGoodStanding": False
    },
    {
        "clientID": 3,
        "firstName": "Ned",
        "lastName": "Stark",
        "inGoodStanding": False
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

locations = [
     {
          'businessID': 1,
          'ownerID': 1,
          'streetAddress': '1234 Main St',
          'cityName': 'Chicago',
          'stateName': 'Illinois',
          'zipCode': 60603
     },
     {
          'businessID': 2,
          'ownerID': 1,
          'streetAddress': '5678 Westeros Pl',
          'cityName': 'Paris',
          'stateName': 'Texas',
          'zipCode': 75462
     },
     {
          'businessID': 3,
          'ownerID': 2,
          'streetAddress': '23rd W. Broadway',
          'cityName': 'New York',
          'stateName': 'New York',
          'zipCode': 10016
     },
     {
          'businessID': 4,
          'ownerID': 3,
          'streetAddress': '327 Beagle St',
          'cityName': 'San Diego',
          'stateName': 'California',
          'zipCode': 92038
     }
]

loans = [
     {
          "loanID": 1,
          "clientID": 1,
          "originationAmount": 50000,
          "principalRemaining": 50000,
          "originationDate": "2024-07-04",
          "interestRate": 33,
          "paymentDue": 15
     },
     {
          "loanID": 2,
          "clientID": 1,
          "originationAmount": 50000,
          "principalRemaining": 50000,
          "originationDate": "2024-07-05",
          "interestRate": 33,
          "paymentDue": 15
     },  
     {
          "loanID": 3,
          "clientID": 2,
          "originationAmount": 200000,
          "principalRemaining": 150000,
          "originationDate": "2022-01-01",
          "interestRate": 45,
          "paymentDue": 10
     },
     {
          "loanID": 4,
          "clientID": 3,
          "originationAmount": 100000,
          "principalRemaining": 55000,
          "originationDate": "2023-12-25",
          "interestRate": 23,
          "paymentDue": 10
     },
]

collections = [
      {
            "collectionID": 1,
            "enforcerID": 1,
            "loanID": 1,
            "businessID": 2,
            "amountCollected": 1000,
            "dateOfCollection": "2024-07-01"
      },
      {
            "collectionID": 2,
            "enforcerID": 2,
            "loanID": 2,
            "businessID": 1,
            "amountCollected": 5000,
            "dateOfCollection": "2024-07-10"
      },
      {
            "collectionID": 3,
            "enforcerID": 3,
            "loanID": 3,
            "businessID": 3,
            "amountCollected": 1500,
            "dateOfCollection": "2024-07-07"
      },
]

ranks = [
      {
            "rankID": 1,
            "rankName": "Underboss"
      },
      {
            "rankID": 2,
            "rankName": "Captain"
      },
      {
            "rankID": 3,
            "rankName": "Soldier"
      }
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
                              "startDate": request.form.get("startDate"),
                              "rankID": request.form.get("rankID")})
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

@app.route('/update_client', methods=["POST", "GET"])
def update_client():
    if request.method == "POST":
            print("Client updated.")
    return render_template("update_client.j2", clients=clients)

@app.route('/delete_client', methods=["POST", "GET"])
def delete_client():
    if request.method == "POST":
            print("Client deleted.")
    return render_template("delete_client.j2", clients=clients)

@app.route('/add_location', methods=["POST", "GET"])
def add_location():
    if request.method == "POST":
            print("Location added.")

    return render_template("add_location.j2", locations=locations, clients=clients)

@app.route('/add_loan', methods=["POST", "GET"])
def add_loan():
    if request.method == "POST":
            print("Loan added.")

    return render_template("add_loan.j2", loans=loans, clients=clients)

@app.route('/add_collection', methods=["POST", "GET"])
def add_collection():
    if request.method == "POST":
            print("Collection added.")

    return render_template("add_collection.j2", collections=collections, loans=loans, enforcers=enforcers, locations=locations)

@app.route('/add_rank', methods=["POST", "GET"])
def add_rank():
    if request.method == "POST":
            print("Rank added.")
            id = len(ranks) + 1
            ranks.append({"rankName": request.form.get("rankName"),
                          "rankID": len(ranks) +1})
    return render_template("add_rank.j2", ranks=ranks)

@app.route('/test')
def test():
    return render_template("test.j2")


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', PORT))
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port) 