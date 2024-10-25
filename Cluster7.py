# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:51:45 2024

@author: lenovo
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 15:04:32 2023

@author: lenovo
"""

import base64
import streamlit as st
import pandas as pd
from sklearn.cluster import DBSCAN

# Title
st.title("Distance Based Clustering App")

# User Guide
st.write(
    """
    ## User Guide

    This app clusters latitude and longitude points from an Excel sheet based on user-defined distance, 
    assigns cluster labels, and provides the output as a downloadable CSV file.

    ### Instructions:
    
    1. Upload an Excel sheet with the following details:
       - Column A: Issue Number
       - Column B: Latitude
       - Column C: Longitude
    2. Use the slider to select a distance for clustering.
    3. The app will display the clusters in a table and provide a download link for the clustered data.
    4. Click on the Column Labels in the table to sort the entries.
    5. All the Issue Numbers having the same Cluster Label are within the selected distance.
    6. Cluster Labels having only one Issue Number are individual complaints not within the proximity of the selected distance.
    """
)

# File upload
uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])

if uploaded_file is not None:
    # Read data from Excel
    data = pd.read_excel(uploaded_file)

    # Distance filter
    min_distance = 35
    max_distance = 100
    step = 5

    selected_distance = st.slider("Select Distance (in meters)", min_distance, max_distance, step)

    # Clustering
    coords = data[['Latitude', 'Longitude']].to_numpy()
    kms_per_radian = 6371.0
    epsilon = selected_distance / 1000 / kms_per_radian  # Convert to radians

    # Apply DBSCAN clustering
    db = DBSCAN(eps=epsilon, min_samples=1, algorithm='ball_tree', metric='haversine').fit(
        (coords * (3.141592653589793 / 180))
    )
    cluster_labels = db.labels_

    # Assign cluster labels
    data['Cluster Label'] = cluster_labels

    # Display clusters in a table
    st.subheader("Clusters Table")
    st.write(data)

    # Provide download link for CSV file
    st.subheader("Download Clusters as CSV")
    csv = data.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # B64 encoding for download link
    href = f'<a href="data:file/csv;base64,{b64}" download="clustered_complaints.csv">Download CSV File</a>'
    st.markdown(href, unsafe_allow_html=True)
