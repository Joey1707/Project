from backend.app import MYSQLdb
from werkzeug.security import generate_password_hash
import datetime

class User(MYSQLdb.Model):
    __tablename__ = 'userData'  # Table name should match the actual table in your database

    id = MYSQLdb.Column(MYSQLdb.Integer, primary_key=True, autoincrement=True)  # Ensure correct primary key
    username = MYSQLdb.Column(MYSQLdb.String(50), nullable=True, unique = True)  # Matching column name and type
    passwd = MYSQLdb.Column(MYSQLdb.String(512), nullable=True)  # Matching column name and type
    email = MYSQLdb.Column(MYSQLdb.String(50), nullable=True, unique = True)
    date = MYSQLdb.Column(MYSQLdb.DateTime, default = datetime.datetime.now, nullable = True)
    number_of_data = MYSQLdb.Column(MYSQLdb.INT, default = 0)

    def __repr__(self):
        return f"<User {self.username}>"
    
    # CREATE TABLE userData (
#     id INT PRIMARY KEY AUTO_INCREMENT, 
#     username VARCHAR(50), 
#     passwd VARCHAR(50), 
#     email VARCHAR(50) UNIQUE
# );
