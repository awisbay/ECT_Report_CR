##########################################################################################################################################################################################   
#
#   Thailand TRUE - DTAC ECT Merge Co. Project    
#   Post Cutover CR Automation    
#   Prgram Requester                 ::   Andika Mulyawan
#   Program Developer                ::   RDC/COE - Avisek Mukherjee [eavmukh]
#   Program Executor                 ::   Ericsson SDU Team 
#   Tools Needed                     ::   Cygwin / Debian [ Windows Based Linux Subsystem] 
#                                    ::   Python 3.11
#                                    ::   Packages include : "Pandas" , "Openpyxl" , "Numpy"     
#    
#   Python Script/Tool Name          ::   "" IFLB_TrueENM_XXX.py  ""
#   Process                          ::
#       1. Create a Folder under C:\cygwin64\home\"signum"\  with name  " CR_AUTO_7 "  
#       2. Keep the Python script and CR Excel Input file for e.g. "08_CR882310ERIWWAN412_D_CMI0024_IFLB_TrueENM_20231005.xlsx " in the CR_AUTO_7 folder.
#       3. put the command "python  IFLB_TrueENM_XXX.py
#       4. Please enter your Ericsson signum  :                
#       5. Please Enter the name of the GUtrancellrelation_XXX_TRUE_ENM CR Excel including the .xlsx part   :
#       6. Please Enter the name of the CR Number  :       e.g. CR882310ENCASHI023
#
##########################################################################################################################################################################################


import pandas as pd
import os
import time
import sys
import time as today
import shutil
import numpy as np
from subprocess import STDOUT
import re
from collections import Counter


def generate_script(workdir_path=None, file_path=None, selected_file=None, output_dir=None):

    # signum = input("Please enter your Ericsson signum  :  ")
    # file_real_name = input("Please Enter the name of the IFLB_TrueENM_XXX CR Excel including the .xlsx part  :  ")
    # crn = input("Please Enter the name of the CR Number  :  ")
    # file_name = r"C:\cygwin64\home\{}\CR_AUTO_7\{}".format(signum, file_real_name)

    cr_code =  re.search(r"_(CR.*?)_", selected_file).group(1) if re.search(r"_(CR.*?)_", selected_file).group(1) else f"{selected_file}"
    cr_file_name_1 =  re.search(r"(\d+.*?)\.xlsx", selected_file).group(1) if re.search(r"(\d+.*?)\.xlsx", selected_file).group(1) else f"{selected_file}"
    cr_file_name = cr_file_name_1.replace("-", "_")    
    number_cr = re.search(r"(\d+)\_CR.*?$", selected_file).group(1)
    customer = re.search(r".*(True|DTAC).*?$", selected_file, re.IGNORECASE).group(1)
    crn = f"{number_cr}_" +cr_code[:8]
    ##crn = cr_code
    file_name =file_path
    print(selected_file, output_dir, file_name, crn, sep=" == ")
    # exit()

    ds = pd.read_excel(file_name, None)     ## ds - Reads the Whole File
    sheet_list = list(ds.keys())            ## Reads the sheet names and puts in the list 
    unique_node_values = []
    print(sheet_list)
    original_stdout = sys.stdout
    cwd = os.getcwd()

    site_list_array = []

    ##folder_name = crn +"_IFLB_"+ customer +"M_XXX"+ today.strftime('_%Y%m%d_%H%M%S')
    folder_name = cr_file_name
    new_dir = os.path.join( output_dir, folder_name)    
    # Check if the directory already exists
    if os.path.exists(new_dir):  # Check if the directory exists
        try:
            shutil.rmtree(new_dir)  # Remove the directory and its contents
            print(f"Directory '{new_dir}' removed successfully.")
        except OSError as error:
            print(f"Error removing directory '{new_dir}': {error}")
    else:
        print(f"Directory '{new_dir}' does not exist.")

    # Create the new directory
    os.mkdir(new_dir)
    os.chdir(new_dir) 


    # Fetches Enodeb name list for site_list file 
    dk = pd.read_excel(file_name, sheet_list[0])       ## ds - Reads a single first sheet
    column_names = list(dk.keys())
    enb_names = column_names[2]
    print(enb_names)

    #
    # with open( crn +'_sites_list.txt','w') as f :
    #     sys.stdout = f
    #     dk = dk.sort_values(enb_names)
    #     unique_node_count = dk[enb_names].nunique()
    #     unique_node_values = dk[enb_names].unique()
    #     for item in unique_node_values :
    #         print(item)

    # sys.stdout = original_stdout


    with open( 'command_mos.txt','w') as f :
        sys.stdout = f
        command = """
uv com_username=rbs
uv com_password=rbs


lt all


"""
        print(f"lcd  ~/PATH/{folder_name} \n")
        print(command)
        for item in sheet_list :
            item = item.replace(' ', '_')
            command_item = f"run  $nodename_{item}.mos"
            print(command_item)
        
        print(f"\ncvms {crn}_{today.strftime('%Y%m%d_%H%M%S')}")

    sys.stdout = original_stdout
    
    

    #######################################################################
    #######################################################################
    #######################################################################
    ##############  RE ASSIGN ARRAY to match prev codes
    #######################################################################
    #######################################################################
    #######################################################################
    sheet_list_rdel = [value for value in sheet_list if value not in [
'ADD_EUtranFreqRelation',
'ADD_UtranFrequency',
'ADD_UtranFreqRelation',
'ADD_ExternalENodeBFunction',
'ADD_ExternalEUtranCellTDD',
'ADD_ExternalEUtranCellFDD',
'ADD_ExtEUtranCellRelation',
'ADD_EUtrancellRelation',
'Parameter_Change'    
    ]]
    sheet_list = [value for value in sheet_list if value in ['ADD_EUtranFrequency',
'ADD_EUtranFreqRelation',
'ADD_UtranFrequency',
'ADD_UtranFreqRelation',
'ADD_ExternalENodeBFunction',
'ADD_ExternalEUtranCellTDD',
'ADD_ExternalEUtranCellFDD',
'ADD_ExtEUtranCellRelation',
'ADD_EUtrancellRelation',
'Parameter_Change'
    ]]
 
 
 
 
 
 
 
    #######################################################################
    #######################################################################
    for item in sheet_list_rdel :
    #######################################################################
    #######################################################################
    #######################################################################    
            if (item == "Disable ANR"):

        #######################################################################
        #######################################################################
        #######################################################################
        ###########################     Disable_ANR
        #######################################################################
        #######################################################################
        #######################################################################
        
        
                    sheet = item
                    df = pd.read_excel(io=file_name, sheet_name=sheet)
                    row_count = len(df)
                    column_count = len(df.columns)

                    column_names = list(df.keys())                         # takes column names from FA sheet
                    enb_names = column_names[2]
                    df = df.sort_values(enb_names)
                    enodebcounts = df[enb_names].value_counts()
                    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
                    #
                    print(df)
                    #
                    column_count = len(df.columns)
                    original_stdout = sys.stdout
                    unique_node_count = df[enb_names].nunique()
                    print(unique_node_count)
                    pointer = 0
                    #max_retries = 3
                    #retries = 0
                    for y in range (0,unique_node_count):
                        with open('Disable_ANR.mos', 'a') as f:
                            sys.stdout = f
                            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                            print(f" \nconfb+ \ngs+\n \n")
                            ecount=df.iloc[pointer,column_count-1]
                            prefix = df.iloc[pointer,2]
                            site_list_array.append(prefix)
                            for x in range(pointer,pointer+ecount) :
                                #print(f'''set {df.iloc[x,3]} {df.iloc[x,4]} {df.iloc[x,6]}  \n''')
                                print(f'''set {df.iloc[x,3]} {df.iloc[x,4]} 0  \n''')
                            pointer = pointer + ecount
                            print(f"\nconfb- \ngs-")
                            oldname = r"{}\{}\Disable_ANR.mos".format(output_dir, folder_name)
                            newname = r"{}\{}\{}_Disable_ANR.mos".format(output_dir, folder_name, prefix)
                        os.rename(oldname, newname)   
                        
                    sys.stdout = original_stdout # Reset the standard output to its original value


    
    #######################################################################
    #######################################################################
            if (item == "RDEL_ExternalEUtranCellFDD"):
        #######################################################################
        #######################################################################
        #######################################################################
        ###########################     RDEL_ExternalEUtranCellFDD
        #######################################################################
        #######################################################################
        #######################################################################
                    sheet = item
                    df = pd.read_excel(io=file_name, sheet_name=sheet)
                    row_count = len(df)
                    column_count = len(df.columns)

                    column_names = list(df.keys())                         # takes column names from FA sheet
                    enb_names = column_names[2]
                    df = df.sort_values(enb_names)
                    enodebcounts = df[enb_names].value_counts()
                    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
                    #
                    print(df)
                    #
                    column_count = len(df.columns)
                    original_stdout = sys.stdout
                    unique_node_count = df[enb_names].nunique()
                    print(unique_node_count)
                    pointer = 0
                    #max_retries = 3
                    #retries = 0
                    for y in range (0,unique_node_count):
                        with open('RDEL_ExternalEUtranCellFDD.mos', 'a') as f:
                            sys.stdout = f
                            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                            print(f" \nconfbd+ \ngs+\n \n")
                            ecount=df.iloc[pointer,column_count-1]
                            prefix = df.iloc[pointer,2]
                            site_list_array.append(prefix)
                            for x in range(pointer,pointer+ecount) :
                                print(f'''rdel ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,3]},ExternalEUtranCellFDD={df.iloc[x,4]}  \n''')
                            pointer = pointer + ecount
                            print(f"\nconfbd- \ngs-")
                            oldname = r"{}\{}\RDEL_ExternalEUtranCellFDD.mos".format(output_dir, folder_name)
                            newname = r"{}\{}\{}_RDEL_ExternalEUtranCellFDD.mos".format(output_dir, folder_name, prefix)
                        os.rename(oldname, newname)   
                        
                    sys.stdout = original_stdout # Reset the standard output to its original value
    #######################################################################
    #######################################################################
            if (item == "RDEL_ExternalEUtranCellTDD"):
        #######################################################################
        #######################################################################
        #######################################################################
        ###########################     RDEL_ExternalEUtranCellTDD
        #######################################################################
        #######################################################################
        #######################################################################
                    sheet = item
                    df = pd.read_excel(io=file_name, sheet_name=sheet)
                    row_count = len(df)
                    column_count = len(df.columns)

                    column_names = list(df.keys())                         # takes column names from FA sheet
                    enb_names = column_names[2]
                    df = df.sort_values(enb_names)
                    enodebcounts = df[enb_names].value_counts()
                    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
                    #
                    print(df)
                    #
                    column_count = len(df.columns)
                    original_stdout = sys.stdout
                    unique_node_count = df[enb_names].nunique()
                    print(unique_node_count)
                    pointer = 0
                    #max_retries = 3
                    #retries = 0
                    for y in range (0,unique_node_count):
                        with open('RDEL_ExternalEUtranCellTDD.mos', 'a') as f:
                            sys.stdout = f
                            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                            print(f" \nconfbd+ \ngs+\n \n")
                            ecount=df.iloc[pointer,column_count-1]
                            prefix = df.iloc[pointer,2]
                            site_list_array.append(prefix)
                            for x in range(pointer,pointer+ecount) :
                                print(f'''rdel ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,3]},ExternalEUtranCellTDD={df.iloc[x,4]}  \n''')
                            pointer = pointer + ecount
                            print(f"\nconfbd- \ngs-")
                            oldname = r"{}\{}\RDEL_ExternalEUtranCellTDD.mos".format(output_dir, folder_name)
                            newname = r"{}\{}\{}_RDEL_ExternalEUtranCellTDD.mos".format(output_dir, folder_name, prefix)
                        os.rename(oldname, newname)   
                        
                    sys.stdout = original_stdout # Reset the standard output to its original value
    #######################################################################
    #######################################################################

        #############################################
        #############################################
        ########################### DEL_EUtrancellRelation  
        #############################################
        #############################################
            if (item.upper() == "DEL_EUtrancellRelation".upper()):            
                sheet = item 
                df = pd.read_excel(io=file_name, sheet_name=sheet)
                row_count = len(df)
                column_count = len(df.columns)

                column_names = list(df.keys())                         # takes column names from FA sheet
                enb_names = column_names[2]
                df = df.sort_values(enb_names)
                enodebcounts = df[enb_names].value_counts()
                df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
                #
                print(df)
                #
                column_count = len(df.columns)
                original_stdout = sys.stdout
                unique_node_count = df[enb_names].nunique()
                print(unique_node_count)
                pointer = 0
                df.columns = df.columns.str.upper()
                for y in range (0,unique_node_count):
                    with open(sheet + '.mos', 'w') as f:
                        sys.stdout = f
                        print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                        print(f" \nconfb+ \ngs+\n \n")
                        ecount=df.iloc[pointer,column_count-1]
                        prefix = df.iloc[pointer,2]
                        site_list_array.append(prefix)
                        for x in range(pointer,pointer+ecount) :
                            print(f'''del {df.iloc[x,df.columns.tolist().index("EUtranCell".upper())]},EUtranFreqRelation={df.iloc[x,df.columns.tolist().index("EUtranFreqRelation".upper())]},EUtranCellRelation={df.iloc[x,df.columns.tolist().index("EUtranCellRelation".upper())]}  \n''')
                        pointer = pointer + ecount
                        print(f"\nconfb- \ngs-")
                        oldname = r"{}\{}\{}.mos".format(output_dir, folder_name,sheet)
                        newname = r"{}\{}\{}_{}.mos".format(output_dir, folder_name, prefix,sheet)
                    os.rename(oldname, newname)
                    
                sys.stdout = original_stdout # Reset the standard output to its original value
                #############################################
                #############################################
    
            if (item == "Enable ANR"):

        #######################################################################
        #######################################################################
        #######################################################################
        ###########################     Enable_ANR
        #######################################################################
        #######################################################################
        #######################################################################
        
        
                    sheet = item
                    df = pd.read_excel(io=file_name, sheet_name=sheet)
                    row_count = len(df)
                    column_count = len(df.columns)

                    column_names = list(df.keys())                         # takes column names from FA sheet
                    enb_names = column_names[2]
                    df = df.sort_values(enb_names)
                    enodebcounts = df[enb_names].value_counts()
                    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
                    #
                    print(df)
                    #
                    column_count = len(df.columns)
                    original_stdout = sys.stdout
                    unique_node_count = df[enb_names].nunique()
                    print(unique_node_count)
                    pointer = 0
                    #max_retries = 3
                    #retries = 0
                    for y in range (0,unique_node_count):
                        with open('Enable_ANR.mos', 'a') as f:
                            sys.stdout = f
                            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                            print(f" \nconfb+ \ngs+\n \n")
                            ecount=df.iloc[pointer,column_count-1]
                            prefix = df.iloc[pointer,2]
                            site_list_array.append(prefix)
                            for x in range(pointer,pointer+ecount) :
                                #print(f'''set {df.iloc[x,3]} {df.iloc[x,4]} {df.iloc[x,6]}  \n''')
                                print(f'''set {df.iloc[x,3]} {df.iloc[x,4]} 1  \n''')
                            pointer = pointer + ecount
                            print(f"\nconfb- \ngs-")
                            oldname = r"{}\{}\Enable_ANR.mos".format(output_dir, folder_name)
                            newname = r"{}\{}\{}_Enable_ANR.mos".format(output_dir, folder_name, prefix)
                        os.rename(oldname, newname)   
                        
                    sys.stdout = original_stdout # Reset the standard output to its original value


    
    #######################################################################
    #######################################################################  
 
 
              
 
 
 
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################    

    ###########################     ADD_EUtranFrequency

    sheet = sheet_list[0] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
    row_count = len(df)
    column_count = len(df.columns)

    column_names = list(df.keys())                         # takes column names from FA sheet
    enb_names = column_names[2]
    df = df.sort_values(enb_names)
    enodebcounts = df[enb_names].value_counts()
    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
    #
    print(df)
    #
    column_count = len(df.columns)
    original_stdout = sys.stdout
    unique_node_count = df[enb_names].nunique()
    print(unique_node_count)
    pointer = 0
    #max_retries = 3
    #retries = 0
    for y in range (0,unique_node_count):
        with open('ADD_EUtranFrequency.mos', 'a') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f" \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,2]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                print(f'''crn ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency={df.iloc[x,3]}  \narfcnValueEUtranDl  {df.iloc[x,3]} \nuserLabel {df.iloc[x,3]} \nend \n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_EUtranFrequency.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_EUtranFrequency.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
    #while retries < max_retries:
    #    try:
    #        os.rename(oldname, newname)
    #        print("File renamed successfully.")
    #        break
    #    except PermissionError:
    #        print("PermissionError: File is in use. Retrying in 2 seconds...")
    #        time.sleep(2)
    #        retries += 1
    #
    #if retries >= max_retries:
    #    print("Unable to rename the file after multiple retries.")
            
        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=100
    #arfcnValueEUtranDl 100
    #userLabel 100
    #end
    ### ADD_EUtranFreqRelation

    sheet = sheet_list[1] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
    row_count = len(df)
    column_count = len(df.columns)

    column_names = list(df.keys())                         # takes column names from FA sheet
    enb_names = column_names[2]
    df = df.sort_values(enb_names)
    enodebcounts = df[enb_names].value_counts()
    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
    #
    print(df)
    #
    column_count = len(df.columns)
    original_stdout = sys.stdout
    unique_node_count = df[enb_names].nunique()
    print(unique_node_count)
    pointer = 0
    for y in range (0,unique_node_count):
        with open('ADD_EUtranFreqRelation.mos', 'a') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f" \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,2]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                if "L23" in df.iloc[x,3]:
                    TIPE = "TDD"
                else:
                    TIPE = "FDD"
                print(f'''crn ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,4]} \namoAllowed  {df.iloc[x,5]} \ncellReselectionPriority {df.iloc[x,6]} \neutranFreqToQciProfileRelation {df.iloc[x,6]} \neutranFrequencyRef {df.iloc[x,9]} \nmdtMeasOn {df.iloc[x,10]}  \ninterFreqMeasType 0  \nqRxLevMin {df.iloc[x,11]} \nthreshXHigh {df.iloc[x,13]}  \nthreshXLow {df.iloc[x,12]} \nvoicePrio {df.iloc[x,8]}\nconnectedModeMobilityPrio {df.iloc[x,7]} ''')
                print(f'''end \n ''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_EUtranFreqRelation.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_EUtranFreqRelation.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        #while retries < max_retries:
        #    try:
        #        os.rename(oldname, newname)
        #        print("File renamed successfully.")
        #        break
        #    except PermissionError:
        #        print("PermissionError: File is in use. Retrying in 2 seconds...")
        #        time.sleep(5)
        #        retries += 1
        #
        #if retries >= max_retries:
        #    print("Unable to rename the file after multiple retries.")

        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn ENodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100
    #amoAllowed False
    #cellReselectionPriority 5
    #eutranFreqToQciProfileRelation lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,a5Thr1RsrpFreqQciOffset=6,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=2,a5Thr2RsrqFreqQciOffset=0;lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,a5Thr1RsrpFreqQciOffset=6,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=2,a5Thr2RsrqFreqQciOffset=0;lbQciProfileHandling=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3,lbA5Threshold2RsrpOffset=8,lbA5Threshold2RsrqOffset=0,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=-2,a5Thr2RsrqFreqQciOffset=0;lbQciProfileHandling=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4,lbA5Threshold2RsrpOffset=8,lbA5Threshold2RsrqOffset=0,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=-2,a5Thr2RsrqFreqQciOffset=0;lbQciProfileHandling=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5,lbA5Threshold2RsrpOffset=8,lbA5Threshold2RsrqOffset=0,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=-2,a5Thr2RsrqFreqQciOffset=0;lbQciProfileHandling=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6,lbA5Threshold2RsrpOffset=8,lbA5Threshold2RsrqOffset=0,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=-2,a5Thr2RsrqFreqQciOffset=0;lbQciProfileHandling=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7,lbA5Threshold2RsrpOffset=8,lbA5Threshold2RsrqOffset=0,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=-2,a5Thr2RsrqFreqQciOffset=0;lbQciProfileHandling=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8,lbA5Threshold2RsrpOffset=8,lbA5Threshold2RsrqOffset=0,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=-2,a5Thr2RsrqFreqQciOffset=0;lbQciProfileHandling=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9,lbA5Threshold2RsrpOffset=8,lbA5Threshold2RsrqOffset=0,a5Thr1RsrpFreqQciOffset=0,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrpFreqQciOffset=-2,a5Thr2RsrqFreqQciOffset=0
    #eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=100
    #mdtMeasOn False
    #interFreqMeasType 0
    #qRxLevMin -124
    #threshXHigh 16
    #threshXLow 0
    #voicePrio 5
    #connectedModeMobilityPrio 5
    #end

    #################################### ADD_UtranFrequency

    sheet = sheet_list[2] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
    row_count = len(df)
    column_count = len(df.columns)

    column_names = list(df.keys())                         # takes column names from FA sheet
    enb_names = column_names[2]
    df = df.sort_values(enb_names)
    enodebcounts = df[enb_names].value_counts()
    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
    #
    print(df)
    #
    column_count = len(df.columns)
    original_stdout = sys.stdout
    unique_node_count = df[enb_names].nunique()
    print(unique_node_count)
    pointer = 0
    for y in range (0,unique_node_count):
        with open('ADD_UtranFrequency.mos', 'a') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f" \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,2]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) : 
                print(f'''crn ENodeBFunction=1,UtraNetwork=1,UtranFrequency={df.iloc[x,3]}   \narfcnValueUtranDl  {df.iloc[x,3]} \nuserLabel {df.iloc[x,3]} \nend \n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_UtranFrequency.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_UtranFrequency.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        #while retries < max_retries:
        #    try:
        #        os.rename(oldname, newname)
        #        print("File renamed successfully.")
        #        break
        #    except PermissionError:
        #        print("PermissionError: File is in use. Retrying in 2 seconds...")
        #        time.sleep(5)
        #        retries += 1
        #
        #if retries >= max_retries:
        #    print("Unable to rename the file after multiple retries.")
        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn ENodeBFunction=1,UtraNetwork=1,UtranFrequency=2987
    #arfcnValueUtranDl 2987
    #userLabel 2987
    #end


    ## ADD_UtranFreqRelation

    sheet = sheet_list[3] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
    row_count = len(df)
    column_count = len(df.columns)

    column_names = list(df.keys())                         # takes column names from FA sheet
    enb_names = column_names[2]
    df = df.sort_values(enb_names)
    enodebcounts = df[enb_names].value_counts()
    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
    #
    print(df)
    #
    column_count = len(df.columns)
    original_stdout = sys.stdout
    unique_node_count = df[enb_names].nunique()
    print(unique_node_count)
    pointer = 0
    for y in range (0,unique_node_count):
        with open('ADD_UtranFreqRelation.mos', 'a') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f" \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,2]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                if "L23" in df.iloc[x,3]:
                    TIPE = "TDD"
                else:
                    TIPE = "FDD"            
                print(f'''crn ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,3]},UtranFreqRelation={df.iloc[x,4]} \ncellReselectionPriority {df.iloc[x,6]} \nconnectedModeMobilityPrio {df.iloc[x,7]}  \ncsFallbackPrio  {df.iloc[x,8]}  \nmobilityActionCsfb {df.iloc[x,9]}\nqRxLevMin {df.iloc[x,11]} \nthreshXHigh {df.iloc[x,12]}\nthreshXLow {df.iloc[x,13]}\nutranFrequencyRef UtraNetwork=1,UtranFrequency={df.iloc[x,4]} \nvoicePrio  {df.iloc[x,10]}\nend \n''')           
                print(f'''SET ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,3]},UtranFreqRelation={df.iloc[x,4]}$ cellReselectionPriority {df.iloc[x,6]}''')
                print(f'''SET ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,3]},UtranFreqRelation={df.iloc[x,4]}$ connectedModeMobilityPrio {df.iloc[x,7]}''')
                print(f'''SET ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,3]},UtranFreqRelation={df.iloc[x,4]}$ csFallbackPrio {df.iloc[x,8]}''')
                print(f'''SET ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,3]},UtranFreqRelation={df.iloc[x,4]}$ qRxLevMin {df.iloc[x,11]}''')
                print(f'''SET ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,3]},UtranFreqRelation={df.iloc[x,4]}$ threshXHigh {df.iloc[x,12]}''')
                print(f'''SET ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,3]},UtranFreqRelation={df.iloc[x,4]}$ threshXLow {df.iloc[x,13]}''')
                print(f'''SET ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,3]},UtranFreqRelation={df.iloc[x,4]}$ mobilityActionCsfb {df.iloc[x,9]} \n''')        
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_UtranFreqRelation.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_UtranFreqRelation.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        #while retries < max_retries:
        #    try:
        #        os.rename(oldname, newname)
        #        print("File renamed successfully.")
        #        break
        #    except PermissionError:
        #        print("PermissionError: File is in use. Retrying in 2 seconds...")
        #        time.sleep(5)
        #        retries += 1
        #
        #if retries >= max_retries:
        #    print("Unable to rename the file after multiple retries.")

        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn ENodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,UtranFreqRelation=2987
    #cellReselectionPriority 1
    #connectedModeMobilityPrio 1
    #csFallbackPrio 1
    #mobilityActionCsfb 0
    #qRxLevMin -115
    #threshXHigh 14
    #threshXLow 14
    #utranFrequencyRef UtraNetwork=1,UtranFrequency=2987
    #voicePrio 1
    #end
    #
    #set NodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,UtranFreqRelation=2987 cellReselectionPriority 1
    #set NodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,UtranFreqRelation=2987 connectedModeMobilityPrio 1
    #set NodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,UtranFreqRelation=2987 csFallbackPrio 1
    #set NodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,UtranFreqRelation=2987 mobilityActionCsfb 0
    #set NodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,UtranFreqRelation=2987 qRxLevMin -115
    #set NodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,UtranFreqRelation=2987 threshXHigh 14
    #set NodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,UtranFreqRelation=2987 threshXLow 14
    #set NodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,UtranFreqRelation=2987 voicePrio 1


    ## ADD_ExternalENodeBFunction

    sheet = sheet_list[4] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
    row_count = len(df)
    column_count = len(df.columns)

    column_names = list(df.keys())                         # takes column names from FA sheet
    enb_names = column_names[2]
    df = df.sort_values(enb_names)
    enodebcounts = df[enb_names].value_counts()
    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
    #
    print(df)
    #
    column_count = len(df.columns)
    original_stdout = sys.stdout
    unique_node_count = df[enb_names].nunique()
    print(unique_node_count)
    pointer = 0
    for y in range (0,unique_node_count):
        with open('ADD_ExternalENodeBFunction.mos', 'a') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f" \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,2]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
###                print(f'''crn ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,3]}
###    eNBId {df.iloc[x,4]}
###    eNodeBPlmnId mcc=520,mnc={df.iloc[x,5]},mncLength=2
###    eSCellCapacityScaling 100
###    eranLinkMaxRttDelay 60
###    eranPrioritizationDisabled false
###    eranUlCompVlanPortRef
###    eranVlanPortRef
###    interENodeBCAInteractionMode 2
###    masterEnbFunctionId
###    mfbiSupport false
###    ulTrigHoSupport 0
###    userLabel {df.iloc[x,6]}
###    zzzTemporary1 -2000000000
###    zzzTemporary2 -2000000000
###    zzzTemporary3
###    zzzTemporary4 -2000000000
###    zzzTemporary5 -2000000000
###    zzzTemporary6 -2000000000
###    zzzTemporary7 -2000000000
###    zzzTemporary8 -2000000000
###    zzzTemporary9 -2000000000
###    end  
###                \n ''')
                print(f'''crn ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,3]}
    eNBId {df.iloc[x,4]}
    eNodeBPlmnId mcc=520,mnc={df.iloc[x,5]},mncLength=2
    eSCellCapacityScaling 100
    eranLinkMaxRttDelay 60
    eranPrioritizationDisabled false
    eranUlCompVlanPortRef
    eranVlanPortRef
    masterEnbFunctionId
    mfbiSupport false
    ulTrigHoSupport 0
    userLabel {df.iloc[x,6]}
    zzzTemporary2 -2000000000
    zzzTemporary3 -2000000000
    zzzTemporary4 -2000000000
    zzzTemporary5 -2000000000
    zzzTemporary6 -2000000000
    zzzTemporary7 -2000000000
    zzzTemporary8 -2000000000
    zzzTemporary9 -2000000000
    end  
                \n ''')
                
                print(f'''crn ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,3]},TermPointToENB={df.iloc[x,3]}
    administrativeState 1
    domainName
    ipAddress 0.0.0.0
    ipv6Address ::
    end
                \n ''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_ExternalENodeBFunction.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_ExternalENodeBFunction.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction=5205-58412
    #eNBId 58412
    #eNodeBPlmnId mcc=520,mnc=5,mncLength=2
    #eSCellCapacityScaling 100
    #eranLinkMaxRttDelay 60
    #eranPrioritizationDisabled false
    #eranUlCompVlanPortRef
    #eranVlanPortRef
    #interENodeBCAInteractionMode 2
    #masterEnbFunctionId
    #mfbiSupport false
    #ulTrigHoSupport 0
    #userLabel CMI0024X_2NB06
    #zzzTemporary1 -2000000000
    #zzzTemporary2 -2000000000
    #zzzTemporary3
    #zzzTemporary4 -2000000000
    #zzzTemporary5 -2000000000
    #zzzTemporary6 -2000000000
    #zzzTemporary7 -2000000000
    #zzzTemporary8 -2000000000
    #zzzTemporary9 -2000000000
    #end
    #
    #crn ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction=5205-58412,TermPointToENB=5205-58412
    #administrativeState 1
    #domainName
    #ipAddress 0.0.0.0
    #ipv6Address ::
    #end

    ## ADD_ExternalEUtranCellTDD

    sheet = sheet_list[5] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
    row_count = len(df)
    column_count = len(df.columns)

    column_names = list(df.keys())                         # takes column names from FA sheet
    enb_names = column_names[2]
    df = df.sort_values(enb_names)
    enodebcounts = df[enb_names].value_counts()
    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
    #
    print(df)
    #
    column_count = len(df.columns)
    original_stdout = sys.stdout
    unique_node_count = df[enb_names].nunique()
    print(unique_node_count)
    pointer = 0
    for y in range (0,unique_node_count):
        with open('ADD_ExternalEUtranCellTDD.mos', 'a') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f" \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,2]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                #print(f'''crn ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,3]},ExternalEUtranCellTDD={df.iloc[x,4]}
#activePlmnList mcc=520,mnc={df.iloc[x,5]},mncLength=2
#activeServiceAreaId
#endcAllowedPlmnList
#eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency={df.iloc[x,6]}
#isRemoveAllowed {df.iloc[x,11]}
#lbEUtranCellOffloadCapacity 1000
#localCellId {df.iloc[x,7]}
#masterEUtranCellFDDId
#noOfTxAntennas 2
#pciConflict
#pciConflictCell
#pciDetectingCell
#physicalLayerCellIdGroup {df.iloc[x,8]}
#physicalLayerSubCellId {df.iloc[x,9]}
#tac {df.iloc[x,10]}
#userLabel {df.iloc[x,13]}
#zzzTemporaryExt1 -2000000000
#zzzTemporaryExt2 -2000000000
#zzzTemporaryExt3 -2000000000
#zzzTemporaryExt4 -2000000000
#zzzTemporaryExt5 -2000000000
#end
#                \n ''')

                print(f'''crn ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,3]},ExternalEUtranCellTDD={df.iloc[x,4]}
activePlmnList mcc=520,mnc={df.iloc[x,5]},mncLength=2
activeServiceAreaId
endcAllowedPlmnList
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency={df.iloc[x,6]}
isRemoveAllowed {df.iloc[x,11]}
lbEUtranCellOffloadCapacity 1000
localCellId {df.iloc[x,7]}
pciConflict
pciConflictCell
pciDetectingCell
physicalLayerCellIdGroup {df.iloc[x,8]}
physicalLayerSubCellId {df.iloc[x,9]}
tac {df.iloc[x,10]}
userLabel {df.iloc[x,13]}
end
                \n ''')                
                print(f'''set ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,3]},ExternalEUtranCellTDD={df.iloc[x,4]}$ isRemoveAllowed {df.iloc[x,11]}
                \n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_ExternalEUtranCellTDD.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_ExternalEUtranCellTDD.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)

        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction=5205-58412,ExternalEUtranCellFDD=CMI0024E_2NB06_S01
    #activePlmnList mcc=520,mnc=5,mncLength=2
    #activeServiceAreaId
    #endcAllowedPlmnList
    #eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=100
    #isRemoveAllowed False
    #lbEUtranCellOffloadCapacity 1000
    #localCellId 16
    #masterEUtranCellFDDId
    #noOfTxAntennas 2
    #pciConflict
    #pciConflictCell
    #pciDetectingCell
    #physicalLayerCellIdGroup 85
    #physicalLayerSubCellId 1
    #tac 504
    #userLabel
    #zzzTemporaryExt1 -2000000000
    #zzzTemporaryExt2 -2000000000
    #zzzTemporaryExt3 -2000000000
    #zzzTemporaryExt4 -2000000000
    #zzzTemporaryExt5 -2000000000
    #end
    #set ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction=5205-58412,ExternalEUtranCellFDD=CMI0024E_2NB06_S01$ isRemoveAllowed False


    ## ADD_ExternalEUtranCellFDD

    sheet = sheet_list[6] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
    row_count = len(df)
    column_count = len(df.columns)

    column_names = list(df.keys())                         # takes column names from FA sheet
    enb_names = column_names[2]
    df = df.sort_values(enb_names)
    enodebcounts = df[enb_names].value_counts()
    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
    #
    print(df)
    #
    column_count = len(df.columns)
    original_stdout = sys.stdout
    unique_node_count = df[enb_names].nunique()
    print(unique_node_count)
    pointer = 0
    for y in range (0,unique_node_count):
        with open('ADD_ExternalEUtranCellFDD.mos', 'a') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f" \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,2]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                ##activePlmnList mcc=520,mnc={df.iloc[x,5]},mncLength=2
                print(f'''crn ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,3]},ExternalEUtranCellFDD={df.iloc[x,4]}
activePlmnList {df.iloc[x,5]}
activeServiceAreaId
endcAllowedPlmnList
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency={df.iloc[x,6]}
isRemoveAllowed {df.iloc[x,11]}
lbEUtranCellOffloadCapacity 1000
localCellId {df.iloc[x,7]}
masterEUtranCellFDDId
noOfTxAntennas 2
pciConflict
pciConflictCell
pciDetectingCell
physicalLayerCellIdGroup {df.iloc[x,8]}
physicalLayerSubCellId {df.iloc[x,9]}
tac {df.iloc[x,10]}
userLabel {df.iloc[x,13]}
zzzTemporaryExt1 -2000000000
zzzTemporaryExt2 -2000000000
zzzTemporaryExt3 -2000000000
zzzTemporaryExt4 -2000000000
zzzTemporaryExt5 -2000000000
end
                \n ''')
                print(f'''set ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,3]},ExternalEUtranCellFDD={df.iloc[x,4]}$ isRemoveAllowed {df.iloc[x,11]}  \n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_ExternalEUtranCellFDD.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_ExternalEUtranCellFDD.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction=5205-58412,ExternalEUtranCellFDD=CMI0024E_2NB06_S01
    #activePlmnList mcc=520,mnc=5,mncLength=2
    #activeServiceAreaId
    #endcAllowedPlmnList
    #eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=100
    #isRemoveAllowed False
    #lbEUtranCellOffloadCapacity 1000
    #localCellId 16
    #masterEUtranCellFDDId
    #noOfTxAntennas 2
    #pciConflict
    #pciConflictCell
    #pciDetectingCell
    #physicalLayerCellIdGroup 85
    #physicalLayerSubCellId 1
    #tac 504
    #userLabel
    #zzzTemporaryExt1 -2000000000
    #zzzTemporaryExt2 -2000000000
    #zzzTemporaryExt3 -2000000000
    #zzzTemporaryExt4 -2000000000
    #zzzTemporaryExt5 -2000000000
    #end
    #set ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction=5205-58412,ExternalEUtranCellFDD=CMI0024E_2NB06_S01$ isRemoveAllowed False

    ## ADD_ExtEUtranCellRelation

    sheet = sheet_list[7] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
    row_count = len(df)
    column_count = len(df.columns)

    column_names = list(df.keys())                         # takes column names from FA sheet
    enb_names = column_names[2]
    df = df.sort_values(enb_names)
    enodebcounts = df[enb_names].value_counts()
    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
    #
    print(df)
    #
    column_count = len(df.columns)
    original_stdout = sys.stdout
    unique_node_count = df[enb_names].nunique()
    print(unique_node_count)
    pointer = 0
    for y in range (0,unique_node_count):
        with open('ADD_ExtEUtranCellRelation.mos', 'a') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f" \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,2]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                if "L23" in df.iloc[x,3]:
                    TIPE = "TDD"
                else:
                    TIPE = "FDD" 
                if "L23" in df.iloc[x,5]:
                    TIPE2 = "TDD"
                else:
                    TIPE2 = "FDD"                      
                print(f'''crn ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}
    amoAllowed true
    asmSCellDlOnlyAllowed 1
    cellIndividualOffsetEUtran 0
    cellIndividualOffsetEUtranQci1 0
    coverageIndicator {df.iloc[x,11]}
    crsAssistanceInfoPriority 0
    eranUlCompCoopCellAllowed true
    ieNBUlCompCoopCellAllowed true
    includeInSystemInformation true
    isHoAllowed {df.iloc[x,8]}
    isRemoveAllowed {df.iloc[x,9]}
    lbBnrAllowed true
    lbCovIndicated false
    loadBalancing {df.iloc[x,10]}
    neighborCellRef ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction={df.iloc[x,4]},ExternalEUtranCell{TIPE2}={df.iloc[x,5]}
    qOffsetCellEUtran 0
    reportDlActivity 1
    sCellCandidate {df.iloc[x,12]}
    sCellPriority 7
    sleepModeCovCellCandidate 2
    zzzTemporary1 -2000000000
    zzzTemporary2 -2000000000
    zzzTemporary3
    end
                \n ''')
                print(f'''set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}$ coverageIndicator {df.iloc[x,11]} ''')
                print(f'''set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}$ isHoAllowed {df.iloc[x,8]} ''')
                print(f'''set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}$ isRemoveAllowed {df.iloc[x,9]} ''')
                print(f'''set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}$ loadBalancing {df.iloc[x,10]} ''')
                print(f'''set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}$ sCellCandidate {df.iloc[x,12]} \n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_ExtEUtranCellRelation.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_ExtEUtranCellRelation.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
    
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn ENodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01
    #amoAllowed true
    #asmSCellDlOnlyAllowed 1
    #cellIndividualOffsetEUtran 0
    #cellIndividualOffsetEUtranQci1 0
    #coverageIndicator 1
    #crsAssistanceInfoPriority 0
    #eranUlCompCoopCellAllowed true
    #ieNBUlCompCoopCellAllowed true
    #includeInSystemInformation true
    #isHoAllowed True
    #isRemoveAllowed False
    #lbBnrAllowed true
    #lbCovIndicated false
    #loadBalancing 1
    #neighborCellRef ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction=5205-58412,ExternalEUtranCellFDD=CMI0024E_2NB06_S01
    #qOffsetCellEUtran 0
    #reportDlActivity 1
    #sCellCandidate 1
    #sCellPriority 7
    #sleepModeCovCellCandidate 2
    #zzzTemporary1 -2000000000
    #zzzTemporary2 -2000000000
    #zzzTemporary3
    #end
    #
    #set EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01$ coverageIndicator 1
    #set EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01$ isHoAllowed True
    #set EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01$ isRemoveAllowed False
    #set EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01$ loadBalancing 1
    #set EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01$ sCellCandidate 1

    ## ADD_EUtrancellRelation

    sheet = sheet_list[8] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
    row_count = len(df)
    column_count = len(df.columns)

    column_names = list(df.keys())                         # takes column names from FA sheet
    enb_names = column_names[2]
    df = df.sort_values(enb_names)
    enodebcounts = df[enb_names].value_counts()
    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
    #
    print(df)
    #
    column_count = len(df.columns)
    original_stdout = sys.stdout
    unique_node_count = df[enb_names].nunique()
    print(unique_node_count)
    pointer = 0
    df.columns = df.columns.str.upper()
    
    for y in range (0,unique_node_count):
        with open(sheet + '.mos', 'a') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f" \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,2]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                if "L23" in df.iloc[x,df.columns.tolist().index("EUtranCell".upper())]:
                    TIPE = "TDD"
                else:
                    TIPE = "FDD"    
                if "L23" in str(df.iloc[x,df.columns.tolist().index("EUtranCellRelation".upper())]):
                    TIPE2 = "TDD"
                else:
                    TIPE2 = "FDD"                      
                print(f'''crn ENodeBFunction=1,EUtranCell{TIPE}={df.iloc[x,df.columns.tolist().index("EUtranCell".upper())]},EUtranFreqRelation={df.iloc[x,df.columns.tolist().index("EUtranFreqRelation".upper())]},EUtranCellRelation={df.iloc[x,df.columns.tolist().index("EUtranCellRelation".upper())]}
    amoAllowed true
    asmSCellDlOnlyAllowed 1
    cellIndividualOffsetEUtran 0
    cellIndividualOffsetEUtranQci1 0
    coverageIndicator {df.iloc[x,df.columns.tolist().index("coverageIndicator".upper())]}
    crsAssistanceInfoPriority 0
    eranUlCompCoopCellAllowed true
    ieNBUlCompCoopCellAllowed true
    includeInSystemInformation true
    isHoAllowed {df.iloc[x,df.columns.tolist().index("isHoAllowed".upper())]}
    isRemoveAllowed {df.iloc[x,df.columns.tolist().index("isRemoveAllowed".upper())]}
    lbBnrAllowed true
    lbCovIndicated false
    loadBalancing {df.iloc[x,df.columns.tolist().index("loadBalancing".upper())]}
    neighborCellRef ENodeBFunction=1,EUtranCell{TIPE2}={df.iloc[x,df.columns.tolist().index("EUtranCellRelation".upper())]}
    qOffsetCellEUtran 0
    reportDlActivity 1
    sCellCandidate {df.iloc[x,df.columns.tolist().index("sCellCandidate".upper())]}
    sCellPriority 7
    sleepModeCovCellCandidate 2
    zzzTemporary1 -2000000000
    zzzTemporary2 -2000000000
    zzzTemporary3
    end
                \n ''')
                ####print(f'''set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}$ coverageIndicator {df.iloc[x,11]} ''')
                ####print(f'''set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}$ isHoAllowed {df.iloc[x,8]} ''')
                ####print(f'''set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}$ isRemoveAllowed {df.iloc[x,9]} ''')
                ####print(f'''set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}$ loadBalancing {df.iloc[x,10]} ''')
                ####print(f'''set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,7]},EUtranCellRelation={df.iloc[x,6]}$ sCellCandidate {df.iloc[x,12]} \n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\{}.mos".format(output_dir, folder_name, sheet)
            newname = r"{}\{}\{}_{}.mos".format(output_dir, folder_name, prefix, sheet)
        os.rename(oldname, newname)

    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn ENodeBFunction=1,EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01
    #amoAllowed true
    #asmSCellDlOnlyAllowed 1
    #cellIndividualOffsetEUtran 0
    #cellIndividualOffsetEUtranQci1 0
    #coverageIndicator 1
    #crsAssistanceInfoPriority 0
    #eranUlCompCoopCellAllowed true
    #ieNBUlCompCoopCellAllowed true
    #includeInSystemInformation true
    #isHoAllowed True
    #isRemoveAllowed False
    #lbBnrAllowed true
    #lbCovIndicated false
    #loadBalancing 1
    #neighborCellRef ENodeBFunction=1,EUtraNetwork=1,ExternalENodeBFunction=5205-58412,ExternalEUtranCellFDD=CMI0024E_2NB06_S01
    #qOffsetCellEUtran 0
    #reportDlActivity 1
    #sCellCandidate 1
    #sCellPriority 7
    #sleepModeCovCellCandidate 2
    #zzzTemporary1 -2000000000
    #zzzTemporary2 -2000000000
    #zzzTemporary3
    #end
    #
    #set EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01$ coverageIndicator 1
    #set EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01$ isHoAllowed True
    #set EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01$ isRemoveAllowed False
    #set EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01$ loadBalancing 1
    #set EUtranCellFDD=CMI0024Y_7NB05_S01,EUtranFreqRelation=100,EUtranCellRelation=CMI0024E_2NB06_S01$ sCellCandidate 1


    ## Parameter_Change

    sheet = sheet_list[9] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
    row_count = len(df)
    column_count = len(df.columns)

    column_names = list(df.keys())                         # takes column names from FA sheet
    enb_names = column_names[2]
    df = df.sort_values(enb_names)
    enodebcounts = df[enb_names].value_counts()
    df['Enodeb_Count'] = df[enb_names].map(enodebcounts)
    #
    print(df)
    #
    column_count = len(df.columns)
    original_stdout = sys.stdout
    unique_node_count = df[enb_names].nunique()
    print(unique_node_count)
    pointer =  0
    for y in range (0,unique_node_count):
        with open('Parameter_Change.mos', 'a') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f" \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,2]
            site_list_array.append(prefix)
            # cell_criteria = {df.iloc[x,5]} #old
            #cell_criteria = df.iloc[pointer,6]
            for x in range(pointer,pointer+ecount) :
                if "L23" in df.iloc[x,3]:
                    TIPE = "TDD"
                else:
                    TIPE = "FDD"  
                cell_criteria = df.iloc[x,6]
                if isinstance(df.iloc[x,7], str):
                    if df.iloc[x,7].lower() == "isHoAllowed".lower() or df.iloc[x,7].lower() == "isRemoveAllowed".lower():
                        value_param = df.iloc[x,9]
                    elif isinstance(df.iloc[x,9], str):
                        value_param = df.iloc[x,9]
                    else:
                        value_param = int(df.iloc[x,9])
                ####print(f' {df.iloc[x,2]} [{df.iloc[x,5]}]  [{df.iloc[x,6]}]   [{df.iloc[x,7]}] [{str(df.iloc[x,9])}] ') 
                if  cell_criteria == "EUtranFreqRelation"   :
                    print(f'set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,5]}$  {df.iloc[x,7]} {value_param} ')  
                elif  cell_criteria == "EUtranCellRelation"  :
                    print(f'set EUtranCell{TIPE}={df.iloc[x,3]},EUtranFreqRelation={df.iloc[x,5]},EUtranCellRelation={df.iloc[x,4]}$ {df.iloc[x,7]} {value_param} ')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\Parameter_Change.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_Parameter_Change.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        
    sys.stdout = original_stdout # Reset the standard output to its original value



    with open( 'sites_list.txt','w') as f :
        sys.stdout = f
        unique_node_values = Counter(site_list_array)
        for item in unique_node_values :
            print(item)

    sys.stdout = original_stdout

    os.chdir(cwd)
    return new_dir