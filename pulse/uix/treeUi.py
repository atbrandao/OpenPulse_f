from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QBrush, QColor, QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt

class TreeUi(QTreeWidget):
    def __init__(self, main_window):
        super().__init__()
        self.mainWindow = main_window
        self._createNames()
        self._createIcons()
        self._createFonts()
        self._createColorsBrush()
        self._configTree()
        self._createItems()
        self._configItems()
        self._addItems()
        self._updateItems()

    def _createNames(self):
        self.name_top_structuralmodelSetup = "Structural Model Setup"
        self.name_child_set_material = "Set Material"
        self.name_child_set_crossSection = "Set Cross-Section"
        self.name_child_setElementType = "Set Element Type"
        self.name_child_setPrescribedDofs = "Set Prescribed DOFs"
        self.name_child_setNodalLoads = "Set Nodal Loads"
        self.name_child_addMassSpringDamper = "Add: Mass / Spring / Damper"

        self.name_top_acousticmodelSetup = "Acoustic Model Setup"
        self.name_child_set_fluid = "Set Fluid"
        self.name_child_setAcousticPressure = "Set Acoustic Pressure"
        self.name_child_setVolumeVelocity = "Set Volume Velocity"
        self.name_child_setSpecificImpedance = "Set Specific Impedance"
        self.name_child_setRadiationImpedance = "Set Radiation Impedance"
        
        self.name_top_analysis = "Analysis"
        self.name_child_selectAnalysisType = "Select Analysis Type"
        self.name_child_analisysSetup = "Analysis Setup"
        self.name_child_selectTheOutputResults = "Select the Outputs Results"
        self.name_child_runAnalysis = "Run Analysis"

        self.name_top_resultsViewer = "Results Viewer"
        self.name_child_plotStructuralModeShapes = "Plot Structural Mode Shapes"
        self.name_child_plotStructuralHarmonicResponse = "Plot Structural Harmonic Response"
        self.name_child_plotStructuralFrequencyResponse = "Plot Structural Frequency Response"
        self.name_child_plotStressField = "Plot Stress Field"
        self.name_child_plotAcousticModeShapes = "Plot Acoustic Mode Shapes"
        self.name_child_plotAcousticHarmonicResponse = "Plot Acoustic Harmonic Response"
        self.name_child_plotAcousticFrequencyResponse = "Plot Acoustic Frequency Response"
        self.name_child_plot_TL_NR = "Plot Transmission Loss or Attenuation"
        self.name_child_plot_reactions = "Plot Reactions"


    def _createIcons(self):
        self.icon_child_set_material = QIcon()
        self.icon_child_set_material.addPixmap(QPixmap("pulse/data/icons/pulse.png"), QIcon.Active, QIcon.On)

    def _createFonts(self):
        self.font_top = QFont()
        #self.font_child = QFont()

        self.font_top.setFamily("Segoe UI")
        self.font_top.setPointSize(10)
        self.font_top.setBold(True)
        self.font_top.setItalic(True)
        self.font_top.setWeight(75)

    def _createColorsBrush(self):
        #color_top = QColor(39, 180, 211)
        color_top = QColor(178, 178, 178)
        #color_child = QColor(0, 0, 0)
        self.brush_top = QBrush(color_top)
        self.brush_top.setStyle(Qt.SolidPattern)

    def _configTree(self):
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setTabKeyNavigation(True)
        self.setIndentation(0)
        self.itemClicked.connect(self.on_click_item)

    def _createItems(self):
        self.item_top_structuralmodelSetup = QTreeWidgetItem([self.name_top_structuralmodelSetup])
        self.item_child_set_material = QTreeWidgetItem([self.name_child_set_material])
        self.item_child_set_crossSection = QTreeWidgetItem([self.name_child_set_crossSection])
        self.item_child_setElementType = QTreeWidgetItem([self.name_child_setElementType])
        self.item_child_setPrescribedDofs = QTreeWidgetItem([self.name_child_setPrescribedDofs])
        self.item_child_setNodalLoads = QTreeWidgetItem([self.name_child_setNodalLoads])
        self.item_child_addMassSpringDamper = QTreeWidgetItem([self.name_child_addMassSpringDamper])

        self.item_top_acousticmodelSetup = QTreeWidgetItem([self.name_top_acousticmodelSetup])
        self.item_child_set_fluid = QTreeWidgetItem([self.name_child_set_fluid])
        self.item_child_setAcousticPressure = QTreeWidgetItem([self.name_child_setAcousticPressure])
        self.item_child_setVolumeVelocity = QTreeWidgetItem([self.name_child_setVolumeVelocity])
        self.item_child_setSpecificImpedance = QTreeWidgetItem([self.name_child_setSpecificImpedance])
        self.item_child_setRadiationImpedance = QTreeWidgetItem([self.name_child_setRadiationImpedance])

        self.item_top_analysis = QTreeWidgetItem([self.name_top_analysis])
        self.item_child_selectAnalysisType = QTreeWidgetItem([self.name_child_selectAnalysisType])
        self.item_child_analisysSetup = QTreeWidgetItem([self.name_child_analisysSetup])
        self.item_child_selectTheOutputResults = QTreeWidgetItem([self.name_child_selectTheOutputResults])
        self.item_child_runAnalysis = QTreeWidgetItem([self.name_child_runAnalysis])

        self.item_top_resultsViewer = QTreeWidgetItem([self.name_top_resultsViewer])
        self.item_child_plotStructuralModeShapes = QTreeWidgetItem([self.name_child_plotStructuralModeShapes])
        self.item_child_plotStructuralHarmonicResponse = QTreeWidgetItem([self.name_child_plotStructuralHarmonicResponse])
        self.item_child_plotAcousticModeShapes = QTreeWidgetItem([self.name_child_plotAcousticModeShapes])
        self.item_child_plotAcousticHarmonicResponse = QTreeWidgetItem([self.name_child_plotAcousticHarmonicResponse])
        self.item_child_plotStressField = QTreeWidgetItem([self.name_child_plotStressField])
        self.item_child_plotStructuralFrequencyResponse = QTreeWidgetItem([self.name_child_plotStructuralFrequencyResponse])
        self.item_child_plotAcousticFrequencyResponse = QTreeWidgetItem([self.name_child_plotAcousticFrequencyResponse])
        self.item_child_plot_TL_NR = QTreeWidgetItem([self.name_child_plot_TL_NR])
        self.item_child_plot_reactions = QTreeWidgetItem([self.name_child_plot_reactions])

    def _configItems(self):
        self.item_top_structuralmodelSetup.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.item_top_structuralmodelSetup.setFont(0, self.font_top)
        self.item_top_structuralmodelSetup.setTextAlignment(0, Qt.AlignHCenter)
        self.item_top_structuralmodelSetup.setBackground(0, self.brush_top)

        self.item_top_acousticmodelSetup.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.item_top_acousticmodelSetup.setFont(0, self.font_top)
        self.item_top_acousticmodelSetup.setTextAlignment(0, Qt.AlignHCenter)
        self.item_top_acousticmodelSetup.setBackground(0, self.brush_top)

        self.item_top_analysis.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.item_top_analysis.setFont(0, self.font_top)
        self.item_top_analysis.setTextAlignment(0, Qt.AlignHCenter)
        self.item_top_analysis.setBackground(0, self.brush_top)

        self.item_top_resultsViewer.setFlags(Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled)
        self.item_top_resultsViewer.setFont(0, self.font_top)
        self.item_top_resultsViewer.setTextAlignment(0, Qt.AlignHCenter)
        self.item_top_resultsViewer.setBackground(0, self.brush_top)

        # self.item_child_setElementType.setDisabled(True)
        self.item_child_selectTheOutputResults.setDisabled(True)
        self.item_child_plotStressField.setDisabled(True)

    def _addItems(self):
        self.addTopLevelItem(self.item_top_structuralmodelSetup)
        self.addTopLevelItem(self.item_child_setElementType)
        self.addTopLevelItem(self.item_child_set_material)
        self.addTopLevelItem(self.item_child_set_crossSection)
        self.addTopLevelItem(self.item_child_setPrescribedDofs)
        self.addTopLevelItem(self.item_child_setNodalLoads)
        self.addTopLevelItem(self.item_child_addMassSpringDamper)

        self.addTopLevelItem(self.item_top_acousticmodelSetup)      
        self.addTopLevelItem(self.item_child_set_fluid)             
        self.addTopLevelItem(self.item_child_setAcousticPressure) 
        self.addTopLevelItem(self.item_child_setVolumeVelocity)     
        self.addTopLevelItem(self.item_child_setSpecificImpedance)
        self.addTopLevelItem(self.item_child_setRadiationImpedance)     

        self.addTopLevelItem(self.item_top_analysis)
        self.addTopLevelItem(self.item_child_selectAnalysisType)
        self.addTopLevelItem(self.item_child_analisysSetup)
        self.addTopLevelItem(self.item_child_selectTheOutputResults)
        self.addTopLevelItem(self.item_child_runAnalysis)

        self.addTopLevelItem(self.item_top_resultsViewer)
        self.addTopLevelItem(self.item_child_plotStructuralModeShapes)
        self.addTopLevelItem(self.item_child_plotStructuralHarmonicResponse)
        self.addTopLevelItem(self.item_child_plotStructuralFrequencyResponse)
        self.addTopLevelItem(self.item_child_plotStressField)
        self.addTopLevelItem(self.item_child_plotAcousticModeShapes)
        self.addTopLevelItem(self.item_child_plotAcousticHarmonicResponse)
        self.addTopLevelItem(self.item_child_plotAcousticFrequencyResponse)
        self.addTopLevelItem(self.item_child_plot_TL_NR)
        self.addTopLevelItem(self.item_child_plot_reactions)

        
    def on_click_item(self, item, column):
        if item.text(0) == self.name_child_set_material:
            self.mainWindow.getInputWidget().set_material()
        elif item.text(0) == self.name_child_set_fluid: 
            self.mainWindow.getInputWidget().set_fluid()
        elif item.text(0) == self.name_child_setAcousticPressure:
            self.mainWindow.getInputWidget().setAcousticPressure()
        elif item.text(0) == self.name_child_setVolumeVelocity: 
            self.mainWindow.getInputWidget().setVolumeVelocity()
        elif item.text(0) == self.name_child_setSpecificImpedance:
            self.mainWindow.getInputWidget().setSpecificImpedance()
        elif item.text(0) == self.name_child_setRadiationImpedance:
            self.mainWindow.getInputWidget().setRadiationImpedance()
        elif item.text(0) == self.name_child_set_crossSection:
            self.mainWindow.getInputWidget().set_crossSection()
        elif item.text(0) == self.name_child_setElementType:
            self.mainWindow.getInputWidget().setElementType()
        elif item.text(0) == self.name_child_setPrescribedDofs:
            self.mainWindow.getInputWidget().setDOF()
        elif item.text(0) == self.name_child_setNodalLoads:
            self.mainWindow.getInputWidget().setNodalLoads()
        elif item.text(0) == self.name_child_addMassSpringDamper:
            self.mainWindow.getInputWidget().addMassSpringDamper()
        elif item.text(0) == self.name_child_selectAnalysisType:
            self.mainWindow.getInputWidget().analysisTypeInput()
            self._updateItems()
        elif item.text(0) == self.name_child_analisysSetup:
            self.mainWindow.getInputWidget().analysisSetup()
        elif item.text(0) == self.name_child_selectTheOutputResults:
            self.mainWindow.getInputWidget().analysisOutputResults()
        elif item.text(0) == self.name_child_runAnalysis:
            self.mainWindow.getInputWidget().runAnalysis()
            self._updateItems()
        elif item.text(0) == self.name_child_plotStructuralModeShapes:
            self.mainWindow.getInputWidget().plotStructuralModeShapes()
        elif item.text(0) == self.name_child_plotStructuralHarmonicResponse:
            self.mainWindow.getInputWidget().plotStructuralHarmonicResponse()
        elif item.text(0) == self.name_child_plotAcousticModeShapes:
            self.mainWindow.getInputWidget().plotAcousticModeShapes()
        elif item.text(0) == self.name_child_plotAcousticHarmonicResponse:
            self.mainWindow.getInputWidget().plotAcousticHarmonicResponse()
        elif item.text(0) == self.name_child_plotStressField:
            self.mainWindow.getInputWidget().plotStressField()
        elif item.text(0) == self.name_child_plotStructuralFrequencyResponse:
            self.mainWindow.getInputWidget().plotStructuralFrequencyResponse()
        elif item.text(0) == self.name_child_plotAcousticFrequencyResponse:
            self.mainWindow.getInputWidget().plotAcousticFrequencyResponse()
        elif item.text(0) == self.name_child_plot_TL_NR:
            self.mainWindow.getInputWidget().plot_TL_NR()
        elif item.text(0) == self.name_child_plot_reactions:
            self.mainWindow.getInputWidget().plot_reactions()


    def _updateItems(self):
        project = self.mainWindow.getProject()

        if True:
            self.item_child_plotStructuralModeShapes.setDisabled(True)
            self.item_child_plotStructuralHarmonicResponse.setDisabled(True)
            self.item_child_plotStructuralFrequencyResponse.setDisabled(True)
            self.item_child_plotAcousticModeShapes.setDisabled(True)
            self.item_child_plotAcousticFrequencyResponse.setDisabled(True)
            self.item_child_plotAcousticHarmonicResponse.setDisabled(True)
            self.item_child_plot_TL_NR.setDisabled(True)
            self.item_child_plot_reactions.setDisabled(True)
        
        if project.get_structural_solution() is not None or project.get_acoustic_solution() is not None:
        
            if project.analysis_ID == 0 or project.analysis_ID == 1:
                self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
                self.item_child_plotStructuralHarmonicResponse.setDisabled(False)
                self.item_child_plot_reactions.setDisabled(False)
            elif project.analysis_ID == 2:
                self.item_child_plotStructuralModeShapes.setDisabled(False)
            elif project.analysis_ID == 4:
                self.item_child_plotAcousticModeShapes.setDisabled(False)
            elif project.analysis_ID == 3:
                self.item_child_plotAcousticFrequencyResponse.setDisabled(False)
                self.item_child_plotAcousticHarmonicResponse.setDisabled(False)
                self.item_child_plot_TL_NR.setDisabled(False)
            elif project.analysis_ID in [5,6]:
                self.item_child_plotStructuralFrequencyResponse.setDisabled(False)
                self.item_child_plotAcousticFrequencyResponse.setDisabled(False)
                self.item_child_plotStructuralHarmonicResponse.setDisabled(False)
                self.item_child_plotAcousticHarmonicResponse.setDisabled(False)
                self.item_child_plot_TL_NR.setDisabled(False)
                self.item_child_plot_reactions.setDisabled(False)     
