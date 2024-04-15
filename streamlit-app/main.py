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

        list_agent = preprocessed_data['Session Delivered By (Outcomes)'].unique()
        agent = st.selectbox(label='Agent', options=list_agent)
        
        start_date = st.date_input('Starting Date')
        end_date = st.date_input('Ending Date')
        
        if st.button("Analyse Data"):
            # Calculate statistics
            try:
                analysed_date = preprocessed_data[preprocessed_data["Session Delivered By (Outcomes)"] == agent]
                analysed_date = analysed_date[(analysed_date['Session Date (Outcomes)'] >= start_date) & (analysed_date['Session Date (Outcomes)'] <= end_date)]
            except:
                pass
            eda.analyse(preprocessed_data)

if __name__ == "__main__":
    main()
