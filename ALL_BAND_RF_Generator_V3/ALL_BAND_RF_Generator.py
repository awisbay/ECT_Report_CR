import sys
import os
import pandas as pd
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QListWidget,
    QVBoxLayout,
    QPushButton,
    QWidget,
    QMessageBox,
    QLabel,
    QLineEdit,
    QProgressBar,
    QAbstractItemView
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import re
from datetime import datetime
import time
import zipfile
import sys
from collections import Counter
from additional.GUtrancellrelation_XXX_TRUE_ENM_Cygwin import generate_script as gGU
from additional.IFLB_TrueENM_XXX_Cygwin import generate_script as gIFLB
from additional.NRCellrelation_XXX_Neighbor_XXX_DTAC_Cygwin import generate_script as gNRNe
from additional.NRCellrelation_XXX_Co_site_XXX_DTAC_Cygwin import generate_script as gNRCo
from additional.add01_XXX_TRUE_ENM_Cygwin import generate_script as ADD01
from additional.add99_other_Cygwin import generate_script as ADD99
from additional.add02_ExternalGNBCUCPFunction_Cygwin import generate_script as ExternalGNBCUCPFunction_GEN


class WorkerThread(QThread):
    finished = pyqtSignal(str, dict ,str, str)
    overall_progress = pyqtSignal(int)

    def __init__(self, file_path ,selected_file, output_dir):
        super().__init__()
        self.file_path = file_path
        self.selected_file = selected_file
        self.output_dir = output_dir

    def run(self):
        # Read all sheets from the Excel file
        xl = pd.ExcelFile(self.file_path)
        sheet_names = xl.sheet_names

        all_data = {}
        total_sheets = len(sheet_names)
        cumulative_progress = 0

        for idx, sheet_name in enumerate(sheet_names, start=1):
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)
            all_data[sheet_name] = df

            # Simulate processing by sleeping for a while
            for i in range(101):
                progress_percent = int((idx / total_sheets) * 100 + (i / 100 / total_sheets) * 100)
                cumulative_progress = progress_percent
                self.overall_progress.emit(cumulative_progress)
                self.msleep(50)

        self.finished.emit(self.file_path, all_data , self.selected_file , self.output_dir)
        
class ExcelReaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    
    def initUI(self):
        self.setWindowTitle("SCRIPT GENERATOR")
        self.setGeometry(100, 100, 400, 300)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        layout = QVBoxLayout(self.central_widget)

        placeholder_style = "font-style: italic;"
        # self.input_directory = QLineEdit(self)
        # # self.input_directory.setGeometry(X, Y, Length, Hight) 
        # self.input_directory.setPlaceholderText("Input Directory to save CR_FOLDER on ENM: e.g: /home/username/")
        
        self.browse_button = QPushButton("Browse", self)
        layout.addWidget(self.browse_button)
        self.browse_button.clicked.connect(self.open_folder_dialog)

        # self.file_list = QListWidget(self)
        # # self.file_list = QListWidgetItem(self)
        # layout.addWidget(self.file_list)

        self.file_list = QListWidget(self)
        self.file_list.setSelectionMode(QAbstractItemView.MultiSelection)  # Mengaktifkan modus seleksi multiple
        layout.addWidget(self.file_list)


        self.read_button = QPushButton("Generate Script", self)
        layout.addWidget(self.read_button)
        self.read_button.clicked.connect(self.read_selected_excel)

        self.quit_button = QPushButton("Quit", self)
        layout.addWidget(self.quit_button)
        self.quit_button.clicked.connect(self.close)

        self.progress_bar = QProgressBar()
        layout.addWidget(self.progress_bar)


        self.show()


    def open_folder_dialog(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if self.folder_path:
            self.populate_file_list()

    def populate_file_list(self):
        self.file_list.clear()
        if self.folder_path:
            files = [
                file
                for file in os.listdir(self.folder_path)
                if file.lower().endswith(".xlsx")
            ]
            self.file_list.addItems(files)


    def show_success_message(self, message):
        success_box = QMessageBox()
        success_box.setIcon(QMessageBox.Information)
        success_box.setWindowTitle("Success")
        success_box.setText(message)
        success_box.exec_()

    def show_error_message(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Critical)
        error_box.setWindowTitle("Error")
        error_box.setText(message)
        error_box.exec_()


    def update_overall_progress(self, value):
        self.progress_bar.setValue(value)

    def on_thread_finished(self, file_path, all_data , selected_file , output_dir):
        sheet_array = []
        # Here, 'all_data' is a dictionary where keys are sheet names
        # and values are corresponding DataFrames
        for sheet_name, df in all_data.items():
            print(f"DataFrame loaded successfully from sheet '{sheet_name}  {file_path}':")
            print(df.head())  # Just printing the first few rows to verify
            print("=" * 40)
            sheet_array.append(sheet_name)

        if (re.search(r"(DEL_ExternalGNodeBFunction_PLMN_Cleanup|ExternalGnodeBFunction_Audit).*?$", selected_file, re.IGNORECASE)): 
            print(f"File loaded successfully: {file_path}  {selected_file}\n")
            result = ADD01(file_path=file_path,selected_file=selected_file, output_dir=output_dir, all_df=all_data , sheet_list=sheet_array)                                    
            self.show_success_message(f"Your Script Available On :\n{result}")
        elif (re.search(r"(ExternalGNBCUCPFunction).*?$", selected_file, re.IGNORECASE)):
            print(f"File loaded successfully: {file_path}  {selected_file}\n")
            result = ExternalGNBCUCPFunction_GEN(file_path=file_path,selected_file=selected_file, output_dir=output_dir, all_df=all_data , sheet_list=sheet_array)                                    
            self.show_success_message(f"Your Script Available On :\n{result}")
        elif (re.search(r"(TermPointToGNB_Audit|Decor2300_mobility|700PoolingBuffer).*?$", selected_file, re.IGNORECASE)):
            print(f"File loaded successfully: {file_path}  {selected_file}\n")
            result = ADD99(file_path=file_path,selected_file=selected_file, output_dir=output_dir, all_df=all_data , sheet_list=sheet_array)                                    
            self.show_success_message(f"Your Script Available On :\n{result}")               
        # ExternalGNBCUCPFunction
        else :
           print("Error Select Excel file:\nPlease select CR file for GeranCellRelation and UtranCellRelation Only")
           self.show_error_message(f"Error Select Excel file:\nPlease select CR file for GeranCellRelation and UtranCellRelation Only")           
            
            

    def read_selected_excel(self):
        # work_dir = os.path.dirname(os.path.abspath(__file__))

        self.dict_transmission_scheme = {
            'SINGLE_ANTENNA': 0,
        }

        work_dir = os.getcwd()
        now = datetime.today()
        self.date_now = now.strftime("%Y%m%d_%H%M%S")
        self.output_dir = os.path.join(work_dir, "output")
        self.result_dir = os.path.join(work_dir, "result")

        print(work_dir)
        selected_items = self.file_list.selectedItems()

        if not selected_items:
            return
        
        print(selected_items)

        for i in selected_items:
            
            # selected_file = selected_items[0].text()
            selected_file = i.text()
            print(f" process {selected_file}")
            # exit()
            file_path = os.path.join(self.folder_path, selected_file)

            try:
                ##excel_data = pd.read_excel(file_path, sheet_name=None)

                if (re.search(r"(GeranCellRelation|UtranCellRelation|GUtrancellrelation|IFLB|NRCellrelation).*?$", selected_file)):
                    excel_data = pd.read_excel(file_path, sheet_name=None)
                    
                    self.type_script = re.search(r"(GeranCellRelation|UtranCellRelation|GUtrancellrelation|IFLB|NRCellrelation).*?$", selected_file).group(1)
                    self.number_cr = re.search(r"(\d+)\_CR.*?$", selected_file).group(1)
                    self.customer = re.search(r".*(True|DTAC).*?$", selected_file, re.IGNORECASE).group(1)

                    
                    print(self.type_script)

                    if (self.type_script == "GeranCellRelation"):
                        self.geran_cell_relation(excel_data=excel_data, selected_file=selected_file)
                    elif (self.type_script == "UtranCellRelation"):
                        self.utran_cell_relation(excel_data=excel_data, selected_file=selected_file)
                    elif (self.type_script == "GUtrancellrelation"):
                        result = gGU(workdir_path=work_dir,file_path=file_path,selected_file=selected_file, output_dir=self.output_dir)
                        ##self.show_success_message(f"Your Script Available On :\n{result}")
                    elif (self.type_script == "IFLB"):
                        result = gIFLB(workdir_path=work_dir,file_path=file_path,selected_file=selected_file, output_dir=self.output_dir)
                        ##self.show_success_message(f"Your Script Available On :\n{result}")

                    elif (self.type_script == "NRCellrelation"):
                        if (re.search(r"(Neighbor|Co-site).*?$", selected_file, re.IGNORECASE)):
                            type_cr = re.search(r"(Neighbor|Co-site).*?$", selected_file, re.IGNORECASE).group(1)

                            if (type_cr == "Neighbor"):
                                result = gNRNe(workdir_path=work_dir,file_path=file_path,selected_file=selected_file, output_dir=self.output_dir)
                                ##self.show_success_message(f"Your Script Available On :\n{result}")

                            elif(type_cr == "Co-site"):
                                result = gNRCo(workdir_path=work_dir,file_path=file_path,selected_file=selected_file, output_dir=self.output_dir)
                                ##self.show_success_message(f"Your Script Available On :\n{result}")
                            

                ###elif (re.search(r"(DEL_ExternalGNodeBFunction_PLMN_Cleanup|ExternalGnodeBFunction_Audit|ExternalGNBCUCPFunction).*?$", selected_file, re.IGNORECASE)):                
                    ##excel_data = pd.read_excel(file_path, sheet_name=None)

                    ##result = ADD01(workdir_path=work_dir,file_path=file_path,selected_file=selected_file, output_dir=self.output_dir)                                    
                    ##self.show_success_message(f"Your Script Available On :\n{result}")

 
                    
                else :
                    ##print("Error Select Excel file:\nPlease select CR file for GeranCellRelation and UtranCellRelation Only")
                    ##self.show_error_message(f"Error Select Excel file:\nPlease select CR file for GeranCellRelation and UtranCellRelation Only")
                    self.progress_bar.setValue(0)

                    if hasattr(self, 'worker_thread') and self.worker_thread.isRunning():
                        self.worker_thread.finished.connect(lambda: self.start_worker_thread(file_path, selected_file, self.output_dir))
                    else:
                        self.start_worker_thread(file_path, selected_file, self.output_dir)



            except Exception as e:
                print(f"Error reading Excel file: {e}")
                self.show_error_message(f"Error reading Excel file: {e}")

    def start_worker_thread(self, file_path, selected_file, output_dir):
        self.worker_thread = WorkerThread(file_path, selected_file, output_dir)
        self.worker_thread.overall_progress.connect(self.update_overall_progress)
        self.worker_thread.finished.connect(self.on_thread_finished)
        self.worker_thread.start()
    
    def check_folder (self,output_dir):
        isExist_output_dir = os.path.exists(output_dir)
                            
        if not isExist_output_dir:
            os.makedirs(output_dir)
        return output_dir

    
    def geran_cell_relation(self,excel_data,selected_file):
        # print(selected_file)
        ##cr_file_name = re.search(r"_(CR.*?)_", selected_file).group(1) if re.search(r"_(CR.*?)_", selected_file).group(1) else f"{selected_file}"
        cr_file_name = re.search(r"(02_CR.*?).xlsx", selected_file).group(1) if re.search(r"(02_CR.*?).xlsx", selected_file) else f"{selected_file}"
        
        try:
            for sheet_name, df in excel_data.items():
                print(f"Sheet: {sheet_name}\n{df}\n{'='*40}")
                # ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                if (sheet_name == "2G_ADD_Internal_Relation"):

                    
                    for index, row in df.iterrows():
                        cr_no = str(row['CR No'])
                        bsc_name = str(row['BSC'])
                        cell_name = str(row['CELL'])
                        n_cell = str(row['n_cell_0'])
                        CS = str(row['CS'])

                        #cr_file_name = cr_no[:8]
                        #cr_file_name = cr_file_name[:8]
                        ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                        result_on = self.check_folder(os.path.join(ouput_result_dir,bsc_name))
                        filename = os.path.join(result_on,f"01_{sheet_name}.mo")

                        writeFile =f"""
!BSC {bsc_name} !
!CELL {cell_name} !
!n_cell_0 {n_cell} !

RLNRI:CELL={cell_name},CELLR={n_cell};
RLNRC:CELL={cell_name},CELLR={n_cell},CAND=BOTH,CS={CS},KHYST=3,KOFFSETP=0,LHYST=3,LOFFSETP=0,TRHYST=2,TROFFSETP=0,AWOFFSET=10;
RLNRC:CELL={cell_name},CELLR={n_cell},BQOFFSET=3,HIHYST=5,LOHYST=3,OFFSETP=0,BQOFFSETAFR=3;
RLNRP:CELL={cell_name},CELLR={n_cell};
"""
                        with open(filename,"a+") as file:
                            file.write(writeFile)
                        file.close()

                if (sheet_name == "2G_ADD_External_Relation"):
                    for index, row in df.iterrows():
                        cr_no = str(row['CR No'])
                        BSC = str(row['BSC'])
                        CELL = str(row['CELL'])
                        CELL_R = str(row['CELL_R _BSC'])
                        n_cell_0 = str(row['n_cell_0'])
                        CGI = str(row['CGI'])
                        BCCHNO = str(row['BCCHNO'])
                        BSIC = str(row['BSIC'])
                        CSYSTYPE = str(row['CSYSTYPE'])
                        BSPWR = str(row['BSPWR'])
                        BSTXPWR = str(row['BSTXPWR'])
                        BSRXMIN = str(row['BSRXMIN'])
                        BSRXSUFF = str(row['BSRXSUFF'])
                        MSRXMIN = str(row['MSRXMIN'])
                        MSRXSUFF = str(row['MSRXSUFF'])
                        SCHO = str(row['SCHO'])
                        MISSNM = str(row['MISSNM'])
                        AW = str(row['AW'])
                        EXTPEN = str(row['EXTPEN'])
                        MSTXPWR = str(row['MSTXPWR'])
                        LAYER = str(row['LAYER'])
                        LAYERTHR = str(row['LAYERTHR'])
                        LAYERHYST = str(row['LAYERHYST'])
                        PSSTEMP = str(row['PSSTEMP'])
                        PTIMTEMP = str(row['PTIMTEMP'])
                        #Remark = str(row['Remark'])

                        # cr_file_name = cr_no[:8]
                        #cr_file_name = cr_file_name[:8]
                        ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                        result_on = self.check_folder(os.path.join(ouput_result_dir,BSC.strip()))
                        filename = os.path.join(result_on,f"02_{sheet_name}.mo")

                        writeFile = f"""
!BSC {BSC} !
!CELL				{CELL} !
!CELL_R_BSC			{CELL_R} !
!n_cell_0			{n_cell_0} !
!CGI				{CGI} !
!BSIC				{BSIC} !
!BCCHNO				{BCCHNO} !

RLDEI:CELL={n_cell_0},CSYSTYPE={CSYSTYPE},EXT ;
RLDEC:CELL={n_cell_0},CGI={CGI},BSIC={BSIC},BCCHNO={BCCHNO} ;
RLLOC:CELL={n_cell_0},BSPWR={BSPWR},BSTXPWR={BSTXPWR},BSRXMIN={BSRXMIN},BSRXSUFF={BSRXSUFF},MSRXMIN={MSRXMIN} ;
RLLOC:CELL={n_cell_0},MSRXSUFF={MSRXSUFF},SCHO={SCHO},MISSNM={MISSNM},AW={AW},EXTPEN={EXTPEN} ;
RLCPC:CELL={n_cell_0},MSTXPWR={MSTXPWR} ;
RLLHC:CELL={n_cell_0},LAYER={LAYER},LAYERTHR={LAYERTHR},LAYERHYST={LAYERHYST},PSSTEMP={PSSTEMP},PTIMTEMP={PTIMTEMP} ;

RLNRI:CELL={CELL},CELLR={n_cell_0},SINGLE;
RLMFC:CELL={CELL},MBCCHNO=1,MRNIC;
RLNRP:CELL={CELL},CELLR=ALL;

RLDEP:CELL={n_cell_0} ;
RLLOP:CELL={n_cell_0} ;
RLLOP:CELL={n_cell_0} ;
RLCPP:CELL={n_cell_0} ;
RLLHP:CELL={n_cell_0} ;
RLNRP:CELL={CELL},CELLR=ALL,NODATA;

"""
                        with open(filename, "a+") as file:
                            file.write(writeFile)
                        file.close()
                


                if (sheet_name == "2G_InterRanMobility"):
                    for index, row in df.iterrows():
                        CR_No = str(row['CR No'])
                        ENM = str(row['ENM'])
                        BSC = str(row['BSC'])
                        GeranCell = str(row['GeranCell'])
                        MO_Class = str(row['MO Class'])
                        Parameter = str(row['Parameter'])
                        Current_Value = str(row['Current Value'])
                        New_Value = str(row['New Value'])

                        # cr_file_name = cr_no[:8]
                        #cr_file_name = cr_file_name[:8]
                        ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                        result_on = self.check_folder(os.path.join(ouput_result_dir,BSC.strip()))
                        filename = os.path.join(result_on,f"03_{sheet_name}.mo")

                        writeFile = f"""
!BSC {BSC} !
!CELL {GeranCell} !"""
                        arr_new_value = New_Value.split()
                        for item in arr_new_value:
                            text = f"RLUMC:CELL={GeranCell},ADD,UMFI={item} ,LISTTYPE=IDLE;"
                            writeFile =  "\n".join([writeFile,text])

                        # print(writeFile)
                        with open(filename, "a+") as file:
                            file.write(writeFile + "\n")
                        file.close()

            ##self.show_success_message(f"Your Script Available On :\n{ouput_result_dir}")
            print(f"Your Script Available On :\n{ouput_result_dir}")

        except IOError as e:
            print(f"File couldn't be opened: {e}")
            self.show_error_message(f"File couldn't be opened: {e}")

        

    def utran_cell_relation(self,excel_data,selected_file):
        ##cr_file_name = re.search(r"_(CR.*?)_", selected_file).group(1) if re.search(r"_(CR.*?)_", selected_file) else f"{selected_file}"
        ##part_TD = re.search(r"(_[DT]_)", selected_file, re.IGNORECASE).group(1) if re.search(r"_(D|T)_", selected_file).group(1) else ""
        cr_file_name = re.search(r"(03_CR.*?).xlsx", selected_file).group(1) if re.search(r"(03_CR.*?).xlsx", selected_file) else f"{selected_file}"
        ##cr_name = cr_file_name[:8]+ part_TD
        cr_name = cr_file_name
        
        node_list_array = []
        unique_node_values = []
        ouput_result_dir = ""
        sheets_selected = ["Del_InternalUtranRelation","Del_ExternalUtranCell","Del_ExternalUtranRelation","Add_InternalUtranRelation","Add_ExternalUtranCell","Add_ExternalUtranRelation","Add_ExternalUtrancell"]
        try:
            for sheet_name, df in excel_data.items():

                if sheet_name not in sheets_selected:
                    continue

                if df.empty:
                    continue

                print(f"Sheet: {sheet_name} == {cr_name}\n{df}\n{'='*40}")

                if (sheet_name == "Del_InternalUtranRelation"):
                    for index, row in df.iterrows():
                        CRNo = str(row['CR No'])
                        RNC = str(row['RNC'])
                        SourceCell = str(row['SourceCell'])
                        DestinationCell = str(row['DestinationCell'])
                        UtranRelationId = str(row['UtranRelationId'])
                        nodeRelationType = str(row['nodeRelationType'])
                        frequencyRelationType = str(row['frequencyRelationType'])
                        selectionPriority = str(row['selectionPriority'])

                        cr_file_name = cr_name if CRNo == "nan" else CRNo
                        BSC = SourceCell[:7]
                        node_list_array.append(RNC)

                        ##ouput_bukan_result_dir = os.path.join(self.output_dir, f"{self.number_cr}_{cr_file_name}_{self.type_script}_{self.customer}_{self.date_now}")
                        ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                        result_on = self.check_folder(os.path.join(ouput_result_dir,RNC.strip()))
                        filename = os.path.join(result_on,f"01_{sheet_name}.mo")

                        writeFile = f"""
DELETE
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={SourceCell},UtranRelation={UtranRelationId}"
   exception none
)
"""
                        # print (f"{CRNo} == {sheet_name} == {selected_file}")
                        with open(filename, "a+") as file:
                            file.write(writeFile + "\n")
                        file.close()

                if (sheet_name == "Del_ExternalUtranRelation"):
                    for index, row in df.iterrows():
                        CRNo = str(row['CR No'])
                        Source_RNC = str(row['Source RNC'])
                        SourceCell = str(row['SourceCell'])
                        Destination_RNC = str(row['Destination RNC'])
                        DestinationCell = str(row['DestinationCell'])
                        UtranRelationId = str(row['UtranRelationId'])
                        IurLink = str(row['IurLink'])
                        nodeRelationType = str(row['nodeRelationType'])
                        frequencyRelationType = str(row['frequencyRelationType'])
                        selectionPriority = str(row['selectionPriority'])
                        qOffset1sn = str(row['qOffset1sn'])
                        qOffset2sn = str(row['qOffset2sn'])

                        cr_file_name = cr_name if CRNo == "nan" else CRNo
                        BSC = SourceCell[:7]
                        node_list_array.append(Source_RNC)

                        ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                        result_on = self.check_folder(os.path.join(ouput_result_dir,Source_RNC.strip()))
                        filename = os.path.join(result_on,f"02_{sheet_name}.mo")

                        writeFile = f"""
DELETE
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={SourceCell},UtranRelation={UtranRelationId}"
   exception none
)
"""

                        # print (f"{CRNo} == {sheet_name} == {selected_file}")
                        with open(filename, "a+") as file:
                            file.write(writeFile + "\n")
                        file.close()





                if (sheet_name == "RDEL_ExternalUtranCell"):
                    for index, row in df.iterrows():
                        CR_No = str(row['CR No'])
                        Source_RNC = str(row['RNC'])
                        ExternalUtranCellId = str(row['ExternalUtranCellId'])
                        IurLink = str(row['IurLink'])
                        cid = str(row['cid'])
                        lac = str(row['lac'])
                        rac = str(row['rac'])
                        PSC = str(row['PSC'])
                        uarfcnDl = str(row['uarfcnDl'])
                        uarfcnUl = str(row['uarfcnUl'])
                        individualOffset = str(row['individualOffset'])
                        maxTxPowerUl = str(row['maxTxPowerUl'])
                        primaryCpichPower = str(row['primaryCpichPower'])
                        qQualMin = str(row['qQualMin'])
                        qRxLevMin = str(row['qRxLevMin'])
                        transmissionScheme = str(row['transmissionScheme'])

                        cr_file_name = cr_name if CR_No == "nan" else CR_No
                        #BSC = SourceCell[:7]
                        node_list_array.append(Source_RNC)

                        ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                        result_on = self.check_folder(os.path.join(ouput_result_dir,Source_RNC.strip()))
                        filename = os.path.join(result_on,f"03_{sheet_name}.mos")

                        writeFile = f"""
rdel ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={ExternalUtranCellId}  
"""

                        # print (f"{CRNo} == {sheet_name} == {selected_file}")
                        with open(filename, "a+") as file:
                            file.write(writeFile + "\n")
                        file.close()





                if (sheet_name == "Del_ExternalUtranCell"):
                    for index, row in df.iterrows():
                        CR_No = str(row['CR No'])
                        Source_RNC = str(row['RNC'])
                        ExternalUtranCellId = str(row['ExternalUtranCellId'])
                        IurLink = str(row['IurLink'])
                        cid = str(row['cid'])
                        lac = str(row['lac'])
                        rac = str(row['rac'])
                        PSC = str(row['PSC'])
                        uarfcnDl = str(row['uarfcnDl'])
                        uarfcnUl = str(row['uarfcnUl'])
                        individualOffset = str(row['individualOffset'])
                        maxTxPowerUl = str(row['maxTxPowerUl'])
                        primaryCpichPower = str(row['primaryCpichPower'])
                        qQualMin = str(row['qQualMin'])
                        qRxLevMin = str(row['qRxLevMin'])
                        transmissionScheme = str(row['transmissionScheme'])

                        cr_file_name = cr_name if CRNo == "nan" else CRNo
                        BSC = SourceCell[:7]
                        node_list_array.append(Source_RNC)

                        ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                        result_on = self.check_folder(os.path.join(ouput_result_dir,Source_RNC.strip()))
                        filename = os.path.join(result_on,f"03_{sheet_name}.mo")

                        writeFile = f"""
DELETE
(
   mo "ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={ExternalUtranCellId}"
   exception none
)
"""

                        # print (f"{CRNo} == {sheet_name} == {selected_file}")
                        with open(filename, "a+") as file:
                            file.write(writeFile + "\n")
                        file.close()




                if (sheet_name == "Add_InternalUtranRelation"):
                    for index, row in df.iterrows():
                        CR_No = str(row['CR No'])
                        RNC = str(row['RNC'])
                        SourceCell = str(row['SourceCell'])
                        DestinationCell = str(row['DestinationCell'])
                        UtranRelationId = str(row['UtranRelationId'])
                        nodeRelationType = str(row['nodeRelationType'])
                        frequencyRelationType = str(row['frequencyRelationType'])
                        selectionPriority = str(row['selectionPriority'])
                        qOffset2sn = str(row['qOffset2sn'])
                        loadSharingCandidate = str(row['loadSharingCandidate'])
                        mobilityRelationType = str(row['mobilityRelationType'])

                        cr_file_name = cr_name if CR_No == "nan" else CR_No
                        # BSC = SourceCell[:7]
                        node_list_array.append(RNC)

                        ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                        result_on = self.check_folder(os.path.join(ouput_result_dir,RNC.strip()))
                        filename = os.path.join(result_on,f"04_{sheet_name}.mo")

                        writeFile = f"""
CREATE
(
   parent "ManagedElement=1,RncFunction=1,UtranCell={SourceCell}"
   identity "{UtranRelationId}"
   moType UtranRelation
   exception none
   nrOfAttributes 7
   hcsSib11Config Struct
      nrOfElements 5
         hcsPrio Integer 0
         qHcs Integer 0
         penaltyTime Integer 0
         temporaryOffset1 Integer 0
         temporaryOffset2 Integer 0
   loadSharingCandidate Integer {loadSharingCandidate}
   mobilityRelationType Integer {mobilityRelationType}
   qOffset1sn Integer 0
   qOffset2sn Integer {qOffset2sn}
   selectionPriority Integer {selectionPriority}
   utranCellRef Ref "ManagedElement=1,RncFunction=1,UtranCell={DestinationCell}"
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={SourceCell},UtranRelation={DestinationCell}"
   exception none
   qOffset2sn Integer {qOffset2sn}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={SourceCell},UtranRelation={DestinationCell}"
   exception none
   selectionPriority Integer {selectionPriority}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={SourceCell},UtranRelation={DestinationCell}"
   exception none
   loadSharingCandidate Integer {loadSharingCandidate}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={SourceCell},UtranRelation={DestinationCell}"
   exception none
   mobilityRelationType Integer {mobilityRelationType}
)

"""

                        with open(filename, "a+") as file:
                            file.write(writeFile + "\n")
                        file.close()

                if (sheet_name == "Add_ExternalUtranCell" or sheet_name == "Add_ExternalUtrancell"):
                    for index, row in df.iterrows():
                        CR_No = str(row['CR No'])
                        RNC = str(row['RNC'])
                        ExternalUtranCellId = str(row['ExternalUtranCellId'])
                        IurLink = str(row['IurLink'])
                        cid = str(row['cid'])
                        lac = str(row['lac'])
                        rac = str(row['rac'])
                        PSC = str(row['PSC'])
                        uarfcnDl = str(row['uarfcnDl'])
                        uarfcnUl = str(row['uarfcnUl'])
                        individualOffset = str(row['individualOffset'])
                        maxTxPowerUl = str(row['maxTxPowerUl'])
                        primaryCpichPower = str(row['primaryCpichPower'])
                        qQualMin = str(row['qQualMin'])
                        qRxLevMin = str(row['qRxLevMin'])
                        transmissionScheme = str(row['transmissionScheme'])
                        
 
                            
                        if 'mocnCellProfileRef' in df.columns:
                            if str(row['mocnCellProfileRef']) == "nan":
                               mocnCellProfileRef = "null"
                            else:
                               ##mocnCellProfileRef_VALUE = str(row['mocnCellProfileRef'])
                               try:
                                   mocnCellProfileRef_VALUE = str(int(float(row['mocnCellProfileRef'])))
                               except ValueError:
                                   mocnCellProfileRef_VALUE = str(row['mocnCellProfileRef'])
                                                              
                               mocnCellProfileRef = f"ManagedElement=1,RncFunction=1,MocnCellProfile={mocnCellProfileRef_VALUE}"
                               
                        else:
                            mocnCellProfileRef = "null"

                        ###if mocnCellProfileRef == "1":
                        ###    MocnProfile = "MocnCellProfile=2"
                        ###elif mocnCellProfileRef == "2":
                        ###    MocnProfile = "MocnCellProfile=2"
                        ###else:
                        ###    MocnProfile = "null"

                        def check_VALUE(df, column_name, row):
                            # Check if the column exists in the DataFrame
                            if column_name not in df.columns:
                                return 0  # Return 0 if the column does not exist
                            
                            # Get the value from the row
                            value = row[column_name]
                            
                            # Extract numeric value if it matches the format "99 (xxx)", otherwise return the whole value
                            match = re.match(r"(\d+)\s*\(.*\)", str(value))
                            return int(match.group(1)) if match else value  # return the matched numeric part or the whole value
                        
                        

                        antennaPosition_latitudeSign = check_VALUE(df, 'antennaPosition_latitudeSign' , row)
                        antennaPosition_latitude = check_VALUE(df, 'antennaPosition_latitude' , row)
                        antennaPosition_longitude = check_VALUE(df, 'antennaPosition_longitude' , row)
                        ##check_VALUE(row['qRxLevMin'])
                        ##antennaPosition_latitude	antennaPosition_longitude

                        
                        cr_file_name = cr_name if CR_No == "nan" else CR_No
                        # BSC = SourceCell[:7]
                        node_list_array.append(RNC)

                        ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                        result_on = self.check_folder(os.path.join(ouput_result_dir,RNC.strip()))
                        filename = os.path.join(result_on,f"05_{sheet_name}.mo")


                        writeFile = f""" 
CREATE
(
   parent "ManagedElement=1,RncFunction=1,IurLink={IurLink}"
   identity "{ExternalUtranCellId}"
   moType ExternalUtranCell
   exception none
   nrOfAttributes 15
   cId Integer {cid}
   cellCapability Struct
      nrOfElements 8
         hsdschSupport Integer 1
         edchSupport Integer 1
         edchTti2Support Integer 1
         enhancedL2Support Integer 1
         fdpchSupport Integer 0
         cpcSupport Integer 0
         qam64MimoSupport Integer 0
         edchTti2CmSupport Integer 0
   hsAqmCongCtrlSpiSupport Array Integer 0
   hsAqmCongCtrlSupport Integer 0
   individualOffset Integer {individualOffset}
   lac Integer {lac}
   maxTxPowerUl Integer {maxTxPowerUl}
   primaryCpichPower Integer {primaryCpichPower}
   primaryScramblingCode Integer {PSC}
   qQualMin Integer {qQualMin}
   qRxLevMin Integer {qRxLevMin}
   rac Integer {rac}
   transmissionScheme Integer {self.dict_transmission_scheme[transmissionScheme]}
   uarfcnDl Integer {uarfcnDl}
   uarfcnUl Integer {uarfcnUl}
)

SET
(
   mo "ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={ExternalUtranCellId}"
   exception none
   primaryScramblingCode Integer {PSC}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={ExternalUtranCellId}"
   exception none
   individualOffset Integer {individualOffset}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={ExternalUtranCellId}"
   exception none
   maxTxPowerUl Integer {maxTxPowerUl}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={ExternalUtranCellId}"
   exception none
   primaryCpichPower Integer {primaryCpichPower}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={ExternalUtranCellId}"
   exception none
   qQualMin Integer {qQualMin}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={ExternalUtranCellId}"
   exception none
   qRxLevMin Integer {qRxLevMin}
)

SET
(
   mo "ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={ExternalUtranCellId}"
   exception none
   mocnCellProfileRef Ref "{mocnCellProfileRef}"
)


SET
(
   mo "ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={ExternalUtranCellId}"
   exception none
   antennaPosition Struct
      nrOfElements 3
         latitudeSign Integer {antennaPosition_latitudeSign}
         latitude Integer {antennaPosition_latitude}
         longitude Integer {antennaPosition_longitude}
)


"""
                        with open(filename, "a+") as file:
                            file.write(writeFile + "\n")
                        file.close()
                

                if (sheet_name == "Add_ExternalUtranRelation"):
                    for index, row in df.iterrows():
                        CR_No = str(row['CR No'])
                        RNC = str(row['Source RNC'])
                        SourceCell = str(row['SourceCell'])
                        Destination_RNC = str(row['Destination RNC'])
                        DestinationCell = str(row['DestinationCell'])
                        UtranRelationId = str(row['UtranRelationId'])
                        IurLink = str(row['IurLink'])
                        nodeRelationType = str(row['nodeRelationType'])
                        frequencyRelationType = str(row['frequencyRelationType'])
                        selectionPriority = str(row['selectionPriority'])
                        qOffset1sn = str(row['qOffset1sn'])
                        qOffset2sn = str(row['qOffset2sn'])
                        hcsSib11Config_hcsPrio = str(row['hcsSib11Config.hcsPrio'])
                        hcsSib11Config_qHcs = str(row['hcsSib11Config.qHcs'])
                        hcsSib11Config_penaltyTime = str(row['hcsSib11Config.penaltyTime'])
                        hcsSib11Config_temporaryOffset1 = str(row['hcsSib11Config.temporaryOffset1'])
                        hcsSib11Config_temporaryOffset2 = str(row['hcsSib11Config.temporaryOffset2'])
                        mobilityRelationType = str(row['mobilityRelationType'])

                        cr_file_name = cr_name if CR_No == "nan" else CR_No
                        # BSC = SourceCell[:7]
                        node_list_array.append(RNC)

                        ouput_result_dir = os.path.join(self.output_dir, f"{cr_file_name}")
                        result_on = self.check_folder(os.path.join(ouput_result_dir,RNC.strip()))
                        filename = os.path.join(result_on,f"06_{sheet_name}.mo")

                        writeFile = f""" 
CREATE
(
   parent "ManagedElement=1,RncFunction=1,UtranCell={SourceCell}"
   identity "{UtranRelationId}"
   moType UtranRelation
   exception none
   nrOfAttributes 7
   hcsSib11Config Struct
      nrOfElements 5
         hcsPrio Integer {hcsSib11Config_hcsPrio}
         qHcs Integer {hcsSib11Config_qHcs}
         penaltyTime Integer {hcsSib11Config_penaltyTime}
         temporaryOffset1 Integer {hcsSib11Config_temporaryOffset1}
         temporaryOffset2 Integer {hcsSib11Config_temporaryOffset2}
   loadSharingCandidate Integer 0
   mobilityRelationType Integer {mobilityRelationType}
   qOffset1sn Integer {qOffset1sn}
   qOffset2sn Integer {qOffset2sn}
   selectionPriority Integer {selectionPriority}
   utranCellRef Ref "ManagedElement=1,RncFunction=1,IurLink={IurLink},ExternalUtranCell={UtranRelationId}"
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={SourceCell},UtranRelation={UtranRelationId}"
   exception none
   qOffset1sn Integer {qOffset1sn}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={SourceCell},UtranRelation={UtranRelationId}"
   exception none
   qOffset2sn Integer {qOffset2sn}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={SourceCell},UtranRelation={UtranRelationId}"
   exception none
   selectionPriority Integer {selectionPriority}
)
SET
(
   mo "ManagedElement=1,RncFunction=1,UtranCell={SourceCell},UtranRelation={UtranRelationId}"
   exception none
   mobilityRelationType Integer {mobilityRelationType}
)
"""
                        with open(filename, "a+") as file:
                            file.write(writeFile + "\n")
                        file.close()



            original_stdout = sys.stdout
            filename_list = os.path.join(ouput_result_dir,f"sites_list.txt")
            with open( filename_list,'w') as f :
                sys.stdout = f
                unique_node_values = Counter(node_list_array)
                for item in unique_node_values :
                    print(item)

            sys.stdout = original_stdout


            ##self.show_success_message(f"Your Script Available On :\n{ouput_result_dir}") if ouput_result_dir else ""
            print(f"Your Script Available On :\n{ouput_result_dir}")

        except IOError as e:
            print(f"File couldn't be opened: {e}")
            self.show_error_message(f"File couldn't be opened: {e}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ExcelReaderApp()
    sys.exit(app.exec_())
