import pandas as pd


def create_size_independent_tables():
    all_users = pd.read_json("mflix_users.json")
    all_users['_id'] = all_users["_id"].apply(lambda x: {'oid': x["$oid"]})

    all_sessions = pd.read_json("mflix_sessions.json")
    all_sessions['_id'] = all_sessions["_id"].apply(lambda x: {'oid': x["$oid"]})

    return all_users, all_sessions


def create_movie_info(num_rows: int):

    ##Creation of movie_info csv
    all_movies = pd.read_json("mflix_movies.json").iloc[0:num_rows, :]
    all_movies['_id'] = all_movies["_id"].apply(lambda x: {'oid': x["$oid"]})

    return all_movies


def create_comments(all_movies):

    ###### Comments csv
    all_comments = pd.read_json("mflix_comments.json")
    all_comments['join_id'] = all_comments["movie_id"].apply(lambda x: x["$oid"])
    all_comments['_id'] = all_comments["_id"].apply(lambda x: {'oid': x["$oid"]})

    # only select comments from the relevant movies
    all_movies = all_movies["_id"].apply(lambda x: x["oid"])
    all_comments = all_comments.loc[all_comments["join_id"].isin(all_movies)]

    return all_comments