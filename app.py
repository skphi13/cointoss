import pandas as pd
import scipy.stats
import streamlit as st
import time

# Initialize stateful variables
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['no', 'iterations', 'mean'])

st.header('Tossing a Coin')

# Initialize an empty list to store the mean values for plotting
mean_values = [0.5]
chart = st.line_chart(mean_values)

def toss_coin(n):
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    outcome_no = 0
    outcome_1_count = 0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        mean_values.append(mean)
        chart.line_chart(mean_values)  # Update chart with new mean values
        time.sleep(0.05)

    return mean

number_of_trials = st.slider('Number of trials?', 1, 1000, 10)
start_button = st.button('Run')

if start_button:
    st.write(f'Running the experiment of {number_of_trials} trials.')
    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)
    

    new_data = pd.DataFrame(data=[[st.session_state['experiment_no'],
                                  number_of_trials,
                                  mean]],
                            columns=['no', 'iterations', 'mean'])
    st.session_state['df_experiment_results'] = pd.concat([
        st.session_state['df_experiment_results'],
        new_data
    ], axis=0).reset_index(drop=True)

st.write(st.session_state['df_experiment_results'])
