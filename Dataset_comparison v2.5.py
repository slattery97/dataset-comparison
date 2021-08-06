# The purpose of this program is to import data from a CSV file, compare the
# data contained in each dataframe for matches and calculate their similarity.
# The nonmatching data entries and accuracy for each field are exported to Excel.

# import packages
import pandas as pd
import numpy as np

# import truth dataset
df_truth = pd.read_csv('BRYJ Test Truth.csv')

# import dataset to be compared with truth
df1 = pd.read_csv('BRYJ Test Extract.csv')


# get list of column names
col_names = df_truth.columns
col_names = list(col_names)

# initialize list of valid column names where number of entries in truth
# and extracted data match
col_names_valid = []

# initialize list for column accuracy
col_accuracy1 = []

# initialize list for column lengths
col_lengths = []

# initialize list for non-matches in truth dataset
list_truth_no_match = []

# initialize list for non-matches in extract dataset
list_extract_no_match = []

## get column accuracy of dataframe with blank entries removed

# initialize column matches variable
col_matches1 = 0
# loop through every column in the dataframes
for i in range(len(col_names)):
    # get individual column of dataframe
    df_truth_clean = df_truth[col_names[i]]
    df1_clean = df1[col_names[i]]
    # convert data columns to lists
    list_truth_clean = list(df_truth_clean)
    list1_clean = list(df1_clean)
    
    # ensure number of entries in truth and extract data lists match
    if len(list_truth_clean) == len(list1_clean):
        # get number of entries in each column
        col_lengths.append(len(list_truth_clean))
        # get list of only valid field names
        col_names_valid.append(col_names[i])
        
        # loop through every data entry in column
        for j in range(len(list_truth_clean)):
            # replace any empty strings with an underscore placeholder
            if pd.isna(list_truth_clean[j]):
                list_truth_clean[j] = '_'
            if pd.isna(list1_clean[j]):
                list1_clean[j] = '_'

            # determine number of matches for column
            if list_truth_clean[j] == list1_clean[j]:
                col_matches1 += 1
            else:
                # append non-matches to respective lists
                list_truth_no_match.append(list_truth_clean[j])
                list_extract_no_match.append(list1_clean[j])
        # append number of matches for column to list
        col_accuracy1.append(col_matches1)
        col_matches1 = 0

# initialize list of number non-matches for each column
list_no_match = []

# append number of non-matches for each column to list
for i in range(len(col_names_valid)):
    non_matches = col_lengths[i] - col_accuracy1[i]
    list_no_match.append(non_matches)
    non_matches = 0
    
# create empty dataframe to store non-matches
df_non_matches = pd.DataFrame()

# get total number of non-matches
total_non_matches = sum(list_no_match)

# get largest value in list of total entries
max_entries = max(col_lengths)

# initialize variables for start and end of index slice (section of non-match
# list that corresponds to each field
ind_start = 0
ind_end = int(list_no_match[0])
    
# append non-matches to their respective columns in the dataframe
for i in range(len(col_names_valid)):
    # for fields with all matches insert all asterisks (or any filler content)
    if list_no_match[i] == 0:
        df_non_matches.insert(i*2,col_names_valid[i]+' Truth',' ',allow_duplicates=True)
        df_non_matches.insert(i*2+1,col_names_valid[i]+ ' Extract',' ',allow_duplicates=True)
    # for fields with only one non-match, insert the non-match entry followed by all asterisks
    elif list_no_match[i] == 1:
        df_non_matches.insert(i*2,col_names_valid[i]+' Truth',[list_truth_no_match[ind_start]]+[' ']*(max_entries-list_no_match[i]),allow_duplicates=True)
        df_non_matches.insert(i*2+1,col_names_valid[i]+' Extract',[list_extract_no_match[ind_start]]+[' ']*(max_entries-list_no_match[i]),allow_duplicates=True)
    # for fields with multiple non-matches, insert the non-matching entries followed by all asterisks
    else:
        df_non_matches.insert(i*2,col_names_valid[i]+' Truth',list_truth_no_match[ind_start:ind_end]+[' ']*(max_entries-list_no_match[i]),allow_duplicates=True)
        df_non_matches.insert(i*2+1,col_names_valid[i]+' Extract',list_extract_no_match[ind_start:ind_end]+[' ']*(max_entries-list_no_match[i]),allow_duplicates=True)
    # for all columns prior to last column, update slice variable indexes
    if i == (len(col_names_valid)-1):
        ind_start = ind_end
    else:
        ind_start = ind_end
        ind_end = ind_end + list_no_match[i+1]
      
# export dataframe of non-matches to Excel spreadsheet
df_non_matches.to_excel("Non Matching Data.xlsx")

# check number of entries (fields), if necessary
print('Number of total fields: ',len(col_names))
print('Number of valid fields: ',len(col_names_valid))

# create empty dataframe to store accuracy and export to excel
df_export = pd.DataFrame(columns = col_names_valid)

# append number of matches and entries in each column to export dataframe
df_export.loc[0] = col_accuracy1
df_export.loc[1] = col_lengths

# get number of total matches and entries
total_matches = sum(col_accuracy1)
total_entries = sum(col_lengths)

# calculate overall accuracy
accuracy_total = (total_matches / total_entries) * 100
accuracy_total = "{:.2f}".format(accuracy_total)

# display overall accuracy for batch
print('Overall accuracy: ',accuracy_total)

# calculate percentage of accuracy for each column
for i in range(len(col_accuracy1)):
    col_accuracy1[i] = (float(col_accuracy1[i]) / float(col_lengths[i])) * 100
    col_accuracy1[i] = "{:.2f}".format(col_accuracy1[i])

# display accuracy for each field
print('Field accuracy: ',col_accuracy1)

# append column accuracy to export dataframe
df_export.loc[2] = col_accuracy1

# check export dataframe, if necessary
print(df_export)

# export comparison table to excel file
df_export.to_excel("Field Accuracy Data.xlsx")





