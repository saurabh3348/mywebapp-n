import os
import psycopg2
import requests
from flask import Flask, request, render_template

app = Flask(__name__)

# Configuration for backend service name and namespace
FRONTEND_SERVICE_NAME = os.environ.get("FRONTEND_SERVICE_NAME", "frontend-service")
FRONTEND_NAMESPACE = os.environ.get("FRONTEND_NAMESPACE", "frontend")

# Frontend URL configuration
app.config["FRONTEND_URL"] = f"http://{FRONTEND_SERVICE_NAME}.{FRONTEND_NAMESPACE}.svc.cluster.local"

# Use environment variables to configure the database connection
DATABASE_URL = (
    f"dbname='{os.getenv('DB_NAME')}' "
    f"user='{os.getenv('DB_USER')}' "
    f"password='{os.getenv('DB_PASSWORD')}' "
    f"host='{os.getenv('DB_HOST')}'"
)

# Establish a connection to the database
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

# SQL command to create a table named "users" in the "test" schema
create_table_sql = """
CREATE TABLE IF NOT EXISTS test.users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255),
    email VARCHAR(255)
);
"""

# Execute the SQL command to create the table
cur.execute(create_table_sql)

@app.route('/')
def index():
    # Fetch index.html from the frontend service
    frontend_url = app.config["FRONTEND_URL"]
    response = requests.get(f"{frontend_url}/index.html")
    return response.text

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    email = request.form['email']
    cur.execute("INSERT INTO test.users (username, email) VALUES (%s, %s)", (username, email))
    conn.commit()
    return "Submitted!"

# Define other routes and functions as needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
