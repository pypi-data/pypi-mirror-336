"""
    File renaming utility - plugin for snipgenie
    Created October 2022
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import sys,os,platform,time,tempfile,glob
import pickle, gzip
import random
from collections import OrderedDict
from snipgenie.qt import *
import pandas as pd
from Bio import Phylo
import geopandas as gpd
from snipgenie import app, widgets, tables
from snipgenie.plugin import Plugin
from snipgenie import simulate

newick = os.path.join(app.module_path, 'testing', 'sim.newick')

class RenamePlugin(Plugin):
    """Rename plugin for SNiPgenie"""

    #uncomment capabilities list to appear in menu
    capabilities = ['gui']
    menuentry = 'Batch File Rename'
    name = 'Batch File Rename'
    iconfile = 'filerename.png'
    side = 'right'

    def __init__(self, parent=None, table=None):
        """Customise this and/or doFrame for your widgets"""

        if parent==None:
            return
        self.parent = parent
        self.table = table
        self.outpath = tempfile.gettempdir()
        self.create_widgets()
        return

    def create_widgets(self):
        """Create widgets if GUI plugin"""

        self.main = QWidget()
        self.main.setGeometry(QtCore.QRect(200, 200, 900, 600))
        layout = self.layout = QHBoxLayout()
        #layout.addStretch()
        self.main.setLayout(layout)
        left = QSplitter()
        layout.addWidget(left)
        self.left_tree = QTreeWidget()
        self.left_tree.setHeaderItem(QTreeWidgetItem(["name","filename"]))
        left.addWidget(self.left_tree)
        self.right_tree = QTreeWidget()
        self.right_tree.setHeaderItem(QTreeWidgetItem(["name","filename"]))
        left.addWidget(self.right_tree)
        bw = self.create_buttons(self.main)
        left.addWidget(bw)
        left.setSizes((2,2,1))
        return

    def create_buttons(self, parent):

        bw = QWidget(parent)
        bw.setMaximumWidth(250)
        vbox = QVBoxLayout(bw)
        vbox.setAlignment(QtCore.Qt.AlignTop)
        button = QPushButton("Load Files")
        button.clicked.connect(self.load_files)
        vbox.addWidget(button)
        button = QPushButton("Clear")
        button.clicked.connect(self.clear)
        vbox.addWidget(QLabel('Wildcard:'))
        vbox.addWidget(button)
        self.wildcardentry = w = QLineEdit()
        w.setText('*.*')
        vbox.addWidget(w)
        vbox.addWidget(QLabel('Find:'))
        self.searchentry = w = QLineEdit()
        w.setText('')
        vbox.addWidget(w)
        vbox.addWidget(QLabel('Replace with:'))
        self.replaceentry = w = QLineEdit()
        w.setText('')
        vbox.addWidget(w)
        button = QPushButton("Preview")
        button.clicked.connect(self.preview)
        vbox.addWidget(button)
        button = QPushButton("Execute")
        button.clicked.connect(self.execute)
        vbox.addWidget(button)
        return bw

    def load_files(self):
        """"Load files"""

        filenames, _ = QFileDialog.getOpenFileNames(self.main, 'Add files', './',
                                        filter="All Files(*.*)")
        if not filenames:
            return
        names = [os.path.basename(f) for f in filenames]
        data = {'filename':filenames,'name':names}
        self.df = pd.DataFrame(data)
        self.update_tree(self.left_tree, self.df)
        return

    def update_tree(self, tree, df):

        tree.clear()
        for i,r in df.iterrows():
            #print (i,r)
            item = QTreeWidgetItem(tree)
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(0, QtCore.Qt.Checked)
            item.setText(0, r['name'])
            item.setText(1, r.filename)
        return

    def clear(self):
        ltree = self.left_tree
        rtree = self.right_tree
        #self.update_tree(self.left_tree)
        return

    def preview(self):

        search = self.searchentry.text()
        replace = self.replaceentry.text()
        new = self.df.copy()
        new['name'] = new['name'].str.replace('_', ' ')
        self.update_tree(self.right_tree, new)
        return

    def execute(self):
        """"Do rename"""


        return
