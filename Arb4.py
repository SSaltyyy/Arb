from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime
import os

url = 'https://arbworld.net/en/dropping-odds/football-1-x-2?hidden=&shown=&timeZone=%2B01%3A00&refreshInterval=60&order=5&min=0&max=100&day=All'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Select all table rows with the class "belowHeader"
rows = soup.select('tr.belowHeader') 

# Define a list to translate index numbers into '1', 'X', '2'
index_translator = ['1', 'X', '2']

games = []
for row in rows:
    # Select all "odds_col" elements within the row
    odds_elements = row.select('td.odds_col')
    
    for i, odds_element in enumerate(odds_elements):
        # Check if the current "odds_col" element is orange or red
        if 'background:orange' in odds_element['style']:
            box_color = 'orange'
        elif 'background:red' in odds_element['style']:
            box_color = 'red'
        else:
            continue

        date = row.select_one('td.tdate').text
        home_team = row.select_one('td.thome').text
        away_team = row.select_one('td.taway').text
        league = row.select_one('td.tleague').text
        # Split the odds on the <br> tag and join them with ' --> '
        odds = ' --> '.join(odds_element.stripped_strings)
        # Use the index to determine whether the orange box is '1', 'X', or '2'
        odds_box = index_translator[i]
        games.append((date, league, home_team, away_team, odds, odds_box, box_color))

# Now `games` is a list of tuples, each containing the date, home team, odds, odds box, and box color for each game

# Convert the list of games to a pandas DataFrame
columns = ['Date', 'League', 'Home Team', 'Away Team', 'Odds', 'Odds Box', 'Box Color']
df = pd.DataFrame(games, columns=columns)

# Get the current date and time, format it as DD-MM-YYYY HH:MM:SS, and add it as a new column
df['Timestamp'] = datetime.now().strftime('%d-%m-%Y %H:%M:%S')

# Ask user if they want to append data
append_data = input("Do you want to append data to the existing file? (yes/no): ")

# Define file paths
csv_filename = r'C:\Users\navyt\Documents\ARB\ARB.csv'
excel_filename = r'C:\Users\navyt\Documents\ARB\ARB.xlsx'

# Set the maximum number of displayed columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# Set the maximum width to None for unlimited
pd.set_option('display.width', None)

print(df)

if append_data.lower() == 'yes':
    # Check if the files exist
    if os.path.isfile(csv_filename) and os.path.isfile(excel_filename):
        # Read the existing data
        df_existing = pd.read_excel(excel_filename)

        # Append the new data to the existing data
        df_combined = pd.concat([df_existing, df], ignore_index=True)
        
        # Write the DataFrame to a CSV file
        df.to_csv(csv_filename, mode='a', header=False, index=False)

        # Write the combined DataFrame to an Excel file
        df_combined.to_excel(excel_filename, index=False)

        print(f"Data successfully appended to {csv_filename} and {excel_filename}.")
    else:
        # Write the DataFrame to a CSV and Excel file
        df.to_csv(csv_filename, index=False)
        df.to_excel(excel_filename, index=False)

        print(f"Data successfully written to {csv_filename} and {excel_filename}. New files were created as they did not exist.")
else:
    print("No data written. Operation cancelled by user.")
    


