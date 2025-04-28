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
import math
import shutil

def check_and_set(variable):
    if not variable or math.isnan(variable) or not str(variable).replace('.', '').isdigit():
        variable = "NULL"
    return variable 


def generate_script(workdir_path=None, file_path=None, selected_file=None, output_dir=None):

    
    #signum = input("Please enter your Ericsson signum  :  ")
    #file_real_name = input("Please Enter the name of the GUtrancellrelation_XXX_TRUE_ENM CR Excel including the .xlsx part  :  ")
    # crn = input("Please Enter the name of the CR Number  :  ")
    # file_name = r"C:\cygwin64\home\{}\CR_AUTO_7\{}".format(signum, file_real_name)
    #cr_file_name =  re.search(r"_(CR.*?)_", selected_file).group(1) if re.search(r"_(CR.*?)_", selected_file).group(1) else f"{selected_file}"
    cr_file_name_1 =  re.search(r"(\d+.*?)\.xlsx", selected_file).group(1) if re.search(r"(\d+.*?)\.xlsx", selected_file).group(1) else f"{selected_file}"
    cr_file_name = cr_file_name_1.replace("-", "_")
    number_cr = re.search(r"(\d+)\_CR.*?$", selected_file).group(1)
    customer = re.search(r".*(True|DTAC).*?$", selected_file, re.IGNORECASE).group(1)
    crn = cr_file_name[:11]
    file_name =file_path
    # print(selected_file, output_dir, file_name, crn, sep=" == ")

    # exit()
    ds = pd.read_excel(file_name, None)     ## ds - Reads the Whole File
    sheet_list = list(ds.keys())            ## Reads the sheet names and puts in the list 
    unique_node_values = []
    print(sheet_list)
    original_stdout = sys.stdout
    cwd = os.getcwd()

    site_list_array = []

    # folder_name = crn +"_GUtrancellrelation_XXX_TRUE_ENM"+ today.strftime('_%d_%m_%Y_%H_%M_%s')
    #folder_name = crn +"_GUtrancellrelation_XXX_"+ customer +"_ENM"+ today.strftime('_%Y%m%d_%H%M%S')
    folder_name = cr_file_name
    
    # new_dir = os.path.join( cwd,folder_name)        
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
    dk = pd.read_excel(file_name, sheet_list[1])       ## ds - Reads a single first sheet
    column_names = list(dk.keys())
    enb_names = column_names[1]
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

hget fiel prod
if $nr_of_mos = 0
$node_cr_run = DUS
else
$node_cr_run = BB
fi


"""
        print(f"\nconfbd+ \ngs+\n \n")
        print(command)
        print(f"lcd  ~/PATH/{folder_name} \n")
        for item in sheet_list :
            if item == "ADD_GUtranSyncSignalFrequency" or item == "ADD_GUtranFreqRelation" :
                command_item = f"run $nodename_{item}_$node_cr_run.mos"
            else:
                command_item = f"run $nodename_{item}.mos"                
            print(command_item)

        print(f"\nconfbd- \ngs-\n")
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
"ADD_GUtranSyncSignalFrequency",
"ADD_GUtranFreqRelation",
"ADD_ExternalGNodeBFunction",
"ADD_ExternalGUtranCell",
"ADD_GUtranCellRelation"     
    ]]
    sheet_list = [value for value in sheet_list if value in [
"ADD_GUtranSyncSignalFrequency",
"ADD_GUtranFreqRelation",
"ADD_ExternalGNodeBFunction",
"ADD_ExternalGUtranCell",
"ADD_GUtranCellRelation"    
    ]]
    
    
    
    #######################################################################
    #######################################################################
    for item in sheet_list_rdel :
    #######################################################################
    #######################################################################    
    
    
        #############################################
        #############################################
        ########################### DEL_ExternalGNodeBFunction  
        #############################################
        #############################################
            if (item.upper() == "DEL_ExternalGNodeBFunction".upper()):            
                sheet = item 
                df = pd.read_excel(io=file_name, sheet_name=sheet)
                row_count = len(df)
                column_count = len(df.columns)

                column_names = list(df.keys())                         # takes column names from FA sheet
                enb_names = column_names[1]  ## column Node
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
                        print(f" \nconfbd+ \ngs+\n \n")
                        ecount=df.iloc[pointer,column_count-1]
                        prefix = df.iloc[pointer,1]  ## column Node
                        site_list_array.append(prefix)
                        for x in range(pointer,pointer+ecount) :
                            print(f'''bl ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction={df.iloc[x,2]},TermPointToGNB=  \n''')
                            print(f'''mr GUtranCellRelation_del \nma GUtranCellRelation_del  ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction={df.iloc[x,2]},ExternalGUtranCell= reservedby \ndel GUtranCellRelation_del\n''')
                            ##print(f'''bl ExternalGNBCUCPFunction={df.iloc[x,4]},TermPointToGNodeB=  \n''')
                            print(f'''rdel ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction={df.iloc[x,2]}  \n''')
                        pointer = pointer + ecount
                        print(f"\nconfbd- \ngs-")
                        oldname = r"{}\{}\{}.mos".format(output_dir, folder_name,sheet)
                        newname = r"{}\{}\{}_{}.mos".format(output_dir, folder_name, prefix,sheet)
                    os.rename(oldname, newname)
                    
                sys.stdout = original_stdout # Reset the standard output to its original value
                #############################################
                #############################################    
    
    
        #############################################
        ########################### DEL_ExternalGUtranCell_2  
        #############################################
        #############################################
            ####if (sheet_name == "DEL_ExternalGUtranCell"):
            if (item.upper() == "DEL_ExternalGUtranCell".upper()):        
                sheet = item 
                sheet_name = item 
                df = pd.read_excel(io=file_name, sheet_name=sheet)
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
                        print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
                        ####print(f"lt all \n \nconfbd+ \ngs+\n \n")
                        ecount=df.iloc[pointer,column_count-1]
                        prefix = df.iloc[pointer,1]

                        site_list_array.append(prefix)

                        for x in range(pointer,pointer+ecount) :
                            print(f'''bl ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction={df.iloc[x,2]},TermPointToENodeB=  \n''')
                            print(f'''mr GUtranCellRelation_del \nma GUtranCellRelation_del  ExternalGNodeBFunction={df.iloc[x,2]},ExternalGUtranCell={df.iloc[x,3]} reservedby \ndel GUtranCellRelation_del\n''')
                            ##print(f'''bl ExternalGNBCUCPFunction={df.iloc[x,4]},TermPointToGNodeB=  \n''')
                            print(f'''del ExternalGNodeBFunction={df.iloc[x,2]},ExternalGUtranCell={df.iloc[x,3]}  \n''')
                            
                        pointer = pointer + ecount
                        ####print(f"\nconfbd- \ngs-")
                        # oldname = r":\cygwin64\home\{}\CR_AUTO_7\{}\ADD_Anchor_ExternalGNodeB.mos".format(signum, folder_name)
                        # newname = r":\cygwin64\home\{}\CR_AUTO_7\{}\{}_ADD_Anchor_ExternalGNodeB.mos".format(signum, folder_name, prefix)
                        oldname = r"{}\{}\{}.mos".format(output_dir, folder_name,sheet_name)
                        newname = r"{}\{}\{}_{}.mos".format(output_dir, folder_name, prefix,sheet_name)
                    os.rename(oldname, newname)

                    
                sys.stdout = original_stdout # Reset the standard output to its original value
                #############################################
                #############################################
        
    
 
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    ####################################################################### 
    ########################### ADD_GUtranSyncSignalFrequency BASEBAND
    
    
    sheet = sheet_list[0] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
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
        with open('ADD_GUtranSyncSignalFrequency.mos', 'w') as f:
            sys.stdout = f
            ######print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            ####print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]

            site_list_array.append(prefix)

            for x in range(pointer,pointer+ecount) :
                print(f'''
                
crn ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency={df.iloc[x,df.columns.tolist().index("GUtranSyncSignalFrequency".upper())]}
arfcn {df.iloc[x,df.columns.tolist().index("arfcn".upper())]}
band {df.iloc[x,df.columns.tolist().index("band".upper())]}
smtcDuration {df.iloc[x,df.columns.tolist().index("smtcDuration".upper())]}
smtcOffset {df.iloc[x,df.columns.tolist().index("smtcOffset".upper())]}
smtcPeriodicity {df.iloc[x,df.columns.tolist().index("smtcPeriodicity".upper())]}
smtcScs {df.iloc[x,df.columns.tolist().index("smtcScs".upper())]}
userLabel {df.iloc[x,df.columns.tolist().index("userLabel".upper())]}
end\n''')
                
            pointer = pointer + ecount
            ######print(f"\nconfb- \ngs-")

            oldname = r"{}\{}\ADD_GUtranSyncSignalFrequency.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_GUtranSyncSignalFrequency_BB.mos".format(output_dir, folder_name, prefix)
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
    


    ####################################################################### 
    ########################### ADD_GUtranSyncSignalFrequency DUS
    
    
    sheet = sheet_list[0] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
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
        with open('ADD_GUtranSyncSignalFrequency.mos', 'w') as f:
            sys.stdout = f
            ######print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            ####print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]

            site_list_array.append(prefix)

            for x in range(pointer,pointer+ecount) :
                GUtranSyncSignalFrequency = df.iloc[x,df.columns.tolist().index("GUtranSyncSignalFrequency".upper())]
                ###smtcScs = df.iloc[x,df.columns.tolist().index("smtcScs".upper())]
                smtcPeriodicity = df.iloc[x,df.columns.tolist().index("smtcPeriodicity".upper())]
                smtcOffset = df.iloc[x,df.columns.tolist().index("smtcOffset".upper())]
                smtcDuration = df.iloc[x,df.columns.tolist().index("smtcDuration".upper())]
                print(f'''
                
crn ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency={GUtranSyncSignalFrequency}-{smtcPeriodicity}-{smtcOffset}-{smtcDuration}
arfcn {df.iloc[x,df.columns.tolist().index("arfcn".upper())]}
band {df.iloc[x,df.columns.tolist().index("band".upper())]}
smtcDuration {df.iloc[x,df.columns.tolist().index("smtcDuration".upper())]}
smtcOffset {df.iloc[x,df.columns.tolist().index("smtcOffset".upper())]}
smtcPeriodicity {df.iloc[x,df.columns.tolist().index("smtcPeriodicity".upper())]}
smtcScs {df.iloc[x,df.columns.tolist().index("smtcScs".upper())]}
userLabel {df.iloc[x,df.columns.tolist().index("userLabel".upper())]}
end\n''')
                
            pointer = pointer + ecount
            ######print(f"\nconfb- \ngs-")

            oldname = r"{}\{}\ADD_GUtranSyncSignalFrequency.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_GUtranSyncSignalFrequency_DUS.mos".format(output_dir, folder_name, prefix)
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
    
    
    
    
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    
    
    
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    ####################################################################### 
    ########################### ADD_Anchor_ExternalGNodeB

    sheet = sheet_list[1] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
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
        with open('ADD_ExternalGNodeBFunction.mos', 'w') as f:
            sys.stdout = f
            ######print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f"set  ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 anrStateNR 0 \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]

            site_list_array.append(prefix)

            for x in range(pointer,pointer+ecount) :
                GNBID=df.iloc[x,3]
                GNBID=check_and_set(GNBID)
                
                print(f'''bl ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=520.*{GNBID},TermPointToGNB=  \n''')
                print(f'''mr GUtranCellRelation_del \nma GUtranCellRelation_del  ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=520.*{GNBID},ExternalGUtranCell= reservedby \ndel GUtranCellRelation_del\n''')
                print(f'''rdel ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=520.*{GNBID}$  \n''')
            
                print(f'''crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction={df.iloc[x,2]}  \ngNodeBId  {GNBID} \ngNodeBIdLength {df.iloc[x,4]} \ngNodeBPlmnId mcc={df.iloc[x,5]},mnc={df.iloc[x,6]},mncLength={df.iloc[x,7]} \nuserLabel \nend  \n''')
                print(f'''crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction={df.iloc[x,2]},TermPointToGNB={df.iloc[x,8]}  \nadministrativeState 1 \ndomainName \nipAddress {df.iloc[x,9]} \nipv6Address :: \nend  \n''')
            pointer = pointer + ecount
            ######print(f"\nconfb- \ngs-")
            print(f"set  ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 anrStateNR 1 \n")
            # oldname = r":\cygwin64\home\{}\CR_AUTO_7\{}\ADD_Anchor_ExternalGNodeB.mos".format(signum, folder_name)
            # newname = r":\cygwin64\home\{}\CR_AUTO_7\{}\{}_ADD_Anchor_ExternalGNodeB.mos".format(signum, folder_name, prefix)
            oldname = r"{}\{}\ADD_ExternalGNodeBFunction.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_ExternalGNodeBFunction.mos".format(output_dir, folder_name, prefix)
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


    #r"C:\cygwin64\home\{}\CR_AUTO_7\{}\ADD_Anchor_ExternalGNodeB.mos".format(signum, folder_name)
    #r"C:\cygwin64\home\{}\CR_AUTO_7\{}\{}_ADD_Anchor_ExternalGNodeB.mos".format(signum, folder_name, prefix)


    #crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=CMI6896P_9NB01
    #gNodeBId 135912
    #gNodeBIdLength 22
    #gNodeBPlmnId mcc=520,mnc=4,mncLength=2
    #userLabel
    #end
    #
    #crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=CMI6896P_9NB01,TermPointToGNB=CMI6896P_9NB01
    #administrativeState 1
    #domainName
    #ipAddress 10.153.226.106
    #ipsecEpAddress ::
    #ipv6Address ::
    #upIpAddress ::
    #end



    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    ## ADD_GUtranFreqRelation
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    
    ## ADD_GUtranFreqRelation BB
    #######################################################################
    
    sheet = sheet_list[2] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
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
    
    for y in range (0,unique_node_count):
        with open('ADD_GUtranFreqRelation.mos', 'w') as f:
            sys.stdout = f
            ######print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            ####print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=int(df.iloc[pointer,column_count-1])
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
            ##for x in range(int(pointer), int(pointer) + int(ecount)):    
                print(f'''
crn ENodeBFunction=1,EUtranCell{df.iloc[x,3]}={df.iloc[x,2]},GUtranFreqRelation={df.iloc[x,4]}  
allowedPlmnList   
cellReselectionPriority {df.iloc[x,df.columns.tolist().index("cellReselectionPriority".upper())]}  
cellReselectionSubPriority {df.iloc[x,df.columns.tolist().index("cellReselectionSubPriority".upper())]} 
connectedModeMobilityPrio {df.iloc[x,df.columns.tolist().index("connectedModeMobilityPrio".upper())]} 
endcB1MeasPriority {df.iloc[x,df.columns.tolist().index("endcB1MeasPriority".upper())]} 
gUtranSyncSignalFrequencyRef {df.iloc[x,df.columns.tolist().index("gUtranSyncSignalFrequencyRef".upper())]} 
pMaxNR {df.iloc[x,df.columns.tolist().index("pMaxNR".upper())]}   
qOffsetFreq {df.iloc[x,df.columns.tolist().index("qOffsetFreq".upper())]} 
qRxLevMin {df.iloc[x,df.columns.tolist().index("qRxLevMin".upper())]} 
threshXHigh {df.iloc[x,df.columns.tolist().index("threshXHigh".upper())]}   
threshXLow {df.iloc[x,df.columns.tolist().index("threshXLow".upper())]}  
end \n''')
            pointer = pointer + ecount
            ######print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_GUtranFreqRelation.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_GUtranFreqRelation_BB.mos".format(output_dir, folder_name, prefix)
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





    ## ADD_GUtranFreqRelation DUS
    #######################################################################
    
    sheet = sheet_list[2] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
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
    
    for y in range (0,unique_node_count):
        with open('ADD_GUtranFreqRelation.mos', 'w') as f:
            sys.stdout = f
            ######print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            ####print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=int(df.iloc[pointer,column_count-1])
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
            ##for x in range(int(pointer), int(pointer) + int(ecount)):    
                print(f'''
crn ENodeBFunction=1,EUtranCell{df.iloc[x,3]}={df.iloc[x,2]},GUtranFreqRelation={df.iloc[x,4]}  
allowedPlmnList   
cellReselectionPriority {df.iloc[x,df.columns.tolist().index("cellReselectionPriority".upper())]}  
connectedModeMobilityPrio {df.iloc[x,df.columns.tolist().index("connectedModeMobilityPrio".upper())]} 
endcB1MeasPriority {df.iloc[x,df.columns.tolist().index("endcB1MeasPriority".upper())]} 
gUtranSyncSignalFrequencyRef {df.iloc[x,df.columns.tolist().index("gUtranSyncSignalFrequencyRef".upper())]} 
pMaxNR {df.iloc[x,df.columns.tolist().index("pMaxNR".upper())]}   
qOffsetFreq {df.iloc[x,df.columns.tolist().index("qOffsetFreq".upper())]} 
qRxLevMin {df.iloc[x,df.columns.tolist().index("qRxLevMin".upper())]} 
threshXHigh {df.iloc[x,df.columns.tolist().index("threshXHigh".upper())]}   
threshXLow {df.iloc[x,df.columns.tolist().index("threshXLow".upper())]}  
end \n''')
            pointer = pointer + ecount
            ######print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_GUtranFreqRelation.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_GUtranFreqRelation_DUS.mos".format(output_dir, folder_name, prefix)
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




    
    
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    ##############################################################################################################################################
    

    #crn ENodeBFunction=1,EUtranCellFDD=CMI0024P_9NB01_S01,GUtranFreqRelation=152690-15
    #allowedPlmnList
    #cellReselectionPriority -1
    #connectedModeMobilityPrio 6
    #endcB1MeasPriority 5
    #gUtranSyncSignalFrequencyRef GUtraNetwork=1,GUtranSyncSignalFrequency=152690-15
    #pMaxNR 33
    #qOffsetFreq 0
    #qRxLevMin -140
    #threshXHigh 4
    #threshXLow 0
    #end

    ## ADD_ExternalGUtranCell

    sheet = sheet_list[3] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
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
    for y in range (0,unique_node_count):
        with open('ADD_ExternalGUtranCell.mos', 'w') as f:
            sys.stdout = f
            ######print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            ####print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                print(f'''crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction={df.iloc[x,2]},ExternalGUtranCell={df.iloc[x,4]}  \nabsSubFrameOffset 0  \nabsTimeOffset 0  \ngUtranSyncSignalFrequencyRef GUtraNetwork=1,GUtranSyncSignalFrequency={df.iloc[x,5]}   \nisRemoveAllowed {df.iloc[x,6]} \nlocalCellId {df.iloc[x,7]}  \nphysicalLayerCellIdGroup {df.iloc[x,8]}  \nphysicalLayerSubCellId {df.iloc[x,9]}  \nend  \n''')
            pointer = pointer + ecount
            ######print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_ExternalGUtranCell.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_ExternalGUtranCell.mos".format(output_dir, folder_name, prefix)
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

    #crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=AYT0171P_9NB01,ExternalGUtranCell=5204-0000000000107673-1001
    #absSubFrameOffset 0
    #absTimeOffset 0
    #gUtranSyncSignalFrequencyRef GUtraNetwork=1,GUtranSyncSignalFrequency=152690-15
    #isRemoveAllowed False
    #localCellId 1001
    #physicalLayerCellIdGroup 18
    #physicalLayerSubCellId 0
    #end

    ## ADD_GUtranCellRelation

    sheet = sheet_list[4] 
    df = pd.read_excel(io=file_name, sheet_name=sheet)
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
    for y in range (0,unique_node_count):
        with open('ADD_GUtranCellRelation.mos', 'w') as f:
            sys.stdout = f
            ######print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            ####print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                print(f'''crn ENodeBFunction=1,EUtranCell{df.iloc[x,3]}={df.iloc[x,2]},GUtranFreqRelation={df.iloc[x,7]},GUtranCellRelation={df.iloc[x,8]} \nessEnabled {df.iloc[x,9]} \nisRemoveAllowed  {df.iloc[x,10]} \nneighborCellRef  {df.iloc[x,11]} \nuserLabel \nend  \n''')
                print(f'''set ENodeBFunction=1,EUtranCell{df.iloc[x,3]}={df.iloc[x,2]},GUtranFreqRelation={df.iloc[x,7]},GUtranCellRelation={df.iloc[x,8]}$ isRemoveAllowed  {df.iloc[x,10]}''')
            pointer = pointer + ecount
            ######print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_GUtranCellRelation.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_GUtranCellRelation.mos".format(output_dir, folder_name, prefix)
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


    with open( 'sites_list.txt','w') as f :
        sys.stdout = f
        unique_node_values = Counter(site_list_array)
        for item in unique_node_values :
            print(item)

    sys.stdout = original_stdout


    os.chdir(cwd)
    return new_dir

    ##Anchor#
    #crn ENodeBFunction=1,EUtranCellFDD=CMI0024P_9NB01_S01,GUtranFreqRelation=152690-15,GUtranCellRelation=5204-0000000000135912-1002
    #essEnabled False
    #isRemoveAllowed False
    #neighborCellRef GUtraNetwork=1,ExternalGNodeBFunction=CMI6896P_9NB01,ExternalGUtranCell=5204-0000000000135912-1002
    #userLabel
    #end
    #
    #set ENodeBFunction=1,EUtranCellFDD=CMI0024P_9NB01_S01,GUtranFreqRelation=152690-15,GUtranCellRelation=5204-0000000000135912-1002$ isRemoveAllowed False

