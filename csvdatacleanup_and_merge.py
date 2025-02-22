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


# context_1 = csv_to_dict('context_ungrouped1.csv')
# context_2 = csv_to_dict('context_ungrouped2.csv')
# noncontext_1 = csv_to_dict('noncontext_ungrouped1.csv')
# noncontext_2 = csv_to_dict('noncontext_ungrouped2.csv')
# grouped_1 = csv_to_dict('groupted_data1.csv')
# grouped_2 = csv_to_dict('groupted_data2.csv')
# combined_context = combine_csvs(context_1, context_2, ['label', 'text'])
# combined_noncontext = combine_csvs(noncontext_1, noncontext_2, ['label', 'text'])
# combined_grouped = combine_csvs(grouped_1, grouped_2, ['label', 'text'])

# print(len(combined_context['label']))
# combined_context = pd.DataFrame(combined_context)
# combined_context = combined_context.drop_duplicates()
# combined_context.dropna()

# print(len(combined_noncontext['label']))
# combined_noncontext = pd.DataFrame(combined_noncontext)
# combined_noncontext = combined_noncontext.drop_duplicates()
# combined_noncontext.dropna()

# print(len(combined_grouped['label']))
# combined_grouped = pd.DataFrame(combined_grouped)
# combined_grouped = combined_grouped.drop_duplicates()
# combined_grouped.dropna()

# combined_context.to_csv('combined_context.csv', index=False, index_label=False)
# combined_noncontext.to_csv('combined_noncontext.csv', index=False, index_label=False)
# combined_grouped.to_csv('combined_grouped.csv', index=False, index_label=False)

# if label = surname and text has [element-citation[person-group[name[]]]],
# replace surname with person-group[name[surname]]]] and make text group[name[surname]]]] [element-citation]

import csv
import re

def process_csv(input_file, output_file):
    processed_rows = []

    with open(input_file, mode='r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header
        processed_rows.append(header)

        print("Processing...")
        for row in reader:
            label, text = row

            # Replace the target pattern in the text column
            text = re.sub(r"\[element-citation\[person-group\[name\[\]\]\]\]", "[element-citation]", text)

            processed_rows.append([label, text])

    with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(processed_rows)

    print("Processing complete. Output saved to", output_file)

# Example usage
process_csv("combined_context.csv", "combined_simplecontext_Corrected.csv")
