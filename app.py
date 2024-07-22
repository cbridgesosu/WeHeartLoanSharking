from flask import Flask, render_template, request, redirect
import os
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv('PORT')

# temporary data until DB implemented
enforcers = [
    {
    "firstName": "Sergei",
    "lastName": None,
    "startDate": "1990-01-01"
    },
    {
    "firstName": "Elena",
    "lastName": "Stark",
    "startDate": "2015-08-22"
    },
    {
    "firstName": "Georg",
    "lastName": "Rulin",
    "startDate": "2007-02-27"
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
                              "startDate": request.form.get("startDate")})
    return render_template("add_enforcer.j2", enforcers=enforcers)

@app.route('/test')
def test():
    return render_template("test.j2")


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', PORT))
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True, threaded=True) 