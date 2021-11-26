#!/usr/bin/env python
""" File: load_cdc_df.py

 Author: Mike Lum (From socrata code sample at:
         https://dev.socrata.com/foundry/data.cdc.gov/9mfq-cb36

 Copyright (c) 2021 by the author and Socrata
 All rights reserved.
 No part of this software may be reproduced or transmitted
 in any manner without the prior permission of the right holders

 Implementation of the SNR_Data object

 Requires:
    Pandas
    Socrata

Revision History:
2021-05-21 (MLum) : Functionalized Socrata's code
"""

# make sure to install these packages before running:
# pip install pandas
# pip install sodapy

import numpy as np
import pandas as pd
from sodapy import Socrata

from state_pops import STATE_POPS

def load_cdc_df():
    """
    load_cdc_df

    Downloads the "United States COVID-19 Cases and Deaths by State over Time"
    database from the CDC at:
    http://https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36

    Args:
        (none)
    Returns:
        results_df (Pandas dataframe) : The requested database
    Raises:
        (none)
    """
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    client = Socrata("data.cdc.gov", None)

    # Example authenticated client (needed for non-public datasets):
    # client = Socrata(data.cdc.gov,
    #                  MyAppToken,
    #                  userame="user@example.com",
    #                  password="AFakePassword")

    # Limited results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy. Note, as of 5-21-2021, the full DB is ~29,000 lines
    results = client.get("9mfq-cb36", limit=100000)

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)

    return results_df


def comp_7day_cases(dframe, state='HI'):
    """
    comp_7day_cases

    Return a dataframe containing the passed state's running 7-day average of
    new cases

    Args:
        df (dataframe) : Dataframe with the full data set
        state (string) : field value of 'state' to sort on

    Returns:
        new_df (dataframe) : Contains the same columns as the passed df, plus
                    the 7-day average

    Raises:
        (none)
    """
    new_df = dframe[dframe['state'] == state]
    new_df = new_df.sort_values(by=['submission_date'])
    new_df['new_7day_rate'] = [sum(new_df['new_case'][i-7:i].astype(float))/7.\
                               if i > 6 else 0 for i in range(len(new_df))]
    return new_df


def plot_case_rate(dframe, state='HI'):
    """
    plot_case_rate

    Plots the population normalized case rate (per 100K) for the passed state

    Args:
        (none)
    Returns:
        results_df (Pandas dataframe) : The requested database
    Raises:
        (none)
    """
    statedf = comp_7day_cases(dframe, state=state)
    statedf.plot(x='submission_date', y='new_7day_rate', title=state)


def case_rate_list(dframe, state_list=None, alpha=True):
    """
    case_rate_lists

    Create a list with entries: [[state, <current new case rate>], ...]

    Returns:
        rate_list (list) : The (state, rate) list

    Raises:
        (none)
    """

    rate_list = []
    if not state_list:
        state_list = list(set(dframe['state']))

    for state in state_list:
        state_df = dframe[dframe['state'] == state]
        state_df = state_df.sort_values(by=['submission_date'])
        day_rate =  sum(state_df['new_case'][-7:].astype(float))/7.
        day_rate = day_rate / STATE_POPS[state] * 1e6 # Cases per million
        rate_list.append([state, day_rate])

    if alpha:
        rate_list = sorted(rate_list, key=lambda i: i[0])

    return rate_list
