import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Medical Appointment Analysis",
    page_icon="🏥",
    layout="wide"
)

# Load data with proper encoding
@st.cache_data
def load_data():
    return pd.read_csv('KaggleV2-May-2016-Cleaned.csv', encoding='ISO-8859-1', low_memory=False)

df = load_data()

# Clean up column names (remove trailing space in 'No-show ')
df.columns = df.columns.str.strip()

# Title and description
st.title("🏥 Medical Appointment No-Show Analysis")
st.markdown("Analyze appointment patterns and no-show rates by various factors")

# Sidebar for filters
st.sidebar.header("Filter Data")

# Day of week filter
days = st.sidebar.multiselect(
    "Select days of week:",
    options=sorted(df['AppointmentDays'].unique()),
    default=sorted(df['AppointmentDays'].unique())
)

# Gender filter
genders = st.sidebar.multiselect(
    "Select gender:",
    options=df['Gender'].unique(),
    default=df['Gender'].unique()
)

# Age range filter
min_age, max_age = st.sidebar.slider(
    "Select age range:",
    min_value=int(df['Age'].min()),
    max_value=int(df['Age'].max()),
    value=(int(df['Age'].min()), int(df['Age'].max()))
)

# Comorbidity filters
st.sidebar.subheader("Comorbidity Filters")
hipertension = st.sidebar.checkbox("Hypertension", value=True)
diabetes = st.sidebar.checkbox("Diabetes", value=True)
alcoholism = st.sidebar.checkbox("Alcoholism", value=True)
handicap = st.sidebar.checkbox("Handicap", value=True)

# Apply filters
filtered_df = df.copy()
if days:
    filtered_df = filtered_df[filtered_df['AppointmentDays'].isin(days)]
if genders:
    filtered_df = filtered_df[filtered_df['Gender'].isin(genders)]
filtered_df = filtered_df[(filtered_df['Age'] >= min_age) & (filtered_df['Age'] <= max_age)]

comorbidity_filters = []
if hipertension:
    comorbidity_filters.append('Hipertension')
if diabetes:
    comorbidity_filters.append('Diabetes')
if alcoholism:
    comorbidity_filters.append('Alcoholism')
if handicap:
    comorbidity_filters.append('Handicap')

# Display metrics
st.header("Overview Metrics")
col1, col2, col3, col4 = st.columns(4)

total_appointments = len(filtered_df)
no_show_count = filtered_df[filtered_df['No-show'] == 1].shape[0]  # Changed from 'Yes' to 1
no_show_rate = (no_show_count / total_appointments * 100) if total_appointments > 0 else 0
avg_age = filtered_df['Age'].mean()

col1.metric("Total Appointments", f"{total_appointments:,}")
col2.metric("No-Shows", f"{no_show_count:,}")
col3.metric("No-Show Rate", f"{no_show_rate:.2f}%")
col4.metric("Average Age", f"{avg_age:.1f}")

# Day of week analysis
st.header("No-Show Analysis by Day of Week")
day_data = filtered_df.groupby('AppointmentDays').agg({
    'No-show': lambda x: (x == 1).sum(),  # Changed from 'Yes' to 1
    'PatientId': 'count'
}).rename(columns={'No-show': 'NoShows', 'PatientId': 'TotalAppointments'}).reset_index()
day_data['NoShowRate'] = (day_data['NoShows'] / day_data['TotalAppointments']) * 100

fig_day = px.bar(
    day_data, 
    x='AppointmentDays', 
    y='NoShowRate',
    title='No-Show Rate by Day of Week',
    color='AppointmentDays',
    text='NoShowRate'
)
fig_day.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
st.plotly_chart(fig_day, use_container_width=True)

# Comorbidity analysis
st.header("No-Show Analysis by Comorbidity")
comorbidity_data = []

for condition in ['Hipertension', 'Diabetes', 'Alcoholism', 'Handicap']:
    if condition in comorbidity_filters:
        total_with_condition = filtered_df[filtered_df[condition] == 1].shape[0]
        no_shows_with_condition = filtered_df[(filtered_df[condition] == 1) & (filtered_df['No-show'] == 1)].shape[0]  # Changed from 'Yes' to 1
        no_show_rate_condition = (no_shows_with_condition / total_with_condition * 100) if total_with_condition > 0 else 0
        
        comorbidity_data.append({
            'Condition': condition,
            'Total': total_with_condition,
            'NoShows': no_shows_with_condition,
            'NoShowRate': no_show_rate_condition
        })

if comorbidity_data:
    comorbidity_df = pd.DataFrame(comorbidity_data)
    fig_comorbidity = px.bar(
        comorbidity_df, 
        x='Condition', 
        y='NoShowRate',
        title='No-Show Rate by Comorbidity',
        color='Condition',
        text='NoShowRate'
    )
    fig_comorbidity.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    st.plotly_chart(fig_comorbidity, use_container_width=True)
else:
    st.info("Select at least one comorbidity to see analysis.")

# Gender analysis
st.header("No-Show Analysis by Gender")
gender_data = filtered_df.groupby('Gender').agg({
    'No-show': lambda x: (x == 1).sum(),  # Changed from 'Yes' to 1
    'PatientId': 'count'
}).rename(columns={'No-show': 'NoShows', 'PatientId': 'TotalAppointments'}).reset_index()
gender_data['NoShowRate'] = (gender_data['NoShows'] / gender_data['TotalAppointments']) * 100

fig_gender = px.bar(
    gender_data, 
    x='Gender', 
    y='NoShowRate',
    title='No-Show Rate by Gender',
    color='Gender',
    text='NoShowRate'
)
fig_gender.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
st.plotly_chart(fig_gender, use_container_width=True)

# Age analysis
st.header("No-Show Analysis by Age")

# Create age groups
bins = [0, 18, 30, 45, 60, 100]
labels = ['0-18', '19-30', '31-45', '46-60', '61+']
filtered_df['AgeGroup'] = pd.cut(filtered_df['Age'], bins=bins, labels=labels, right=False)

age_data = filtered_df.groupby('AgeGroup').agg({
    'No-show': lambda x: (x == 1).sum(),  # Changed from 'Yes' to 1
    'PatientId': 'count'
}).rename(columns={'No-show': 'NoShows', 'PatientId': 'TotalAppointments'}).reset_index()
age_data['NoShowRate'] = (age_data['NoShows'] / age_data['TotalAppointments']) * 100

fig_age = px.bar(
    age_data, 
    x='AgeGroup', 
    y='NoShowRate',
    title='No-Show Rate by Age Group',
    color='AgeGroup',
    text='NoShowRate'
)
fig_age.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
st.plotly_chart(fig_age, use_container_width=True)

# SMS received analysis
st.header("No-Show Analysis by SMS Received")
sms_data = filtered_df.groupby('SMS_received').agg({
    'No-show': lambda x: (x == 1).sum(),  # Changed from 'Yes' to 1
    'PatientId': 'count'
}).rename(columns={'No-show': 'NoShows', 'PatientId': 'TotalAppointments'}).reset_index()
sms_data['SMS_received'] = sms_data['SMS_received'].map({0: 'No SMS', 1: 'SMS Received'})
sms_data['NoShowRate'] = (sms_data['NoShows'] / sms_data['TotalAppointments']) * 100

fig_sms = px.bar(
    sms_data, 
    x='SMS_received', 
    y='NoShowRate',
    title='No-Show Rate by SMS Notification',
    color='SMS_received',
    text='NoShowRate'
)
fig_sms.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
st.plotly_chart(fig_sms, use_container_width=True)

# Data export
st.header("Export Data")
st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False),
    file_name=f"filtered_appointment_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
    mime="text/csv"
)

# Show raw data
if st.checkbox("Show Filtered Data Preview"):
    st.subheader("Filtered Appointment Data")
    st.dataframe(filtered_df.head(100))
