import csv
import os
import pandas as pd
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

#open books.csv
books = csv.reader(file("books.csv"))




try:
    db.execute("""
        CREATE TABLE books (
        isbn INTEGER PRIMARY KEY,
        title VARCHAR NOT NULL,
        author VARCHAR NOT NULL, 
        year INTEGER );
        """
        )
    db.commit()
    print("table created.")
except:
    print("table exists.")



# export DATABASE_URL="postgres://zwtbynvdmuhqzj:8ef8a4d9bc771976d0ee3ed1b09fae82072726642d8ba4593d393baac502803a@ec2-54-163-246-159.compute-1.amazonaws.com:5432/d14i40bolicsn5"
