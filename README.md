# Patient Appointment Analyzer - Streamlit App

## 📊 Project Overview
This project helps healthcare administrators and staff understand why patients miss appointments.
It uses Excel to clean raw data and Streamlit to create an interactive dashboard.
Users can filter the data by age, gender, medical conditions, and day of the week to spot patterns in no-shows.
The goal is to uncover key factors that affect attendance and use those insights to reduce missed appointments.
## 🛠️ Technical Implementation

# 📊 Excel-Based Data Preparation
Excel was used extensively to clean and structure the raw appointment data:

# 🔁 Pivot Tables: Analyzed no-show patterns by day, gender, and comorbidities
- 🧹 Remove Duplicates: Ensured data integrity
- ✂️ TRIM Function: Standardized text fields
- 🔍 Find & Replace: Converted gender codes (F → Female, M → Male)
- 🧬 UNIQUE Function: Resolved Unicode import errors
- 📈 COUNTIF: Generated summary statistics
- 🧮 Custom Formulas: Converted no-show status to binary (0/1)

# ⌨️ Excel Shortcuts Used
- Ctrl+H – Find and Replace
- Alt+H+W – Wrap Text
- Alt+H+O+I – Auto-fit Column Width
- Ctrl+Home/End – Navigate to Worksheet Extremes
- Page Up/Down – Rapid Vertical Navigation
- Shift+Space – Select Entire Row
- 📸 Screenshots of applied shortcuts and Excel steps are available in the Screenshots folder.

# 🗂️ Workbook Structure
- OG – Original raw data (hidden)
- Clean Sheet – Processed and standardized data
- Worksheet – Analysis, charts, and pivot tables

# 🌐 Streamlit Web Application
The interactive dashboard allows users to:
- 📅 Select a day of the week to analyze no-show patterns
- 🩺 View no-show rates by comorbidities (Alcoholism, Hypertension, Diabetes, Handicap)
- 👥 Analyze trends by gender and age
- 📊 Explore visualizations of appointment data

# 🎓 Excel Learning Resources
- 📘 Click [here](https://www.youtube.com/watch?v=opJgMj1IUrc&t=264s) to watch:Excel Tutorials for Beginners
- 📘 Click [here](https://www.youtube.com/watch?v=Y8xhrUa3KH4) to watch: Excel Formulas and Functions
