import pandas as pd
from datetime import datetime

# Function to track the number of overlapping calls at any given time
def count_simultaneous_overlaps(csv_file):
    # Load the CSV file into a dataset
    calls = pd.read_csv(csv_file)
    
    # Parse the CallDate and combine with CallStart and CallEnd to create datetime 
    
    calls['start_time'] = pd.to_datetime(calls['CallDate'] + ' ' + calls['CallStart'], format='%d/%m/%Y %H:%M:%S')
    calls['end_time'] = pd.to_datetime(calls['CallDate'] + ' ' + calls['CallEnd'], format='%d/%m/%Y %H:%M:%S')
    
    # Create a list of events 
    events = []
    for _, row in calls.iterrows():
        events.append((row['start_time'], 'start'))
        events.append((row['end_time'], 'end'))
    
    # Sort events by time, 
    
    events.sort(key=lambda x: (x[0], x[1] == 'start'))
    
    # Track the maximum number of simultaneous calls 
    overlap_count = 0
    simultaneous_overlaps = {}

    # Iterate over events and calculate how many calls are happening at any moment
    for event in events:
        if event[1] == 'start':
            overlap_count += 1
        else:
            overlap_count -= 1

        if overlap_count > 1:
            simultaneous_overlaps[overlap_count] = simultaneous_overlaps.get(overlap_count, 0) + 1

    return simultaneous_overlaps

# Example usage
csv_file = 'calldata.csv'  # Replace with the path to the CSV file
overlaps = count_simultaneous_overlaps(csv_file)
for num_calls, count in overlaps.items():
    print(f'{num_calls} calls overlapped {count} times.')
