# Weak Scaling Experiment: PostgreSQL vs. MongoDB


**Performs all steps required to perform our weak scaling experiment**

The code  contained in this repository perform the following tasks:
- Pre-processing
- The experiment itself
- Plotting of the results (Jupyter Notebook)

## Getting started

##### Required Packages
Install all required packages using:
```bash
pip install -r requirements.txt
```

##### Pre-processing script

In order to run the *pre-processing script*, please make sure the following files are present in the directory in which `main.py` is located:
- `mflix_comments.json`
- `mflix_movies.json`
- `mflix_sessions.json`
- `mflix_users.json`
- `NYPD_Arrest_Data__Year_to_Date.csv`

To run the data pre-processing script:

```bash
python main.py
```

##### Experiment script

In order to run the *experiment script*, please make sure to have ran the *pre-processing script* first.

Subsequently, ensure both PostgreSQL and MongoDB have been installed locally, and are running. 

Additionally, please make sure to update the parameters located in `main_experiment.py` to the settings
applicable to your local instances of PostgreSQL and MongoDB.

To run the experiment script:

```bash
python main_experiment.py
```

##### Visualisation Notebook

Subsequently, the `create_plots.ipynb` file can be used to create plots from the results 
output by the `experiment.py` script. 

Make sure Jupyter Notebook is installed, and the results CSV output by the *experiment script* is in the same
directory as the Notebook.