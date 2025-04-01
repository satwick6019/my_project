import uuid
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
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.String(8), primary_key=True)
    content = db.Column(db.String(1000), nullable=False)


@app.before_request
def create_tables():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        message_content = request.form.get("message", "").strip()
        if not message_content:
            return "Error: No message entered!"

        D
        message_id = str(uuid.uuid4())[:8]

       
        new_message = Message(id=message_id, content=message_content)
        db.session.add(new_message)
        db.session.commit()

       
        message_link = url_for("read_message", message_id=message_id, _external=True)

       
        return render_template("index.html", link=message_link)

    return render_template("index.html")

@app.route("/read/<message_id>")
def read_message(message_id):
    
    msg = db.session.get(Message, message_id)
    
    if msg:
        content = msg.content

        
        time.sleep(10)  

       
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
