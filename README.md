# Weak Scaling Experiment: PostgreSQL vs. MongoDB


**Performs all steps required to perform our weak scaling experiment**

The code  contained in this repository perform the following tasks:
- Pre-processing
- The experiment itself
- Plotting of the results (Jupyter Notebook)

## Getting started

Install all required packages using:
```bash
pip install -r requirements.txt
```

Make sure the following files are present in the directory in which `main.py` is located:
- `mflix_comments.json`
- `mflix_movies.json`
- `mflix_sessions.json`
- `mflix_users.json`
- `NYPD_Arrest_Data__Year_to_Date.csv`

To run the data pre-processing script:

```bash
python main.py
```

To run the experiment script:

```bash
python main_experiment.py
```

Subsequently, the `create_plots.ipynb` file can be used to create plots from the results 
output by the `experiment.py` script.