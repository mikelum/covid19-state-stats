## covid19-state-stats

Simple Python scripts to obtain and plot/list state level Covid19 statistics from the CDC database

### Usage:
1. Load the stats into a (Pandas) dataframe:
    - `df = load_cdc_df()`
2. View Data:
    - state_df = comp_7day_cases(df, state='HI')
        - Adds a 7-day running average column to the passed df for the indicated state
    - plot_case_rate(dframe, state='HI')
        - Uses Pandas internal plotting (matplotlib.pyplot) to plot the running 7-day case rate for a given state
    - rate_list = case_rate_list(dframe, state_list=None, alpha=True)
        - Create a list with entries: [[state, <current new case rate>], ...]
