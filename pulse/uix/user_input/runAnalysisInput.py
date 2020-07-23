from PyQt5.QtWidgets import QLineEdit, QDialog, QTreeWidget, QRadioButton, QTreeWidgetItem, QTabWidget, QLabel, QCheckBox
from pulse.utils import error
from os.path import basename
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import uic
from time import time
import configparser

from pulse.processing.solution_structural import *

class RunAnalysisInput(QDialog):
    def __init__(self, solve, analysis_ID, analysis_type, frequencies, modes, damping, project=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('pulse/uix/user_input/ui/runAnalysisInput.ui', self)

        icons_path = 'pulse\\data\\icons\\'
        self.icon = QIcon(icons_path + 'pulse.png')
        self.setWindowIcon(self.icon)

        self.project = project
        self.solve = solve
        self.analysis_ID = analysis_ID
        self.analysis_type = analysis_type
        self.frequencies = frequencies
        self.damping = damping
        self.modes = modes
        # self.solution = None
        self.solution_acoustic = None
        self.solution_structural = None
        self.natural_frequencies_acoustic = []
        self.natural_frequencies_structural = []

        self.label_title = self.findChild(QLabel, 'label_title')

        self.run()
        self.exec_()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()

    def run(self):
        t0 = time()
        if self.analysis_ID == 0:
            self.solution_structural = self.solve.direct_method(self.damping) # Structural Harmonic Analysis - Direct Method
            self.dict_reactions_at_constrained_dofs = self.solve.get_reactions_at_fixed_nodes(self.damping)
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = self.solve.get_reactions_at_springs_and_dampers()
        elif self.analysis_ID == 1: # Structural Harmonic Analysis - Mode Superposition Method
            self.solution_structural = self.solve.mode_superposition(self.modes, self.damping)
            self.dict_reactions_at_constrained_dofs = self.solve.get_reactions_at_fixed_nodes(self.damping)
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = self.solve.get_reactions_at_springs_and_dampers()
        elif self.analysis_ID == 3: # Acoustic Harmonic Analysis - Direct Method
            self.solution_acoustic = self.solve.direct_method()
        elif self.analysis_ID == 5: # Coupled Harmonic Analysis - Direct Method
            self.solution_acoustic = self.solve.direct_method() #Acoustic Harmonic Analysis - Direct Method
            self.project.set_acoustic_solution(self.solution_acoustic)
            self.solve = self.project.get_structural_solve()
            self.solution_structural = self.solve.direct_method(self.damping) #Coupled Harmonic Analysis - Direct Method
            self.dict_reactions_at_constrained_dofs = self.solve.get_reactions_at_fixed_nodes(self.damping)
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = self.solve.get_reactions_at_springs_and_dampers()
        elif self.analysis_ID == 6: # Coupled Harmonic Analysis - Mode Superposition Method
            self.solution_acoustic = self.solve.direct_method() #Acoustic Harmonic Analysis - Direct Method
            self.project.set_acoustic_solution(self.solution_acoustic)
            self.solve = self.project.get_structural_solve()
            self.solution_structural = self.solve.mode_superposition(self.modes, self.damping)
            self.dict_reactions_at_constrained_dofs = self.solve.get_reactions_at_fixed_nodes(self.damping)
            self.dict_reactions_at_springs, self.dict_reactions_at_dampers = self.solve.get_reactions_at_springs_and_dampers()
        elif self.analysis_ID == 2: # Structural Modal Analysis
            self.natural_frequencies_structural, self.solution_structural = self.solve.modal_analysis(modes = self.modes)
        elif self.analysis_ID == 4: # Acoustic Modal Analysis
            self.natural_frequencies_acoustic, self.solution_acoustic = self.solve.modal_analysis(modes = self.modes)
        dt = time() - t0

        text = "Solution finished!\n"
        text += "Time elapsed: {} [s]\n".format(dt)
        text += "Press ESC to continue..."
        self.label_title.setText(text)

        # WARNINGS REACHED DURING SOLUTION
        if self.analysis_type == "Harmonic Analysis - Structural":
            if self.solve.flag_ModeSup_prescribed_NonNull_DOFs:
                error(self.solve.warning_ModeSup_prescribedDOFs, title = "WARNING")
            if self.solve.flag_Clump and self.analysis_ID==1:
                error(self.solve.warning_Clump[0], title = "WARNING")
        if self.analysis_type == "Modal Analysis - Structural":
            if self.solve.flag_Modal_prescribed_NonNull_DOFs:
                error(self.solve.warning_Modal_prescribedDOFs[0], title = "WARNING")