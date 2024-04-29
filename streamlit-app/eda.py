import streamlit as st
from datetime import date
# from . import credentials
import pandas as pd
import numpy as np
from plotly import graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns

def percent_answer_satisfaction(scoring_df):
    try:
        satisfaction_df = scoring_df[scoring_df['Question Type (Outcomes)'] == 'SCORE: Satisfaction']
        satisfaction_df.dropna(inplace=True)

        # Aggregate answers if there are duplicates for the same client and question
        satisfaction_df_grouped = satisfaction_df.groupby(['Client ID (Clients)', 'Question (Outcomes)'])['Response (Outcomes)'].first().unstack()
        
        # Group up 2 questions
        try:
            satisfaction_df_grouped['I am happy/satisfied with the services I have received'] = satisfaction_df_grouped['I am happy with the services I have received'].fillna(satisfaction_df_grouped['I am satisfied with the services I have received'])
            satisfaction_df_grouped.drop(columns=['I am happy with the services I have received', 'I am satisfied with the services I have received'], inplace=True)
        except:
            pass
        # Check if each client has answered all questions
        answered_all = satisfaction_df_grouped.notna().all(axis=1).sum()
        number_client = scoring_df['Client ID (Clients)'].nunique()

        st.header('SCORE Statisfaction Questions')
        st.write(f'Number of Client who answered all questions: {answered_all}')
        st.write(f'The percentage of clients who had all three questions under SCORE: Satisfaction answered at least once in the reporting period: {answered_all/number_client:.2f}')

        st.subheader('Statisfaction Q&A')
        st.dataframe(satisfaction_df_grouped)

        non_missing_counts = satisfaction_df_grouped.count()
        # Create a figure and axis object
        fig, ax = plt.subplots(1,1,figsize=(12, 6))

        # Create a bar chart
        bars = ax.barh(non_missing_counts.index, non_missing_counts.values, color='skyblue')
        ax.set_xlabel('Columns')
        ax.set_ylabel('Number of Non-Missing Values')
        ax.set_title('Number of Non-Missing Values for Each Column')

        # Attach counts on each bar
        for bar, count in zip(bars, non_missing_counts.values):
            ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, str(count), ha='left', va='center')

        st.subheader('Number of Answer for each Question')
        st.pyplot(fig)
        
        return answered_all, answered_all/number_client
    except:
        return None, None

def percent_answer_circumstance(scoring_df):
    try:
        circumstance_df = scoring_df[scoring_df['Question Type (Outcomes)'] == 'SCORE: Circumstances']
        circumstance_df.dropna(inplace=True)

        # Group by 'Client ID' and 'Question' and count occurrences
        circumstance_question_counts = circumstance_df.groupby(['Client ID (Clients)', 'Session ID (Outcomes)', 'Question (Outcomes)']).size()

        # Count the number of clients who answered at least one question twice
        circumstance_answered_twice = circumstance_question_counts[circumstance_question_counts > 1].index.get_level_values(0).nunique()
        number_client = scoring_df['Client ID (Clients)'].nunique()

        st.header('SCORE Circumstance Questions')
        st.write("Number of clients who answered at least one question twice:", circumstance_answered_twice)
        st.write('The percentage of clients who had two responses for at least one question under SCORE: Circumstances in the reporting period: ', circumstance_answered_twice / number_client * 100)

        # Calculate the percentage of clients who had two responses for at least one question
        percentage_clients_twice = (circumstance_answered_twice / number_client) * 100

        # Create a figure and axis object
        fig, ax = plt.subplots()

        # Create a pie chart
        labels = ['Clients with at least one question answered twice', 'Other clients']
        sizes = [percentage_clients_twice, 100 - percentage_clients_twice]
        colors = ['lightblue', 'lightgrey']
        explode = (0.1, 0)  # explode the first slice

        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        ax.set_title('Percentage of Clients with at Least One Question Answered Twice')

        st.subheader('Circumstance Answers Percentage')
        st.pyplot(fig)
        
        return circumstance_answered_twice, circumstance_answered_twice/number_client
    except:
        return None, None

def percent_answer_goal(scoring_df):
    try:
        goal_df = scoring_df[scoring_df['Question Type (Outcomes)'] == 'SCORE: Goals']
        goal_df.dropna(inplace=True)

        # Group by 'Client ID' and 'Question' and count occurrences
        goal_question_counts = goal_df.groupby(['Client ID (Clients)', 'Session ID (Outcomes)', 'Question (Outcomes)']).size()

        # Count the number of clients who answered at least one question twice
        goal_answered_twice = goal_question_counts[goal_question_counts > 1].index.get_level_values(0).nunique()
        number_client = scoring_df['Client ID (Clients)'].nunique()

        st.header('SCORE Goal Questions')
        st.write("Number of clients who answered at least one question twice:", goal_answered_twice)
        st.write('The percentage of clients who had two responses for at least one question under SCORE: Goals in the reporting period: ', goal_answered_twice / number_client * 100)

        # Calculate the percentage of clients who had two responses for at least one question
        percentage_clients_twice = (goal_answered_twice / number_client) * 100

        # Create a figure and axis object
        fig, ax = plt.subplots()

        # Create a pie chart
        labels = ['Clients with at least one question answered twice', 'Other clients']
        sizes = [percentage_clients_twice, 100 - percentage_clients_twice]
        colors = ['lightblue', 'lightgrey']
        explode = (0.1, 0)  # explode the first slice

        ax.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', startangle=140)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        ax.set_title('Percentage of Clients with at Least One Question Answered Twice')

        st.subheader('Goals Answers Percentage')
        st.pyplot(fig)
        
        return goal_answered_twice, goal_answered_twice/number_client
    except:
        return None, None

def weighted_average_change(df):
    try:
        # Assuming df is your DataFrame containing the data
        # Sort the DataFrame by Client ID, session ID, and question
        df.sort_values(by=['Client ID (Clients)', 'Session ID (Outcomes)', 'Question (Outcomes)'], inplace=True)

        # Group by Client ID and question, then aggregate to get the first and last answer
        first_last_answers = df.groupby(['Client ID (Clients)', 'Question Type (Outcomes)', 'Question (Outcomes)']).agg(first_answer=('Response (Outcomes)', 'first'), last_answer=('Response (Outcomes)', 'last')).reset_index()

        # Drop rows where answers are NaN
        first_last_answers.dropna(axis=0, inplace=True)

        first_last_answers['difference'] = first_last_answers['last_answer'] - first_last_answers['first_answer']
        average_change = first_last_answers.groupby(['Question Type (Outcomes)', 'Question (Outcomes)'])['difference'].mean()
        
        st.header('Weighted average change in Circumstances and Goals for each question')

        average_change_df = average_change.reset_index()
        average_change_df = average_change_df[average_change_df['Question Type (Outcomes)'].isin(['SCORE: Goals', 'SCORE: Circumstances'])]
        
        csv_file = convert_df(average_change_df)
        st.dataframe(average_change_df)
        st.download_button(
            label="Download CSV",
            data=csv_file,
            file_name="average_change.csv",
            mime="text/csv"
        )

        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(12, 10))

        # Use Seaborn to create the bar plot
        sns.barplot(data=average_change_df, x="difference", y="Question (Outcomes)", hue="Question Type (Outcomes)", ax=ax)

        # Set labels and title
        ax.set_xlabel('Average Change')
        ax.set_ylabel('Question')
        ax.set_title('Average Change in Responses for Each Question')

        # Add legend
        ax.legend()

        st.subheader('Average Change in Responses')
        st.pyplot(fig)
    except:
        pass

def scoring_overtime(scoring_df):
    try:
        # Set the window size for smoothing
        window_size = 50

        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(12, 8))

        # Iterate over each category in 'Question Type (Outcomes)'
        for category, data in scoring_df.groupby('Question Type (Outcomes)'):
            # Smooth the 'Response (Outcomes)' column using a rolling window for each category
            data['Smoothed Response'] = data['Response (Outcomes)'].rolling(window=window_size, min_periods=window_size//2).mean()
            
            # Plot the smoothed line for each category
            sns.lineplot(data=data, x='Session Date (Outcomes)', y='Smoothed Response', ax=ax, label=category)

        # Set labels and title
        ax.set_xlabel('Date')
        ax.set_ylabel('Response')
        ax.set_title('Trend of Response Over Time')

        # Add legend
        ax.legend()

        st.header('Trend of Average Response Over Time')
        st.pyplot(fig)
    except:
        pass

    
def agent_performance(scoring_df):
    try:
        # Group the DataFrame by 'Session Delivered By' and calculate the number of responses and mean response
        agent_stats = scoring_df.groupby('Session Delivered By (Outcomes)').agg(
            num_responses=('Response (Outcomes)', 'count'),
            avg_response=('Response (Outcomes)', 'mean')
        ).reset_index()

        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(12, 8))

        # Create a scatter plot
        scatter = ax.scatter(agent_stats['num_responses'], agent_stats['avg_response'])

        # Add labels for each agent
        for i, row in agent_stats.iterrows():
            ax.annotate(row['Session Delivered By (Outcomes)'], (row['num_responses'], row['avg_response']))

        # Set labels and title
        ax.set_xlabel('Number of Responses')
        ax.set_ylabel('Average Response')
        ax.set_title('Agent Performance')

        st.header('Agent Performance')
        st.pyplot(fig)
    except:
        pass
    
def response_distribution(df):
    try:
        # Assuming df is your DataFrame containing the data
        # Sort the DataFrame by Client ID, session ID, and question
        df.sort_values(by=['Client ID (Clients)', 'Session ID (Outcomes)', 'Question (Outcomes)'], inplace=True)

        # Group by Client ID and question, then aggregate to get the first and last answer
        first_last_answers = df.groupby(['Client ID (Clients)', 'Question Type (Outcomes)', 'Question (Outcomes)']).agg(first_answer=('Response (Outcomes)', 'first'), last_answer=('Response (Outcomes)', 'last')).reset_index()

        # Drop rows where answers are NaN
        first_last_answers.dropna(axis=0, inplace=True)
        first_last_answers = first_last_answers[first_last_answers['Question Type (Outcomes)'].isin(['SCORE: Goals', 'SCORE: Circumstances'])]
        
        # Create a figure and axes to plot the distributions
        fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(10, 12))

        # Define the bin edges for the histograms
        bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5]  # Specify bins for integer responses from 1 to 5

        # Group data by question type
        grouped_data = first_last_answers.groupby('Question Type (Outcomes)')

        # Loop through each question type group
        for (question_type, data), ax in zip(grouped_data, axes):
            # Plot histogram of first_answer distribution
            sns.histplot(data['first_answer'], bins=bins, kde=False, ax=ax, label='First Answer', color='blue', alpha=0.6)
            
            # Plot histogram of last_answer distribution
            sns.histplot(data['last_answer'], bins=bins, kde=False, ax=ax, label='Last Answer', color='red', alpha=0.6)
            
            # Set title for each plot
            ax.set_title(f'Distribution of First and Last Answers for {question_type}')
            
            # Add legend to the plot
            ax.legend()
            
            # Set x-ticks from 1 to 5
            ax.set_xticks([1, 2, 3, 4, 5])
    
            # Add labels to the axes
            ax.set_xlabel('Response (1-5)')
            ax.set_ylabel('Count')

        st.header('Distribution of First and Last Answers')
        st.pyplot(fig)
    except:
        pass
        
@st.cache_data
def convert_df(df):
    return df.to_csv().encode('utf-8')

def analyse(scoring_df):
    satisfaction_num, satisfaction_percent = percent_answer_satisfaction(scoring_df)
    circum_num, circum_percent = percent_answer_circumstance(scoring_df)
    goal_num, goal_percent = percent_answer_goal(scoring_df)
    # Show table of result
    result_dict = {'Clients': ['clients who had all three questions under SCORE: Satisfaction', 'clients who had two responses for at least one question under SCORE: Circumstances', 'clients who had two responses for at least one question under SCORE: Goals '],
        'Number': [satisfaction_num, circum_num, goal_num],
        'Percent': [satisfaction_percent, circum_percent, goal_percent]}
    st.header('Result')
    result_df = pd.DataFrame(result_dict)
    
    csv_file = convert_df(result_df)
    
    st.dataframe(result_df)
    
    st.download_button(
        label="Download CSV",
        data=csv_file,
        file_name="result.csv",
        mime="text/csv"
    )


    # weighted_average_change(scoring_df)
    # scoring_overtime(scoring_df)
    # agent_performance(scoring_df)
