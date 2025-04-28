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
#   Python Script/Tool Name          ::   "" GUTRAN_CELLRELATION_TRUE_ENM_Cygwin.py  ""
#   Process                          ::
#       1. Create a Folder under C:\cygwin64\home\"signum"\  with name  " CR_AUTO_7 "  
#       2. Keep the Python script and CR Excel Input file for e.g. "04_CR882310ENCASHI023_GUtrancellrelation_CMI0024_20231006_TRUE-ENM.xlsx " in the CR_AUTO_7 folder.
#       3. put the command "python  GUTRAN_CELLRELATION_TRUE_ENM_Cygwin.py
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
import numpy as np
from subprocess import STDOUT
import re
from collections import Counter


##def generate_script(workdir_path=None, file_path=None, selected_file=None, output_dir=None, all_df=None):
def generate_script(file_path=None, selected_file=None, output_dir=None, all_df=None , sheet_list=None):

    
    #signum = input("Please enter your Ericsson signum  :  ")
    #file_real_name = input("Please Enter the name of the GUtrancellrelation_XXX_TRUE_ENM CR Excel including the .xlsx part  :  ")
    # crn = input("Please Enter the name of the CR Number  :  ")
    # file_name = r"C:\cygwin64\home\{}\CR_AUTO_7\{}".format(signum, file_real_name)
    cr_file_name =  re.search(r"(ErCR.*?)\_[0-9]{8}", selected_file).group(1) if re.search(r"(ErCR.*?)\_[0-9]{8}", selected_file).group(1) else f"{selected_file}"
    number_cr = "99"
    customer = re.search(r".*(True|DTAC).*?$", selected_file, re.IGNORECASE).group(1)
    ##crn = f"{number_cr}_" +cr_file_name[:8]
    crn = f"{number_cr}_" +cr_file_name
    
    ##ExternalGnodeBFunction_Audit
    file_name =file_path
    # print(selected_file, output_dir, file_name, crn, sep=" == ")

    # exit()
    #ds = pd.read_excel(file_name, None)     ## ds - Reads the Whole File

    #sheet_list = list(ds.keys())            ## Reads the sheet names and puts in the list 
    unique_node_values = []
    print(sheet_list)
    original_stdout = sys.stdout
    cwd = os.getcwd()

    site_list_array = []
    sheet_list = [value for value in sheet_list if value not in ["Reference"]]

    
    folder_name = crn +"_"+ customer +"_ENM"+ today.strftime('_%Y%m%d_%H%M%S')
    # new_dir = os.path.join( cwd,folder_name)        
    new_dir = os.path.join( output_dir, folder_name)        
    # Check if the directory already exists
    if os.path.exists(new_dir):
        # If it exists, remove it (and its contents)
        try:
            os.rmdir(new_dir)
        except OSError as e:
            
            print(f"Error deleting the old directory: {e}")
        else:
            print("Old directory deleted.")

    # Create the new directory
    os.mkdir(new_dir)
    os.chdir(new_dir) 


    # Fetches Enodeb name list for site_list file 
    #dk = pd.read_excel(file_name, sheet_list[1])       ## ds - Reads a single first sheet
    #column_names = list(dk.keys())
    #enb_names = column_names[1]
    #print(enb_names)

    #
    # with open( crn +'_sites_list.txt','w') as f :
    #     sys.stdout = f
    #     dk = dk.sort_values(enb_names)
    #     unique_node_count = dk[enb_names].nunique()
    #     unique_node_values = dk[enb_names].unique()
    #     for item in unique_node_values :
    #         print(item)

    # sys.stdout = original_stdout

    with open( crn +'_command_mos.txt','w') as f :
        sys.stdout = f
        command = """
lt all

uv com_username=rbs
uv com_password=rbs
"""
        print(command)
        for item in sheet_list :
            command_item = f"run ~/PATH/$nodename_{item}.mos"
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
    sheet_list_rdel = [value for value in sheet_list if value in ["DEL_WOW","Reference"]]
    sheet_list = [value for value in sheet_list if value not in ["DEL_WOW","Reference"]]
 
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    ####################################################################### 

    #for item_sheet in sheet_list :
    for sheet_name, df in all_df.items():
    
    
    #############################################
    #############################################
    ########################### DEL_ExternalGNBCUCPFunction  
    #############################################
    #############################################
        if (sheet_name == "DEL_ExternalGNBCUCPFunction"):
            ##sheet = item_sheet 
            ##df = pd.read_excel(io=file_name, sheet_name=sheet)
            row_count = len(df)
            column_count = len(df.columns)

            column_names = list(df.keys())                         # takes column names from FA sheet
            enb_names = column_names[1]
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
                with open('DEL_ExternalGNBCUCPFunction.mos', 'w') as f:
                    sys.stdout = f
                    print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                    print(f"lt all \n \nconfbd+ \ngs+\n \n")
                    ecount=df.iloc[pointer,column_count-1]
                    prefix = df.iloc[pointer,1]

                    site_list_array.append(prefix)

                    for x in range(pointer,pointer+ecount) :
                        ##print(f'''bl ExternalGNodeBFunction={df.iloc[x,2]},TermPointToGNB=  \n''')
                        print(f'''mr NRCellRelation_del \nma NRCellRelation_del  ExternalGNBCUCPFunction={df.iloc[x,2]},ExternalNRCellCU= reservedby \ndel NRCellRelation_del\n''')
                        print(f'''bl ExternalGNBCUCPFunction={df.iloc[x,2]},TermPointToGNodeB=  \n''')
                        print(f'''rdel ExternalGNBCUCPFunction={df.iloc[x,2]}  \n''')
                        
                    pointer = pointer + ecount
                    print(f"\nconfbd- \ngs-")
                    # oldname = r":\cygwin64\home\{}\CR_AUTO_7\{}\ADD_Anchor_ExternalGNodeB.mos".format(signum, folder_name)
                    # newname = r":\cygwin64\home\{}\CR_AUTO_7\{}\{}_ADD_Anchor_ExternalGNodeB.mos".format(signum, folder_name, prefix)
                    oldname = r"{}\{}\DEL_ExternalGNBCUCPFunction.mos".format(output_dir, folder_name)
                    newname = r"{}\{}\{}_DEL_ExternalGNBCUCPFunction.mos".format(output_dir, folder_name, prefix)
                os.rename(oldname, newname)

                
            sys.stdout = original_stdout # Reset the standard output to its original value
            #############################################
            #############################################

            
    #############################################
    #############################################
    ########################### DEL_ExternalGNodeBFunction  
    #############################################
    #############################################
        elif (sheet_name == "DEL_ExternalGNodeBFunction"):            
            ##sheet = item_sheet 
            ##df = pd.read_excel(io=file_name, sheet_name=sheet)
            row_count = len(df)
            column_count = len(df.columns)

            column_names = list(df.keys())                         # takes column names from FA sheet
            enb_names = column_names[1]
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
                with open('DEL_ExternalGNodeBFunction.mos', 'w') as f:
                    sys.stdout = f
                    print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                    print(f"lt all \n \nconfbd+ \ngs+\n \n")
                    ecount=df.iloc[pointer,column_count-1]
                    prefix = df.iloc[pointer,1]

                    site_list_array.append(prefix)

                    for x in range(pointer,pointer+ecount) :
                        print(f'''bl ExternalGNodeBFunction={df.iloc[x,2]},TermPointToGNB=  \n''')
                        print(f'''mr gutrancellrel_del \nma gutrancellrel_del ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction={df.iloc[x,2]},ExternalGUtranCell= reservedby \ndel gutrancellrel_del\n''')
                        print(f'''rdel ExternalGNodeBFunction={df.iloc[x,2]}  \n''')
                        
                    pointer = pointer + ecount
                    print(f"\nconfbd- \ngs-")

                    oldname = r"{}\{}\DEL_ExternalGNodeBFunction.mos".format(output_dir, folder_name)
                    newname = r"{}\{}\{}_DEL_ExternalGNodeBFunction.mos".format(output_dir, folder_name, prefix)
                os.rename(oldname, newname)

                
            sys.stdout = original_stdout # Reset the standard output to its original value
            #############################################
            #############################################



    with open( crn +'_sites_list.txt','w') as f :
        sys.stdout = f
        unique_node_values = Counter(site_list_array)
        for item in unique_node_values :
            print(item)

    sys.stdout = original_stdout


    os.chdir(cwd)
    return new_dir


