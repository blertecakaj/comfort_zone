from flask import Flask, render_template, request, redirect, session, flash
from flask_bcrypt import Bcrypt    


app = Flask(__name__)
app.secret_key = 'secret' 
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
