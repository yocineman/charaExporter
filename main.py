# -*- coding: utf-8 -*-

#------------------------------
__version__ = '0.4.0'
__author__ = "Yoshihisa Okano"
#------------------------------

import sys
import os

import util
import batch
from importlib import import_module

# import ninaSetup
# import hikalSetup
# import ikkaSetup

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
        self.ui_path = '.\\gui.ui'
        self.mode = mode

        self.ui = QUiLoader().load(self.ui_path)
        self.setCentralWidget(self.ui)

        self.setWindowTitle('%s %s'%(self.WINDOW, __version__))
        self.setGeometry(400, 400, 400, 300)
        if mode == 'ZGR':
            self.exportTgtList = ['nina', 'hikal', 'all']
            self.ui.comboBox.addItems(self.exportTgtList)
        else:
            self.exportTgtList = ['ikka', 'juran', 'manato', 'tatsuya', 'naoto', 'SMO', 'UKI', 'YPI', 'FBTKN', 'TKN', 'all']
            self.ui.comboBox.addItems(self.exportTgtList)
        self.ui.groupBox.installEventFilter(self)


    def eventFilter (self, object, event):
        if event.type() == QEvent.DragEnter:
            event.acceptProposedAction()
            return True
        
        if event.type() == QEvent.Drop:
            mimedata = event.mimeData()
            if mimedata.hasUrls:
                url_list = mimedata.urls()
                for url in url_list:
                    inputpath = url.toString().replace("file:///", "")

                    # opc = util.outputPathConf(inputpath)

                    chara = self.ui.comboBox.currentText()
                    print chara
                    # if chara == 'nina' or (chara == 'all' and self.mode == 'ZGR'):
                    #     self.ui.progressBar.setValue(0)

                    #     opc.createOutputDir('nina')

                    #     abcOutput = opc.publishfullabcpath + '/' + 'nina.abc'
                    #     hairOutput = opc.publishfullpath + '/' + 'hair.ma'
                    #     ninaOutput = opc.publishfullpath + '/' + 'nina.ma'

                    #     batch.abcExport(ninaSetup.nsChara, ninaSetup.abcSet, abcOutput, inputpath)
                    #     self.ui.progressBar.setValue(30)

                    #     abcFiles = os.listdir(opc.publishfullabcpath)
                    #     for abc in abcFiles:
                    #         ns = abc.replace('nina_', '').replace('.abc', '')
                    #         hairOutput = opc.publishfullpath + '/' + 'hair_' + ns + '.ma'
                    #         if '___' in ns:
                    #             ns = ns.replace('___', ':')
                    #         batch.hairExport(ninaSetup.assetHair, ns, ns+':'+ninaSetup.topNode, hairOutput, inputpath)
                    #     self.ui.progressBar.setValue(60)

                    #     for abc in abcFiles:
                    #         ns = abc.replace('nina_', '').replace('.abc', '')
                    #         abcOutput = opc.publishfullabcpath + '/' + abc
                    #         ninaOutput = opc.publishfullpath + '/' + abc.replace('abc', 'ma')
                    #         if '___' in ns:
                    #             ns = ns.split('___')[-1]
                    #         batch.abcAttach(ninaSetup.assetChara, ns, ns+':'+ninaSetup.topNode, abcOutput, ninaOutput)
                    #     opc.makeCurrentDir()
                    #     self.ui.progressBar.setValue(100)

                    # if chara == 'hikal' or (chara == 'all' and self.mode == 'ZGR'):
                    #     self.ui.progressBar.setValue(0)
                    #     opc.createOutputDir('hikal')

                    #     abcOutput = opc.publishfullabcpath + '/' + 'hikal.abc'
                    #     hairOutput = opc.publishfullpath + '/' + 'hair.ma'
                    #     hikalOutput = opc.publishfullpath + '/' + 'hikal.ma'

                    #     batch.abcExport(hikalSetup.nsChara, hikalSetup.abcSet, abcOutput, inputpath)
                    #     self.ui.progressBar.setValue(30)

                    #     abcFiles = os.listdir(opc.publishfullabcpath)
                    #     for abc in abcFiles:
                    #         ns = abc.replace('hikal_', '').replace('.abc', '')
                    #         hairOutput = opc.publishfullpath + '/' + 'hair_' + ns + '.ma'
                    #         if '___' in ns:
                    #             ns = ns.replace('___', ':')
                    #         batch.hairExport(hikalSetup.assetHair, ns, ns+':'+hikalSetup.topNode, hairOutput, inputpath)
                    #     self.ui.progressBar.setValue(60)

                    #     for abc in abcFiles:
                    #         ns = abc.replace('hikal_', '').replace('.abc', '')
                    #         abcOutput = opc.publishfullabcpath + '/' + abc
                    #         hikalOutput = opc.publishfullpath + '/' + abc.replace('abc', 'ma')
                    #         if '___' in ns:
                    #             ns = ns.split('___')[-1]
                    #         batch.abcAttach(hikalSetup.assetChara, ns, ns+':'+hikalSetup.topNode, abcOutput, hikalOutput)
                    #     opc.makeCurrentDir()
                    #     self.ui.progressBar.setValue(100)

                    # if self.mode != 'ZGR':

                    if chara != 'all':
                        if chara == 'TKN':
                            self.execExportAnim(chara, inputpath)
                        else:
                            self.execExport(chara, inputpath)
                    else:
                        charaList = self.exportTgtList
                        charaList.remove('all')
                        for chara in charaList:
                            if chara == 'TKN':
                                pass
                            else:
                                self.execExport(chara, inputpath)

                # QMessageBox.information()
                print '******************* end *********************'

    def execExport (self, charaName, inputpath):
        opc = util.outputPathConf(inputpath)
        opc.createOutputDir(charaName)

        abcOutput = opc.publishfullabcpath + '/' + charaName + '.abc'
        hairOutput = opc.publishfullpath + '/' + 'hair.abc'
        charaOutput = opc.publishfullpath + '/' + charaName + '.abc'

        charaSetup = import_module(charaName+'Setup')
        batch.abcExport(charaSetup.nsChara, charaSetup.abcSet, abcOutput, inputpath)

        abcFiles = os.listdir(opc.publishfullabcpath)
        print abcFiles
        for abc in abcFiles:
            ns = abc.replace(charaName+'_', '').replace('.abc', '')
            hairOutput = opc.publishfullabcpath + '/' + 'hair_' + ns + '.ma'
            if '___' in ns:
                ns = ns.replace('___', ':')
            if charaSetup.assetHair != '':
                batch.hairExport(charaSetup.assetHair, ns, ns+':'+charaSetup.topNode, hairOutput, inputpath)

            abcOutput = opc.publishfullabcpath + '/' + abc
            charaOutput = opc.publishfullpath + '/' + abc.replace('abc', 'ma')
            batch.abcAttach(charaSetup.assetChara, ns, ns+':'+charaSetup.topNode, abcOutput, charaOutput)
        opc.makeCurrentDir()

    def execExportAnim (self, charaName, inputpath):
        opc = util.outputPathConf(inputpath, True)
        opc.createOutputDir(charaName)

        output = opc.publishfullanimpath
        charaSetup = import_module(charaName+'Setup')
        regex = ["*_Cntrl","*_Cntrl_01","*_Cntrl_02","*_Cntrl_03","*_Cntrl_04","*Attr_CntrlShape","*Wire","*All_Grp","*_ctrl"]
        regex = ','.join(regex)
        batch.animExport(output, 'anim', charaSetup.nsChara, regex, inputpath)

        animFiles = os.listdir(opc.publishfullanimpath)
        if len(animFiles) != 0:
            ns = animFiles[0].replace('anim_', '').replace('.ma', '')
            animOutput = opc.publishfullanimpath + '/' + animFiles[0]
            charaOutput = opc.publishfullpath + '/' + ns + '.ma'
            batch.animAttach(charaSetup.assetChara, ns, animOutput, charaOutput)


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