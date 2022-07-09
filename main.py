# Importing required modules
import streamlit as st
import pandas as pd
import plotly.express as px

#Importing data 
url='https://raw.githubusercontent.com/plotly/datasets/master/salaries-ai-jobs-net.csv'
df=pd.read_csv(url)

#Dashboard creation
page=st.set_page_config(layout="wide")
#Measures creation
st.sidebar.radio('simple',['one','two'])
if page=='one':
    #Creating three columns in a row
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
    # TO display horizontal line 
    st.markdown('''---''')
    col1,col2=st.columns(2)
    with col1:
        #Employee Count on each year
        df1=df.groupby("work_year").count().reset_index()[["work_year","employment_type"]]
        df1.rename(columns={"employment_type":"Employees_count"},inplace=True)
        colors=['royalblue','cyan','lightcyan']
        fig1 = px.pie(df1, values='Employees_count', names='work_year',color_discrete_sequence=colors,title='Employee Count on each year')
        st.plotly_chart(fig1)
        # ----
        # Top 10 AI jobs based on salary
        df2=df[['job_title','employee_residence','salary_in_usd']].groupby('job_title').mean().sort_values(by='salary_in_usd',ascending=False)
        df2['Job Title']=df2.index
        df3=df2.head(10)
        fig=px.bar(df3,x='Job Title',y='salary_in_usd',title='Top 10 AI jobs based on average salary',color='salary_in_usd')
        st.plotly_chart(fig)


    with col2:
        # Count of employees on each year based on compay size
        df2=df.groupby(['work_year','company_size']).count().reset_index()
        df2['work_year']=df2['work_year'].astype(str)
        df2=df2.rename(columns={'experience_level':'count'})
        fig=px.bar(df2,x='work_year',y='count',color='company_size',color_discrete_sequence=colors,title='Count of employees on each year based on compay size')
        st.plotly_chart(fig)
        # Employees Count based on company size
        df1=df.groupby('company_size').count().reset_index()
        df1=df1.rename(columns={'work_year':'Employee_count'})
        fig2=px.pie(df1,names='company_size',values='Employee_count',hole=0.5,color_discrete_sequence=colors,title='Employees Count based on company size')
        st.plotly_chart(fig2)
if page=='two':
    pass

