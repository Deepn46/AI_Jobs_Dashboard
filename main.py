# Importing required modules
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#Importing data 
url='https://raw.githubusercontent.com/plotly/datasets/master/salaries-ai-jobs-net.csv'
df=pd.read_csv(url)

#Dashboard creation
st.set_page_config(layout='wide')
#Measures creation
page=st.sidebar.radio('Choose your page',['Intro page','Salary Analysis'])
if page=='Intro page':
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
        st.title(str(int(df['salary_in_usd'].mean()))+" "+"USD")
    # TO display horizontal line 
    st.markdown('''---''')
    col1,col2=st.columns(2)
    with col1:
        #Employee Count on each year
        df1=df.groupby("work_year").count().reset_index()[["work_year","employment_type"]]
        df1.rename(columns={"employment_type":"Employees_count"},inplace=True)
        colors=['royalblue','cyan','lightcyan']
        fig1 = px.pie(df1, values='Employees_count', names='work_year',color_discrete_sequence=colors,title='Employee Count on each year')
        fig1.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig1)
        # ----
        # Employees count by employment type
        df5=df.groupby(by="employment_type").count().reset_index()
        df5=df5.rename(columns={'work_year':'Employee Count'})
        df5=df5.rename(columns={'employment_type':'Employment Type'})
        fig=px.bar(df5,x=df5['Employee Count'],y=df5['Employment Type'],color_discrete_sequence=['#50EBEC'],orientation="h",title="Employees count by employment type")
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig)



    with col2:
    # Count of employees on each year based on compay size
        df2=df.groupby(['work_year','company_size']).count().reset_index()
        df2['work_year']=df2['work_year'].astype(str)
        df2=df2.rename(columns={'experience_level':'count'})
        fig=px.bar(df2,x='work_year',y='count',color='company_size',color_discrete_sequence=colors,title='Count of employees on each year based on compay size')
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig)
        # Employees Count based on company size
        df1=df.groupby('company_size').count().reset_index()
        df1=df1.rename(columns={'work_year':'Employee_count'})
        fig2=px.pie(df1,names='company_size',values='Employee_count',hole=0.5,color_discrete_sequence=colors,title='Employees Count based on company size')
        fig2.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig2)
if page=='Salary Analysis':
    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader("Select the Location")
        a=list(df.sort_values('company_location')['company_location'].unique())
        a.insert(0,'Select All')
        country=st.multiselect("",a)
        if len(country)>=1 and country[0]=="Select All":
            country=list(df['company_location'].unique())

    with col2:
        st.subheader("Select the Job title")
        b=list(df.sort_values('job_title')['job_title'].unique())
        b.insert(0,'Select All')
        job=st.multiselect("",b) 
        if len(job)>=1 and job[0]=="Select All":
            job=list(df['job_title'].unique())  
      
    with col3:
        st.subheader("Select the Work Year")
        c=list(df.sort_values('work_year')['work_year'].unique())
        c.insert(0,'Select All')
        year=st.multiselect("",c) 
        if len(year)>=1 and year[0]=="Select All":
            year=list(df['work_year'].unique())   
    col1,col2,col3=st.columns(3)  
    newdf=df[(df['job_title'].isin(job)) & (df['work_year'].isin(year)) & (df['company_location'].isin(country)) ].reset_index()
    with col1:
        #Sum
        st.header("Total Salary")
        try:
            st.subheader(str(int(newdf['salary_in_usd'].sum()))+" "+"USD")
        except:
            st.subheader(0)
    with col2:
        st.header("Average Salary")
        try:
            st.subheader(str(int(newdf['salary_in_usd'].mean()))+" "+"USD")  
        except:
            st.subheader(0)
    with col3:
        st.header("Maximum Salary")
        try:
            st.subheader(str(int(newdf['salary_in_usd'].max()))+" "+"USD")
        except:
            st.subheader(0)
    st.markdown("----")
    col1,col2=st.columns(2)
    with col1  :
        # Top 5 countries based on maximum salary
        df1=df.groupby('company_location').max().sort_values(by='salary_in_usd',ascending=False).head()
        df1=df1.sort_values(by='company_location').reset_index()
        df1=df1.rename(columns={'salary_in_usd':'Maximum Salary'})
        country=list(df1['company_location'])
        df2=df.groupby('company_location').mean().reset_index()
        df2=df2[df2['company_location'].isin(country)].sort_values(by='company_location').reset_index()
        df2=df2.rename(columns={'salary_in_usd':'Salary Average'})
        colors=['#151B54',"LightSeaGreen",'lightcyan','royalblue','cyan']
        fig=px.line(x=df2['company_location'],y=df2['Salary Average'],color_discrete_sequence=colors,labels=dict(x="Country", y="Salary"),color=px.Constant("Average Salary"),title='Top 5 countries by maximum salary')#,name='Average Salary')
        fig.add_bar(x=df1['company_location'],y=df1['Maximum Salary'],name='Maximum Salary',marker=dict(color='#43BFC7'))
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig)
        # Average Salary on each year
        df4=df.groupby(by='work_year').mean().reset_index()
        df4=df4.rename(columns={'salary_in_usd':'Average Salary'})
        df4['Average Salary']=df4['Average Salary'].astype(int)
        df4['work_year']=df4['work_year'].astype(str)
        fig=px.bar(df4,y=df4['work_year'],x=df4['Average Salary'],color_discrete_sequence=['#77BFC7'],orientation="h",title="Average Salary by year")
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig)
    with col2:
        # Company size salary contribution
        df3=df.groupby(by='company_size').sum()
        df3=df3.rename(columns={'salary_in_usd':'Total Salary'})
        df3=df3.reset_index()
        fig=px.pie(df3,names='company_size',values='Total Salary',color_discrete_sequence=colors,title='Total salary contribution by company size',hole=0.5)
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
        st.plotly_chart(fig)
        # Top 10 AI jobs based on salary
        df2=df[['job_title','employee_residence','salary_in_usd']].groupby('job_title').mean().sort_values(by='salary_in_usd',ascending=False)
        df2['Job Title']=df2.index
        df3=df2.head(10)
        fig=px.bar(df3,x='Job Title',y='salary_in_usd',title='Top 10 AI jobs by average salary',color='salary_in_usd')
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig)
 
