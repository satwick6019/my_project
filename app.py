# # from flask import Flask, render_template, request, redirect, url_for
# # from flask_sqlalchemy import SQLAlchemy
import uuid

# # app = Flask(__name__)
# # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///messages.db"
# # db = SQLAlchemy(app)

# # # Database model
# # class Message(db.Model):
# #     id = db.Column(db.String, primary_key=True)
# #     content = db.Column(db.Text, nullable=False)

# # # Home page (enter message)
# # @app.route("/", methods=["GET", "POST"])
# # # def index():
# # #     if request.method == "POST":
# # #         message_content = request.form["message"]
# # #         message_id = str(uuid.uuid4())[:8]  # Generate short random ID
# # #         new_message = Message(id=message_id, content=message_content)
# # #         db.session.add(new_message)
# # #         db.session.commit()
# # #         return redirect(url_for("read_message", message_id=message_id))
# # #     return render_template("index.html")
# # def index():
# #     if request.method == "POST":
# #         print("Form Submitted!")  # Debugging
# #         message_content = request.form.get("message", "").strip()
# #         if not message_content:
# #             print("No message entered!")
# #             return "Error: No message entered!"
        
# #         message_id = str(uuid.uuid4())[:8]
# #         new_message = Message(id=message_id, content=message_content)
# #         db.session.add(new_message)
# #         db.session.commit()
        
# #         print("Generated Link:", url_for("read_message", message_id=message_id, _external=True))
# #         return redirect(url_for("read_message", message_id=message_id))

# #     return render_template("index.html")
# # # Read message page
# # @app.route("/read/<message_id>")
# # def read_message(message_id):
# #     msg = db.session.get(Message, message_id)  # Updated query
# #     if msg:
# #         content = msg.content
# #         print("Message read:", content)  # Debugging

# #         db.session.delete(msg)
# #         db.session.commit()
# #         return render_template("message.html", message=content)

# #     print("Message not found or already deleted.")  # Debugging
# #     return "Message not found or already deleted."

# # if __name__ == "__main__":
# #     with app.app_context():
# #         db.create_all()  # Create database tables
# #     app.run(debug=True)


from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, render_template, request, redirect, url_for, jsonify

from flask_sqlalchemy import SQLAlchemy
import uuid
import time

app = Flask(__name__)
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(BASE_DIR, 'instance', 'messages.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/messages.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    content = db.Column(db.String(1000), nullable=False)

# Create the database tables if they don't exist
@app.before_request
def create_tables():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message_content = request.form.get("message", "").strip()
        if not message_content:
            return "Error: No message entered!"

        # Generate a unique message ID
        message_id = str(uuid.uuid4())[:8]

        # Add the message to the database
        new_message = Message(id=message_id, content=message_content)
        db.session.add(new_message)
        db.session.commit()

        # Generate the link
        message_link = url_for("read_message", message_id=message_id, _external=True)

        # Return the link to the user
        return render_template("index.html", link=message_link)

    return render_template("index.html")

@app.route("/read/<message_id>")
def read_message(message_id):
    # Retrieve the message from the database
    msg = db.session.get(Message, message_id)
    
    if msg:
        content = msg.content

        # Set a delay before deleting the message
        time.sleep(10)  # Wait for 10 seconds

        # Delete the message from the database after 10 seconds
        db.session.delete(msg)
        db.session.commit()

        return render_template("message.html", message=content)
    
    return "Message not found or already deleted."

@app.route('/delete_message', methods=['POST'])
def delete_message():
    message_data = request.get_json()
    message_id = message_data.get('message_id')
    msg = Message.query.filter_by(id=message_id).first()
    if msg:
        db.session.delete(msg)
        db.session.commit()
        return jsonify({'status': 'Message deleted'}), 200
    return jsonify({'status': 'Message not found'}), 404
if __name__ == "__main__":
    app.run(debug=True)
# from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask_sqlalchemy import SQLAlchemy
# import threading
# import time

# app = Flask(__name__)
# import os
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# db_path = os.path.join(BASE_DIR, 'instance', 'messages.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/message.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     message = db.Column(db.String(200), nullable=False)
#     link = db.Column(db.String(100), nullable=False)

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/', methods=['POST'])
# def generate_message():
#     secret_message = request.form['message']
#     message_link = str(uuid.uuid4().hex)
#     new_message = Message(message=secret_message, link=message_link)
#     db.session.add(new_message)
#     db.session.commit()
#     link = url_for('read', message_id=message_link, _external=True)
#     return render_template('index.html', link=link)

# @app.route('/read/<message_id>')
# def read(message_id):
#     msg = Message.query.filter_by(link=message_id).first()
#     if msg:
#         return render_template('message.html', message=msg.message, message_id=msg.id)
#     else:
#         return "Message not found", 404

# @app.route('/delete_message', methods=['POST'])
# def delete_message():
#     message_data = request.get_json()
#     message_id = message_data.get('message_id')
#     msg = Message.query.filter_by(id=message_id).first()
#     if msg:
#         db.session.delete(msg)
#         db.session.commit()
#         return jsonify({'status': 'Message deleted'}), 200
#     return jsonify({'status': 'Message not found'}), 404

# if __name__ == "__main__":
#     app.run(debug=True)
