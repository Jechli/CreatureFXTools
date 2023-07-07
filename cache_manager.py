from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import pymel.core as pm

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class CacheManager(QtWidgets.QDialog):
    
    def __init__(self, parent=maya_main_window()):
        super(CacheManager, self).__init__(parent)
        
        self.setWindowTitle("Cache Manager")
        self.setMinimumWidth(400)
        self.setWindowFlags(QtCore.Qt.Window)
        
        self.create_widgets()
        self.create_layouts()
        self.create_connections()
        
        
    def create_widgets(self):
        
        self.nDynamicsNodesLabel = QtWidgets.QLabel("nDynamics Nodes in Scene")
        self.nDynamicsNodesLabel.setStyleSheet("padding:5px;")
        
        self.warningLabel = QtWidgets.QLabel("** Changing the name of the nodes in the scene will dissociate them from their original caches")
        
        self.nDynamicsNodesList = QtWidgets.QListWidget()
        self.nDynamicsNodesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.nClothCheckBox = QtWidgets.QCheckBox("nCloth")
        self.nClothCheckBox.setChecked(True)
        self.nHairCheckBox = QtWidgets.QCheckBox("nHair")  
        
        self.nHairCheckBox.setChecked(True)
        for node in self.getNDynamicsNodes():
            self.nDynamicsNodesList.addItem(str(node))
            
        self.cacheLabel = QtWidgets.QLabel("Associated Caches")
        self.cacheLabel.setStyleSheet("padding:5px;")
        
        self.cacheList = QtWidgets.QListWidget()
        self.cacheList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.saveLocationLabel = QtWidgets.QLabel("Save Location")
        self.saveLocationEdit = QtWidgets.QLineEdit("C:/Users/J9e1n/OneDrive/Documents/maya/projects/default/cache/nCache/")
        
        self.cacheNameLabel = QtWidgets.QLabel("Cache Name")
        self.cacheNameEdit = QtWidgets.QLineEdit("general_settings")
    
        self.saveLocationDialog = QtWidgets.QFileDialog()
        self.saveLocationDialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        
        self.saveButton = QtWidgets.QPushButton("Save Cache")
        self.assignButton = QtWidgets.QPushButton("Assign Cache")
        
        self.checkBox1 = QtWidgets.QCheckBox("Check box 1")
        self.checkBox2 = QtWidgets.QCheckBox("Check box 2")
        self.button1 = QtWidgets.QPushButton("Button 1")
        self.button2 = QtWidgets.QPushButton("Button 2")
        
    def create_layouts(self):
        
        self.nodes_checkboxes_layout = QtWidgets.QHBoxLayout()
        self.nodes_checkboxes_layout.addWidget(self.nClothCheckBox)
        self.nodes_checkboxes_layout.addWidget(self.nHairCheckBox)
        self.nodes_list_layout = QtWidgets.QVBoxLayout()
        self.nodes_list_layout.addWidget(self.nDynamicsNodesLabel)
        self.nodes_list_layout.addWidget(self.warningLabel)
        self.nodes_list_layout.addWidget(self.nDynamicsNodesList)
        self.nodes_list_layout.addLayout(self.nodes_checkboxes_layout)
        
        self.main_layout = QtWidgets.QVBoxLayout(self)
        
        self.main_layout.addLayout(self.nodes_checkboxes_layout)
        self.main_layout.addLayout(self.nodes_list_layout)
        
        self.main_layout.addWidget(self.cacheLabel)
        self.main_layout.addWidget(self.cacheList)
        
        self.main_layout.addWidget(self.saveLocationLabel)
        self.main_layout.addWidget(self.saveLocationEdit)
        
        self.main_layout.addWidget(self.cacheNameLabel)
        self.main_layout.addWidget(self.cacheNameEdit)
        
        self.buttons_layout = QtWidgets.QHBoxLayout()
        
        self.buttons_layout.addWidget(self.saveButton)
        self.buttons_layout.addWidget(self.assignButton)
        
        self.main_layout.addLayout(self.buttons_layout)
        
        
    def create_connections(self):
        self.nClothCheckBox.toggled.connect(self.setNDynamicsNodesList)
        self.nHairCheckBox.toggled.connect(self.setNDynamicsNodesList)
        
        
    """
    Helper Functions
    """
    # cmds.ls(type=['nCloth', 'hairSystem', 'nRigid'] )
    def getNDynamicsNodes(self):
        nFilter = []
        if self.nClothCheckBox.isChecked():
            for n in pm.ls(type=['nCloth']):
                nFilter.append( n )
        if self.nHairCheckBox.isChecked():
            for n in pm.ls(type=['hairSystem']):
                nFilter.append( n )
        nFilter.sort()
        return nFilter
        
        
    def setNDynamicsNodesList(self):
        self.nDynamicsNodesList.clear()
        for node in self.getNDynamicsNodes():
            self.nDynamicsNodesList.addItem(str(node))
        
        
if __name__ == "__main__":
    try:
        ui.deleteLater()
    except:
        pass
    ui = CacheManager()
    
    try:
        ui.show()
    except:
        ui.deleteLater()