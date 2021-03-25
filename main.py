import select_subset_movies_db as movie_db
import select_subset_arrest_db as arrest_db


def main_script():
    run_movies_db()
    run_arrest_db()


def run_movies_db():
    # Specify the number of rows
    num_rows = [8000, 10000, 13000, 18000, 23000]

    movie_db.create_mongo(num_rows)
    movie_db.create_sql(num_rows)


def run_arrest_db():
    # Read in data, format and add sizes
    dataframes, dataframe_names, sizes = arrest_db.read_and_format()

    arrest_db.create_sql(dataframes, dataframe_names, sizes)
    arrest_db.create_mongo(dataframes, dataframe_names, sizes)


if __name__ == "__main__":
    main_script()
