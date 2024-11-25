import pandas as pd
from datetime import datetime

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('hunt20_7.csv')

# Drop unanswered calls
df = df[df['Status'] == 'answered']

# Convert Call Time to datetime (file2 uses ISO format)
df['Call Time'] = pd.to_datetime(df['Call Time'])

# Convert Talking time to timedelta
df['Talking'] = pd.to_timedelta(df['Talking'])

# Format dates
date = df['Call Time'].dt.date
formatted_dates = date.apply(lambda x: x.strftime('%d/%m/%Y'))
df['CallDate'] = formatted_dates

# Split the Call Time column into time
df['CallStart'] = df['Call Time'].dt.time

# Add the times to determine when the call ended
add = df['Call Time'] + df['Talking']
df['CallEnd'] = add.dt.time

# Drop the original datetime and Talking columns
#df = df.drop(['Call Time', 'Talking'], axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('calldata.csv', index=False)
print("Call date and time columns have been successfully split and saved to 'calldata.csv'")