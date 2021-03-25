import json
import pandas as pd


def create_movie_info(num_rows: int):

    ##Creation of movie_info csv
    all_movies = pd.read_json("mflix_movies.json").rename(columns ={"_id": "movie_id"}).iloc[0:num_rows, :]

    #Released is dropped due to incorrect values
    award_df = pd.json_normalize(all_movies['awards']).rename(columns={"wins": "award_wins", "nominations": "award_nominations", "text": "award_text"})
    imdb_df = pd.json_normalize(all_movies['imdb']).rename(columns={"rating": "imdb_rating", "votes": "imdb_votes", "id": "imdb_id"})
    tomatoes_df = all_movies["tomatoes"]

    ## fill na values with empty dicts
    tomatoes_df = tomatoes_df.fillna({i: {} for i in tomatoes_df.index})
    tomatoes_df_flat = pd.json_normalize(tomatoes_df)
    tomatoes_df_final = tomatoes_df_flat.rename(columns={"viewer.rating": "tomato_viewer_rating", "viewer.numReviews": "tomato_viewer_num_reviews", "viewer.meter": "tomato_viewer_meter", "lastUpdated.$date": "tomato_lastupdated",
                                                        "fresh": "tomato_fresh", "rotten": "tomato_rotten", "critic.rating": "tomato_critic_rating", "critic.numReviews": "tomato_critic_num_reviews",
                                                          "critic.meter": "tomato_critic_meter", "dvd.$date": "tomato_dvd_date", "website": "tomato_website", "production": "tomato_production", "consensus": "tomato_consensus"}).drop("dvd.$date.$numberLong", axis=1)

    #Released is dropped due to incorrect values
    movies_info = all_movies.drop(["genres", "directors", "countries", "cast", "writers", "languages", "released", "awards", "imdb", "tomatoes"], axis=1)
    movies_info = pd.merge(movies_info, award_df, right_index=True, left_index=True)
    movies_info = pd.merge(movies_info, imdb_df, right_index=True, left_index=True)
    movies_info = pd.merge(movies_info, tomatoes_df_final , right_index=True, left_index=True)
    #change id to correct key value from dict
    movies_info["movie_id"] = movies_info["movie_id"].apply(lambda x: x["$oid"])

    return movies_info, all_movies


def create_dependent_tables_movies(all_movies):

    # Creation of movie genre csv
    movie_genres = all_movies[["movie_id", "genres"]].explode("genres")
    movie_genres = movie_genres.dropna()
    movie_genres["movie_id"] = movie_genres["movie_id"].apply(lambda x: x["$oid"])

    # Creation of movie cast csv
    movie_cast = all_movies[["movie_id", "cast"]].explode("cast")
    movie_cast = movie_cast.dropna()
    movie_cast["movie_id"] = movie_cast["movie_id"].apply(lambda x: x["$oid"])

    # creation of movie countries csv
    movie_countries = all_movies[["movie_id", "countries"]].explode("countries")
    movie_countries = movie_countries.dropna()
    movie_countries["movie_id"] = movie_countries["movie_id"].apply(lambda x: x["$oid"])

    # creation of movie directors csv
    movie_directors = all_movies[["movie_id", "directors"]].explode("directors")
    movie_directors = movie_directors.dropna()
    movie_directors["movie_id"] = movie_directors["movie_id"].apply(lambda x: x["$oid"])

    # creation of movie_languages csv
    movie_languages = all_movies[["movie_id", "languages"]].explode("languages")
    movie_languages = movie_languages.dropna()
    movie_languages["movie_id"] = movie_languages["movie_id"].apply(lambda x: x["$oid"])

    # creation of movie writers #csv
    movie_writers = all_movies[["movie_id", "writers"]].explode("writers")
    movie_writers = movie_writers.dropna()
    movie_writers["movie_id"] = movie_writers["movie_id"].apply(lambda x: x["$oid"])

    # Remove all additional explanation beyond writers name
    movie_writers["writers"] = movie_writers["writers"].str.replace(r"\([^()]*\)","")

    # remove duplicates since same writer could have written multiple parts of the movie
    movie_writers = movie_writers[["movie_id", "writers"]].astype(str).drop_duplicates()

    return movie_genres, movie_cast, movie_countries, movie_directors, movie_languages, movie_writers


def create_users():
    ### Users csv
    all_users = pd.read_json("mflix_users.json").rename(columns ={"_id": "user_id"})
    all_users["user_id"] = all_users["user_id"].apply(lambda x: x["$oid"])

    return all_users


def create_comments(all_users, all_movies):

    ###### Comments csv
    all_comments = pd.read_json("mflix_comments.json").rename(columns ={"_id": "comment_id"})
    all_comments["comment_id"] = all_comments["comment_id"].apply(lambda x: x["$oid"])
    all_comments["movie_id"] = all_comments["movie_id"].apply(lambda x: x["$oid"])
    all_comments["date"] = all_comments["date"].apply(lambda x: x["$date"])

    # Add the user_id to each comment
    all_users_ids_name = all_users[['user_id', 'name']]
    all_comments = pd.merge(all_comments, all_users_ids_name, how='left', on='name')

    # Only select comments that have a movie associated with them
    all_movies["movie_id"] = all_movies["movie_id"].apply(lambda x: x["$oid"])
    all_movies = all_movies["movie_id"]
    all_comments = all_comments.loc[all_comments["movie_id"].isin(all_movies)]

    # Change order
    all_comments = all_comments[['comment_id', 'user_id', 'movie_id', 'name', 'email', 'text', 'date']]

    return all_comments


def create_sessions():
    ### Session csv
    all_sessions = pd.read_json("mflix_sessions.json").rename(columns={"_id": "session_id"})
    all_sessions["session_id"] = all_sessions["session_id"].apply(lambda x: x["$oid"])

    return all_sessions




















