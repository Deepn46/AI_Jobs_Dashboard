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
page=st.sidebar.radio('Choose your page',['Analysis on count','Salary Analysis','Analysis on location'])
if page=='Analysis on count':
    #Creating three columns in a row
    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader('Total Employees')
        st.title(df.shape[0])
    with col2:
        st.subheader('AI Job Catagories')
        st.title(df['job_title'].nunique())
    with col3:
        st.subheader('Employment Type count')
        st.title(df["employment_type"].nunique())
    # TO display horizontal line 
    st.markdown('''---''')
    col1,col2=st.columns(2)
    with col1:
        #Employee Count on each year
        df1=df.groupby("work_year").count().reset_index()[["work_year","employment_type"]]
        df1.rename(columns={"employment_type":"Employees_count"},inplace=True)
        colors=['royalblue','cyan','lightcyan']
        fig1 = px.pie(df1, values='Employees_count', names='work_year',color_discrete_sequence=colors)
        fig1.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.subheader("Employee Count on each year")
        st.plotly_chart(fig1)
        # ----
        # Employees count by employment type
        df5=df.groupby(by="employment_type").count().reset_index()
        df5=df5.rename(columns={'work_year':'Employee Count'})
        df5=df5.rename(columns={'employment_type':'Employment Type'})
        fig=px.bar(df5,x=df5['Employee Count'],y=df5['Employment Type'],color_discrete_sequence=['#50EBEC'],orientation="h")
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.subheader("Employees count by employment type")
        st.plotly_chart(fig)



    with col2:
    # Count of employees on each year based on compay size
        df2=df.groupby(['work_year','company_size']).count().reset_index()
        df2['work_year']=df2['work_year'].astype(str)
        df2=df2.rename(columns={'experience_level':'count'})
        fig=px.bar(df2,x='work_year',y='count',color='company_size',color_discrete_sequence=colors)
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.subheader('Count of employees on each year based on compay size')
        st.plotly_chart(fig)
        # Employees Count based on company size
        df1=df.groupby('company_size').count().reset_index()
        df1=df1.rename(columns={'work_year':'Employee_count'})
        fig2=px.pie(df1,names='company_size',values='Employee_count',hole=0.5,color_discrete_sequence=colors)
        fig2.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.subheader('Employees Count based on company size')
        st.plotly_chart(fig2)
if page=='Salary Analysis':
    col1,col2,col3=st.columns(3)
    with col1:
        st.subheader("Select the Location")
        a=list(df.sort_values('company_location')['company_location'].unique())
        a.insert(0,'Select All')
        country=st.multiselect("",a,["Select All"])
        if len(country)>=1 and country[0]=="Select All":
            country=list(df['company_location'].unique())

    with col2:
        st.subheader("Select the Job title")
        b=list(df.sort_values('job_title')['job_title'].unique())
        b.insert(0,'Select All')
        job=st.multiselect("",b,["Select All"]) 
        if len(job)>=1 and job[0]=="Select All":
            job=list(df['job_title'].unique())  
      
    with col3:
        st.subheader("Select the Work Year")
        c=list(df.sort_values('work_year')['work_year'].unique())
        c.insert(0,'Select All')
        year=st.multiselect("",c,["Select All"]) 
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
        fig=px.line(x=df2['company_location'],y=df2['Salary Average'],color_discrete_sequence=colors,labels=dict(x="Country", y="Salary"),color=px.Constant("Average Salary"))#,name='Average Salary')
        fig.add_bar(x=df1['company_location'],y=df1['Maximum Salary'],name='Maximum Salary',marker=dict(color='#43BFC7'))
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.subheader('Top 5 countries by maximum salary')
        st.plotly_chart(fig)
        # Average Salary on each year
        df4=df.groupby(by='work_year').mean().reset_index()
        df4=df4.rename(columns={'salary_in_usd':'Average Salary'})
        df4['Average Salary']=df4['Average Salary'].astype(int)
        df4['work_year']=df4['work_year'].astype(str)
        fig=px.bar(df4,y=df4['work_year'],x=df4['Average Salary'],color_discrete_sequence=['#77BFC7'],orientation="h")
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.subheader("Average Salary by year")
        st.plotly_chart(fig)
    with col2:
        # Company size salary contribution
        df3=df.groupby(by='company_size').sum()
        df3=df3.rename(columns={'salary_in_usd':'Total Salary'})
        df3=df3.reset_index()
        fig=px.pie(df3,names='company_size',values='Total Salary',color_discrete_sequence=colors,hole=0.5)
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
        st.subheader('Total salary contribution by company size')
        st.plotly_chart(fig)
        # Top 10 AI jobs based on salary
        df2=df[['job_title','employee_residence','salary_in_usd']].groupby('job_title').mean().sort_values(by='salary_in_usd',ascending=False)
        df2['Job Title']=df2.index
        df3=df2.head(10)
        fig=px.bar(df3,x='Job Title',y='salary_in_usd',color='salary_in_usd')
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.subheader('Top 10 AI jobs by average salary')
        st.plotly_chart(fig)
if page=='Analysis on location':
    # Top 5 countries on AI job count
    col1,col2,col3=st.columns(3)
    with col1:
        s=st.selectbox("Select ",["Top 5 Countries","Bottom 5 Countries"])
        if s=="Top 5 Countries":
            df1=pd.DataFrame(df['company_location'].value_counts().head())
        else:
            df1=pd.DataFrame(df['company_location'].value_counts().tail())
        df1=df1.reset_index()
        df1=df1.rename(columns={"index":"Location"})
        df1=df1.rename(columns={"company_location":"Count"})
        l=list(df1["Location"])
        df2=df.groupby(by="company_location").sum().reset_index()
        df3=df2[df2["company_location"].isin(l)]
    col1,col2,col3=st.columns(3)
    with col1:
        fig=px.bar(df1,x="Location",y="Count",color_discrete_sequence=['#77BFC7'])
        st.subheader(str(s)+" Employee Count")
        fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False),paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig)
    with col2:
        pass
    with col3:
        st.header(" ")
        st.header(" ")
        st.header(" ")
        st.markdown("<h2>Total Salary</h2>",unsafe_allow_html=True)
        st.subheader(str(df3["salary_in_usd"].sum())+" USD")
        st.markdown("<h2>Average Salary</h2>",unsafe_allow_html=True)
        st.subheader(str(df3["salary_in_usd"].mean())+" USD")  
    # Analysis based on company size      
    
    st.header("Analysis on Company Size")
    st.header(" ")
    col1,col2,col3=st.columns(3)
    with col1:
        l=list(df['company_size'].unique())
        s=st.selectbox("Select the company size ",l)
        st.markdown("<h2>Total Salary</h2>",unsafe_allow_html=True)
        df5=df.groupby(by="company_size").sum().reset_index()
        df5=df5[df5["company_size"]==s]      
        st.subheader(str(int(df5["salary"]))+" USD")
    with col2:
        st.header(" ")
        st.header(" ")
        st.header(" ")
        st.markdown("<h2>Average Salary</h2>",unsafe_allow_html=True)
        df5=df.groupby(by="company_size").mean().reset_index()
        df5=df5[df5["company_size"]==s]      
        st.subheader(str(int(df5["salary"]))+" USD")
    with col3:
        st.header(" ")
        st.header(" ")
        st.header(" ")
        st.markdown("<h2>Employees Count</h2>",unsafe_allow_html=True)
        df5=df.groupby(by="company_size").count().reset_index()
        df5=df5[df5["company_size"]==s]      
        st.subheader(str(int(df5["salary"])))
   