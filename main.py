# Importing required modules
import streamlit as st
import pandas as pd
import plotly.express as px

#Importing data 
url='https://raw.githubusercontent.com/plotly/datasets/master/salaries-ai-jobs-net.csv'
df=pd.read_csv(url)

#Dashboard creation

#Measures creation
col1,col2,col3=st.columns(3)
with col1:
    st.subheader('Total Employees')
    st.title(df.shape[0])
with col2:
    st.subheader('AI Job Catagories')
    st.title(df['job_title'].nunique())
with col3:
    st.subheader('Average Salary')
    st.title(int(df['salary'].mean()),"USD")
st.markdown('''---''')
col1,col2,col3=st.columns(3)
with col1:
    df1=df.groupby("work_year").count().reset_index()[["work_year","employment_type"]]
    df1.rename(columns={"employment_type":"Employees_count"},inplace=True)
    colors=['royalblue','cyan','lightcyan']
    fig = px.pie(df1, values='Employees_count', names='work_year',color_discrete_sequence=colors)
    st.plotly_chart(fig)
