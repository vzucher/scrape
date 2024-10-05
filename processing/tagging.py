import os
import pandas as pd

def determine_type(url):
    """Helper function to determine the type based on the URL."""
    if "/p/" in url:
        return 'POST URL'
    else:
        return 'USER URL'

def post_or_user(urls_df):
    # Check if 'Type' column exists
    if 'Type' not in urls_df.columns:
        urls_df.insert(0, 'Type', None)  # Add a 'Type' column with None values

    # Iterate over the rows of the DataFrame
    for index, row in urls_df.iterrows():
        # If the 'Type' is not filled or if it looks like a URL, determine the type based on the URL
        if pd.isnull(row['Type']) or (row['Type'] and row['Type'].startswith('http')):
            type_value = determine_type(row['Type'] if row['Type'] and row['Type'].startswith('http') else row['URL'])
            if row['Type'] and row['Type'].startswith('http'):
                urls_df.at[index, 'URL'] = row['Type']
            urls_df.at[index, 'Type'] = type_value

    # Drop rows where 'URL' is NaN
    urls_df = urls_df.dropna(subset=['URL'])

    # Sort the DataFrame by the 'Type' column
    sorted_df = urls_df.sort_values(by="Type", ascending=False)

    # Save the updated DataFrame back to the CSV
    sorted_df.to_csv('data/urls.csv', index=False)
    return sorted_df

# Read the CSV into a DataFrame
urls_df = pd.read_csv('data/urls.csv')
post_or_user(urls_df)
