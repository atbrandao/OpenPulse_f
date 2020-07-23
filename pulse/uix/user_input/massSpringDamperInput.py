import os
from os.path import basename
import numpy as np
from PyQt5.QtWidgets import QToolButton, QFileDialog, QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QPushButton, QTabWidget, QWidget, QMessageBox, QCheckBox
from pulse.utils import error, info_messages, remove_bc_from_file
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
import configparser
from shutil import copyfile

class MassSpringDamperInput(QDialog):
    def __init__(self, project, list_node_ids, transform_points, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/addMassSpringDamperInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.transform_points = transform_points
        self.project_file_path = project.project_file_path
        self.structural_bc_info_path = project.file._nodeStructuralPath

        self.userPath = os.path.expanduser('~')
        self.new_load_path_table = ""
        self.imported_table_name = ""

        self.nodes = project.mesh.nodes
        self.loads = None
        self.nodes_typed = []
        self.imported_table = False

        self.lumped_masses = None
        self.lumped_stiffness = None
        self.lumped_dampings = None
        self.stop = False

        self.lineEdit_nodeID = self.findChild(QLineEdit, 'lineEdit_nodeID')

        self.lineEdit_Mx = self.findChild(QLineEdit, 'lineEdit_Mx')
        self.lineEdit_My = self.findChild(QLineEdit, 'lineEdit_My')
        self.lineEdit_Mz = self.findChild(QLineEdit, 'lineEdit_Mz')
        self.lineEdit_Jx = self.findChild(QLineEdit, 'lineEdit_Jx')
        self.lineEdit_Jy = self.findChild(QLineEdit, 'lineEdit_Jy')
        self.lineEdit_Jz = self.findChild(QLineEdit, 'lineEdit_Jz')

        self.lineEdit_Kx = self.findChild(QLineEdit, 'lineEdit_Kx')
        self.lineEdit_Ky = self.findChild(QLineEdit, 'lineEdit_Ky')
        self.lineEdit_Kz = self.findChild(QLineEdit, 'lineEdit_Kz')
        self.lineEdit_Krx = self.findChild(QLineEdit, 'lineEdit_Krx')
        self.lineEdit_Kry = self.findChild(QLineEdit, 'lineEdit_Kry')
        self.lineEdit_Krz = self.findChild(QLineEdit, 'lineEdit_Krz')

        self.lineEdit_Cx = self.findChild(QLineEdit, 'lineEdit_Cx')
        self.lineEdit_Cy = self.findChild(QLineEdit, 'lineEdit_Cy')
        self.lineEdit_Cz = self.findChild(QLineEdit, 'lineEdit_Cz')
        self.lineEdit_Crx = self.findChild(QLineEdit, 'lineEdit_Crx')
        self.lineEdit_Cry = self.findChild(QLineEdit, 'lineEdit_Cry')
        self.lineEdit_Crz = self.findChild(QLineEdit, 'lineEdit_Crz')

        self.lineEdit_path_table_Mx = self.findChild(QLineEdit, 'lineEdit_path_table_Mx')
        self.lineEdit_path_table_My = self.findChild(QLineEdit, 'lineEdit_path_table_My')
        self.lineEdit_path_table_Mz = self.findChild(QLineEdit, 'lineEdit_path_table_Mz')
        self.lineEdit_path_table_Jx = self.findChild(QLineEdit, 'lineEdit_path_table_Jx')
        self.lineEdit_path_table_Jy = self.findChild(QLineEdit, 'lineEdit_path_table_Jy')
        self.lineEdit_path_table_Jz = self.findChild(QLineEdit, 'lineEdit_path_table_Jz')

        self.toolButton_load_Mx_table = self.findChild(QToolButton, 'toolButton_load_Mx_table')
        self.toolButton_load_My_table = self.findChild(QToolButton, 'toolButton_load_My_table')
        self.toolButton_load_Mz_table = self.findChild(QToolButton, 'toolButton_load_Mz_table')
        self.toolButton_load_Jx_table = self.findChild(QToolButton, 'toolButton_load_Jx_table')
        self.toolButton_load_Jy_table = self.findChild(QToolButton, 'toolButton_load_Jy_table')
        self.toolButton_load_Jz_table = self.findChild(QToolButton, 'toolButton_load_Jz_table') 

        self.toolButton_load_Mx_table.clicked.connect(self.load_Mx_table)
        self.toolButton_load_My_table.clicked.connect(self.load_My_table)
        self.toolButton_load_Mz_table.clicked.connect(self.load_Mz_table)
        self.toolButton_load_Jx_table.clicked.connect(self.load_Jx_table)
        self.toolButton_load_Jy_table.clicked.connect(self.load_Jy_table)
        self.toolButton_load_Jz_table.clicked.connect(self.load_Jz_table)

        self.Mx_table = None
        self.My_table = None
        self.Mz_table = None
        self.Jx_table = None
        self.Jy_table = None
        self.Jz_table = None

        self.basename_Mx = None
        self.basename_My = None
        self.basename_Mz = None
        self.basename_Jx = None
        self.basename_Jy = None
        self.basename_Jz = None

        self.lineEdit_path_table_Kx = self.findChild(QLineEdit, 'lineEdit_path_table_Kx')
        self.lineEdit_path_table_Ky = self.findChild(QLineEdit, 'lineEdit_path_table_Ky')
        self.lineEdit_path_table_Kz = self.findChild(QLineEdit, 'lineEdit_path_table_Kz')
        self.lineEdit_path_table_Krx = self.findChild(QLineEdit, 'lineEdit_path_table_Krx')
        self.lineEdit_path_table_Kry = self.findChild(QLineEdit, 'lineEdit_path_table_Kry')
        self.lineEdit_path_table_Krz = self.findChild(QLineEdit, 'lineEdit_path_table_Krz')

        self.toolButton_load_Kx_table = self.findChild(QToolButton, 'toolButton_load_Kx_table')
        self.toolButton_load_Ky_table = self.findChild(QToolButton, 'toolButton_load_Ky_table')
        self.toolButton_load_Kz_table = self.findChild(QToolButton, 'toolButton_load_Kz_table')
        self.toolButton_load_Krx_table = self.findChild(QToolButton, 'toolButton_load_Krx_table')
        self.toolButton_load_Kry_table = self.findChild(QToolButton, 'toolButton_load_Kry_table')
        self.toolButton_load_Krz_table = self.findChild(QToolButton, 'toolButton_load_Krz_table') 

        self.toolButton_load_Kx_table.clicked.connect(self.load_Kx_table)
        self.toolButton_load_Ky_table.clicked.connect(self.load_Ky_table)
        self.toolButton_load_Kz_table.clicked.connect(self.load_Kz_table)
        self.toolButton_load_Krx_table.clicked.connect(self.load_Krx_table)
        self.toolButton_load_Kry_table.clicked.connect(self.load_Kry_table)
        self.toolButton_load_Krz_table.clicked.connect(self.load_Krz_table)

        self.Kx_table = None
        self.Ky_table = None
        self.Kz_table = None
        self.Krx_table = None
        self.Kry_table = None
        self.Krz_table = None

        self.basename_Kx = None
        self.basename_Ky = None
        self.basename_Kz = None
        self.basename_Krx = None
        self.basename_Kry = None
        self.basename_Krz = None

        self.lineEdit_path_table_Cx = self.findChild(QLineEdit, 'lineEdit_path_table_Cx')
        self.lineEdit_path_table_Cy = self.findChild(QLineEdit, 'lineEdit_path_table_Cy')
        self.lineEdit_path_table_Cz = self.findChild(QLineEdit, 'lineEdit_path_table_Cz')
        self.lineEdit_path_table_Crx = self.findChild(QLineEdit, 'lineEdit_path_table_Crx')
        self.lineEdit_path_table_Cry = self.findChild(QLineEdit, 'lineEdit_path_table_Cry')
        self.lineEdit_path_table_Crz = self.findChild(QLineEdit, 'lineEdit_path_table_Crz')

        self.toolButton_load_Cx_table = self.findChild(QToolButton, 'toolButton_load_Cx_table')
        self.toolButton_load_Cy_table = self.findChild(QToolButton, 'toolButton_load_Cy_table')
        self.toolButton_load_Cz_table = self.findChild(QToolButton, 'toolButton_load_Cz_table')
        self.toolButton_load_Crx_table = self.findChild(QToolButton, 'toolButton_load_Crx_table')
        self.toolButton_load_Cry_table = self.findChild(QToolButton, 'toolButton_load_Cry_table')
        self.toolButton_load_Crz_table = self.findChild(QToolButton, 'toolButton_load_Crz_table') 

        self.toolButton_load_Cx_table.clicked.connect(self.load_Cx_table)
        self.toolButton_load_Cy_table.clicked.connect(self.load_Cy_table)
        self.toolButton_load_Cz_table.clicked.connect(self.load_Cz_table)
        self.toolButton_load_Crx_table.clicked.connect(self.load_Crx_table)
        self.toolButton_load_Cry_table.clicked.connect(self.load_Cry_table)
        self.toolButton_load_Crz_table.clicked.connect(self.load_Crz_table)

        self.Cx_table = None
        self.Cy_table = None
        self.Cz_table = None
        self.Crx_table = None
        self.Cry_table = None
        self.Crz_table = None

        self.basename_Cx = None
        self.basename_Cy = None
        self.basename_Cz = None
        self.basename_Crx = None
        self.basename_Cry = None
        self.basename_Crz = None

        self.flag_lumped_masses = False
        self.flag_lumped_stiffness = False
        self.flag_lumped_dampings = False

        self.checkBox_remove_mass = self.findChild(QCheckBox, 'checkBox_remove_mass')
        self.checkBox_remove_spring = self.findChild(QCheckBox, 'checkBox_remove_spring')
        self.checkBox_remove_damper = self.findChild(QCheckBox, 'checkBox_remove_damper')

        self.tabWidget_external_elements = self.findChild(QTabWidget, "tabWidget_external_elements")
        self.tab_single_values = self.tabWidget_external_elements.findChild(QWidget, "tab_single_values")
        self.tab_table = self.tabWidget_external_elements.findChild(QWidget, "tab_table_values")

        self.pushButton_single_value_confirm = self.findChild(QPushButton, 'pushButton_single_value_confirm')
        self.pushButton_single_value_confirm.clicked.connect(self.check_all_single_values_inputs)

        self.pushButton_table_values_confirm = self.findChild(QPushButton, 'pushButton_table_values_confirm')
        self.pushButton_table_values_confirm.clicked.connect(self.check_all_table_values_inputs)

        self.pushButton_remove_bc_confirm = self.findChild(QPushButton, 'pushButton_remove_bc_confirm')
        self.pushButton_remove_bc_confirm.clicked.connect(self.check_remove_bc_from_node)

        self.writeNodes(list_node_ids)
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            if self.tabWidget_external_elements.currentIndex()==0:
                self.check_all_single_values_inputs()
            elif self.tabWidget_external_elements.currentIndex()==1:
                self.check_all_table_values_inputs()
        elif event.key() == Qt.Key_Escape:
            self.close()

    def writeNodes(self, list_node_ids):
        text = ""
        for node in list_node_ids:
            text += "{}, ".format(node)
        self.lineEdit_nodeID.setText(text)

    def check_input_nodes(self):
        try:
            tokens = self.lineEdit_nodeID.text().strip().split(',')
            try:
                tokens.remove('')
            except:     
                pass
            self.nodes_typed = list(map(int, tokens))

            if self.lineEdit_nodeID.text()=="":
                error("Inform a valid Node ID before to confirm the input!", title = "Error Node ID's")
                return True

        except Exception:
            error("Wrong input for Node ID's!", "Error Node ID's")
            return True

        try:
            for node in self.nodes_typed:
                self.nodes[node].external_index
        except:
            message = [" The Node ID input values must be\n major than 1 and less than {}.".format(len(self.nodes))]
            error(message[0], title = " INCORRECT NODE ID INPUT! ")
            return True
        return False

    def check_entries(self, lineEdit, label):

        self.stop = False
        if lineEdit.text() != "":
            try:
                value = float(lineEdit.text())
            except Exception:
                error("Wrong input for real part of {}!".format(label), "Error")
                self.stop = True
                return
        else:
            value = 0

        if value == 0:
            return None
        else:
            return value

    def check_single_values_lumped_masses(self):

        if self.check_input_nodes():
            self.stop = True
            return

        Mx = self.check_entries(self.lineEdit_Mx, "Mx")
        if self.stop:
            return
        My = self.check_entries(self.lineEdit_My, "My")
        if self.stop:
            return        
        Mz = self.check_entries(self.lineEdit_Mz, "Mz")
        if self.stop:
            return        
        Jx = self.check_entries(self.lineEdit_Jx, "Jx")
        if self.stop:
            return        
        Jy = self.check_entries(self.lineEdit_Jy, "Jy")
        if self.stop:
            return        
        Jz = self.check_entries(self.lineEdit_Jz, "Jz")
        if self.stop:
            return

        lumped_masses = [Mx, My, Mz, Jx, Jy, Jz]
        
        if lumped_masses.count(None) != 6:
            self.flag_lumped_masses = True
            self.lumped_masses = lumped_masses
            self.project.add_lumped_masses_by_node(self.nodes_typed, self.lumped_masses, False)
        
    def check_single_values_lumped_stiffness(self):

        if self.check_input_nodes():
            self.stop = True
            return

        Kx = self.check_entries(self.lineEdit_Kx, "Kx")
        if self.stop:
            return
        Ky = self.check_entries(self.lineEdit_Ky, "Ky")
        if self.stop:
            return        
        Kz = self.check_entries(self.lineEdit_Kz, "Kz")
        if self.stop:
            return        
        Krx = self.check_entries(self.lineEdit_Krx, "Krx")
        if self.stop:
            return        
        Kry = self.check_entries(self.lineEdit_Kry, "Kry")
        if self.stop:
            return        
        Krz = self.check_entries(self.lineEdit_Krz, "Krz")
        if self.stop:
            return

        lumped_stiffness = [Kx, Ky, Kz, Krx, Kry, Krz]
        
        if lumped_stiffness.count(None) != 6:
            self.flag_lumped_stiffness = True
            self.lumped_stiffness = lumped_stiffness
            self.project.add_lumped_stiffness_by_node(self.nodes_typed, self.lumped_stiffness, False)
 
    def check_single_values_lumped_dampings(self):

        if self.check_input_nodes():
            self.stop = True
            return

        Cx = self.check_entries(self.lineEdit_Cx, "Cx")
        if self.stop:
            return
        Cy = self.check_entries(self.lineEdit_Cy, "Cy")
        if self.stop:
            return        
        Cz = self.check_entries(self.lineEdit_Cz, "Cz")
        if self.stop:
            return        
        Crx = self.check_entries(self.lineEdit_Crx, "Crx")
        if self.stop:
            return        
        Cry = self.check_entries(self.lineEdit_Cry, "Cry")
        if self.stop:
            return        
        Crz = self.check_entries(self.lineEdit_Crz, "Crz")
        if self.stop:
            return

        lumped_dampings = [Cx, Cy, Cz, Crx, Cry, Crz]
         
        if lumped_dampings.count(None) != 6:
            self.flag_lumped_dampings = True
            self.lumped_dampings = lumped_dampings
            self.project.add_lumped_dampings_by_node(self.nodes_typed, self.lumped_dampings, False)

    def check_all_single_values_inputs(self):

        self.check_single_values_lumped_masses()
        if self.stop:
            return

        self.check_single_values_lumped_stiffness()
        if self.stop:
            return

        self.check_single_values_lumped_dampings()
        if self.stop:
            return

        if not (self.flag_lumped_masses or self.flag_lumped_stiffness or self.flag_lumped_dampings):
            error("You must to add at least one external element before confirm the input!", title = " ERROR ")
            return

        self.close()

    def load_table(self, lineEdit, text, header):
        
        self.basename = ""
        window_label = 'Choose a table to import the {} nodal load'.format(text)
        self.path_imported_table, _type = QFileDialog.getOpenFileName(None, window_label, self.userPath, 'Dat Files (*.dat)')

        if self.path_imported_table == "":
            return "", ""

        self.basename = os.path.basename(self.path_imported_table)
        lineEdit.setText(self.path_imported_table)
        if self.basename != "":
            self.imported_table_name = self.basename
        
        if "\\" in self.project_file_path:
            self.new_load_path_table = "{}\\{}".format(self.project_file_path, self.basename)
        elif "/" in self.project_file_path:
            self.new_load_path_table = "{}/{}".format(self.project_file_path, self.basename)

        try:                
            imported_file = np.loadtxt(self.path_imported_table, delimiter=",")
        except Exception as e:
            error(str(e))
            
        if imported_file.shape[1]<2:
            error("The imported table has insufficient number of columns. The spectrum \ndata must have frequencies and values columns.")
            return
    
        try:
            self.imported_values = imported_file[:,1]
            if imported_file.shape[1]>=2:

                self.frequencies = imported_file[:,0]
                self.f_min = self.frequencies[0]
                self.f_max = self.frequencies[-1]
                self.f_step = self.frequencies[1] - self.frequencies[0] 
                self.imported_table = True
               
                _values = self.imported_values
                data = np.array([self.frequencies, _values, np.zeros_like(self.frequencies)]).T
                np.savetxt(self.new_load_path_table, data, delimiter=",", header=header)

        except Exception as e:
            error(str(e))

        return self.imported_values, self.basename

    def load_Mx_table(self):
        header = "Mx || Frequency [Hz], value[kg]"
        self.Mx_table, self.basename_Mx = self.load_table(self.lineEdit_path_table_Mx, "Mx", header)

    def load_My_table(self):
        header = "My || Frequency [Hz], value[kg]"
        self.My_table, self.basename_My = self.load_table(self.lineEdit_path_table_My, "My", header)

    def load_Mz_table(self):
        header = "Mz || Frequency [Hz], value[kg]"
        self.Mz_table, self.basename_Mz = self.load_table(self.lineEdit_path_table_Mz, "Mz", header)
    
    def load_Jx_table(self):
        header = "Jx || Frequency [Hz], value[kg.m²]"
        self.Jx_table, self.basename_Jx = self.load_table(self.lineEdit_path_table_Jx, "Fx", header)
    
    def load_Jy_table(self):
        header = "Jy || Frequency [Hz], value[kg.m²]"
        self.Jy_table, self.basename_Jy = self.load_table(self.lineEdit_path_table_Jy, "Jy", header)

    def load_Jz_table(self):
        header = "Jz || Frequency [Hz], value[kg.m²]"
        self.Jz_table, self.basename_Jz = self.load_table(self.lineEdit_path_table_Jz, "Jz", header)

    def load_Kx_table(self):
        header = "Kx || Frequency [Hz], value[N/m]"
        self.Kx_table, self.basename_Kx = self.load_table(self.lineEdit_path_table_Kx, "Kx", header)

    def load_Ky_table(self):
        header = "Ky || Frequency [Hz], value[N/m]"
        self.Ky_table, self.basename_Ky = self.load_table(self.lineEdit_path_table_Ky, "Ky", header)

    def load_Kz_table(self):
        header = "Kz || Frequency [Hz], value[N/m]"
        self.Kz_table, self.basename_Kz = self.load_table(self.lineEdit_path_table_Kz, "Kz", header)

    def load_Krx_table(self):
        header = "Krx || Frequency [Hz], value[N.m/rad]"
        self.Krx_table, self.basename_Krx = self.load_table(self.lineEdit_path_table_Krx, "Krx", header)

    def load_Kry_table(self):
        header = "Kry || Frequency [Hz], value[N.m/rad]"
        self.Kry_table, self.basename_Kry = self.load_table(self.lineEdit_path_table_Kry, "Kry", header)

    def load_Krz_table(self):
        header = "Krz || Frequency [Hz], value[N.m/rad]"
        self.Krz_table, self.basename_Krz = self.load_table(self.lineEdit_path_table_Krz, "Krz", header)

    def load_Cx_table(self):
        header = "Cx || Frequency [Hz], value[N.s/m]"
        self.Cx_table, self.basename_Cx = self.load_table(self.lineEdit_path_table_Cx, "Cx", header)

    def load_Cy_table(self):
        header = "Cy || Frequency [Hz], value[N.s/m]"
        self.Cy_table, self.basename_Cy = self.load_table(self.lineEdit_path_table_Cy, "Cy", header)

    def load_Cz_table(self):
        header = "Cz || Frequency [Hz], value[N.s/m]"
        self.Cz_table, self.basename_Cz = self.load_table(self.lineEdit_path_table_Cz, "Cz", header)

    def load_Crx_table(self):
        header = "Crx || Frequency [Hz], value[N.m/rad/s]"
        self.Crx_table, self.basename_Crx = self.load_table(self.lineEdit_path_table_Crx, "Crx", header)

    def load_Cry_table(self):
        header = "Cry || Frequency [Hz], value[N.m/rad/s]"
        self.Cry_table, self.basename_Cry = self.load_table(self.lineEdit_path_table_Cry, "Cry", header)

    def load_Crz_table(self):
        header = "Crz || Frequency [Hz], value[N.m/rad/s]"
        self.Crz_table, self.basename_Crz = self.load_table(self.lineEdit_path_table_Crz, "Crz", header)
      
    def check_table_values_lumped_masses(self):

        if self.check_input_nodes():
            self.stop = True
            return

        Mx = My = Mz = None
        if self.lineEdit_path_table_Mx != "":
            if self.Mx_table is not None:
                Mx = self.Mx_table
        if self.lineEdit_path_table_My != "":
            if self.My_table is not None:
                My = self.My_table
        if self.lineEdit_path_table_Mz != "":
            if self.Mz_table is not None:
                Mz = self.Mz_table

        Jx = Jy = Jz = None
        if self.lineEdit_path_table_Jx != "":
            if self.Jx_table is not None:
                Jx = self.Jx_table
        if self.lineEdit_path_table_Jy != "":
            if self.Jy_table is not None:
                Jy = self.Jy_table
        if self.lineEdit_path_table_Jz != "":
            if self.Jz_table is not None:
                Jz = self.Jz_table
        
        lumped_masses = [Mx, My, Mz, Jx, Jy, Jz]

        if sum([1 if bc is not None else 0 for bc in lumped_masses]) != 0:
            self.flag_lumped_masses = True
            self.basenames = [self.basename_Mx, self.basename_My, self.basename_Mz, self.basename_Jx, self.basename_Jy, self.basename_Jz]
            self.lumped_masses = lumped_masses
            self.project.add_lumped_masses_by_node(self.nodes_typed, self.lumped_masses, True, table_name=self.basenames)

    def check_table_values_lumped_stiffness(self):

        if self.check_input_nodes():
            self.stop = True
            return

        Kx = Ky = Kz = None
        if self.lineEdit_path_table_Kx != "":
            if self.Kx_table is not None:
                Kx = self.Kx_table
        if self.lineEdit_path_table_Ky != "":
            if self.Ky_table is not None:
                Ky = self.Ky_table
        if self.lineEdit_path_table_Kz != "":
            if self.Kz_table is not None:
                Kz = self.Kz_table

        Krx = Kry = Krz = None
        if self.lineEdit_path_table_Krx != "":
            if self.Krx_table is not None:
                Krx = self.Krx_table
        if self.lineEdit_path_table_Kry != "":
            if self.Kry_table is not None:
                Kry = self.Kry_table
        if self.lineEdit_path_table_Krz != "":
            if self.Krz_table is not None:
                Krz = self.Krz_table
        
        lumped_stiffness = [Kx, Ky, Kz, Krx, Kry, Krz]

        if sum([1 if bc is not None else 0 for bc in lumped_stiffness]) != 0:
            self.flag_lumped_stiffness = True
            self.basenames = [self.basename_Kx, self.basename_Ky, self.basename_Kz, self.basename_Krx, self.basename_Kry, self.basename_Krz]
            self.lumped_stiffness = lumped_stiffness
            self.project.add_lumped_stiffness_by_node(self.nodes_typed, self.lumped_stiffness, True, table_name=self.basenames)

    def check_table_values_lumped_dampings(self):

        if self.check_input_nodes():
            self.stop = True
            return

        Cx = Cy = Cz = None
        if self.lineEdit_path_table_Cx != "":
            if self.Cx_table is not None:
                Cx = self.Cx_table
        if self.lineEdit_path_table_Cy != "":
            if self.Cy_table is not None:
                Cy = self.Cy_table
        if self.lineEdit_path_table_Cz != "":
            if self.Cz_table is not None:
                Cz = self.Cz_table

        Crx = Cry = Crz = None
        if self.lineEdit_path_table_Crx != "":
            if self.Crx_table is not None:
                Crx = self.Crx_table
        if self.lineEdit_path_table_Cry != "":
            if self.Cry_table is not None:
                Cry = self.Cry_table
        if self.lineEdit_path_table_Crz != "":
            if self.Crz_table is not None:
                Crz = self.Crz_table
            
        lumped_dampings = [Cx, Cy, Cz, Crx, Cry, Crz]

        if sum([1 if bc is not None else 0 for bc in lumped_dampings]) != 0:
            self.flag_lumped_dampings = True
            self.basenames = [self.basename_Cx, self.basename_Cy, self.basename_Cz, self.basename_Crx, self.basename_Cry, self.basename_Crz]
            self.lumped_dampings = lumped_dampings
            self.project.add_lumped_dampings_by_node(self.nodes_typed, self.lumped_dampings, True, table_name=self.basenames)

    def check_all_table_values_inputs(self):

        self.check_table_values_lumped_masses()
        if self.stop:
            return

        self.check_table_values_lumped_stiffness()
        if self.stop:
            return

        self.check_table_values_lumped_dampings()
        if self.stop:
            return

        if not (self.flag_lumped_masses or self.flag_lumped_stiffness or self.flag_lumped_dampings):
            error("You must to add at least one external element before confirm the input!", title = " ERROR ")
            return

        self.close()      

    def check_remove_bc_from_node(self):

        self.remove_mass = self.checkBox_remove_mass.isChecked()
        self.remove_spring = self.checkBox_remove_spring.isChecked()
        self.remove_damper = self.checkBox_remove_damper.isChecked()

        if self.check_input_nodes():
            return

        if self.remove_mass:
            key_strings = ["masses", "moments of inertia"]
            message = "The masses and moments of inertia attributed to the {} node(s) have been removed.".format(self.nodes_typed)
            remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
            self.project.mesh.add_mass_to_node(self.nodes_typed, [None, None, None, None, None, None])

        if self.remove_spring:
            key_strings = ["spring stiffness", "torsional spring stiffness"]
            message = "The stiffness (translational and tosional) attributed to the {} node(s) have been removed.".format(self.nodes_typed)
            remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
            self.project.mesh.add_spring_to_node(self.nodes_typed, [None, None, None, None, None, None])

        if self.remove_damper:
            key_strings = ["damping coefficients", "torsional damping coefficients"]
            message = "The dampings (translational and tosional) attributed to the {} node(s) have been removed.".format(self.nodes_typed)
            remove_bc_from_file(self.nodes_typed, self.structural_bc_info_path, key_strings, message)
            self.project.mesh.add_damper_to_node(self.nodes_typed, [None, None, None, None, None, None])

        self.close()