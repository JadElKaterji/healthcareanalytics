import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objects as go


def overview_page():
    st.title("Overview")
    
    # Introduction
    st.markdown("The objective of this project is to explore trends and patterns in mental illness and suicide rates in Sweden, over time.")
    
    # Trends explored
    st.subheader("Trends Explored Include:")
    st.markdown("- **Suicide trends in Sweden** over time, across genders, and compared to countries across the world.")
    st.markdown("- **Mental illness trends in Sweden** over time, across genders, and compared to countries across the world.")
    st.markdown("- A **survey** administered to more than 400 people that explores the **relation between social media and depression.**")
    
    # Data, notes, and limitations
    st.subheader("Data, Notes, and Limitations:")
    st.markdown("The objective of the dashboard is not to set causal relations, as many variables could be the determinants of changes in suicide, mental illness, and depression. Moreover, it aims at showing trends and patterns that warrant the need for further investigation.")
    st.markdown("The data was extracted from:")
    st.markdown("- **WHO:** [Suicide Rates](https://www.who.int/data/gho/data/themes/mental-health/suicide-rates)")
    st.markdown("- **OECD:** [Mental Health Statistics](https://stats.oecd.org/Index.aspx?QueryId=24879)")
    st.markdown("- **Kaggle:** [Social Media and Mental Health](https://www.kaggle.com/datasets/souvikahmed071/social-media-and-mental-health)")
    st.markdown("- **Healthdata:** [Mental Illness and Depression](https://vizhub.healthdata.org/gbd-results/)")

def suicide_rates_page():
    st.title("Suicide in Sweden")

    # Read the Excel file for suicide rates over time
    def read_data_suicide_rates(file_path):
        return pd.read_excel(file_path)

    # Read the Excel file for suicide rates per age group
    def read_data_age_group(file_path):
        return pd.read_excel(file_path)

    # Filter data for Sweden for suicide rates over time
    def filter_data_for_sweden_suicide_rates(data):
        return data[data['Location'] == 'Sweden']

    # Filter data for Sweden for suicide rates per age group
    def filter_data_for_sweden_age_group(data):
        return data[(data['Location'] == 'Sweden') & (data['Indicator'] == 'Crude suicide rates (per 100 000 population)')]

    # Line graph for suicide rates over time
    def line_graph_suicide_rates(data):
        fig = px.line(data, x='Year', y='FactValueNumeric', color='Gender',
                      color_discrete_map={'Male': 'orange', 'Female': 'orange', 'Both sexes': 'blue'},
                      title='Suicide Rates in Sweden Over Time')
        fig.update_xaxes(showgrid=False)  # Remove grid lines for x-axis
        fig.update_yaxes(showgrid=False)  # Remove grid lines for x-axis        
        st.plotly_chart(fig)  # Plot the chart

    # Bar graph for suicide rates across different age groups
    def bar_graph_suicide_rates_age_group(data, year, gender):
        filtered_data = data[(data['Period'] == year) & (data['Dim1'] == gender)]
        fig = px.bar(filtered_data, x='Dim2', y='First Tooltip', color='Dim1',
                     title=f'Suicide Rates Across Age Groups in Sweden ({year}, {gender})',
                     labels={'Dim2': 'Age Group', 'First Tooltip': 'Suicide Rate per 100,000 Population'})
        fig.update_layout(xaxis={'categoryorder': 'total descending'})
        fig.update_xaxes(showgrid=False)  # Remove grid lines for x-axis
        fig.update_yaxes(showgrid=False)  # Remove grid lines for x-axis
        st.plotly_chart(fig)

    # Map comparing Sweden to other countries in 2019
    def map_comparison(data):
        data_2019 = data[data['Year'] == 2019]
        fig = px.choropleth(data_2019, locations='Location', locationmode='country names',
                            color='FactValueNumeric', title='Suicide Rates Comparison in 2019',
                            labels={'FactValueNumeric': 'Suicide Rates'}, range_color=[1, 25])  # Set color scale
        st.plotly_chart(fig)


    # Read data for suicide rates over time
    file_path_suicide_rates = 'Data_About_suicide_rates_world_wide.xlsx'
    data_suicide_rates = read_data_suicide_rates(file_path_suicide_rates)

    # Filter data for Sweden for suicide rates over time
    sweden_suicide_rates_data = filter_data_for_sweden_suicide_rates(data_suicide_rates)

    # Display line graph for suicide rates over time in Sweden
    st.subheader('Suicide Rates in Sweden Over Time')
    st.markdown('Sweden has had a consistent suicide rate per 100,000 individuals, with the increase from 2000 to 2019 being less than 0.5%, a neglible increase.')
    line_graph_suicide_rates(sweden_suicide_rates_data)

    # Read data for suicide rates per age group
    file_path_age_group = 'Suicide_rates_per_age_group.xlsx'
    data_age_group = read_data_age_group(file_path_age_group)

    # Filter data for Sweden for suicide rates per age group
    sweden_age_group_data = filter_data_for_sweden_age_group(data_age_group)

    # Selectbox for gender
    genders = sweden_age_group_data['Dim1'].unique()
    selected_gender = st.selectbox('Select Gender', genders)

    # Display bar graph for suicide rates across different age groups in Sweden
    selected_year = 2019
    st.subheader('Suicide Rates Across Age Groups in Sweden')
    st.markdown('Suicide rates are highest among the 85+ age group, a shocking statistic. There might be many underlying reasons which need to be explored to explain this high suicide rates in the larger age groups.')
    st.markdown('Upon consulting with experts from the Lebanese Red Cross, it seems that there might be issues in reporting such cases, with younger individuals who commit suicide not being reported correctly. This might be an explanation, yet what applies to Lebanon might not be ideal in Sweden.')
    bar_graph_suicide_rates_age_group(sweden_age_group_data, selected_year, selected_gender)
    st.markdown('Not only that, but the younger age category, 15 to 24, is at the lower end of the spectrum. This could be a promising indicator for Sweden.')
    # Display map comparing Sweden to other countries in 2019
    st.subheader('Comparing Sweden to other world countries in 2019')
    st.markdown("Compared to countries across the world, Sweden seems to be at the lower end of the spectrum, in terms os suicide rates per 100,000. This is evident in the below map.")
    map_comparison(data_suicide_rates)

def mental_illness_page():
    st.title("Mental Illness and Depressive Disorders in Sweden")

    # Read the data from Excel
    df = pd.read_excel("YLL_mental_illness.xlsx", index_col=0)

    st.subheader("YLL Due to Mental Illness in Sweden")
    st.markdown("The overall years of life lost has decreased from 2010 to 2018, by almost 10 years. This  is a positive indicator that might be the result of more awareness in the country. To put that in numbers, the YLL in 2010 was 54.8 years, while in 2018, it reached 45.4 years.")
    # Filter the data for Sweden
    df_sweden = df.loc["Sweden"].reset_index().rename(columns={"index": "Year", "Sweden": "YLL"})

    # Create a line chart for Sweden
    fig = px.line(df_sweden, x="Year", y="YLL", title="YLL Due to Mental Illness Over Time in Sweden")

    # Customize the chart layout
    fig.update_layout(xaxis_title="Year", yaxis_title="YLL")
    fig.update_yaxes(range=[0, 70])
    fig.update_xaxes(showgrid=False)  # Remove grid lines for x-axis
    fig.update_yaxes(showgrid=False)  # Remove grid lines for x-axis

    # Show the chart
    st.plotly_chart(fig)  
    st.title("Mental Illness")

    # Read the data from the CSV file
    df_1 = pd.read_csv("mental-illness-data.csv")

    # Prevalence of Mental Illness by Age Group in Sweden
    st.subheader("Prevalence of Mental Illness by Age Group in Sweden")
    st.markdown("As evident in the figure below, the prevalence of Mental Illness across the different age groups varies based on gender. Yet, the age groups that have the highest number, are the same across, and they are: ")
    st.markdown("- 15-24")
    st.markdown("- 25-34")
    st.markdown("- 45-54")
    st.markdown("- 55-64")
    # Selectbox for gender
    genders = df_1['sex_name'].unique()
    selected_gender_age = st.selectbox('Select Gender for Age Group Comparison', genders)

    # Filter data for selected gender
    filtered_data_age = df_1[(df_1['location_name'] == 'Kingdom of Sweden') & (df_1['sex_name'] == selected_gender_age) & (df_1['age_name'] != "All ages")]
    
    # Aggregate age groups
    aggregated_data_age = filtered_data_age.replace({
        '15-19 years': '15-24 years',
        '20-24 years': '15-24 years',
        '25-29 years': '25-34 years',
        '30-34 years': '25-34 years',
        '35-39 years': '35-44 years',
        '40-44 years': '35-44 years',
        '45-49 years': '45-54 years',
        '50-54 years': '45-54 years',
        '55-59 years': '55-64 years',
        '60-64 years': '55-64 years'
    }).groupby('age_name')['val'].sum().reset_index()
    
    # Sort the data by age group
    aggregated_data_age = aggregated_data_age.sort_values(by='age_name')
    
    # Bar chart for prevalence by aggregated age group
    fig_age_aggregated = px.bar(aggregated_data_age, x='age_name', y='val', 
                                title='Prevalence of Mental Illness by Age Group in Sweden (Aggregated)',
                                labels={'age_name': 'Age Group', 'val': 'Prevalence'})
    fig_age_aggregated.update_layout(xaxis={'categoryorder': 'total descending'})
    fig_age_aggregated.update_xaxes(title="Age Group", showgrid=False)  # Remove grid lines for x-axis
    fig_age_aggregated.update_yaxes(title="Prevalence", showgrid=False)  # Remove grid lines for y-axis
    st.plotly_chart(fig_age_aggregated)
        
    # Read the data from the depression dataset
    depression_df = pd.read_excel("depression-data.xlsx")

    # Prevalence of Depression by Age Group in Sweden (Both Genders)
    st.subheader("Prevalence of Depression by Age Group in Sweden (Both Genders)")
    st.markdown("The same trend that appears in mental disorders appears in the depressive disorders cateogry. This could be due to a potential dominance of depressive disorders with respect to other mental illnesses.")
    # Filter data for Both genders
    filtered_age_depression_data_both = depression_df[(depression_df['sex_name'] == 'Both') & (depression_df['age_name'] != "All ages")]
    
    # Aggregate age groups
    aggregated_age_depression_data_both = filtered_age_depression_data_both.replace({
        '15-19 years': '15-24 years',
        '20-24 years': '15-24 years',
        '25-29 years': '25-34 years',
        '30-34 years': '25-34 years',
        '35-39 years': '35-44 years',
        '40-44 years': '35-44 years',
        '45-49 years': '45-54 years',
        '50-54 years': '45-54 years',
        '55-59 years': '55-64 years',
        '60-64 years': '55-64 years'
    }).groupby('age_name')['value'].sum().reset_index()
    
    # Sort the data by age group
    aggregated_age_depression_data_both = aggregated_age_depression_data_both.sort_values(by='age_name')
    
    # Bar chart for prevalence by aggregated age group
    age_depression_fig_aggregated_both = px.bar(aggregated_age_depression_data_both, x='age_name', y='value', 
                                title='Prevalence of Depression by Age Group in Sweden (Both Genders, Aggregated)',
                                labels={'age_name': 'Age Group', 'value': 'Prevalence'})
    age_depression_fig_aggregated_both.update_layout(xaxis = {'categoryorder': 'total descending'})
    age_depression_fig_aggregated_both.update_layout(xaxis_title="Age Group", yaxis_title="Prevalence")
    age_depression_fig_aggregated_both.update_xaxes(showgrid=False)  # Remove grid lines for x-axis
    age_depression_fig_aggregated_both.update_yaxes(showgrid=False)  # Remove grid lines for y-axis
    st.plotly_chart(age_depression_fig_aggregated_both)

              
def factors_page():
    st.title("Depression and Social Media: A Survey Analysis")
    st.write("The objective is this analysis is not to infer on Sweden specifically, but to showcase how a factor which is engrained within our daily lives, is related to depression.")
    st.title("Depression and Social Media: A Survey Analysis")
    st.write("The objective of this analysis is not to infer on Sweden specifically, but to showcase how a factor which is ingrained within our daily lives is related to depression.")

    data = pd.read_excel("final-survey-dataset.xlsx", sheet_name="Generated Percentages")

    # Filter the data for the "Sum of Frequency of Depression" variable
    depression_data = data[data['Question'] == 'Sum of Frequency of Depression']

    # Pivot the data
    depression_pivot = depression_data.pivot(index='Time Spent', columns='Question', values=[1, 2, 3, 4, 5])

    # Flatten the column names
    depression_pivot.columns = ['_'.join(map(str, col)) for col in depression_pivot.columns]

    # Reset index to make 'Time Spent' a column instead of index
    depression_pivot.reset_index(inplace=True)

    # Melt the dataframe to prepare for plotting
    depression_melted = depression_pivot.melt(id_vars='Time Spent', var_name='Rating', value_name='Percentage')

    # Plot the line chart
    fig = px.line(depression_melted, x='Rating', y='Percentage', color='Time Spent', 
                  title='Frequency of Depression by Time Spent on Social Media',
                  labels={'Rating': 'Rating', 'Percentage': 'Percentage', 'Time Spent': 'Time Spent'})

    fig.update_xaxes(title_text='Rating')
    fig.update_yaxes(title_text='Percentage')
    fig.update_layout(yaxis_tickformat=',.0%')
    fig.update_xaxes(showgrid=False)  # Remove grid lines for x-axis
    fig.update_yaxes(showgrid=False)  # Remove grid lines for x-axis

    # Display the line chart
    st.plotly_chart(fig)
    st.markdown("As evident in the graph, people who reported higher frequency of depression are ones who use social media for longer periods of time in their daily lives. This shows that variables such as this, which take around 25% of many people's time, could be a potential cause of mental depression.")

    
def main():
    st.sidebar.title("Navigation")
    pages = {
        "Dashboard Overview": overview_page,
        "Suicide in Sweden": suicide_rates_page,
        "Mental Illness and Depressive Disorders": mental_illness_page,
        "Depression and Social Media": factors_page
    }
    selection = st.sidebar.radio("Go to", list(pages.keys()))
    page = pages[selection]
    page()

if __name__ == "__main__":
    main()
