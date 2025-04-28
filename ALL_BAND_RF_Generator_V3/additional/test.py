import pandas as pd
import os
import time
import sys
import time as today
import numpy as np
from subprocess import STDOUT
import re

file_name = "aaa.xlsx"
sheet = "ADD_InternalNRCellRelation"
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
	
	
df.columns = df.columns.str.lower()	
column_count = len(df.columns)
original_stdout = sys.stdout
unique_node_count = df[enb_names].nunique()
print(unique_node_count)



output_dir=None
folder_name=None


df2 = df.sort_values(by=['2'], ascending=False)
pointer = 0
df.columns = df.columns.str.upper()
for y in range (0,unique_node_count):
    print("nah",pointer,y,ecount)
    ecount=df.iloc[pointer,column_count-1]
    prefix = df.iloc[pointer,1]
    for x in range(pointer,pointer+ecount) :
        ##print("crn [",x,"]",df.iloc[x,2]," \ncellIndividualOffsetNR {df.iloc[x,6]}\ncoverageIndica \n") 
        ##print("CEK head [",x,"]",df.loc[x,"MO"],"\n") 
        ##print("CEK head [",x,"]",df.iloc[x,2],"\n") 
        print("loop 2", x)           
    pointer = pointer + ecount



df.columns.tolist().index('MO')

print(df)
print("CEK head [",df.loc[8,"ENODE"],"]",df.loc[8,"MO"],"\n") 
print("CEK head [",df.iloc[17,1],"]",df.iloc[17,2],"\n") 
print("CEK head [",df.iloc[17,1],"]",df.iloc[17,df.columns.tolist().index('MO'.upper())],"\n") 


df.columns.tolist().index("isHoAllowed".upper())






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
        ##oldname = r"{}\{}\ADD_InternalNRCellRelation.mos".format(output_dir, folder_name)
        ##newname = r"{}\{}\{}_ADD_InternalNRCellRelation.mos".format(output_dir, folder_name, prefix)
    ##os.rename(oldname, newname)
    print("test 123")
    
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