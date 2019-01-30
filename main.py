# -*- coding: utf-8 -*-

#------------------------------
__version__ = '0.1.0'
__author__ = "Yoshihisa Okano"
#------------------------------

import sys
import os

import util
import batch
import ninaSetup

try:
    from PySide.QtGui import *
    from PySide.QtCore import *
    from PySide.QtUiTools import QUiLoader
except:
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtUiTools import QUiLoader
    from PySide2.QtWidgets import *

qtSignal = Signal
qtSlot = Slot


class GUI (QMainWindow):
    WINDOW = 'nina setup'
    def __init__ (self, parent=None):
        super(self.__class__, self).__init__(parent)
        self.ui_path = 'P:\\Project\\mem2\\Library\\Tool\\maya\\scripts\\python\\charaExporter\\gui.ui'

        self.ui = QUiLoader().load(self.ui_path)
        self.setCentralWidget(self.ui)

        self.setWindowTitle('%s %s'%(self.WINDOW, __version__))
        self.setGeometry(400, 400, 400, 300)
        self.ui.groupBox.installEventFilter(self)

    def eventFilter (self, object, event):
        if event.type() == QEvent.DragEnter:
            event.acceptProposedAction()
            return True
        
        if event.type() == QEvent.Drop:
            mimedata = event.mimeData()
            if mimedata.hasUrls:
                url_list = mimedata.urls()
                inputpath = url_list[0].toString().replace("file:///", "")

                opc = util.outputPathConf(inputpath)
                opc.createOutputDir('nina')

                print opc.publishpath
                print opc.publishfullpath
                print opc.publishfullabcpath

                abcOutput = opc.publishfullabcpath + '/' + 'nina.abc'
                hairOutput = opc.publishfullpath + '/' + 'hair.ma'
                ninaOutput = opc.publishfullpath + '/' + 'nina.ma'
                batch.abcExport(ninaSetup.nsNina, abcOutput, inputpath)
                batch.hairExport(ninaSetup.assetHair, ninaSetup.nsNina, ninaSetup.topNode, hairOutput, inputpath)
                batch.abcAttach(ninaSetup.assetNina, ninaSetup.nsNina, ninaSetup.topNode, abcOutput, ninaOutput)

                opc.makeCurrentDir()

def run (*argv):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setStyle('plastique')
    ui = GUI()
    ui.show()

    app.exec_()

if __name__ == '__main__':
    run(sys.argv[1:])