
import pandas as pd
import numpy as np
import datetime as dt
from datetime import date
import plotly.express as px 
import streamlit as st

st.set_page_config(page_title = " COVID-19 2022 Only", page_icon = ":bar_chart:" , layout= "wide")


@st.cache
def get_data_from_csv():

    df = pd.read_csv("COVIDdata.csv")
    return df
df = get_data_from_csv()




#df = df[(df['Country'] == 'United States of America') | (df['Country'] == 'Mexico')]

# Data that will not be used is dropped
df = df.drop(columns= ['WHO_region', 'Cumulative_cases', 'Cumulative_deaths' ])

# Mortality Rate Column added
df['Mortality'] =   (df['New_deaths'].sum()  /df['New_cases'].sum()) * 100

# Converting column Date_reported into datetime data type.
df['Date_reported'] = pd.to_datetime(df['Date_reported'])

# Filtering the Data for 2022 Only.
nf = df[df['Date_reported'] >= '01-01-2022']

# Copied Dataframe and added a monhts column
da = nf.copy()
#da['month'] = da['Date_reported'].dt.weekday()
da['month'] = da['Date_reported'].dt.month_name()


# Sidebar

st.sidebar.header("Filter Data Here:")

Country = st.sidebar.multiselect(
                                "Select the Country:",  options = da['Country'].unique(), default = ['United States of America'] 
                                 )

df_selection = da.query( "Country == @Country")

#st.dataframe(df_selection)

# MAINPAGE

st.title(":bar_chart: Covid 2022 Dashboard")
st.markdown("##")


# TOP KPI'S 
total_covid19_cases = int(df_selection['New_cases'].sum())
total_covid19_deaths = int(df_selection['New_deaths'].sum())
#mortality_percentage = (total_covid19_deaths / total_covid19_cases) * 100


left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Cases:")
    st.subheader(f"Covid {total_covid19_cases:,}")
with middle_column:
    st.subheader("Total Deaths")
    st.subheader(f"Death {total_covid19_deaths:,}")


st.markdown("---")

# Total Covid-19 Cases by Month [BarChart]

totalcovid19_cases_by_month = (df_selection.groupby(by='month').sum()[['New_cases']].sort_values(by='New_cases')
 )

fig_month_total = px.bar ( totalcovid19_cases_by_month, x = "New_cases", y= totalcovid19_cases_by_month.index, orientation = "h", 
                          title= "<b>Total Covid Cases By Month</b>", 
                          color_discrete_sequence= ["#0083B8"] * len(totalcovid19_cases_by_month),
                          template = "plotly_white") 


fig_month_total.update_layout( plot_bgcolor = "rgba(0,0,0,0)", xaxis = (dict(showgrid=False))
    
)



# Covid Deaths by month [Barchart]
Deaths_by_month = df_selection.groupby(by='month').sum()[['New_deaths']].sort_values(by='New_deaths')
fig_Monthly_Death = px.bar( Deaths_by_month, x= Deaths_by_month.index, y= "New_deaths",
title = "<b>Deaths By Month</b>", color_discrete_sequence = ["#0083B8"]* len(Deaths_by_month),
template = "plotly_white", 
    
)

fig_Monthly_Death.update_layout(  xaxis = dict(tickmode="linear"), plot_bgcolor="rgba(0,0,0,0)",
                                yaxis= (dict(showgrid=False)),
                                )

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_month_total, use_container_width = True)
right_column.plotly_chart(fig_Monthly_Death, use_container_width = True)


hide_st_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        </style>
        """
    
st.markdown(hide_st_style, unsafe_allow_html = True)