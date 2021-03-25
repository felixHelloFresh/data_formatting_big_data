import pandas as pd


def create_size_independent_tables():
    all_users = pd.read_json("mflix_users.json")
    all_sessions = pd.read_json("mflix_sessions.json")

    return all_users, all_sessions


def create_movie_info(num_rows: int):

    ##Creation of movie_info csv
    all_movies = pd.read_json("mflix_movies.json").iloc[0:num_rows, :]

    return all_movies


def create_comments(all_movies):

    ###### Comments csv
    all_comments = pd.read_json("mflix_comments.json")
    all_comments['join_id'] = all_comments["movie_id"].apply(lambda x: x["$oid"])

    # only select comments from the relevant movies
    all_movies = all_movies["_id"].apply(lambda x: x["$oid"])
    all_comments = all_comments.loc[all_comments["join_id"].isin(all_movies)]

    return all_comments