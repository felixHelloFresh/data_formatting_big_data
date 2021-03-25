import os
import shutil

import pandas as pd
import json


def read_and_format() -> (pd.DataFrame, pd.DataFrame, [int]):
    full_csv = pd.read_csv("NYPD_Arrest_Data__Year_to_Date_.csv")

    # Select relevant columns and format datetime
    arrest_info = full_csv[["ARREST_KEY", "ARREST_PRECINCT", "ARREST_DATE", "PD_CD", "PD_DESC", "KY_CD", "OFNS_DESC", "LAW_CODE", "LAW_CAT_CD"]]
    arrest_info["ARREST_DATE"] = pd.to_datetime(arrest_info["ARREST_DATE"])

    # Create first separate table
    arrest_person = full_csv[["ARREST_KEY", "AGE_GROUP", "PERP_SEX", "PERP_RACE"]]

    # Create second separate table
    arrest_location = full_csv[["ARREST_KEY", "ARREST_BORO","JURISDICTION_CODE", "X_COORD_CD", "Y_COORD_CD", "Latitude", "Longitude"]]

    # Add together separate tables and names
    dataframes = [arrest_info, arrest_person, arrest_location]
    dataframe_names = ["arrest_info", "arrest_person", "arrest_location"]

    # Define size subsets
    sizes = [50000, 60000, 80000, 110000, 140000]

    return dataframes, dataframe_names, sizes


def create_sql(dataframes: pd.DataFrame, dataframe_names: pd.DataFrame, sizes: [int]):

    # Create movies_db folder
    parent_dir = os.getcwd()
    directory = 'arrest_db_relational'
    path = os.path.join(parent_dir, directory)

    # Create a directory to hold the files
    try:
        os.mkdir(path)
    except FileExistsError:
        shutil.rmtree(path)
        os.mkdir(path)

    for size in sizes:

        # Determine location of P2L outputs
        parent_dir = os.getcwd()
        directory = 'arrest_db_relational'
        subdirectory = str(size)
        individual_path = os.path.join(parent_dir, directory, subdirectory)

        # Create a directory to hold the files
        try:
            os.mkdir(individual_path)
        except FileExistsError:
            shutil.rmtree(individual_path)
            os.mkdir(individual_path)

        for df, df_name in zip(dataframes, dataframe_names):

            temp_df = df[0:size]
            temp_df.to_csv(individual_path + os.sep + f"{df_name}.csv", index=False)


def create_mongo(dataframes: pd.DataFrame, dataframe_names: pd.DataFrame, sizes: [int]):
    # Create movies_db folder
    parent_dir = os.getcwd()
    directory = 'arrest_db_document'
    path = os.path.join(parent_dir, directory)

    # Create a directory to hold the files
    try:
        os.mkdir(path)
    except FileExistsError:
        shutil.rmtree(path)
        os.mkdir(path)

    for size in sizes:

        # Determine location of P2L outputs
        parent_dir = os.getcwd()
        directory = 'arrest_db_document'
        subdirectory = str(size)
        individual_path = os.path.join(parent_dir, directory, subdirectory)

        # Create a directory to hold the files
        try:
            os.mkdir(individual_path)
        except FileExistsError:
            shutil.rmtree(individual_path)
            os.mkdir(individual_path)

        for df, df_name in zip(dataframes, dataframe_names):

            temp_df = df[0:size]

            if df_name == "arrest_info":
                temp_df["ARREST_DATE"] = temp_df["ARREST_DATE"].dt.strftime('%Y-%m-%d')
                temp_df.to_json(individual_path + os.sep + f"{df_name}.json", orient="records")
            else:
                temp_df.to_json(individual_path + os.sep + f"{df_name}.json", orient="records")
