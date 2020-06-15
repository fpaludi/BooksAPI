import os
import pandas as pd
from flask import Flask, request
from factory_app import create_app
from src.models.books import Books
from src.models.users import Users
from src.models.reviews import Reviews
from src import db

app = create_app("default")

def main():
    print("Creating Tables...")
    db.create_all()

    # Add books info
    books_df = pd.read_csv("src/data/books.csv")
    for idx, row in books_df.iterrows():
        book = Books(isbn=row["isbn"],title=row["title"],author=row["author"],year=row["year"])
        print(idx, row)
        db.session.add(book)

    # Commit Changes
    print("Commiting changes...")
    db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        main()
