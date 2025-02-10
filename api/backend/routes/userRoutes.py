from backend.app import db
from werkzeug.security import generate_password_hash
import datetime

INDTimeDelta = datetime.timedelta(hours=7)
INDTZOObject = datetime.timezone(INDTimeDelta,
                                 name = "IND")
class User(db.Model):
    __tablename__ = 'userData'  # Table name should match the actual table in your database

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Ensure correct primary key
    username = db.Column(db.String(50), nullable=True, unique = True)  # Matching column name and type
    passwd = db.Column(db.String(512), nullable=True)  # Matching column name and type
    email = db.Column(db.String(50), nullable=True, unique = True)
    date = db.Column(db.DateTime, default = datetime.datetime.now, nullable = True)

    def __repr__(self):
        return f"<User {self.username}>"
    
# CREATE TABLE userData (
#     id INT PRIMARY KEY AUTO_INCREMENT, 
#     username VARCHAR(50), 
#     passwd VARCHAR(50), 
#     email VARCHAR(50) UNIQUE
# );