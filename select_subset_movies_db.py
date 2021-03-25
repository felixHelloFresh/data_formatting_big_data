import os
import shutil
import json
import pandas as pd

import movies_to_sql
import movies_to_document


def create_sql(num_rows):

    # Create movies_db folder
    parent_dir = os.getcwd()
    directory = 'movies_db_relational'
    path = os.path.join(parent_dir, directory)

    # Create a directory to hold the files
    try:
        os.mkdir(path)
    except FileExistsError:
        shutil.rmtree(path)
        os.mkdir(path)

    for num in num_rows:

        ##Creation of movie_info csv
        movies_info, all_movies = movies_to_sql.create_movie_info(num)
        movie_genres, movie_cast, movie_countries, movie_directors, movie_languages, movie_writers = movies_to_sql.create_dependent_tables_movies(all_movies)

        all_users = movies_to_sql.create_users()
        all_comments = movies_to_sql.create_comments(all_users, all_movies)
        all_sessions = movies_to_sql.create_sessions()

        # Determine location of P2L outputs
        parent_dir = os.getcwd()
        directory = 'movies_db_relational'
        subdirectory = str(num)
        individual_path = os.path.join(parent_dir, directory, subdirectory)

        # Create a directory to hold the files
        try:
            os.mkdir(individual_path)
        except FileExistsError:
            shutil.rmtree(individual_path)
            os.mkdir(individual_path)

        # Write all files to CSV
        movies_info.to_csv(individual_path + os.sep + 'movies_info.csv', index=False)
        movie_genres.to_csv(individual_path + os.sep + 'movie_genres.csv', index=False)
        movie_cast.to_csv(individual_path + os.sep + 'movie_cast.csv', index=False)
        movie_countries.to_csv(individual_path + os.sep + 'movie_countries.csv', index=False)
        movie_directors.to_csv(individual_path + os.sep + 'movie_directors.csv', index=False)
        movie_languages.to_csv(individual_path + os.sep + 'movie_languages.csv', index=False)
        movie_writers.to_csv(individual_path + os.sep + 'movie_writers.csv', index=False)
        all_users.to_csv(individual_path + os.sep + 'all_users.csv', index=False)
        all_comments.to_csv(individual_path + os.sep + 'all_comments.csv', index=False)
        all_sessions.to_csv(individual_path + os.sep + 'all_sessions.csv', index=False)


def create_mongo(num_rows):

    # Create movies_db folder
    parent_dir = os.getcwd()
    directory = 'movies_db_document'
    path = os.path.join(parent_dir, directory)

    # Create a directory to hold the files
    try:
        os.mkdir(path)
    except FileExistsError:
        shutil.rmtree(path)
        os.mkdir(path)

    for num in num_rows:

        ##Creation of movie_info csv
        all_movies = movies_to_document.create_movie_info(num)
        all_comments = movies_to_document.create_comments(all_movies)
        all_users, all_sessions = movies_to_document.create_size_independent_tables()

        # Determine location of P2L outputs
        parent_dir = os.getcwd()
        directory = 'movies_db_document'
        subdirectory = str(num)
        individual_path = os.path.join(parent_dir, directory, subdirectory)

        # Create a directory to hold the files
        try:
            os.mkdir(individual_path)
        except FileExistsError:
            shutil.rmtree(individual_path)
            os.mkdir(individual_path)

        all_movies.to_json(individual_path + os.sep + 'movies_info.json')
        all_comments.to_json(individual_path + os.sep + 'all_comments.json')
        all_users.to_json(individual_path + os.sep + 'all_users.json')
        all_sessions.to_json(individual_path + os.sep + 'all_sessions.json')


def main_func():
    # Specify the number of rows
    num_rows = [8000, 10000, 13000, 18000, 23000]
    create_sql(num_rows)
    create_mongo(num_rows)

