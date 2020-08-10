import contextlib
import pandas as pd
from sqlalchemy.exc import ArgumentError
from settings import update_settings
from src.models.orm import metadata, start_mappers
from src.models.books import Books


def create_tables(engine, session):
    print("Creating Tables...")
    try:
        start_mappers()
    except ArgumentError:
        pass
    metadata.create_all(engine)

    # Add books info
    books_df = pd.read_csv("src/data/books.csv")
    print("Saving books...")
    for idx, row in books_df.iterrows():
        book = Books(
            isbn=row["isbn"], title=row["title"], author=row["author"], year=row["year"]
        )
        session.add(book)

    # Commit Changes
    print("Commiting changes...")
    session.commit()


def delete_tables(engine, session):
    print("\nRemoving Tables...\n")
    with contextlib.closing(engine.connect()) as con:
        trans = con.begin()
        for table in reversed(metadata.sorted_tables):
            con.execute(table.delete())
        trans.commit()


if __name__ == "__main__":
    update_settings("default")
    from src.repositories import RepositoryContainer

    engine = RepositoryContainer.engine()
    session = RepositoryContainer.session()

    create_tables(engine, session)
