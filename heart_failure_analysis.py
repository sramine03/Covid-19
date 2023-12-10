import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

heart_data=pd.read_csv("https://raw.githubusercontent.com/sramine03/Covid-19/main/heart.csv")
heart_data.head()
heart_data.info()
heart_data.describe()

sex = heart_data['Sex'].unique().tolist()
age = heart_data['Age'].unique().tolist()

# Sidebar widgets
st.sidebar.write("**Filter by Age:**")
selected_age = st.sidebar.slider('Select Age:', min_value=min(age), max_value=max(age), value=(min(age), max(age)))

# Filter the dataset based on user input
age_filter = heart_data[(heart_data['Age'].between(selected_age[0], selected_age[1]))]
has_disease = heart_data[(heart_data['Age'].between(selected_age[0], selected_age[1])) & (heart_data['HeartDisease'] == 1)]
sex_counts = has_disease['Sex'].value_counts()


# Table
st.write("**Table**")
st.write(age_filter)

# Pie chart
st.write("**Distribution of Heart Disease by Sex**")
pie_chart = px.pie(
    has_disease,
    names=sex_counts.index,
    values=sex_counts.values,
    labels={'0': 'Female', '1': 'Male'},
    color_discrete_sequence=['#7D0909', '#F6CBD0'] #maroon palette
)
pie_chart.update_traces(textposition='inside', textinfo='percent+value')
st.plotly_chart(pie_chart)

#Histogram
st.write("**Age Distribution with the Occurrence of Heart Disease**")
hist=px.histogram(
    heart_data,
    x="Age",
    y="HeartDisease",
    color_discrete_sequence=px.colors.sequential.RdBu
    )
st.plotly_chart(hist)
