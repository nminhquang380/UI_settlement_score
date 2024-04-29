import streamlit as st
from datetime import date
# from . import credentials
import pandas as pd
from plotly import graph_objs as go
import matplotlib.pyplot as plt
import seaborn as sns

import preprocessing
import eda

def main():
    st.title("Data Analysis Application")
    sns.set_theme()

    
    try:
        uploaded_file = st.file_uploader("Upload CSV File", type="csv")
    except:
        st.warning("Unable to open the file")
    
    if uploaded_file:
        # Read the dataset 
        data = pd.read_csv(uploaded_file)

        # Preprocess dataset
        preprocessed_data = preprocessing.preprocess_data(data)

        # Display DataFrame
        st.subheader("Preprocessed Data Preview")
        st.dataframe(preprocessed_data)

        # More options to specify the format of the report
        full_report = st.radio("**Would you like to print the full report or specify particular details?**", ["Yes", "No"], captions=["Print the entire report", "Specify particular details"])
        if full_report == "No":
            list_agent = preprocessed_data['Session Delivered By (Outcomes)'].unique()
            agents = st.multiselect(label='Agent', options=list_agent)
            
            start_date = st.date_input('Starting Date')
            end_date = st.date_input('Ending Date')
            
            # Convert start_date and end_date from Streamlit to Pandas datetime
            start_date = pd.to_datetime(start_date)
            end_date = pd.to_datetime(end_date)
            
            specific_analysis = ['Weighted average change of Response',
                                 'Trend of Response Over Time',
                                 'Agent Performance']
            
            analysis_options = st.multiselect(label='Analysis', options=specific_analysis)
        
        if st.button("Analyse Data"):
            # Calculate statistics
            if full_report == "No":
                try:
                    analysed_data = preprocessed_data[preprocessed_data["Session Delivered By (Outcomes)"].isin(agents)]
                    analysed_data = analysed_data[(analysed_data['Session Date (Outcomes)'] >= start_date) & (analysed_data['Session Date (Outcomes)'] <= end_date)]
                except:
                    st.warning("Unable to analyse the data")
            else:
                analysed_data = preprocessed_data
                
            eda.analyse(analysed_data)
            
            if full_report == "No":
                if 'Weighted average change of Response' in analysis_options:
                    eda.weighted_average_change(analysed_data)
                
                if 'Trend of Response Over Time' in analysis_options:
                    eda.scoring_overtime(analysed_data)
                    
                if 'Agent Performance' in analysis_options:
                    eda.agent_performance(analysed_data)
            else:
                eda.weighted_average_change(analysed_data)
                eda.scoring_overtime(analysed_data)
                eda.agent_performance(analysed_data)

                

if __name__ == "__main__":
    main()
