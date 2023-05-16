import csv
import sys

from db import DB


def extract(data_path):
    rows = []

    with open(data_path) as file:
        csvreader = csv.reader(file)
        next(csvreader)  # Skip header row
        for row in csvreader:
            rows.append(row)

    return rows


def transform(rows):
    valid_rows = []

    for row in rows:
        valid_row = []
        for field in row:
            valid_row.append(' '.join(field.strip().split()))

        valid_row.append(1)  # book availability
        valid_rows.append(valid_row)

    return valid_rows


def load(db, rows):
    if not rows:
        return

    db.insert_many(
        'INSERT INTO books VALUES(:id, :isbn, :authors, :year, :title, :lang, :available)', rows
    )


class IngestPipeline:
    def __init__(self, data_path, db):
        self.db = db
        self.data_path = data_path

    def execute(self):
        load(self.db, transform(extract(self.data_path)))


if __name__ == "__main__":
    try:
        pipeline = IngestPipeline(sys.argv[1], DB())
        pipeline.execute()
    except FileNotFoundError:
        print("Please point to correct file")
