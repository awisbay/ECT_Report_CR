##########################################################################################################################################################################################   
#
#   Thailand TRUE - DTAC ECT Merge Co. Project    
#   Post Cutover CR Automation    
#   Prgram Requester   ::   Andika Mulyawan
#   Program Developer  ::   RDC/COE - Avisek Mukherjee [eavmukh]
#   Program Executor   ::   Ericsson SDU Team 
#   Tools Needed       ::   Cygwin / Debian [ Windows Based Linux Subsystem] 
#                      ::   Python 3.11
#                      ::   Packages include : "Pandas" , "Openpyxl" , "Numpy"     
#    
#   Python Script/Tool Name          ::   "" NRCellrelation_XXX_Neighbor_XXX_DTAC_Cygwin.py  ""
#   Process            ::
#       1. Create a Folder under C:\cygwin64\home\"signum"\  with name  " CR_AUTO_7 "  
#       2. Keep the Python script and CR Excel Input file for e.g. "05_CR882310EACRIHS691_NRCellrelation_CMI0024_Neighbor_05-Oct-2023_DTAC.xlsx " in the CR_AUTO_7 folder.
#       3. put the command "python  NRCellrelation_XXX_Neighbor_XXX_DTAC_Cygwin.py
#       4. Please enter your Ericsson signum  :                
#       5. Please Enter the name of the NRCellrelation_XXX_Neighbor_XXX_DTAC_Cygwin CR Excel including the .xlsx part   :
#       6. Please Enter the name of the CR Number  :       e.g. CR882310ENCASHI023
#
##########################################################################################################################################################################################


import pandas as pd
import os
import sys
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

    #cr_file_name =  re.search(r"_(CR.*?)_", selected_file).group(1) if re.search(r"_(CR.*?)_", selected_file).group(1) else f"{selected_file}"
    cr_file_name_1 =  re.search(r"(\d+.*?)\.xlsx", selected_file).group(1) if re.search(r"(\d+.*?)\.xlsx", selected_file).group(1) else f"{selected_file}"
    cr_file_name = cr_file_name_1.replace("-", "_")
    number_cr = re.search(r"(\d+)\_CR.*?$", selected_file).group(1)
    customer = re.search(r".*(True|DTAC).*?$", selected_file, re.IGNORECASE).group(1)
    crn = f"{number_cr}_" +cr_file_name[:8]
    file_name =file_path

    ds = pd.read_excel(file_name, None)     ## ds - Reads the Whole File
    sheet_list = list(ds.keys())            ## Reads the sheet names and puts in the list 
    unique_node_values = []
    print(sheet_list)
    original_stdout = sys.stdout
    cwd = os.getcwd()

    site_list_array = []

    #folder_name = crn +"_NRCellrelation_XXX_Neighbor_XXX_"+ customer + today.strftime('_%Y%m%d_%H%M%S')
    folder_name = cr_file_name
    
    new_dir = os.path.join( output_dir,folder_name)        
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


"""
        print(f"lcd  ~/PATH/{folder_name} \n")
        print(command)
        for item in sheet_list :
            command_item = f"run $nodename_{item}.mos"
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
'ADD_NRFrequency',
'ADD_NRFreqRelation',
'ADD_ExternalGNBCUCPFunction',
'ADD_ExternalNRCellCU',
'ADD_ExternalNRCellRelation',
'ADD_InternalNRCellRelation'    
    ]]
    sheet_list = [value for value in sheet_list if value in [
'ADD_NRFrequency',
'ADD_NRFreqRelation',
'ADD_ExternalGNBCUCPFunction',
'ADD_ExternalNRCellCU',
'ADD_ExternalNRCellRelation',
'ADD_InternalNRCellRelation' 
    ]]
    
    sheet_list = [
'ADD_NRFrequency',
'ADD_NRFreqRelation',
'ADD_ExternalGNBCUCPFunction',
'ADD_ExternalNRCellCU',
'ADD_ExternalNRCellRelation',
'ADD_InternalNRCellRelation'    
    ]
 
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################

    #######################################################################
    #######################################################################
    ####################################################################### 

    for item_sheet in sheet_list_rdel :
    #for sheet_name, df in all_df.items():
    #############################################
    #############################################
    ########################### DEL_ExternalGNBCUCPFunction  
    #############################################
    #############################################
        ####if (sheet_name == "DEL_ExternalGNBCUCPFunction"):
        if (item_sheet.upper() == "DEL_ExternalGNBCUCPFunction".upper()):        
            sheet = item_sheet 
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


    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################
    #######################################################################










    ## ADD_NRFrequency

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
    for y in range (0,unique_node_count):
        with open('ADD_NRFrequency.mos', 'w') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                print(f'''crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency={df.iloc[x,3]}  \narfcnValueNRDl  {df.iloc[x,4]} \nbandListManual \nsmtcDuration {df.iloc[x,8]} \nsmtcOffset {df.iloc[x,7]} \nsmtcPeriodicity {df.iloc[x,6]}\nsmtcScs  {df.iloc[x,5]}  \nend  \n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_NRFrequency.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_NRFrequency.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        
    sys.stdout = original_stdout # Reset the standard output to its original value


    #crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=152690-15
    #arfcnValueNRDl 152690
    #bandListManual
    #smtcDuration 1
    #smtcOffset 1
    #smtcPeriodicity 20
    #smtcScs 15
    #end

    ## ADD_NRFreqRelation

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
    for y in range (0,unique_node_count):
        with open('ADD_NRFreqRelation.mos', 'w') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                print(f'''crn GNBCUCPFunction=1,NRCellCU={df.iloc[x,3]},NRFreqRelation={df.iloc[x,4]}  \naddSCellCandidateThresh 15 \nanrMeasOn true \ncellReselectionPriority {df.iloc[x,6]} \nnRFrequencyRef  {df.iloc[x,5]} \nend \n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_NRFreqRelation.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_NRFreqRelation.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn GNBCUCPFunction=1,NRCellCU=CMI0024L_6MM08_S11,NRFreqRelation=152690
    #addSCellCandidateThresh 15
    #anrMeasOn true
    #cellReselectionPriority 7
    #nRFrequencyRef NRNetwork=1,NRFrequency=152690-15
    #end


    ## ADD_ExternalGNBCUCPFunction
 
    
    
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
    for y in range (0,unique_node_count):
        with open('ADD_ExternalGNBCUCPFunction.mos', 'w') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f"lt all \n \nconfbd+ \ngs+\n \n")
            print(f"set AnrFunctionNR=1 anrAutoCreateXnForEndc false \nset AnrFunctionNR=1 anrCgiMeasIntraFreqEnabled false \nset AnrFunctionNR=1 anrEndcX2Enabled false \n\n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                GNBID=df.iloc[x,4]
                GNBID=check_and_set(GNBID)
                ##print(f'''crn GNBCUCPFunction=1,NRNetwork=1,ExternalGNBCUCPFunction={df.iloc[x,3]} \ngNBId  {df.iloc[x,4]} \ngNBIdLength  {df.iloc[x,5]} \nisRemoveAllowed {df.iloc[x,6]} \npLMNId {df.iloc[x,7]} \nend  \n''')
                print(f''' 
mr NCellRelation_del
ma NCellRelation_del  externalGNBCUCPFunction=auto.*{GNBID},ExternalNRCellCU= reservedby
del NCellRelation_del
bl ExternalGNBCUCPFunction=auto.*{GNBID},TermPointToGNodeB=
rdel externalGNBCUCPFunction=auto.*{GNBID}$
               
                ''')
                print(f'''crn {df.iloc[x,2]} \ngNBId  {GNBID} \ngNBIdLength  {df.iloc[x,5]} \nisRemoveAllowed {df.iloc[x,6]} \npLMNId {df.iloc[x,7]} \nend  \n''')
            pointer = pointer + ecount
            print(f"set AnrFunctionNR=1 anrAutoCreateXnForEndc true \nset AnrFunctionNR=1 anrCgiMeasIntraFreqEnabled true \nset AnrFunctionNR=1 anrEndcX2Enabled true \n\n")
            print(f"\nconfbd- \ngs-")
            oldname = r"{}\{}\ADD_ExternalGNBCUCPFunction.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_ExternalGNBCUCPFunction.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn GNBCUCPFunction=1,NRNetwork=1,ExternalGNBCUCPFunction=CMI0024P_9NB01
    #gNBId 129782
    #gNBIdLength 22
    #isRemoveAllowed False
    #pLMNId mcc=520,mnc=04
    #end

    ## ADD_ExternalNRCellCU

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
        with open('ADD_ExternalNRCellCU.mos', 'w') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                print(f'''crn {df.iloc[x,2]} \ncellLocalId {df.iloc[x,3]}\nnCI \nnRFrequencyRef {df.iloc[x,5]}\nnRPCI {df.iloc[x,6]}\nnRTAC {df.iloc[x,7]}\nplmnIdList {df.iloc[x,8]} \nsNSSAIList \nend  \n\n\n''')
                print(f'''crn {df.iloc[x,2]} \ncellLocalId {df.iloc[x,3]}\nnRFrequencyRef {df.iloc[x,5]}\nnRPCI {df.iloc[x,6]}\nnRTAC {df.iloc[x,7]}\nplmnIdList {df.iloc[x,8]} \nsNSSAIList \nend  \n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_ExternalNRCellCU.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_ExternalNRCellCU.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn GNBCUCPFunction=1,NRNetwork=1,ExternalGNBCUCPFunction=CMI0024P_9NB01,ExternalNRCellCU=CMI0024H_7NB01_S01
    #cellLocalId 1001
    #nCI
    #nRFrequencyRef NRNetwork=1,NRFrequency=152690-15
    #nRPCI 18
    #nRTAC 5202223
    #plmnIdList mcc=520,mnc=04
    #sNSSAIList
    #end


    ## ADD_ExternalNRCellRelation

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
    df.columns = df.columns.str.upper()
    for y in range (0,unique_node_count):
        with open('ADD_ExternalNRCellRelation.mos', 'w') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                ##print(f'''crn {df.iloc[x,2]} \ncellIndividualOffsetNR {df.iloc[x,6]}\ncoverageIndicator {df.iloc[x,7]}\nincludeInSIB \nisHoAllowed {df.iloc[x,8]}\nisRemoveAllowed {df.iloc[x,9]}\nnRCellRef {df.iloc[x,3]}\nnRFreqRelationRef {df.iloc[x,5]} \nribtmEnabled \nsCellCandidate {df.iloc[x,10]}\nend  \n''')           
                print(f'''crn {df.iloc[x,df.columns.tolist().index("MO".upper())]} 
cellIndividualOffsetNR {df.iloc[x,df.columns.tolist().index("cellIndividualOffsetNR".upper())]}
coverageIndicator {df.iloc[x,df.columns.tolist().index("coverageIndicator".upper())]}
includeInSIB 
isHoAllowed {df.iloc[x,df.columns.tolist().index("isHoAllowed".upper())]}
isRemoveAllowed {df.iloc[x,df.columns.tolist().index("isRemoveAllowed".upper())]}
nRCellRef {df.iloc[x,df.columns.tolist().index("nRCellRef".upper())]}
nRFreqRelationRef {df.iloc[x,df.columns.tolist().index("nRFreqRelationRef".upper())]} 
ribtmEnabled 
sCellCandidate {df.iloc[x,df.columns.tolist().index("sCellCandidate".upper())]}
end  \n''') 
                print(f'''crn {df.iloc[x,df.columns.tolist().index("MO".upper())]} 
cellIndividualOffsetNR {df.iloc[x,df.columns.tolist().index("cellIndividualOffsetNR".upper())]}
coverageIndicator {df.iloc[x,df.columns.tolist().index("coverageIndicator".upper())]} 
isHoAllowed {df.iloc[x,df.columns.tolist().index("isHoAllowed".upper())]}
isRemoveAllowed {df.iloc[x,df.columns.tolist().index("isRemoveAllowed".upper())]}
nRCellRef {df.iloc[x,df.columns.tolist().index("nRCellRef".upper())]}
nRFreqRelationRef {df.iloc[x,df.columns.tolist().index("nRFreqRelationRef".upper())]}  
sCellCandidate {df.iloc[x,df.columns.tolist().index("sCellCandidate".upper())]}
end  \n''')            
                
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_ExternalNRCellRelation.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_ExternalNRCellRelation.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        
    sys.stdout = original_stdout # Reset the standard output to its original value

    #crn GNBCUCPFunction=1,NRCellCU=CMI0024L_6MM08_S11,NRCellRelation=CMI0024H_7NB01_S01
    #cellIndividualOffsetNR 0
    #coverageIndicator 0
    #includeInSIB
    #isHoAllowed True
    #isRemoveAllowed True
    #nRCellRef NRNetwork=1,ExternalGNBCUCPFunction=CMI0024P_9NB01,ExternalNRCellCU=CMI0024H_7NB01_S01
    #nRFreqRelationRef NRCellCU=CMI0024L_6MM08_S11,NRFreqRelation=152690
    #ribtmEnabled
    #sCellCandidate 0
    #end




    ## ADD_InternalNRCellRelation

    sheet = sheet_list[5] 
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
        with open('ADD_InternalNRCellRelation.mos', 'w') as f:
            sys.stdout = f
            print(f"$password = rbs  \nuv com_username=rbs  \nuv com_password=rbs \n")
            print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                ##print(f'''crn {df.iloc[x,2]} \ncellIndividualOffsetNR {df.iloc[x,6]}\ncoverageIndicator {df.iloc[x,7]}\nincludeInSIB {df.iloc[x,10]}\nisHoAllowed {df.iloc[x,8]}\nisRemoveAllowed {df.iloc[x,9]}\nnRCellRef {df.iloc[x,3]}\nnRFreqRelationRef {df.iloc[x,5]} \nribtmEnabled {df.iloc[x,11]}\nsCellCandidate {df.iloc[x,10]}\nend  \n''')                               
                print(f'''crn {df.iloc[x,df.columns.tolist().index("MO".upper())]} 
cellIndividualOffsetNR {df.iloc[x,df.columns.tolist().index("cellIndividualOffsetNR".upper())]}
coverageIndicator {df.loc[x,"coverageIndicator".upper()]} 
includeInSIB {df.iloc[x,df.columns.tolist().index("includeInSIB".upper())]}
isHoAllowed {df.iloc[x,df.columns.tolist().index("isHoAllowed".upper())]}
isRemoveAllowed {df.iloc[x,df.columns.tolist().index("isRemoveAllowed".upper())]}
nRCellRef {df.iloc[x,df.columns.tolist().index("nRCellRef".upper())]}
nRFreqRelationRef {df.iloc[x,df.columns.tolist().index("nRFreqRelationRef".upper())]}
ribtmEnabled {df.iloc[x,df.columns.tolist().index("ribtmEnabled".upper())]}
sCellCandidate {df.iloc[x,df.columns.tolist().index("sCellCandidate".upper())]}
end\n\n''')
            for x in range(pointer,pointer+ecount) :
                ##print(f'''crn {df.iloc[x,2]} \ncellIndividualOffsetNR {df.iloc[x,6]}\ncoverageIndicator {df.iloc[x,7]}\nincludeInSIB {df.iloc[x,10]}\nisHoAllowed {df.iloc[x,8]}\nisRemoveAllowed {df.iloc[x,9]}\nnRCellRef {df.iloc[x,3]}\nnRFreqRelationRef {df.iloc[x,5]} \nribtmEnabled {df.iloc[x,11]}\nsCellCandidate {df.iloc[x,10]}\nend  \n''')                               
                print(f'''crn {df.iloc[x,df.columns.tolist().index("MO".upper())]} 
cellIndividualOffsetNR {df.iloc[x,df.columns.tolist().index("cellIndividualOffsetNR".upper())]}
coverageIndicator {df.loc[x,"coverageIndicator".upper()]} 
includeInSIB {df.iloc[x,df.columns.tolist().index("includeInSIB".upper())]}
isHoAllowed {df.iloc[x,df.columns.tolist().index("isHoAllowed".upper())]}
isRemoveAllowed {df.iloc[x,df.columns.tolist().index("isRemoveAllowed".upper())]}
nRCellRef {df.iloc[x,df.columns.tolist().index("nRCellRef".upper())]}
nRFreqRelationRef {df.iloc[x,df.columns.tolist().index("nRFreqRelationRef".upper())]}
sCellCandidate {df.iloc[x,df.columns.tolist().index("sCellCandidate".upper())]}
end\n\n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_InternalNRCellRelation.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_InternalNRCellRelation.mos".format(output_dir, folder_name, prefix)
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

    #crn GNBCUCPFunction=1,NRCellCU=CMI0024L_6MM08_S12,NRCellRelation=CMI0024L_6MM08_S11
    #cellIndividualOffsetNR 0
    #coverageIndicator 0
    #includeInSIB True
    #isHoAllowed True
    #isRemoveAllowed False
    #nRCellRef NRCellCU=CMI0024L_6MM08_S11
    #nRFreqRelationRef NRCellCU=CMI0024L_6MM08_S12,NRFreqRelation=529950
    #ribtmEnabled False
    #sCellCandidate 0
    #end