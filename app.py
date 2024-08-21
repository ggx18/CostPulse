# app.py
from routes import app
app.secret_key = '12345'  # Set a secret key for session security

if __name__ == '__main__':
    app.run(debug=True)
