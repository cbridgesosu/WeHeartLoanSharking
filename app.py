from flask import Flask, render_template
import os
from dotenv import load_dotenv

load_dotenv()

PORT = os.getenv('PORT')

# Configuration

app = Flask(__name__)

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/test')
def test():
    return render_template("test.j2")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', PORT))
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 