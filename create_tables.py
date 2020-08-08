import pandas as pd
from src.models.books import Books
from src.repositories import RepositoryContainer

# from src.models.reviews import Reviews
# from src.models.users import Users


def main():
    print("Creating Tables...")
    db = RepositoryContainer.engine()
    db.create_all()

    # Add books info
    books_df = pd.read_csv("src/data/books.csv")
    for idx, row in books_df.iterrows():
        book = Books(
            isbn=row["isbn"], title=row["title"], author=row["author"], year=row["year"]
        )
        print(idx, row)
        db.session.add(book)

    # Commit Changes
    print("Commiting changes...")
    db.session.commit()


if __name__ == "__main__":
    main()
