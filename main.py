# -*- coding: utf-8 -*-

#------------------------------
__version__ = '0.2.0'
__author__ = "Yoshihisa Okano"
#------------------------------

import sys
import os

import util
import batch
import ninaSetup
import hikalSetup

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
    WINDOW = 'ZGR chara export'
    def __init__ (self, parent=None, mode='ZGR'):
        print mode
        super(self.__class__, self).__init__(parent)
        self.ui_path = 'P:\\Project\\mem2\\Library\\Tool\\maya\\scripts\\python\\charaExporter\\gui.ui'

        self.ui = QUiLoader().load(self.ui_path)
        self.setCentralWidget(self.ui)

        self.setWindowTitle('%s %s'%(self.WINDOW, __version__))
        self.setGeometry(400, 400, 400, 300)
        self.ui.comboBox.addItems(['nina', 'hikal', 'all'])
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

                chara = self.ui.comboBox.currentText()
                if chara == 'nina' or chara == 'all':
                    self.ui.progressBar.setValue(0)

                    opc.createOutputDir('nina')

                    abcOutput = opc.publishfullabcpath + '/' + 'nina.abc'
                    hairOutput = opc.publishfullpath + '/' + 'hair.ma'
                    ninaOutput = opc.publishfullpath + '/' + 'nina.ma'

                    batch.abcExport(ninaSetup.nsNina, abcOutput, inputpath)
                    self.ui.progressBar.setValue(30)

                    abcFiles = os.listdir(opc.publishfullabcpath)
                    for abc in abcFiles:
                        ns = abc.replace('nina_', '').replace('.abc', '')
                        hairOutput = opc.publishfullpath + '/' + 'hair_' + ns + '.ma'
                        batch.hairExport(ninaSetup.assetHair, ns, ns+':'+ninaSetup.topNode, hairOutput, inputpath)
                    self.ui.progressBar.setValue(60)

                    for abc in abcFiles:
                        ns = abc.replace('nina_', '').replace('.abc', '')
                        abcOutput = opc.publishfullabcpath + '/' + abc
                        ninaOutput = opc.publishfullpath + '/' + abc.replace('abc', 'ma')
                        batch.abcAttach(ninaSetup.assetNina, ns, ns+':'+ninaSetup.topNode, abcOutput, ninaOutput)
                    opc.makeCurrentDir()
                    self.ui.progressBar.setValue(100)

                if chara == 'hikal' or chara == 'all':
                    self.ui.progressBar.setValue(0)
                    opc.createOutputDir('hikal')

                    abcOutput = opc.publishfullabcpath + '/' + 'hikal.abc'
                    hairOutput = opc.publishfullpath + '/' + 'hair.ma'
                    hikalOutput = opc.publishfullpath + '/' + 'hikal.ma'

                    batch.abcExport(hikalSetup.nsHikal, abcOutput, inputpath)
                    self.ui.progressBar.setValue(30)

                    abcFiles = os.listdir(opc.publishfullabcpath)
                    for abc in abcFiles:
                        ns = abc.replace('hikal_', '').replace('.abc', '')
                        hairOutput = opc.publishfullpath + '/' + 'hair_' + ns + '.ma'
                        batch.hairExport(hikalSetup.assetHair, ns, ns+':'+hikalSetup.topNode, hairOutput, inputpath)
                    self.ui.progressBar.setValue(60)

                    for abc in abcFiles:
                        ns = abc.replace('hikal_', '').replace('.abc', '')
                        abcOutput = opc.publishfullabcpath + '/' + abc
                        hikalOutput = opc.publishfullpath + '/' + abc.replace('abc', 'ma')
                        batch.abcAttach(hikalSetup.assetHikal, ns, ns+':'+hikalSetup.topNode, abcOutput, hikalOutput)
                    opc.makeCurrentDir()
                    self.ui.progressBar.setValue(100)

def run (*argv):
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    app.setStyle('plastique')
    if argv[0][0] == '':
        ui = GUI()
    else:
        ui = GUI(mode=argv[0][0])
    ui.show()

    app.exec_()

if __name__ == '__main__':
    run(sys.argv[1:])