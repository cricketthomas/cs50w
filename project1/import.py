import csv
import os
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


try:
    db.execute("""
        CREATE TABLE books (
        isbn VARCHAR PRIMARY KEY,
        title VARCHAR NOT NULL,
        author VARCHAR NOT NULL,
        year VARCHAR NOT NULL);
        """
               )
    db.commit()
    print("table created.")
except:
    print("table exists.")




# open books.csv

f = open("books.csv")
reader = csv.reader(f)
for isbn, title, author, year in reader: # loop gives each column a name
    db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
              {"isbn": isbn, "title": title, "author": author,"year": year}) # substitute values from CSV line into SQL command, as per this dict
    print(f"Added book {title} by {author} with ISBN of {isbn} from {year}.")
    db.commit() # transactions are assumed, so close the transaction finished






# export DATABASE_URL="postgres://zwtbynvdmuhqzj:8ef8a4d9bc771976d0ee3ed1b09fae82072726642d8ba4593d393baac502803a@ec2-54-163-246-159.compute-1.amazonaws.com:5432/d14i40bolicsn5"
"""
sql = "INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
{"isbn": books['isbn'], "title": books['title'], "author": books['author'], "year": books['year'] }


("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
               {"isbn": books['isbn'], "title": books['title'], "author": books['author'], "year": books['year']})
"""
