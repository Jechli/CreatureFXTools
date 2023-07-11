from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import pymel.core as pm

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class PaintMapsManager(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(PaintMapsManager, self).__init__(parent)
        
        self.setWindowTitle("Paintmaps Manager")
        self.setMinimumWidth(400)
        self.setWindowFlags(QtCore.Qt.Window)
        #self.setStyleSheet("background-color: orange; color: blue;")
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
        
    def create_widgets(self):
        
        self.nDynamicsNodesList = QtWidgets.QListWidget()
        self.nDynamicsNodesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.nClothCheckBox = QtWidgets.QCheckBox("nCloth")
        self.nClothCheckBox.setChecked(True)
        self.nHairCheckBox = QtWidgets.QCheckBox("nHair")  
        self.nHairCheckBox.setChecked(True)
        self.nRigidCheckBox = QtWidgets.QCheckBox("nRigid")  
        self.nRigidCheckBox.setChecked(True)
        for node in self.getNDynamicsNodes():
            self.nDynamicsNodesList.addItem(str(node))
        
        self.saveLocationLabel = QtWidgets.QLabel("Save Location")
        self.saveLocationEdit = QtWidgets.QLineEdit("Choose file")
    
        self.saveLocationDialog = QtWidgets.QFileDialog()
        self.saveLocationDialog.setFileMode(QtWidgets.QFileDialog.AnyFile)

        
        self.mapNameLabel = QtWidgets.QLabel("Map Name")
        self.mapNameEdit = QtWidgets.QLineEdit("name")
        
        self.mapAttrLabel = QtWidgets.QLabel("Map Attributes")
        self.mapAttrList = QtWidgets.QListWidget()
        self.mapAttrList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.mapAttrList.addItem("hello")
        self.mapAttrList.addItem("what")
        
        self.saveButton = QtWidgets.QPushButton("Save Map(s)")
        
        self.checkBox1 = QtWidgets.QCheckBox("Check box 1")
        self.checkBox2 = QtWidgets.QCheckBox("Check box 2")
        self.button1 = QtWidgets.QPushButton("Button 1")
        self.button2 = QtWidgets.QPushButton("Button 2")
        
    def create_layouts(self):
        
        self.nodes_checkboxes_layout = QtWidgets.QHBoxLayout()
        self.nodes_checkboxes_layout.addWidget(self.nClothCheckBox)
        self.nodes_checkboxes_layout.addWidget(self.nHairCheckBox)
        self.nodes_checkboxes_layout.addWidget(self.nRigidCheckBox)
        self.nodes_list_layout = QtWidgets.QVBoxLayout()
        self.nodes_list_layout.addWidget(self.nDynamicsNodesList)
        self.nodes_list_layout.addLayout(self.nodes_checkboxes_layout)
        
        self.main_layout = QtWidgets.QVBoxLayout(self)
        
        self.main_layout.addLayout(self.nodes_checkboxes_layout)
        self.main_layout.addLayout(self.nodes_list_layout)
        
        self.main_layout.addWidget(self.saveLocationLabel)
        self.main_layout.addWidget(self.saveLocationEdit)
        
        self.main_layout.addWidget(self.mapNameLabel)
        self.main_layout.addWidget(self.mapNameEdit)
        
        self.main_layout.addWidget(self.mapAttrLabel)
        self.main_layout.addWidget(self.mapAttrList)
        
        self.main_layout.addWidget(self.saveButton)
        
        #main_layout.addWidget(self.selectedMesh)
        #main_layout.addWidget(self.saveLocation)
        
    def create_connections(self):
        self.nClothCheckBox.toggled.connect(self.setNDynamicsNodesList)
        self.nHairCheckBox.toggled.connect(self.setNDynamicsNodesList)
        self.nRigidCheckBox.toggled.connect(self.setNDynamicsNodesList)
        
        
    """
    Helper Functions
    """
    def getNDynamicsNodes(self):
        nFilter = []
        if self.nClothCheckBox.isChecked():
            for n in pm.ls(type=['nCloth']):
                nFilter.append( n )
        if self.nHairCheckBox.isChecked():
            for n in pm.ls(type=['hairSystem']):
                nFilter.append( n )
        if self.nRigidCheckBox.isChecked():
            for n in pm.ls(type=['nRigid']):
                nFilter.append( n )
        nFilter.sort()
        return nFilter
        
        
    def setNDynamicsNodesList(self):
        self.nDynamicsNodesList.clear()
        for node in self.getNDynamicsNodes():
            self.nDynamicsNodesList.addItem(str(node))
        
"""
Run Window
"""        
if __name__ == "__main__":
    try:
        ui.deleteLater()
    except:
        pass
    ui = PaintMapsManager()
    
    try:
        ui.show()
    except:
        ui.deleteLater()