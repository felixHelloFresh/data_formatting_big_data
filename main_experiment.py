import os
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import importlib
# import sys
# from weak_scaling_postgres_vs_mongo_main import _experiment
# # importlib.reload(sys.modules['_experiment'])
from _experiment import Experiment


def run_experiment():

    # USER INPUT: set personal configurations here

    # Configurations for postgres server: change values only, do not change keys
    postgres_settings = {
        "user": "felixmooij",
        "password": "",
        "host": "localhost",
        "port": "5432",
        "database": "mydb"
    }
    # Configurations for MongoDB: change values only, do not change keys
    mongodb_settings = {
        "host": "mongodb://localhost:27017/",
        "database": "bigdata"
    }

    # Your name for experiment logging
    person = 'felix'




    exp1 = Experiment()
    exp1.connect(postgres_settings, mongodb_settings)
    exp1.prepare_databases(os.getcwd())
    exp1.execute('felix')
    df = exp1.get_results()
    exp1.export_results()


if __name__ == "__main__":
    run_experiment()