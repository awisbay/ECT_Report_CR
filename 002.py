
import os
import re
import pandas as pd
import numpy as np
import xlsxwriter
import glob
import sys
import os
from tqdm import tqdm


##
BEFORE_TIME = "2025-04-10 09:00"
AFTER_TIME = "2025-04-10 09:00"

# Function to extract NODENAME using regex
def extract_nodename(filename):
    ##integProtUserPlaneCapability featCtrlIntegProtUserPlane
    match = re.match(r'(.+?)_(Alarm|bandwidth|cellstatus|SleepState|freqPrioListEUTRA)\.LOGS_FILE', filename)
    if match:
        return match.group(1)
    else:
        return None




def remark_log_as_unremote(logfile_path):
    # Define the regex pattern to match lines that start with "Bye"
    pattern = re.compile(r'^Bye')

    # Read the log file
    with open(logfile_path, 'r') as file:
        lines = file.readlines()

    # Check if any line matches the pattern
    contains_bye = any(pattern.match(line) for line in lines)
    
    ##return contains_bye
    # If no line matches, remark the log as "Unremote"
    if not contains_bye:
        ##print(f"\n [{logfile_path}] # Remark: Unremote \n")
        remark_status = "Unremote"
    else:
        remark_status = "OK"
        
        
    return remark_status
    






def extract_log_patterns(logfile, patterns, log_folder):
    ###log_folder = "02_LOG"
    input_path = os.path.join(log_folder, logfile)
    base_name = os.path.splitext(logfile)[0]
    
    with open(input_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    for pattern in patterns:
        output_file = os.path.join(log_folder, f"{base_name}_{pattern}.LOGS_FILE")
        extracting = False
        
        with open(output_file, 'w', encoding='utf-8') as outfile:
            for line in lines:
                if f'####LOG_{pattern}' in line:
                    extracting = True
                    continue  # Skip writing the start marker
                elif f'####END_LOG_{pattern}' in line:
                    extracting = False
                    break  # Stop reading once end marker is found
                
                if extracting and ";" in line:
                    cleaned_line = re.sub(r'\s{2,}', ' ', line.strip())  # Replace multiple spaces with a single space
                    cleaned_line = re.sub(r' ;', ';', cleaned_line.strip())  # Replace multiple spaces with a single space
                    outfile.write(cleaned_line + "\n")
        
        ##print(f"Extracted content saved to: {output_file}")











def read_files_from_folder(folder_path):
    dataframes = {'Summary': [], 'Alarm': [], 'freqPrioListEUTRA': [], 'Cell Status': [], 'SleepState': []}
    
    log_files = [f for f in os.listdir(folder_path) if f.endswith('.log')]
    
    # Extract logs with tqdm progress bar
    for filename in tqdm(log_files, desc="Extracting Logs"):
        pattern_loop = ("cellstatus", "Alarm", "freqPrioListEUTRA", "SleepState")
        extract_log_patterns(filename, pattern_loop, folder_path)
    
    # Process files with tqdm progress bar
    for filename in tqdm(os.listdir(folder_path), desc="Processing Files"):
        file_path = os.path.join(folder_path, filename)
        
        if filename.endswith('.log'):
            check_log = remark_log_as_unremote(file_path)
            ####print(f"DATA {filename}  [{check_log}]  [{folder_path}]")
            df = pd.DataFrame({'NODENAME': [filename.replace(".log", "")],
                               'MO': [filename.replace(".log", "")],
                               'Status': [check_log]})
            dataframes['Summary'].append(df)
        
        if os.stat(file_path).st_size == 0:
            continue
        
        nodename = extract_nodename(filename)
        if nodename is None:
            ##print(f"Skipping file with unexpected format: {filename}")
            continue
        
        try:
            if '_Alarm.LOGS_FILE' in filename:
                df = pd.read_csv(file_path, delimiter=';', skiprows=0,
                                 names=['Date', 'Time', 'Severity', 'Object', 'Problem', 'Cause'] + 
                                       [f'AdditionalText{i}' for i in range(1, 9)])
                df['AdditionalText'] = df[[f'AdditionalText{i}' for i in range(1, 9)]].apply(
                    lambda x: ';'.join(str(val) for val in x.dropna()), axis=1)
                df = df[df['Date'] != 'Date']
                df = df[['Date', 'Time', 'Severity', 'Object', 'Problem', 'Cause', 'AdditionalText']]
            else:
                df = pd.read_csv(file_path, delimiter=';')
            
            df['NODENAME'] = nodename
            ##print(filename)
            
            if '_Alarm.LOGS_FILE' in filename:
                dataframes['Alarm'].append(df)
            elif '_freqPrioListEUTRA.LOGS_FILE' in filename:
                dataframes['freqPrioListEUTRA'].append(df)
            elif '_cellstatus.LOGS_FILE' in filename:
                dataframes['Cell Status'].append(df)
            elif '_SleepState.LOGS_FILE' in filename:
                dataframes['SleepState'].append(df)
            
            ##print(df.shape[0])
        except pd.errors.EmptyDataError:
            print(f"No columns to parse in file: {filename}")
            continue
    
    # Concatenate DataFrames
    for key in dataframes:
        if dataframes[key]:
            dataframes[key] = pd.concat(dataframes[key], ignore_index=True)
    
    # Clean up temporary files
    files = glob.glob(os.path.join(folder_path, "*.LOGS_FILE"))
    for file in tqdm(files, desc="Deleting Temporary Files"):
        os.remove(file)
        ##print(f"Deleted: {file}")
    
    return dataframes   
    
    
    
    
    
    

# Function to compare two dataframes and format the difference
def compare_dataframes(df_before, df_after):
    df_merged = pd.merge(df_before, df_after, on=['NODENAME', 'MO'], how='outer', suffixes=('_Before', '_After'))

    # Remove rows where the MO column equals "MO"
    df_merged = df_merged[df_merged['MO'] != 'MO']

    # Ensure the columns are in the order: NODENAME, MO, and the rest
    ordered_columns = ['NODENAME', 'MO'] + [col for col in df_merged.columns if col not in ['NODENAME', 'MO']]
    df_merged = df_merged[ordered_columns]

    return df_merged

# Function to clean administrativeState and operationalState columns
def clean_cell_status(df):
    # Regex to extract values within brackets
    def extract_bracket_content(text):
        match = re.search(r'\((.*?)\)', text)
        return f"({match.group(1)})" if match else text

    if 'administrativeState' in df.columns:
        df['administrativeState'] = df['administrativeState'].apply(extract_bracket_content)
    if 'operationalState' in df.columns:
        df['operationalState'] = df['operationalState'].apply(extract_bracket_content)

    return df

# Function to write Alarm DataFrame with count and headers formatting
def write_alarm_dataframe_with_format(df, sheet_name, writer):
    # Create a writer object for xlsxwriter
    workbook  = writer.book
    worksheet = workbook.add_worksheet(sheet_name)

    # Add the count row
    alarm_count = len(df)
    worksheet.write('A1', alarm_count)
    
    # Add the header row
    headers = ['NODENAME', 'Date', 'Time', 'Severity', 'Problem', 'Object', 'Cause', 'AdditionalText']
    df = df[headers]

    for col_num, header in enumerate(headers):
        worksheet.write(1, col_num, header)
    
    # Write the DataFrame data starting from the third row
    for row_num, row_data in enumerate(df.values.tolist(), start=2):
        for col_num, cell_data in enumerate(row_data):
            # Handle NaN values
            if pd.isna(cell_data):
                worksheet.write(row_num, col_num, '')  # Write an empty string for NaN values
            else:
                worksheet.write(row_num, col_num, cell_data)


### for summary Sheet
def write_summary(df, sheet_name, writer , cell_bef, cell_after):
    #####compare cell cek
    df_check_cell = count_df_by_nodename(cell_bef, cell_after , "Cell_COUNT")
    df_result = pd.merge(df, df_check_cell, on='NODENAME', how='left')
    
    df_result.to_excel(writer, sheet_name=sheet_name, index=False)
    
    workbook  = writer.book
    worksheet = writer.sheets[sheet_name]
    
    # Define formats
    header_format1 = workbook.add_format({'bold': True, 'bg_color': '#FFFF00', 'border': 1})
    header_format = workbook.add_format({'bold': True, 'bg_color': '#ffa383', 'border': 1})
    cell_format = workbook.add_format({'border': 1})
    
    # Apply formats
    for col_num, value in enumerate(df.columns.values):
        worksheet.write(0, col_num, value, header_format1)
    
    # Apply cell format to the entire table
    for row in range(1, len(df) + 1):
        print(f"write NODENAME [{df.iloc[row - 1, 0]}] [{row} of {len(df) + 1}]")
        for col in range(len(df.columns)):
            worksheet.write(row, col, df.iloc[row - 1, col], cell_format)    
    
    # Set column widths
    worksheet.set_column('A:A', 20)  # Column A width 35
    worksheet.set_column('B:B', 14)  # Column B width 25
    worksheet.set_column('C:C', 14)  # Column C width 25
    worksheet.set_column('D:D', 14)  # Column C width 25
    worksheet.set_column('E:E', 14)  # Column C width 25
          
    ########################################################
    ########################################################
    ########################################################
    ########################################################
    ########################################################
    
    
    # Define formats
    ##header_format1 = workbook.add_format({'bold': True, 'bg_color': '#FFFF00', 'border': 1})
    header_format = workbook.add_format({'bold': True, 'bg_color': '#FFFF00', 'border': 1})
    cell_format = workbook.add_format({'border': 1})
    
    # Data for summary table
    summary_data = {
        'State': [
            ('Total Cell Enable', '=COUNTIF(\'Cell Status\'!D:D,"(ENABLED)")', '=COUNTIF(\'Cell Status\'!F:F,"(ENABLED)")'),
            ('Total Cell Unlock', '=COUNTIF(\'Cell Status\'!C:C,"(UNLOCKED)")', '=COUNTIF(\'Cell Status\'!E:E,"(UNLOCKED)")'),
            ('Total Cell Lock', '=COUNTIF(\'Cell Status\'!C:C,"(LOCKED)")', '=COUNTIF(\'Cell Status\'!E:E,"(LOCKED)")'),
            ('Total Cell Disable', '=COUNTIF(\'Cell Status\'!D:D,"(DISABLED)")', '=COUNTIF(\'Cell Status\'!F:F,"(DISABLED)")'),
        ],
        'Alarm': [
            ('Alarm', '=Alarm_Before!A1', '=Alarm_After!A1')
        ],
        
        'OTHERS': [
            ('Can connect', '=COUNTIF(B:B,"OK")', '=COUNTIF(C:C,"OK")'),
            ('Can\'t Connect', '=COUNTIF(B:B,"Unremote")', '=COUNTIF(C:C,"Unremote")'),
            ('Successful','=COUNTIF(B:B,"OK")', '=COUNTIF(C:C,"OK")'),
            ('Rollback','=COUNTIF(B:B,"OK")', '=COUNTIF(C:C,"OK")'),
            ('Skip', '=COUNTIF(B:B,"OK")', '=COUNTIF(C:C,"OK")'),
        ]
    }


    # Write summary table
    row_num = 1
    start_column = 6+3
    
    ##format
    header_format = workbook.add_format({'bold': True, 'bg_color': '#ffa383', 'border': 1})
    header_format_1 = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#fea419', 'align': 'center', 'border': 1})
    header_format_2 = workbook.add_format({'bold': True, 'font_color': 'black', 'bg_color': '#b1b1b1', 'align': 'center', 'border': 1})
    
    # Write State section
    worksheet.write(0, start_column+0, 'Summary Cell Status',header_format_1 )
    worksheet.write(0, start_column+1, '',header_format_1 )
    worksheet.write(0, start_column+2, '',header_format_1 )
    worksheet.write(row_num, start_column+0, 'State', header_format)
    worksheet.write(row_num, start_column+1, 'Before', header_format)
    worksheet.write(row_num, start_column+2, 'After', header_format)
    row_num += 1
    for item, formula, formula2 in summary_data['State']:
        if re.search(r'(Unlock|Enable)', item, re.IGNORECASE):
            cell_format = workbook.add_format({'bold': False, 'font_color': '#030b6b', 'bg_color': '#fefd96', 'border': 1})
        else:
            cell_format = workbook.add_format({'bold': False, 'font_color': '#e72919', 'bg_color': '#fefd96', 'border': 1})
        worksheet.write(row_num, start_column+0, item, cell_format)
        worksheet.write_formula(row_num, start_column+1, formula, cell_format)
        worksheet.write_formula(row_num, start_column+2, formula2, cell_format)

        row_num += 1

    # Add a blank row
    ##row_num += 1
    
    # Write Alarm section
    worksheet.write(row_num, start_column+0, 'Alarm Status', header_format_2)
    worksheet.write(row_num, start_column+1, '',header_format_2 )
    worksheet.write(row_num, start_column+2, '',header_format_2 )    
    row_num += 1
    worksheet.write(row_num, start_column+0, 'State', header_format)
    worksheet.write(row_num, start_column+1, 'Before', header_format)
    worksheet.write(row_num, start_column+2, 'After', header_format)
    row_num += 1
    for item, formula, formula2 in summary_data['Alarm']:
        cell_format = workbook.add_format({'bold': False, 'font_color': '#e72919', 'bg_color': '#fefd96', 'border': 1})
        worksheet.write(row_num, start_column+0, item, cell_format)
        worksheet.write_formula(row_num, start_column+1, formula, cell_format)
        worksheet.write_formula(row_num, start_column+2, formula2, cell_format)
        row_num += 1
    
    ##others
    ##row_num += 1
    worksheet.write(row_num, start_column+0, '??? Sites', header_format)
    worksheet.write(row_num, start_column+1, 'Before', header_format)
    worksheet.write(row_num, start_column+2, 'After', header_format)
    
    row_num += 1
    for item, formula, formula2 in summary_data['OTHERS']:
        cell_format = workbook.add_format({'bold': True, 'border': 1})
        worksheet.write(row_num, start_column+0, item, cell_format)
        worksheet.write_formula(row_num, start_column+1, formula, cell_format)
        worksheet.write_formula(row_num, start_column+2, formula2, cell_format)
        row_num += 1
    
    

    # Set column widths
    worksheet.set_column(0,0, 20)  # Column A width 35
    worksheet.set_column(1,4, 14)  # Column B width 25
    
    worksheet.set_column(3+3,5+3, 3)  # Column C width 25    
    worksheet.set_column(6+3,6+3, 68)  # Column C width 25        
    worksheet.set_column(7+3,8+3, 14)  # Column C width 25   

    # Set zoom level
    worksheet.set_zoom(85)  # Adjust the zoom level as needed (e.g., 75% zoom)    
          
          
    


def compare_dataframes_with_check(df_before, df_after, col_lookup):
    # Make a copy to avoid modifying the original col_lookup
    ordered_columns = col_lookup.copy()

    # Ensure all col_lookup columns exist in both DataFrames
    missing_cols_before = [col for col in col_lookup if col not in df_before.columns]
    missing_cols_after = [col for col in col_lookup if col not in df_after.columns]

    if missing_cols_before or missing_cols_after:
        print("Missing columns:")
        if missing_cols_before:
            print(f" - In BEFORE: {missing_cols_before}")
        if missing_cols_after:
            print(f" - In AFTER: {missing_cols_after}")
        return pd.DataFrame()

    df_merged = pd.merge(df_before, df_after, on=col_lookup, how='outer', suffixes=('_Before', '_After'))

    # Remove unwanted rows
    if 'MO' in df_merged.columns:
        df_merged = df_merged[df_merged['MO'] != 'MO']

    for column in df_before.columns:
        if column not in col_lookup:
            col_before = f'{column}_Before'
            col_after = f'{column}_After'
            col_compare = f'{column}_Compare'

            if col_before not in df_merged.columns:
                df_merged[col_before] = None
            if col_after not in df_merged.columns:
                df_merged[col_after] = None

            df_merged[col_compare] = df_merged[col_before] == df_merged[col_after]

            ordered_columns.extend([col_before, col_after, col_compare])

    # Reorder the columns
    df_merged = df_merged[ordered_columns]

    return df_merged






def clean_dataframe(df):
    # Replace NaN and infinite values with None
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.fillna('NULL')  # Or use another placeholder
    return df







# Example usage
# df_before = pd.DataFrame(...)  # Your before dataframe
# df_after = pd.DataFrame(...)   # Your after dataframe
# df_result = compare_dataframes(df_before, df_after)
# print(df_result)




##########################
##########################
###  add count false value
##########################
##########################

def write_count_false(df, sheet_name, writer):
    # Get the xlsxwriter workbook and worksheet objects
    workbook  = writer.book
    #worksheet = writer.sheets[sheet_name]
    worksheet = workbook.add_worksheet(sheet_name)
    
    # Insert an empty row at the top (effectively shifting data down)
    worksheet.write_blank(0, 0, '', workbook.add_format())
    
    # Add the formula in the first row for each column
    for col_num, col in enumerate(df.columns, 0):
        if "Compare" in col:
            formula = f'=COUNTIF({chr(65+col_num)}3:{chr(65+col_num)}{len(df)+2}, FALSE)&"/"&COUNTIF({chr(65+col_num)}3:{chr(65+col_num)}{len(df)+2}, TRUE)'
            worksheet.write(0, col_num, formula)

    
    df.to_excel(writer, sheet_name=sheet_name, startrow=1, index=False)
    # Optionally set a column width for better visibility
    worksheet.set_column(0, len(df.columns), 18)








def count_df_by_nodename(df_before,df_after, col_name):
    col_before = f'{col_name}_Before'
    df_comp1 = df_before.groupby('NODENAME').size().reset_index(name=col_before)
    df_comp1[col_before] = 1

    col_after = f'{col_name}_After'
    df_comp2 = df_after.groupby('NODENAME').size().reset_index(name=col_after)
    df_comp2[col_after] = 1
    
    df_joined = pd.merge(df_comp1, df_comp2, on='NODENAME', how='outer')

    
    return df_joined



#############################################################
#############################################################
#############################################################
#############################################################
####  PROCESS KPI DATA COMPARE
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
# Get the absolute path of REF34 and add it to sys.path
script_dir = os.path.join(os.path.dirname(__file__), "00_LIB")
sys.path.append(script_dir)
counter_color = -1

# Now, import your script
import KPI  # assuming my_script.py exists inside 00_LIB

def reset_counter_color():
    global counter_color  # Ensure it modifies the global variable
    counter_color = -1

def random_color():
    """Returns a color from the predefined list, skipping the first two calls."""
    global counter_color
    counter_color += 1
    if counter_color < 2:
        return 'NOCOLOR'  # No color for the first two calls

    colors = [
        "#33ffce", "#f0ff00", "#fbdb26" , "#62c614",
        "#ff1700", "#00ff46"
    ]  # Add more valid colors
    ##return random.choice(colors(counter_color))
    index = (counter_color - 2) % len(colors)  # Ensure cycling through colors
    return colors[index]  # Select color by index    



                
def write_to_excel(df, df2, data_after, data_before, file_name):
    header_data = KPI.transform_headers(df)
    header_data_5G = KPI.transform_headers(df2)

    df = df.replace([np.inf, -np.inf], np.nan).fillna("")
    df2 = df2.replace([np.inf, -np.inf], np.nan).fillna("")                                                         
    
    with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
        workbook = writer.book
        

        ##pattern_loop = ("SleepState","Cell Status", "Alarm", "freqPrioListEUTRA")
        ##for key in data_after:
        for key in data_after:
            print(f"Processing [{key}]")
            if key == 'Alarm':
                if isinstance(data_before[key], pd.DataFrame):
                    write_alarm_dataframe_with_format(data_before[key].reset_index(drop=True), 'Alarm_Before', writer)
                if isinstance(data_after[key], pd.DataFrame):
                    write_alarm_dataframe_with_format(data_after[key].reset_index(drop=True), 'Alarm_After', writer)
            elif key == "Summary":
                df_diff = compare_dataframes(data_before[key], data_after[key]).drop(columns=['MO'])
                df_diff = clean_dataframe(df_diff)
                write_summary(df_diff, 'Summary', writer, data_before['Cell Status'],data_after['Cell Status'] )
            else:
                if isinstance(data_before[key], pd.DataFrame) and isinstance(data_after[key], pd.DataFrame):
                    col_lookup = ['NODENAME', 'MO', 'arfcnValueEUtranDl'] if key == 'freqPrioListEUTRA' else ['NODENAME', 'MO']
                    if key == 'Cell Status':
                        data_before[key] = clean_cell_status(data_before[key])
                        data_after[key] = clean_cell_status(data_after[key])
                        #####
                        ##count_df_by_nodename(df_before,df_after, col_name):
                        ##df_check_cell = count_df_by_nodename(data_before[key], data_after[key] , "Cell_COUNT")
                        ##write_count_false(df_check_cell, "Cell_COUNT", writer)
                        
                        
                        table_SleepState = "SleepState"
                        print(data_after[table_SleepState])
                        df_diff_sleepstate = compare_dataframes_with_check(data_before[table_SleepState], data_after[table_SleepState], col_lookup)
                        # Clean the "MO" column
                        df_diff_sleepstate["MO"] = df_diff_sleepstate["MO"].str.replace(r",CellSleepFunction=1", "", flags=re.IGNORECASE, regex=True)
                                                
                        
                        cell_status_diff = compare_dataframes_with_check(data_before[key], data_after[key], col_lookup)
                        merged_df = pd.merge(cell_status_diff, df_diff_sleepstate, on=col_lookup, how='left')
                        # Reorder the columns
                        ordered_columns = [
                            "NODENAME",
                            "MO",
                            "administrativeState_Before",
                            "operationalState_Before",
                            "administrativeState_After",
                            "operationalState_After",
                            "administrativeState_Compare",
                            "operationalState_Compare",
                            "sleepState_Before",
                            "sleepState_After",
                            "sleepState_Compare"
                        ]
                        
                        merged_df = merged_df[ordered_columns]                        
                        write_count_false(merged_df, key, writer)                        
                    
                    else:                        
                        df_diff = compare_dataframes_with_check(data_before[key], data_after[key], col_lookup)
                        write_count_false(df_diff, key, writer)


        # Process KPI LTE
        worksheet = workbook.add_worksheet("KPI_LTE")
        writer.sheets["KPI_LTE"] = worksheet
        write_kpi_data(worksheet, header_data, df, workbook)
        
        reset_counter_color()
        # Process KPI 5G
        worksheet_5G = workbook.add_worksheet("KPI_5G")
        writer.sheets["KPI_5G"] = worksheet_5G
        write_kpi_data(worksheet_5G, header_data_5G, df2, workbook)        
    
    print(f"Excel file saved: {file_name}")




def write_kpi_data(worksheet, header_data, df, workbook):
    merge_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'border': 1})
    color_map = {}
    color_map2 = {}
    
    for row_idx, row in enumerate(header_data):
        col_idx = 0
        if row_idx < 2:
            while col_idx < len(row):
                start_col = col_idx
                while col_idx + 1 < len(row) and row[col_idx + 1] == row[start_col]:
                    col_idx += 1
                worksheet.merge_range(row_idx, start_col, row_idx, col_idx, row[start_col], merge_format)
                if row_idx == 1:
                    if row[start_col] not in color_map2:
                        color_remark = random_color()
                        if color_remark == 'NOCOLOR':
                            color_map2[row[start_col]] = workbook.add_format()
                        else:
                            color_map2[row[start_col]] = workbook.add_format({'bg_color': color_remark})
                    for color_col in range(start_col, col_idx + 1):
                        worksheet.set_column(color_col, color_col, None, color_map2[row[start_col]])
                col_idx += 1
        else:
            worksheet.write_row(row_idx, 0, row)
    
    for row_idx, row in enumerate(df.values, start=3):
        worksheet.write_row(row_idx, 0, row)       
 





               










##########################################################################################################################
##########################################################################################################################
##########################################################################################################################
#############################################################
#############################################################
#############################################################
#############################################################
####  TOOLS GUI 
#############################################################
#############################################################
#############################################################
#############################################################
#############################################################
##########################################################################################################################
##########################################################################################################################
##########################################################################################################################



import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QDateEdit, QTimeEdit, QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QDate, QTime

class KPIGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CR Report Tools")
        self.setFixedSize(580, 280)

        self.folder_pairs = []

        layout = QVBoxLayout()

        ##### Folder select button
        ####self.btn_select_folders = QPushButton("Select Folders Containing 'Before' and 'After' [[IGNORE - NOT FUNCTION]]")
        ####self.btn_select_folders.clicked.connect(self.select_folders)
        ####layout.addWidget(self.btn_select_folders)

        # Date/time pickers
        self.date_before = QDateEdit(QDate.currentDate())
        self.time_before = QTimeEdit(QTime.currentTime())
        self.date_after = QDateEdit(QDate.currentDate())
        self.time_after = QTimeEdit(QTime.currentTime())

        for date_edit in [self.date_before, self.date_after]:
            date_edit.setCalendarPopup(True)
            date_edit.setDisplayFormat("yyyy-MM-dd")
        for time_edit in [self.time_before, self.time_after]:
            time_edit.setDisplayFormat("HH:mm")

        dt_layout = QVBoxLayout()

        before_layout = QHBoxLayout()
        before_layout.addWidget(QLabel("Before START Date:"))
        before_layout.addWidget(self.date_before)
        before_layout.addWidget(QLabel("Time:"))
        before_layout.addWidget(self.time_before)

        after_layout = QHBoxLayout()
        after_layout.addWidget(QLabel("After START Date:"))
        after_layout.addWidget(self.date_after)
        after_layout.addWidget(QLabel("Time:"))
        after_layout.addWidget(self.time_after)

        dt_layout.addLayout(before_layout)
        dt_layout.addLayout(after_layout)
        layout.addLayout(dt_layout)

        self.btn_process = QPushButton("Run Process")
        self.btn_process.clicked.connect(self.run_process)
        layout.addWidget(self.btn_process)

        self.setLayout(layout)

    def select_folders(self):
        # Create a QFileDialog for selecting multiple folders
        dialog = QFileDialog(self)
        dialog.setFileMode(QFileDialog.Directory)
        dialog.setOption(QFileDialog.ShowDirsOnly, True)
        
        # Enable multi-folder selection by using MultiSelection option correctly
        dialog.setOption(QFileDialog.DontUseNativeDialog, True)  # Avoid native dialog if needed

        # MultiSelection is enabled automatically in QFileDialog with Directory mode in PyQt5
        dialog.setFileMode(QFileDialog.Directory)  # Ensure directory mode is selected
        dialog.setOption(QFileDialog.ShowDirsOnly, True)  # Show only directories

        if dialog.exec_() == QFileDialog.Accepted:
            selected_folders = dialog.selectedFiles()
            before_dict = {}
            after_dict = {}

            # Sort the folders into "Before" and "After" categories
            for folder in selected_folders:
                folder_name = os.path.basename(folder)
                if "Before" in folder_name:
                    key = folder_name.replace("Before", "").strip("_- ")
                    before_dict[key.lower()] = folder
                elif "After" in folder_name:
                    key = folder_name.replace("After", "").strip("_- ")
                    after_dict[key.lower()] = folder

            self.folder_pairs.clear()

            # Ensure each 'Before' folder has a corresponding 'After' folder
            for key in before_dict:
                if key in after_dict:
                    self.folder_pairs.append((before_dict[key], after_dict[key]))

            if not self.folder_pairs:
                QMessageBox.warning(self, "No Valid Pairs", "No matching 'Before' and 'After' folder pairs found.")
            else:
                msg = "\n".join(
                    f"{i+1}. BEFORE: {b}\n   AFTER:  {a}"
                    for i, (b, a) in enumerate(self.folder_pairs)
                )
                QMessageBox.information(self, "Folder Pairs Found", msg)


    def run_process(self):
        ###if not self.folder_pairs:
        ###    QMessageBox.warning(self, "No Folder Pairs", "Please select valid folder pairs first.")
        ###    return

        BEFORE_TIME = f"{self.date_before.date().toString('yyyy-MM-dd')} {self.time_before.time().toString('HH:mm')}"
        AFTER_TIME = f"{self.date_after.date().toString('yyyy-MM-dd')} {self.time_after.time().toString('HH:mm')}"

        # Example of processing for each folder pair
        try:
            # Placeholder: add your KPI processing logic here
            # Example: process the 'Before' and 'After' folders with the selected datetime
            ###print(f"Processing {before_folder} with {before_datetime} and {after_folder} with {after_datetime}")

            # Your actual KPI logic goes here...
            # For example, loading files, extracting KPI data, etc.


            #############################################################
            #############################################################
            #############################################################
            #############################################################
            # Paths for the "Before" and "After" folders
            folder_before = "Before"
            folder_after = "After"



            # Process KPI 5G and KPI LTE logs for before and after folders
            #### define with NO_START or DATETIME


            KPI_5G_BEFORE = KPI.process_kpi_logs(folder_before, "GREP_KPI_5G",BEFORE_TIME)
            KPI_5G_AFTER = KPI.process_kpi_logs(folder_after, "GREP_KPI_5G",AFTER_TIME)
            KPI_LTE_BEFORE = KPI.process_kpi_logs(folder_before, "GREP_KPI_LTE",BEFORE_TIME)
            KPI_LTE_AFTER = KPI.process_kpi_logs(folder_after, "GREP_KPI_LTE",AFTER_TIME)

            ##KPI_5G_BEFORE = KPI.process_kpi_logs(folder_before, "GREP_KPI_5G","NO_START")
            ##KPI_5G_AFTER = KPI.process_kpi_logs(folder_after, "GREP_KPI_5G","NO_START")
            ##KPI_LTE_BEFORE = KPI.process_kpi_logs(folder_before, "GREP_KPI_LTE","NO_START")
            ##KPI_LTE_AFTER = KPI.process_kpi_logs(folder_after, "GREP_KPI_LTE","NO_START")

            compare_5G = KPI.create_main_merge_df(KPI_5G_BEFORE, KPI_5G_AFTER)
            compare_LTE = KPI.create_main_merge_df(KPI_LTE_BEFORE, KPI_LTE_AFTER)
            ##compare_LTE

            print(KPI_LTE_BEFORE)
            print(KPI_LTE_AFTER)

            #############################################################
            #############################################################
            #############################################################
            #############################################################
            ####  PROCESS LOG DATA COMPARE
            #############################################################
            #############################################################
            #############################################################
            #############################################################
            # Read files from both folders
            data_before = read_files_from_folder(folder_before)
            data_after = read_files_from_folder(folder_after)
                
            write_to_excel(compare_LTE,compare_5G, data_after, data_before,"01_Report_CR_activity.xlsx")	
                    
                

                

            QMessageBox.information(self, "Success", "All KPI processing completed.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KPIGUI()
    window.show()
    sys.exit(app.exec_())
