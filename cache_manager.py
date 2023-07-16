from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import pymel.core as pm
import os

"""
TURN OFF CACHED PLAYBACK TO USE THIS TOOL PROPERLY
"""

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
        
        self.default_file_loc = "C:/Users/J9e1n/OneDrive/Documents/maya/projects/default/cache/nCache/";
        
        self.ndynamics_nodes_label = QtWidgets.QLabel("nDynamics Nodes in Scene")
        self.ndynamics_nodes_label.setStyleSheet("padding:5px; font-weight:bold;")
        
        self.warning_label = QtWidgets.QLabel("** Changing the name of the nodes in the scene will dissociate them from their original caches")
        
        self.ndynamics_nodes_list = QtWidgets.QListWidget()
        self.ndynamics_nodes_list.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.nClothCheckBox = QtWidgets.QCheckBox("nCloth")
        self.nClothCheckBox.setChecked(True)
        self.nHairCheckBox = QtWidgets.QCheckBox("nHair")  
        self.nHairCheckBox.setChecked(True)
        self.refreshButton = QtWidgets.QPushButton("Refresh Nodes List")
        
        for node in self.getNDynamicsNodes():
            self.ndynamics_nodes_list.addItem(str(node))
            
        self.cacheLabel = QtWidgets.QLabel("Previous Caches")
        self.cacheLabel.setStyleSheet("padding:5px; font-weight: bold;")
        
        self.cacheList = QtWidgets.QListWidget()
        self.cacheList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.saveLocationLabel = QtWidgets.QLabel("Save Location")
        self.saveLocationLabel.setStyleSheet("padding:5px; font-weight:bold;")
        self.saveLocationEdit = QtWidgets.QLineEdit(self.default_file_loc)
        
        self.cacheNameLabel = QtWidgets.QLabel("Cache Name")
        self.cacheNameLabel.setStyleSheet("padding:5px; font-weight:bold;")
        self.cacheNameEdit = QtWidgets.QLineEdit("general_settings")
    
        self.saveLocationDialog = QtWidgets.QFileDialog()
        self.saveLocationDialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        
        self.saveButton = QtWidgets.QPushButton("Save Cache")
        self.assignButton = QtWidgets.QPushButton("Assign Selected Cache to Node")
        
    def create_layouts(self):
        
        self.nodes_checkboxes_layout = QtWidgets.QHBoxLayout()
        self.nodes_checkboxes_layout.addWidget(self.nClothCheckBox)
        self.nodes_checkboxes_layout.addWidget(self.nHairCheckBox)
        self.nodes_checkboxes_layout.addWidget(self.refreshButton)
        self.nodes_list_layout = QtWidgets.QVBoxLayout()
        self.nodes_list_layout.addWidget(self.ndynamics_nodes_label)
        self.nodes_list_layout.addWidget(self.warning_label)
        self.nodes_list_layout.addWidget(self.ndynamics_nodes_list)
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
        self.refreshButton.clicked.connect(self.setNDynamicsNodesList)
        self.ndynamics_nodes_list.itemClicked.connect(self.setCachesList)
        self.saveButton.clicked.connect(self.saveCache)
        self.assignButton.clicked.connect(self.switchCache)
        
        
    """
    Helper Functions
    """
    # Get the list of nCloth and nHair nodes in the scene
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
        
        
    # Add the list of nCloth and nHair nodes to the cache list
    def setNDynamicsNodesList(self):
        self.ndynamics_nodes_list.clear()
        self.cacheList.clear()
        for node in self.getNDynamicsNodes():
            self.ndynamics_nodes_list.addItem(str(node))
            
            
    # Set list of caches associated with selected node
    def setCachesList(self):
        self.cacheList.clear()
        items = self.ndynamics_nodes_list.selectedItems()
        if items:
            first_item = items[0].text()
            list_of_files = os.listdir(self.default_file_loc)
            for i in list_of_files:
                if i.endswith('.xml'):
                    if (first_item+"___") in i:
                        self.cacheList.addItem(i.split('.xml')[0])
        
            
    # Save a cache file
    def saveCache(self):
        
        version = "5"
        time_range_mode = "2"
        start_frame = "1"
        end_frame = "10"
        cache_file_dist = "OneFile" #or OneFilePerFrame
        refresh_caching = "1"
        cache_directory = self.saveLocationEdit.text()
        cache_per_geom = "0"
        name_of_cache = self.ndynamics_nodes_list.currentItem().text() + "___" + self.cacheNameEdit.text()
        cache_name_prefix = "0"
        action_to_perform = "add" # replace, merge, mergeDelete
        force_save = "0"
        sim_rate = "1"
        sample_mult = "1"
        inherited_mods = "0"
        store_doubles_as_floats = "1"
        cache_file = "mcx"
        
        ncache_eval_str = 'doCreateNclothCache '
        ncache_eval_str += version + ' { "'
        ncache_eval_str += time_range_mode + '","'
        ncache_eval_str += start_frame + '","'
        ncache_eval_str += end_frame + '","'
        ncache_eval_str += cache_file_dist + '","'
        ncache_eval_str += refresh_caching + '","'
        ncache_eval_str += cache_directory + '","'
        ncache_eval_str += cache_per_geom + '","'
        ncache_eval_str += name_of_cache + '","'
        ncache_eval_str += cache_name_prefix + '","'
        ncache_eval_str += action_to_perform + '","'
        ncache_eval_str += force_save + '","'
        ncache_eval_str += sim_rate + '","'
        ncache_eval_str += sample_mult + '","'
        ncache_eval_str += inherited_mods + '","'
        ncache_eval_str += store_doubles_as_floats + '","'
        ncache_eval_str += cache_file + '" } ;'
        
        selected_node = self.ndynamics_nodes_list.currentItem().text()
        pm.select(selected_node)
        pm.mel.eval(ncache_eval_str)
        
        
    # Switch cache
    def switchCache(self):
        selected_node = self.ndynamics_nodes_list.currentItem().text()
        pm.select(selected_node)
        if pm.listConnections(selected_node, type='cacheFile'):
            pm.mel.eval('deleteCacheFile 2 { "keep", "" } ;') 
            pm.select(selected_node)
        cache_file_mel = 'cacheFile -attachFile -fileName '
        cache_file_mel += '"' + self.cacheList.currentItem().text() + '" '
        cache_file_mel += '-directory "' + self.saveLocationEdit.text() + '"  '
        cache_file_mel += '-cnm "'+self.ndynamics_nodes_list.currentItem().text()
        cache_file_mel += '" -ia ' + self.ndynamics_nodes_list.currentItem().text() + '.positions;'
        pm.mel.eval(cache_file_mel)

"""
Run Window
"""         
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