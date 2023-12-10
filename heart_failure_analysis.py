import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(page_title = "Heart Failure Analysis",layout = 'wide')

heart_data=pd.read_csv("https://raw.githubusercontent.com/sramine03/Covid-19/main/heart.csv")
heart_data.head()
heart_data.info()
heart_data.describe()

sex = heart_data['Sex'].unique().tolist()
age = heart_data['Age'].unique().tolist()
hr = heart_data['MaxHR'].unique().tolist()
chest_pain_type = heart_data['ChestPainType'].unique().tolist()
resting_ecg = heart_data['RestingECG'].unique().tolist()
cholesterol = heart_data['Cholesterol'].unique().tolist()

# Sidebar filters
st.sidebar.write("**Filter by Age:**")
selected_age = st.sidebar.slider('Select Age:', min_value=min(age), max_value=max(age), value=(min(age), max(age)))

st.sidebar.write("**Filter by Sex:**")
selected_sex = st.sidebar.multiselect('Select Sex:', sex, sex)

st.sidebar.write("**Filter by Chest Pain Type:**")
selected_chest_pain_type = st.sidebar.multiselect('Select Chest Pain Type:', chest_pain_type, chest_pain_type)

st.sidebar.write("**Filter by Resting ECG:**")
selected_resting_ecg = st.sidebar.multiselect('Select Resting ECG:', resting_ecg, resting_ecg)

# Filter the dataset based on user input
filtered_data = heart_data[
    (heart_data['Age'].between(selected_age[0], selected_age[1])) &
    (heart_data['Sex'].isin(selected_sex)) &
    (heart_data['ChestPainType'].isin(selected_chest_pain_type)) &
    (heart_data['RestingECG'].isin(selected_resting_ecg)) &
    (heart_data['HeartDisease'] == 1)
]

filtered_data_maxHR = heart_data[
    (heart_data['Age'].between(selected_age[0], selected_age[1])) &
    (heart_data['Sex'].isin(selected_sex)) &
    (heart_data['ChestPainType'].isin(selected_chest_pain_type)) &
    (heart_data['RestingECG'].isin(selected_resting_ecg)) &
    (heart_data['HeartDisease'] == 1) &
    (heart_data['MaxHR'] != 0)
]

filtered_data_cholesterol = heart_data[
    (heart_data['Age'].between(selected_age[0], selected_age[1])) &
    (heart_data['Sex'].isin(selected_sex)) &
    (heart_data['ChestPainType'].isin(selected_chest_pain_type)) &
    (heart_data['RestingECG'].isin(selected_resting_ecg)) &
    (heart_data['Cholesterol'] != 0)
]

filtered_data_resting = heart_data[
    (heart_data['Age'].between(selected_age[0], selected_age[1])) &
    (heart_data['Sex'].isin(selected_sex)) &
    (heart_data['ChestPainType'].isin(selected_chest_pain_type)) &
    (heart_data['RestingECG'].isin(selected_resting_ecg)) &
    (heart_data['RestingBP'] != 0)
]

sex_counts = filtered_data['Sex'].value_counts()

# Pie chart
col1, col2 = st.columns([2,2])
with col1:
    st.write("**Distribution of Heart Disease by Sex**")
    pie_chart = px.pie(
        filtered_data,
        names=sex_counts.index,
        values=sex_counts.values,
        labels={'0': 'Female', '1': 'Male'},
        color_discrete_sequence=['#7D0909', '#F6CBD0'], #maroon palette
        height = 350,
        width = 350
    )
    pie_chart.update_traces(textposition='inside', textinfo='percent+value')
    st.plotly_chart(pie_chart)

#Histogram
with col2:
    st.write("**Age Distribution with the Occurrence of Heart Disease**")
    hist=px.histogram(
        filtered_data,
        x="Age",
        y="HeartDisease",
        labels={'Age': 'Age', 'HeartDisease': 'Heart Disease Count'},
        color_discrete_sequence=px.colors.sequential.RdBu,
        height = 350,
        width = 650
    )
    st.plotly_chart(hist)

#Scatterplot
col1, col2, col3 = st.columns([6,6,7])
with col1:
    st.write("**Age vs. Resting Blood Pressure**")
    scatter_plot = px.scatter(
        filtered_data_resting,
        x="Age",
        y="RestingBP",
        labels={'Age': 'Age', 'RestingBP': 'Resting Blood Pressure'},
        color='Age',  # Use 'Age' as the color parameter to change color based on age
        color_continuous_scale='RdBu_r',  # Use a continuous color scale
        height = 300,
        width = 400
    )
    st.plotly_chart(scatter_plot)

with col2:
    st.write("**Age vs. Maximum Heart Rate**")
    scatter_plot = px.scatter(
        filtered_data_maxHR,
        x="Age",
        y="MaxHR",
        labels={'Age': 'Age', 'MaxHR': 'Max. Heart Rate'},
        color='Age',  # Use 'Age' as the color parameter to change color based on age
        color_continuous_scale='RdBu_r',  # Use a continuous color scale
        height = 300,
        width = 400
    )
    st.plotly_chart(scatter_plot)

with col3:
    st.write("**Age vs. Cholestrol**")
    scatter_plot = px.scatter(
        filtered_data_cholesterol,
        x="Age",
        y="Cholesterol",
        color='Age',  # Use 'Age' as the color parameter to change color based on age
        color_continuous_scale='RdBu_r',  # Use a continuous color scale
        height = 300,
        width = 400
    )
    st.plotly_chart(scatter_plot)

#Boxplots
col1, col2, col3 = st.columns([6,6,7])
with col1:
    st.write("**Cholesterol Levels vs. Chest Pain Type**")
    box_plot = px.box(
        filtered_data_cholesterol,
        x="ChestPainType",
        y="Cholesterol",
        labels={'ChestPainType': 'Chest Pain Type', 'Cholesterol': 'Cholesterol'},
        color_discrete_sequence=['#7D0909'],
        height = 300,
        width = 400
    )
    st.plotly_chart(box_plot)

with col2:
    st.write("**Heart Disease vs. Chest Pain Type**")
    bar = px.bar(
        filtered_data,
        x="ChestPainType",
        y="HeartDisease",
        labels={'ChestPainType': 'Chest Pain Type', 'HeartDisease': 'Heart Disease Count'},
        color = 'ChestPainType',
        height = 300,
        width = 400
    )
    st.plotly_chart(bar)

with col3:
    st.write("**Heart Disease vs. Resting ECG**")
    bar = px.bar(
        filtered_data,
        x="RestingECG",
        y="HeartDisease",
        labels={'RestingECG': 'Resting ECG', 'HeartDisease': 'Heart Disease Count'},
        color = 'RestingECG',  # Use a continuous color scale
        height = 300,
        width = 400
    )
    st.plotly_chart(bar)
