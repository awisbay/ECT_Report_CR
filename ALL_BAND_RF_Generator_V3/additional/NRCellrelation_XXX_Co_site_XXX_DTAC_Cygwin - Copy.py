##########################################################################################################################################################################################   
#
#   Thailand TRUE - DTAC ECT Merge Co. Project    
#   Post Cutover CR Automation    
#   Prgram Requester                  ::   Andika Mulyawan
#   Program Developer                 ::   RDC/COE - Avisek Mukherjee [eavmukh]
#   Program Executor                  ::   Ericsson SDU Team 
#   Tools Needed                      ::   Cygwin / Debian [ Windows Based Linux Subsystem] 
#                                     ::   Python 3.11
#                                     ::   Packages include : "Pandas" , "Openpyxl" , "Numpy"     
#    
#   Python Script/Tool Name           ::   "" NRCellrelation_XXX_Co-site_XXX_DTAC_Cygwin.py  ""
#   Process                           ::
#       1. Create a Folder under C:\cygwin64\home\"signum"\  with name  " CR_AUTO_7 "  
#       2. Keep the Python script and CR Excel Input file for e.g. "05_CR882309EACRIHS181_NRCellrelation_CMI0024_Co-site_05-Oct-2023_DTAC.xlsx " in the CR_AUTO_7 folder.
#       3. put the command "python  NRCellrelation_XXX_Co-site_XXX_DTAC_Cygwin.py
#       4. Please enter your Ericsson signum  :                
#       5. Please Enter the name of the NRCellrelation_XXX_Co-site_XXX_DTAC CR Excel including the .xlsx part  : 
#       6. Please Enter the name of the CR Number  :       e.g. CR882309EACRIHS181
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

def generate_script(workdir_path=None, file_path=None, selected_file=None, output_dir=None):

    cr_file_name =  re.search(r"_(CR.*?)_", selected_file).group(1) if re.search(r"_(CR.*?)_", selected_file).group(1) else f"{selected_file}"
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

    folder_name = crn +"_NRCellrelation_XXX_Co-site_XXX_"+ customer + today.strftime('_%Y%m%d_%H%M%S')
    new_dir = os.path.join( output_dir,folder_name)        
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
            print(f"lt all \n \nconfb+ \ngs+\n \n")
            ecount=df.iloc[pointer,column_count-1]
            prefix = df.iloc[pointer,1]
            site_list_array.append(prefix)
            for x in range(pointer,pointer+ecount) :
                ##print(f'''crn GNBCUCPFunction=1,NRNetwork=1,ExternalGNBCUCPFunction={df.iloc[x,3]} \ngNBId  {df.iloc[x,4]} \ngNBIdLength  {df.iloc[x,5]} \nisRemoveAllowed {df.iloc[x,6]} \npLMNId {df.iloc[x,7]} \nend  \n''')
                print(f'''crn {df.iloc[x,2]} \ngNBId  {df.iloc[x,4]} \ngNBIdLength  {df.iloc[x,5]} \nisRemoveAllowed {df.iloc[x,6]} \npLMNId {df.iloc[x,7]} \nend  \n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
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
                print(f'''crn {df.iloc[x,2]} \ncellLocalId {df.iloc[x,3]}\nnCI \nnRFrequencyRef {df.iloc[x,5]}\nnRPCI {df.iloc[x,6]}\nnRTAC {df.iloc[x,7]}\nplmnIdList {df.iloc[x,8]} \nsNSSAIList \nend  \n''')
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
                print(f'''crn {df.loc[x,"MO"]} \ncellIndividualOffsetNR {df.loc[x,"CELLINDIVIDUALOFFSETNR"]}\ncoverageIndicator {df.loc[x,"COVERAGEINDICATOR"]}\nincludeInSIB \nisHoAllowed {df.loc[x,"ISHOALLOWED"]}\nisRemoveAllowed {df.loc[x,"ISREMOVEALLOWED"]}\nnRCellRef {df.loc[x,"NRCELLREF"]}\nnRFreqRelationRef {df.loc[x,"NRFREQRELATIONREF"]} \nribtmEnabled \nsCellCandidate {df.loc[x,"sCellCandidate".upper()]}\nend  \n''')           
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
                print(f'''crn {df.loc[x,"MO"]} 
cellIndividualOffsetNR {df.loc[x,"cellIndividualOffsetNR".upper()]} 
coverageIndicator {df.loc[x,"coverageIndicator".upper()]} 
includeInSIB {df.loc[x,"includeInSIB".upper()]}
isHoAllowed {df.loc[x,"isHoAllowed".upper()]}
isRemoveAllowed {df.loc[x,"isRemoveAllowed".upper()]}
nRCellRef {df.loc[x,"nRCellRef".upper()]}
nRFreqRelationRef {df.loc[x,"nRFreqRelationRef".upper()]}
ribtmEnabled {df.loc[x,"ribtmEnabled".upper()]}
sCellCandidate {df.loc[x,"sCellCandidate".upper()]}
end\n\n''')
            pointer = pointer + ecount
            print(f"\nconfb- \ngs-")
            oldname = r"{}\{}\ADD_InternalNRCellRelation.mos".format(output_dir, folder_name)
            newname = r"{}\{}\{}_ADD_InternalNRCellRelation.mos".format(output_dir, folder_name, prefix)
        os.rename(oldname, newname)
        
    sys.stdout = original_stdout # Reset the standard output to its original value

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

    with open( crn +'_sites_list.txt','w') as f :
        sys.stdout = f
        unique_node_values = Counter(site_list_array)
        for item in unique_node_values :
            print(item)

    sys.stdout = original_stdout

    os.chdir(cwd)
    return new_dir
