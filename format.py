import pandas as pd
from datetime import datetime

# Load the CSV file into a pandas DataFrame
# Replace 'your_file.csv' with your actual CSV file name.
df = pd.read_csv('BT90.csv')

# Actual column name that contains the datetime.
# If the column isn't already in datetime format, convert it.
df['Call Time'] = pd.to_datetime(df['Call Time'])
df['Talking'] = pd.to_timedelta(df['Talking'])

#Format dates
date = df['Call Time'].dt.date
formatted_dates = date.apply(lambda x: x.strftime('%d/%m/%Y')) 

df['CallDate'] = formatted_dates

# Split the Call Time column into date and time
df['CallStart'] = df['Call Time'].dt.time


# df['CallEnd'] = df['Call Time'] + df['Talking']
add = df['Call Time'] + df['Talking']

addb = add.dt.time
#fmdate = (date.strftime('%d,%m,%Y'))
df['CallEnd'] = addb


# Drop the original datetime column (optional)
df = df.drop('Call Time', axis=1)
df = df.drop('Talking', axis=1)
#df = df.drop('CallDate', axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('calldata.csv', index=False)

print("3CX Date and time columns have been successfully split and saved to 'calldate.csv'")
#print(formatted_dates)

