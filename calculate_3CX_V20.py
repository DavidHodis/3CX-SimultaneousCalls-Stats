import pandas as pd
from datetime import datetime

def analyze_call_overlaps(input_csv):
    # Load the original CSV
    df = pd.read_csv(input_csv)
    
    # Drop unanswered calls
    df = df[df['Status'] == 'answered']
    
    # Convert initial Call Time and Talking
    df['Call Time'] = pd.to_datetime(df['Call Time'])
    df['Talking'] = pd.to_timedelta(df['Talking'])
    
    # Format dates exactly as in format2.py
    date = df['Call Time'].dt.date
    df['CallDate'] = date.apply(lambda x: x.strftime('%d/%m/%Y'))
    df['CallStart'] = df['Call Time'].dt.time
    add = df['Call Time'] + df['Talking']
    df['CallEnd'] = add.dt.time
    
    # Convert to datetime objects with explicit format and dayfirst=True
    df['start_time'] = pd.to_datetime(
        df['CallDate'] + ' ' + df['CallStart'].astype(str), 
        format='%d/%m/%Y %H:%M:%S',
        dayfirst=True
    )
    df['end_time'] = pd.to_datetime(
        df['CallDate'] + ' ' + df['CallEnd'].astype(str), 
        format='%d/%m/%Y %H:%M:%S',
        dayfirst=True
    )
    
    # Create events list
    events = []
    for _, row in df.iterrows():
        events.append((row['start_time'], 'start'))
        events.append((row['end_time'], 'end'))
    
    # Sort events by time
    events.sort(key=lambda x: (x[0], x[1] == 'start'))
    
    # Track overlaps
    overlap_count = 0
    simultaneous_overlaps = {}
    
    for event in events:
        if event[1] == 'start':
            overlap_count += 1
        else:
            overlap_count -= 1
            
        if overlap_count > 1:
            simultaneous_overlaps[overlap_count] = simultaneous_overlaps.get(overlap_count, 0) + 1
    
    return simultaneous_overlaps

# Example usage
csv_file = 'markco.csv'
overlaps = analyze_call_overlaps(csv_file)
for num_calls, count in overlaps.items():
    print(f'{num_calls} calls overlapped {count} times.')