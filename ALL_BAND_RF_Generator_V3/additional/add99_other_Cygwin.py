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
import shutil
import time as today
import numpy as np
from subprocess import STDOUT
import re
from collections import Counter


def extract_first_number(input_string):
    # Regular expression to find the first sequence of digits
    match = re.search(r'^\d+', input_string)
    # Return the matched number if found, otherwise return an empty string
    return match.group() if match else ''
    

##def generate_script(workdir_path=None, file_path=None, selected_file=None, output_dir=None, all_df=None):
def generate_script(file_path=None, selected_file=None, output_dir=None, all_df=None , sheet_list=None):

    
    #signum = input("Please enter your Ericsson signum  :  ")
    #file_real_name = input("Please Enter the name of the GUtrancellrelation_XXX_TRUE_ENM CR Excel including the .xlsx part  :  ")
    # crn = input("Please Enter the name of the CR Number  :  ")
    # file_name = r"C:\cygwin64\home\{}\CR_AUTO_7\{}".format(signum, file_real_name)
    ##cr_file_name =  re.search(r"(CR.*?)\_[0-9]{8}", selected_file).group(1) if re.search(r"(CR.*?)\_[0-9]{8}", selected_file).group(1) else f"{selected_file}"
    cr_file_name_1 =  re.search(r"(\d+.*?)\.xlsx", selected_file).group(1) if re.search(r"(\d+.*?)\.xlsx", selected_file).group(1) else f"{selected_file}"
    cr_file_name = cr_file_name_1.replace("-", "_")     
    ##number_cr = "99"
    number_cr = extract_first_number(selected_file)
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
    truni_script = []
    RNC_list_EutranFrequency9310 = []
    
    
    sheet_list = [value for value in sheet_list if value not in ["Reference"]]

    
    #folder_name = crn +"_"+ customer +"_ENM"+ today.strftime('_%Y%m%d_%H%M%S')
    folder_name = cr_file_name
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



    # Check if the directory exists
    if os.path.exists(new_dir):
        # Remove the directory and all its contents
        shutil.rmtree(new_dir)
        print(f"Directory '{new_dir}' removed.")
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
    ########################### Parameter_Tuning  
    #############################################
    #############################################   
        if (sheet_name == "Parameter_Tuning"):            
            ##sheet = item_sheet 
            ##df = pd.read_excel(io=file_name, sheet_name=sheet)
            row_count = len(df)
            column_count = len(df.columns)

            column_names = list(df.keys())                         # takes column names from FA sheet
            enb_names = column_names[7]
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
                with open('Parameter_Tuning.mos', 'a') as f:
                    sys.stdout = f
                    print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                    print(f"lt all \n \nconfbd+ \ngs+\n \n")
                    ecount=df.iloc[pointer,column_count-1]
                    prefix = df.iloc[pointer,7]

                    site_list_array.append(prefix)

                    for x in range(pointer,pointer+ecount) :
                        print(f'''bl ExternalGNodeBFunction={df.iloc[x,12]},TermPointToGNB={df.iloc[x,10]}  \n''')
                        print(f'''set ExternalGNodeBFunction={df.iloc[x,12]},TermPointToGNB={df.iloc[x,10]}  ipAddress {df.iloc[x,16]} \n''')
                        print(f'''deb ExternalGNodeBFunction={df.iloc[x,12]},TermPointToGNB={df.iloc[x,10]}  \n''')
                        
                    pointer = pointer + ecount
                    print(f"\nconfbd- \ngs-")
                    
                    oldname = r"{}\{}\Parameter_Tuning.mos".format(output_dir, folder_name)
                    newname = r"{}\{}\{}_Parameter_Tuning.mos".format(output_dir, folder_name, prefix)
                os.rename(oldname, newname)
        
            sys.stdout = original_stdout # Reset the standard output to its original value
    #######################################################################
    #######################################################################
    #######################################################################




#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
####
####     CR NO 01
####
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
    





    #############################################
    ########################### CR 4G 5G Pooling 700 Buffer 
    #############################################
    #############################################
        if (re.match(r"^(4G|5G)$", sheet_name.upper()) and number_cr == "11"):            
            ##sheet = item_sheet 
            ##df = pd.read_excel(io=file_name, sheet_name=sheet)
            sheet_name = sheet_name.replace(" ", "_")
            
            row_count = len(df)
            column_count = len(df.columns)

            column_names = list(df.keys())                         # takes column names from FA sheet
            enb_names = column_names[3]
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
                with open(sheet_name + '.mos', 'w') as f:
                    sys.stdout = f
                    ####print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                    ####print(f"lt all \n \nconfbd+ \ngs+\n \n")
                    ecount=df.iloc[pointer,column_count-1]
                    prefix = df.iloc[pointer,3]
                    site_list_array.append(prefix)
                    

                    for x in range(pointer,pointer+ecount) :
                        print(f'''  NULL  ''')

                        
                    pointer = pointer + ecount

                    oldname = r"{}\{}\{}.mos".format(output_dir, folder_name,sheet_name)
                    newname = r"{}\{}\{}_{}.mos".format(output_dir, folder_name, prefix,sheet_name)
                ##os.rename(oldname, newname)
                os.remove(oldname)

                
            sys.stdout = original_stdout # Reset the standard output to its original value
            #############################################
            #############################################     
    #######################################################################
    #######################################################################
    #######################################################################



    
    
    #############################################
    ########################### CR BSC 2G Pooling 700 Buffer
    #############################################
    #############################################
        if (sheet_name.upper() == "2G".upper() and number_cr == "11"):            
            ##sheet = item_sheet 
            ##df = pd.read_excel(io=file_name, sheet_name=sheet)
            sheet_name = sheet_name.replace(" ", "_")
            
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
                with open('01_2G_BSC_700PoolingBuffer.mo', 'w') as f:
                    sys.stdout = f
                    ####print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                    ####print(f"lt all \n \nconfbd+ \ngs+\n \n")
                    ecount=df.iloc[pointer,column_count-1]
                    prefix = df.iloc[pointer,2]
                    ###site_list_array.append(prefix)
                    

                    for x in range(pointer,pointer+ecount) :
                        print(f'''

RLEFP:CELL={df.iloc[x,4]};
RLEFC:CELL={df.iloc[x,4]},ADD,EARFCN=9310;
RLSRC:CELL={df.iloc[x,4]},EARFCN=9310,RATPRIO=5,HPRIOTHR=16,LPRIOTHR=16,QRXLEVMINE=0;
RLESC:CELL={df.iloc[x,4]},EARFCN=9310,MINCHBW=5;
RLRLC:CELL={df.iloc[x,4]},EARFCN=9310,COVERAGEE=GOOD; 
RLSRI:CELL={df.iloc[x,4]};
RLEFP:CELL={df.iloc[x,4]};
RLSRP:CELL={df.iloc[x,4]};
RLESP:CELL={df.iloc[x,4]},MINCHBW;
RLRLP:CELL={df.iloc[x,4]};




''')




        
                    pointer = pointer + ecount
                                       

                    oldname = r"{}\{}\01_2G_BSC_700PoolingBuffer.mo".format(output_dir, folder_name)
                    newname = r"{}\{}\{}\01_2G_BSC_700PoolingBuffer.mo".format(output_dir, folder_name, prefix)
                    
                    
                    


                ###############################################################
                ###############################################################
                ###############################################################
                bsc_dir = r"{}\{}\{}".format(output_dir, folder_name, prefix)
                # Check if the directory exists
                if not os.path.exists(bsc_dir):
                    os.makedirs(bsc_dir) 
                    ##print(f"Directory '{bsc_dir}' created.")
                ##else:
                    ##print(f"Directory '{bsc_dir}' already exists.")
                        
                os.rename(oldname, newname)

                
            sys.stdout = original_stdout # Reset the standard output to its original value
            #############################################
            #############################################     
    #######################################################################
    #######################################################################
    #######################################################################



    #############################################
    ########################### CR 3G Pooling 700 Buffer  RNC 
    #############################################
    #############################################
        if (sheet_name.upper() == "3G".upper() and number_cr == "11"):            
            ##sheet = item_sheet 
            ##df = pd.read_excel(io=file_name, sheet_name=sheet)
            sheet_name = sheet_name.replace(" ", "_")
            script_name = "02_3G_RNC_Pooling_Buffer"
            truni_script.append(script_name)
            
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
                with open(script_name + '.mo', 'w') as f:
                    sys.stdout = f
                    ####print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                    ####print(f"lt all \n \nconfbd+ \ngs+\n \n")
                    ecount=df.iloc[pointer,column_count-1]
                    prefix = df.iloc[pointer,2]
                    site_list_array.append(prefix)
                    
                    

                    for x in range(pointer,pointer+ecount) :
                        RNC_LOC = df.iloc[x,1].upper()
                        OPER_LOC = str(df.iloc[x,7]).upper()
                        Tipe_Script = f'''{RNC_LOC}_{OPER_LOC}'''
                        RNC_DTAC_TRUE = f'''{df.iloc[x,2]}_{RNC_LOC}'''
                        
                        CELLNAME = df.iloc[x,4]
                        ####
                        RNC_list_EutranFrequency9310.append(RNC_DTAC_TRUE)
                        
                        
                        if Tipe_Script == "TrueENM_TRUE".upper():
                            print(f'''

CREATE
(
   parent "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME}"
   identity "9310"
   moType EutranFreqRelation
   exception none
   nrOfAttributes 12
   cellReselectionPriority Integer 4
   coSitedCellAvailable Integer 1
   eutranFrequencyRef Ref "ManagedElement=1,RncFunction=1,EutraNetwork=EUTRAN_1,EutranFrequency=9310"
   qQualMin Integer -17
   qRxLevMin Integer -128
   redirectionOrder Integer 1
   thresh2dRwr Integer -25
   threshHigh Integer 22
   threshHigh2 Integer 10
   threshLow Integer 0
   threshLow2 Integer 10
   userLabel String "EutranFreqRelation_9310"
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   userLabel String "EutranFreqRelation_9310"
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshLow2 Integer 10
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshLow Integer 0
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshHigh2 Integer 10
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshHigh Integer 22
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   thresh2dRwr Integer -25
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   redirectionOrder Integer 1
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   qRxLevMin Integer -128
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   qQualMin Integer -17
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   coSitedCellAvailable Integer 1
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   cellReselectionPriority Integer 4
)




''')                            
                        
                        elif Tipe_Script == "TrueENM_DTAC".upper():
                            print(f'''

CREATE
(
   parent "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME}"
   identity "9310"
   moType EutranFreqRelation
   exception none
   nrOfAttributes 12
   cellReselectionPriority Integer 5
   coSitedCellAvailable Integer 1
   eutranFrequencyRef Ref "ManagedElement=1,RncFunction=1,EutraNetwork=EUTRAN_1,EutranFrequency=9310"
   qQualMin Integer 100
   qRxLevMin Integer -110
   redirectionOrder Integer 7
   thresh2dRwr Integer -85
   threshHigh Integer 0
   threshHigh2 Integer 10
   threshLow Integer 0
   threshLow2 Integer 10
   userLabel String "EutranFreqRelation_9310"
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   userLabel String "EutranFreqRelation_9310"
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshLow2 Integer 10
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshLow Integer 0
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshHigh2 Integer 10
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshHigh Integer 0
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   thresh2dRwr Integer -85
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   redirectionOrder Integer 7
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   qRxLevMin Integer -110
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   qQualMin Integer 100
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   coSitedCellAvailable Integer 1
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   cellReselectionPriority Integer 5
)





''')

                        else:
                            print(f'''

CREATE
(
   parent "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME}"
   identity "9310"
   moType EutranFreqRelation
   exception none
   nrOfAttributes 12
   cellReselectionPriority Integer 5
   coSitedCellAvailable Integer 1
   eutranFrequencyRef Ref "ManagedElement=1,RncFunction=1,EutraNetwork=1,EutranFrequency=9310"
   qQualMin Integer 100
   qRxLevMin Integer -110
   redirectionOrder Integer 7
   thresh2dRwr Integer -85
   threshHigh Integer 0
   threshHigh2 Integer 10
   threshLow Integer 0
   threshLow2 Integer 10
   userLabel String "EutranFreqRelation_9310"
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   userLabel String "EutranFreqRelation_9310"
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshLow2 Integer 10
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshLow Integer 0
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshHigh2 Integer 10
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   threshHigh Integer 0
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   thresh2dRwr Integer -85
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   redirectionOrder Integer 7
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   qRxLevMin Integer -110
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   qQualMin Integer 100
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   coSitedCellAvailable Integer 1
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={CELLNAME},EutranFreqRelation=9310"
   exception none
   cellReselectionPriority Integer 5
)






''')
                        
                    pointer = pointer + ecount

                    oldname = r"{}\{}\{}.mo".format(output_dir, folder_name,script_name)
                    newname = r"{}\{}\{}_{}.mo".format(output_dir, folder_name, prefix,script_name)
                os.rename(oldname, newname)

                
            sys.stdout = original_stdout # Reset the standard output to its original value
            #############################################
            #############################################     
    #######################################################################
    #######################################################################
    #######################################################################
































#####################################################################################################################
#####################################################################################################################
#####################################################################################################################
####
####     CR NO 10
####
#####################################################################################################################
#####################################################################################################################
#####################################################################################################################



    #############################################
    ########################### CR ADD_EUtranFrequency
    #############################################
    #############################################
        if (sheet_name.upper() == "ADD_EUtranFrequency".upper() and number_cr == "10"):            
            ##sheet = item_sheet 
            ##df = pd.read_excel(io=file_name, sheet_name=sheet)
            sheet_name = sheet_name.replace(" ", "_")
            
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
                with open(sheet_name + '.mos', 'w') as f:
                    sys.stdout = f
                    ####print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                    ####print(f"lt all \n \nconfbd+ \ngs+\n \n")
                    ecount=df.iloc[pointer,column_count-1]
                    prefix = df.iloc[pointer,1]
                    site_list_array.append(prefix)
                    

                    for x in range(pointer,pointer+ecount) :
                        print(f'''

crn {df.iloc[x,3]}
arfcnValueEUtranDl {df.iloc[x,8]}
caOffloadingEnabled False
mfbiFreqBandIndPrio False
userLabel DTAC_B40F1_38852
end
set {df.iloc[x,3]}$ caOffloadingEnabled False
set {df.iloc[x,3]}$ mfbiFreqBandIndPrio False
set {df.iloc[x,3]}$ userLabel DTAC_B40F1_38852


''')

                        
                    pointer = pointer + ecount

                    oldname = r"{}\{}\{}.mos".format(output_dir, folder_name,sheet_name)
                    newname = r"{}\{}\{}_{}.mos".format(output_dir, folder_name, prefix,sheet_name)
                os.rename(oldname, newname)

                
            sys.stdout = original_stdout # Reset the standard output to its original value
            #############################################
            #############################################     
    #######################################################################
    #######################################################################
    #######################################################################


    #############################################
    ########################### CR ADD_DTAC_EUtranFreqRelation
    #############################################
    #############################################
        if (sheet_name.upper() == "ADD_DTAC_EUtranFreqRelation".upper() and number_cr == "10"):            
            ##sheet = item_sheet 
            ##df = pd.read_excel(io=file_name, sheet_name=sheet)
            sheet_name = sheet_name.replace(" ", "_")
            
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
            df.columns = df.columns.str.upper()
            #max_retries = 3
            #retries = 0
            for y in range (0,unique_node_count):
                with open(sheet_name + '.mos', 'w') as f:
                    sys.stdout = f
                    ####print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                    ####print(f"lt all \n \nconfbd+ \ngs+\n \n")
                    ecount=df.iloc[pointer,column_count-1]
                    prefix = df.iloc[pointer,1]
                    site_list_array.append(prefix)
                    

                    for x in range(pointer,pointer+ecount) :
                        FULL_MO=f"ENodeBFunction=1,{df.iloc[x,4]},{df.iloc[x,5]}"
                        PARAM_lbBnrPolicy=df.iloc[x,df.columns.tolist().index("lbBnrPolicy".upper())]
                        if isinstance(PARAM_lbBnrPolicy, str):
                            match = re.search(r"(\d+)\s*\(.*\)", PARAM_lbBnrPolicy)
                            if match:
                                # Extract the number
                                PARAM_lbBnrPolicy = match.group(1)

                        
                        print(f'''


crn {FULL_MO}
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency={df.iloc[x,7]}
cellReselectionPriority {df.iloc[x,df.columns.tolist().index("cellReselectionPriority".upper())]}
end



set {FULL_MO}$ qRxLevMin {df.iloc[x,df.columns.tolist().index("qRxLevMin".upper())]}
set {FULL_MO}$ qQualMin {df.iloc[x,df.columns.tolist().index("qQualMin".upper())]}
set {FULL_MO}$ threshXHigh {df.iloc[x,df.columns.tolist().index("threshXHigh".upper())]}
set {FULL_MO}$ threshXLow {df.iloc[x,df.columns.tolist().index("threshXLow".upper())]}
set {FULL_MO}$ voicePrio {df.iloc[x,df.columns.tolist().index("voicePrio".upper())]}
set {FULL_MO}$ voicePrioBr {df.iloc[x,df.columns.tolist().index("voicePrioBr".upper())]}
set {FULL_MO}$ cellReselectionPriority {df.iloc[x,df.columns.tolist().index("cellReselectionPriority".upper())]}
set {FULL_MO}$ connectedModeMobilityPrio {df.iloc[x,df.columns.tolist().index("connectedModeMobilityPrio".upper())]}
set {FULL_MO}$ connectedModeMobilityPrioBr {df.iloc[x,df.columns.tolist().index("connectedModeMobilityPrioBr".upper())]}
set {FULL_MO}$ endcAwareIdleModePriority {df.iloc[x,df.columns.tolist().index("endcAwareIdleModePriority".upper())]}
set {FULL_MO}$ endcHoFreqPriority {df.iloc[x,df.columns.tolist().index("endcHoFreqPriority".upper())]}
set {FULL_MO}$ interFreqMeasType {df.iloc[x,df.columns.tolist().index("interFreqMeasType".upper())]}
set {FULL_MO}$ mdtMeasOn {df.iloc[x,df.columns.tolist().index("mdtMeasOn".upper())]}
set {FULL_MO}$ lbBnrPolicy {PARAM_lbBnrPolicy}
set {FULL_MO}$ allowedPlmnList mcc=520,mnc=47,mncLength=2




''')

###df.columns.tolist().index("coverageIndicator".upper())
                        
                    pointer = pointer + ecount

                    oldname = r"{}\{}\{}.mos".format(output_dir, folder_name,sheet_name)
                    newname = r"{}\{}\{}_{}.mos".format(output_dir, folder_name, prefix,sheet_name)
                os.rename(oldname, newname)

                
            sys.stdout = original_stdout # Reset the standard output to its original value
            #############################################
            #############################################     
    #######################################################################
    #######################################################################
    #######################################################################





    #############################################
    ########################### CR parameter
    #############################################
    #############################################
        if (sheet_name.upper() == "parameter".upper() and number_cr == "10"):            
            ##sheet = item_sheet 
            ##df = pd.read_excel(io=file_name, sheet_name=sheet)
            sheet_name = sheet_name.replace(" ", "_")
            
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
                with open(sheet_name + '.mos', 'w') as f:
                    sys.stdout = f
                    ####print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                    ####print(f"lt all \n \nconfbd+ \ngs+\n \n")
                    ecount=df.iloc[pointer,column_count-1]
                    prefix = df.iloc[pointer,1]
                    site_list_array.append(prefix)
                    

                    for x in range(pointer,pointer+ecount) :  
                        value_set = df.iloc[x,6]
                        parameter = df.iloc[x,4]
                        
                        ##eutranFreqToQciProfileRelation
                        if isinstance(value_set, str) and parameter.upper() == "eutranFreqToQciProfileRelation".upper():
                            value_set = re.sub(r'SubNetwork\=.*?ManagedElement\=', 'ManagedElement=', value_set)
                            value_set = re.sub(r'[\[\]]', '', value_set)                            
                            value_set = re.sub(r'\s+', '', value_set)
                            value_set = re.sub(r'\}\,\{', ';', value_set)
                            value_set = re.sub(r'[\{\}]', '', value_set)                        
                        ###print(f'''SET {df.iloc[x,3]}  {df.iloc[x,4]}   {df.iloc[x,6]}   ''')
                        print(f'''SET  {df.iloc[x,3]}$  {parameter} {value_set} \n''')

                        
                    pointer = pointer + ecount

                    oldname = r"{}\{}\{}.mos".format(output_dir, folder_name,sheet_name)
                    newname = r"{}\{}\{}_{}.mos".format(output_dir, folder_name, prefix,sheet_name)
                os.rename(oldname, newname)

                
            sys.stdout = original_stdout # Reset the standard output to its original value
            #############################################
            #############################################     
    #######################################################################
    #######################################################################
    #######################################################################





    #############################################
    ########################### CR SPID
    #############################################
    #############################################
        if (re.match(r'^SPID', sheet_name) and number_cr == "10"):            
            ##sheet = item_sheet 
            ##df = pd.read_excel(io=file_name, sheet_name=sheet)
            sheet_name = sheet_name.replace(" ", "_")
            
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
                with open(sheet_name + '.mos', 'w') as f:
                    sys.stdout = f
                    ####print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                    ####print(f"lt all \n \nconfbd+ \ngs+\n \n")
                    ecount=df.iloc[pointer,column_count-1]
                    prefix = df.iloc[pointer,1]
                    site_list_array.append(prefix)
                    

                    for x in range(pointer,pointer+ecount) :  
                        FULL_MO=f"ENodeBFunction={df.iloc[x,2]},SubscriberProfileID={df.iloc[x,3]},RATFreqPrio={df.iloc[x,4]}"
                        freqPrioListEUTRA = df.iloc[x,7]
                        freqPrioListUTRA = df.iloc[x,8]
                        freqGroupPrioListGERAN = df.iloc[x,8]
                        ##parameter = df.iloc[x,7]
                        
                        ##
                        if isinstance(freqPrioListEUTRA, str):
                            freqPrioListEUTRA = re.sub(r'SubNetwork\=.*?ManagedElement\=', 'ManagedElement=', freqPrioListEUTRA)
                            freqPrioListEUTRA = re.sub(r'[\[\]]', '', freqPrioListEUTRA)                            
                            freqPrioListEUTRA = re.sub(r'\s+', '', freqPrioListEUTRA)
                            freqPrioListEUTRA = re.sub(r'\}\,\{', ';', freqPrioListEUTRA)
                            freqPrioListEUTRA = re.sub(r'[\{\}]', '', freqPrioListEUTRA) 
                            
                        if isinstance(freqPrioListUTRA, str):
                            freqPrioListUTRA = re.sub(r'SubNetwork\=.*?ManagedElement\=', 'ManagedElement=', freqPrioListUTRA)
                            freqPrioListUTRA = re.sub(r'[\[\]]', '', freqPrioListUTRA)                            
                            freqPrioListUTRA = re.sub(r'\s+', '', freqPrioListUTRA)
                            freqPrioListUTRA = re.sub(r'\}\,\{', ';', freqPrioListUTRA)
                            freqPrioListUTRA = re.sub(r'[\{\}]', '', freqPrioListUTRA)

                        if isinstance(freqGroupPrioListGERAN, str):
                            freqGroupPrioListGERAN = re.sub(r'SubNetwork\=.*?ManagedElement\=', 'ManagedElement=', freqGroupPrioListGERAN)
                            freqGroupPrioListGERAN = re.sub(r'[\[\]]', '', freqGroupPrioListGERAN)                            
                            freqGroupPrioListGERAN = re.sub(r'\s+', '', freqGroupPrioListGERAN)
                            freqGroupPrioListGERAN = re.sub(r'\}\,\{', ';', freqGroupPrioListGERAN)
                            freqGroupPrioListGERAN = re.sub(r'[\{\}]', '', freqGroupPrioListGERAN)
                            
                        ###print(f'''SET {df.iloc[x,3]}  {df.iloc[x,4]}   {df.iloc[x,6]}   ''')
                        print(f''' 

crn {FULL_MO}
freqPrioListEUTRA {freqPrioListEUTRA}
freqPrioListUTRA   {freqPrioListUTRA}
spidList {df.iloc[x,5]}
ueCapPrioAllowed {df.iloc[x,6]}
end
set {FULL_MO}$ freqPrioListEUTRA {freqPrioListEUTRA}
set {FULL_MO}$ freqPrioListUTRA   {freqPrioListUTRA}
set {FULL_MO}$ spidList {df.iloc[x,5]}
set {FULL_MO}$ ueCapPrioAllowed {df.iloc[x,6]}







''')
                        
                    pointer = pointer + ecount

                    oldname = r"{}\{}\{}.mos".format(output_dir, folder_name,sheet_name)
                    newname = r"{}\{}\{}_{}.mos".format(output_dir, folder_name, prefix,sheet_name)
                os.rename(oldname, newname)

                
            sys.stdout = original_stdout # Reset the standard output to its original value
            #############################################
            #############################################     
    #######################################################################
    #######################################################################
    #######################################################################
































    RNC_RUN_EutranFrequency9310 = []
    RNC_RUN_EutranFrequency9310 = Counter(RNC_list_EutranFrequency9310)
    for item in RNC_RUN_EutranFrequency9310 :
        with open( 'RNC_ADD_EutranFrequency9310.mo','w') as f :
            sys.stdout = f   
            parts = item.split("_")
            RNC_NAME = str(parts[0]).upper()
            OPER_LOC = str(parts[1]).upper()            
            
            if OPER_LOC == "TRUEENM":
                ##TRUE
                MO_EutraNetwork="EUTRAN_1"
            else:
                MO_EutraNetwork="1"
            print(f'''   
CREATE
(
   parent "ManagedElement=1,RncFunction=1,EutraNetwork={MO_EutraNetwork}"
   identity "9310"
   moType EutranFrequency
   exception none
   nrOfAttributes 5
   anrEnabled Integer 1
   earfcnDl Integer 9310
   eutraDetection Integer 1
   measBandwidth Integer 6
   userLabel String "L700_20MHz"
)


''')
                


            
            new_script_name = r"01_3G_RNC_ADD_EutranFrequency9310_{}".format(OPER_LOC )
            truni_script.append(new_script_name)
            oldname = r"{}\{}\RNC_ADD_EutranFrequency9310.mo".format(output_dir, folder_name)
            newname = r"{}\{}\{}_01_3G_RNC_ADD_EutranFrequency9310_{}.mo".format(output_dir, folder_name, RNC_NAME , OPER_LOC )
            
        os.rename(oldname, newname)
            
        sys.stdout = original_stdout            




#######################################################################
#######################################################################
#######################################################################
#######################################################################
###  COMMAND MOS
#######################################################################
#######################################################################
#######################################################################
#######################################################################

    with open( 'command_mos.txt','w') as f :
        sys.stdout = f
        command = """
uv com_username=rbs
uv com_password=rbs
lt all

confbd+ 
gs+
 
"""

        ####print(f'''####cvms Before_Execute_{today.strftime('%Y%m%d_%H%M%S')} ''')
        ##joined_string = '|'.join(map(str, my_block_cell_list))
        ##print(f'''ma cell_block ({joined_string}) ''')

        print(command)

        print(f"lcd  ~/PATH/{folder_name} \n")

        if number_cr == "11":
            ### CR NO 01
            ###truni_script
            truni_script.sort()
            unique_truni_script = []
            unique_truni_script = Counter(truni_script)
            
            print("if $nodetype = RNC\n")
            for item in unique_truni_script :
                script_name = item.replace(" ", "_")
                print(f"truni $nodename_{script_name}.mo")            
            print("else\n")
            print(f'''  
###DTAC 4G 5G Script
run /home/shared/VDES1534/ACTIVITY/LNR700_20M_spectrumpooling/Relation_9310_153630.mos
###TRUE 4G 5G Script
run /home/shared/peeracob_v53/ACTIVITY/LNR700_20M_spectrumpooling/Relation_9310_153630.mos

            
''')
            print("fi\n")
            #####create CV
            print(f'''\n
if $nodetype = RNC
else        
cvms {crn}_{today.strftime('%Y%m%d_%H%M%S')}
fi
''')

            
        else:
            ####### OTHER THAN CR NUMBER 01
            for item in sheet_list :
                sheet_name = item.replace(" ", "_")
                print(f"run $nodename_{sheet_name}.mos")
            
            print(f'''cvms {crn}_{today.strftime('%Y%m%d_%H%M%S')} \n''')
        print("\n\n") 
        print("\n\n") 

 
       
        print(f"\nconfbd-\ngs-")


    sys.stdout = original_stdout



#######################################################################
#######################################################################
            
    with open( 'sites_list.txt','w') as f :
        sys.stdout = f
        unique_node_values = Counter(site_list_array)
        for item in unique_node_values :
            print(item)

    sys.stdout = original_stdout


    os.chdir(cwd)
    return new_dir


