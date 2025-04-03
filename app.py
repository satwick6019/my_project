from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
import uuid
import time, os

app = Flask(__name__)

# Database connection details for MySQL
MYSQL_HOST = os.environ['MYSQL_HOST']
MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']
MYSQL_DB = os.environ['MYSQL_DB']

# Create a function to get a database connection
def get_db_connection():
    connection = pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        db=MYSQL_DB,
        cursorclass=pymysql.cursors.DictCursor  # This returns results as dictionaries
    )
    return connection

@app.before_request
def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Create the messages table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id VARCHAR(8) PRIMARY KEY,
            content TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message_content = request.form.get("message", "").strip()
        if not message_content:
            return "Error: No message entered!"

        # Generate a short unique message ID
        message_id = str(uuid.uuid4())[:8]

        # Insert the message into the database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO messages (id, content) VALUES (%s, %s)", (message_id, message_content))
        connection.commit()
        connection.close()

        # Create a link to read the message
        message_link = url_for("read_message", message_id=message_id, _external=True)

        return render_template("index.html", link=message_link)

    return render_template("index.html")

@app.route("/read/<message_id>")
def read_message(message_id):
    connection = get_db_connection()
    cursor = connection.cursor()

    # Fetch the message content from the database
    cursor.execute("SELECT content FROM messages WHERE id = %s", (message_id,))
    msg = cursor.fetchone()

    if msg:
        content = msg['content']

        # Simulate a delay of 10 seconds before deleting the message
        time.sleep(10)

        # Delete the message from the database after reading
        cursor.execute("DELETE FROM messages WHERE id = %s", (message_id,))
        connection.commit()
        connection.close()

        return render_template("message.html", message=content)

    connection.close()
    return "Message not found or already deleted."

@app.route('/delete_message', methods=['POST'])
def delete_message():
    message_data = request.get_json()
    message_id = message_data.get('message_id')

    connection = get_db_connection()
    cursor = connection.cursor()

    # Check if the message exists
    cursor.execute("SELECT * FROM messages WHERE id = %s", (message_id,))
    msg = cursor.fetchone()

    if msg:
        # Delete the message from the database
        cursor.execute("DELETE FROM messages WHERE id = %s", (message_id,))
        connection.commit()
        connection.close()
        return jsonify({'status': 'Message deleted'}), 200

    connection.close()
    return jsonify({'status': 'Message not found'}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)
