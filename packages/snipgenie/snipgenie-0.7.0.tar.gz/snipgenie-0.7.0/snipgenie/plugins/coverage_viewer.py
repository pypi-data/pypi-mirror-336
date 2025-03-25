"""
    Region coverage plot for snipgenie
    Created May 2024
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
import pickle, gzip, subprocess
import random
from collections import OrderedDict
from snipgenie.qt import *
import pandas as pd
from Bio import Phylo, SeqIO
from Bio import Entrez
from snipgenie import app, widgets, aligners, tools, rdiff
from snipgenie.plugin import Plugin

#location for sequences to align against
index_path = os.path.join(app.config_path, 'contam')
if not os.path.exists(index_path):
    os.makedirs(index_path, exist_ok=True)

class CoverageViewPlugin(Plugin):
    """CoverageView plugin for SNiPgenie"""

    #uncomment capabilities list to appear in menu
    capabilities = []
    requires = []
    menuentry = 'Coverage Viewer'
    name = 'Coverage Viewer'
    iconfile = 'bar-code.svg'
    enabled = False
    
    def __init__(self, parent=None):
        """Customise this"""

        if parent==None:
            return
        self.parent = parent
        return

    def plot(self):
        """Plot coverage of the region"""
      
        table = self.parent.fastq_table
        df = table.model.df
        rows = table.getSelectedRows()
        data = df.iloc[rows]
        
        if data is None or len(data) == 0:
            return


        #self.parent.run_threaded_process(func, self.parent.processing_completed)
        return

    def run_completed(self):
        self.parent.processing_completed()
        return
