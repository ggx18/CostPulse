# config.py
import pyodbc

server_name = "HARSHA"
database_name = "Costplan1"
def create_db_connection():
    conn = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes')
    cursor = conn.cursor()
    return conn, cursor



# ########### THIS IS FOR SQLITE ################
# import os

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///students.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False