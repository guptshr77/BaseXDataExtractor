from BaseXClient import BaseXClient
import xml.etree.ElementTree as ET
import pandas as pd
import csv


def csv_to_dict(csv_file):
    data_dict = {}
    
    # Open the file with the utf-8 encoding to avoid UnicodeDecodeError
    with open(csv_file, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        
        # Read the header row (first row) to get column names
        header = next(csv_reader)
        
        # Initialize a list for each column in the dictionary
        for col in header:
            data_dict[col] = []
        
        # Populate the dictionary with values from each row
        for row in csv_reader:
            for i, value in enumerate(row):
                data_dict[header[i]].append(value)
    
    return data_dict

def combine_csvs(csv_file1, csv_file2, col_titles):
    combined_csv = {}
    for title in col_titles:
        combined_csv[title] = []
    print("combined_csv made")
    length2 = len(csv_file1)
    i = 0
    while i < length2:
        for title in col_titles:
            combined_csv[title].append(csv_file1[title][i])
        i += 1
    print("csvfile1 copied")
    length1 = len(csv_file2['label'])
    i = 0
    while i < length1:
        for title in col_titles:
            combined_csv[title].append(csv_file2[title][i])
        i += 1
    print("csvfile2 copied over")
    print("total rows = ", (length2+length1))
    return combined_csv

def get_rid_of_duplicates():
    # ugd = ungrouped labels, gd = grouped labels
    pd.read_csv("combined_ugd_cleaned.csv").drop_duplicates().to_csv("combined_ugd.csv", index=False)
    pd.read_csv("combined_gd_cleaned.csv").drop_duplicates().to_csv("combined_gd.csv", index=False)


grouped1 = csv_to_dict('grouped1.csv')
grouped2 = csv_to_dict('grouped2.csv')
ungrouped1 = csv_to_dict('ungrouped_with_metadata1.csv')
ungrouped2 = csv_to_dict('ungrouped_with_metadata2.csv')
grouped = combine_csvs(grouped1, grouped2, ['label', 'text'])
ungrouped = combine_csvs(ungrouped1, ungrouped2, ['label', 'text'])

print(len(grouped['label']))
grouped = pd.DataFrame(grouped)
grouped = grouped.drop_duplicates()
grouped.dropna()

print(len(ungrouped['label']))
ungrouped = pd.DataFrame(ungrouped)
ungrouped = ungrouped.drop_duplicates()
ungrouped.dropna()


grouped.to_csv('grouped.csv', index=False, index_label=False)
ungrouped.to_csv('ungrouped_with_metadata.csv', index=False, index_label=False)
