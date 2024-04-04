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

    uploaded_file = st.file_uploader("Upload CSV File", type="csv")

    if uploaded_file is not None:
        # Read the dataset 
        data = pd.read_csv(uploaded_file)

        # Preprocess dataset
        preprocessed_data = preprocessing.preprocess_data(data)

        # Display DataFrame
        st.subheader("Preprocessed Data Preview")
        st.dataframe(preprocessed_data)

        if st.button("Analyse Data"):

            # Calculate statistics
            eda.analyse(preprocessed_data)
    else:
        st.warning("Unable to open the file")

if __name__ == "__main__":
    main()
