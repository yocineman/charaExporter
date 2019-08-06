# -*- coding: utf-8 -*-

#------------------------------
__version__ = '0.7.3'
__author__ = "Yoshihisa Okano"
#------------------------------

import sys
import os
import shutil

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


### debug mode
testRun = True


class GUI (QMainWindow):
    WINDOW = 'mem chara export'

    def __init__(self, parent=None, mode='ZGR'):
        print mode
        super(self.__class__, self).__init__(parent)
        self.ui_path = '.\\pycode\\gui.ui'
        self.mode = mode
        self.yeti = False
        self.stepValue = 1.0

        self.ui = QUiLoader().load(self.ui_path)
        self.setCentralWidget(self.ui)
        self.testRun = False

        debug = ''
        if testRun:
            debug = '__debug__'
        self.setWindowTitle('%s %s %s ' % (self.WINDOW, __version__, debug))
        self.setGeometry(400, 400, 400, 300)
        self.exportTgtList = []

        self.modeList = ['ZGR', 'DUCT_C', 'CORA']

        self.ui.mode_comboBox.addItems(self.modeList)
        self.ui.mode_comboBox.currentIndexChanged.connect(self.mode_comboBox_changed)

        self.ui.groupBox.installEventFilter(self)

        self.ui.debug_checkBox.stateChanged.connect(self.debug_checkBox_changed)

        self.exportTgtList = ['nina', 'ninaScan', 'hikal']
        self.exportTgtList.append('Cam')
        self.exportTgtList.append('all')

        self.ui.comboBox.addItems(self.exportTgtList)

        self.ui.overrideValue_LineEdit.setEnabled(False)
        self.ui.cameraScaleOverride_CheckBox.stateChanged.connect(
            self.overrideValue_LineEdit_stateChange)
        self.ui.yeti_CheckBox.stateChanged.connect(self.yeti_checker)

        self.ui.stepValue_LineEdit.setEnabled(False)
        self.ui.stepValue_CheckBox.stateChanged.connect(
            self.stepValue_LineEdit_stateChange)
        self.ui.start_button.clicked.connect(self.push_start_button)

    def eventFilter(self, object, event):
        if event.type() == QEvent.DragEnter:
            event.acceptProposedAction()
            return True

        if event.type() == QEvent.Drop:
            mimedata = event.mimeData()
            if mimedata.hasUrls:
                url_list = mimedata.urls()
                print url_list
                for url in url_list:
                    inputpath = url.toString().replace("file:///", "")
                self.ui.path_line.setText(inputpath)

    def push_start_button(self):
        print 'aaaaaaaaaaaaaaa'
        inputpath = self.ui.path_line.text()

        chara = self.ui.comboBox.currentText()
        print chara
        if chara == None:
            print 'Not Selected!!!!!!!'
            return 0

        camScale = -1
        if self.ui.cameraScaleOverride_CheckBox.isChecked():
            camScale = float(self.ui.overrideValue_LineEdit.text())
        else:
            camScale = -1

        if self.ui.stepValue_CheckBox.isChecked():
            self.stepValue = float(
                self.ui.stepValue_LineEdit.text())
        else:
            self.stepValue = 1.0

        if chara != 'all':
            if chara == 'TKN' or chara == 'TKN_bodyBroken_leg' or chara == 'TKN2ancAlong':
                self.execExportAnim(chara, inputpath)
            elif chara == 'BG':
                for bg in self.bgList:
                    self.execExportAnim(bg, inputpath)
            elif chara == 'Cam':
                self.execExportCam(inputpath, camScale)
            elif chara in ['LgtSetAddCoreA', 'LgtSetCORin']:
                self.execExportAnim(chara, inputpath)
            else:
                self.execExport(chara, inputpath)

            util.addTimeLog(chara, inputpath, test=self.testRun)
        else:
            charaList = self.exportTgtList
            charaList.remove('all')
            for chara in charaList:
                if chara == 'TKN' or chara == 'TKN_bodyBroken_leg' or chara == 'TKN2ancAlong':
                    self.execExportAnim(chara, inputpath)
                elif chara == 'BG':
                    for bg in self.bgList:
                        self.execExportAnim(bg, inputpath)
                elif chara == 'Cam':
                    self.execExportCam(inputpath, camScale)
                elif chara in ['LgtSetAddCoreA', 'LgtSetCORin']:
                    self.execExportAnim(chara, inputpath)
                else:
                    self.execExport(chara, inputpath)

                util.addTimeLog(chara, inputpath, test=self.testRun)

    # QMessageBox.information()
        print '******************* end *********************'

    def mode_comboBox_changed(self):
        currentState = self.ui.mode_comboBox.currentText()
        self.mode = currentState

        if self.mode == 'ZGR':
            self.exportTgtList = ['nina', 'ninaScan', 'hikal']
        elif self.mode == 'DUCT_C':
            self.exportTgtList = ['ikka', 'juran', 'manato', 'tatsuya', 'naoto', 'SMO',
                                    'UKI', 'YPI', 'FBTKN', 'TKN', 'TKN_bodyBroken_leg', 'TKN2ancAlong']
            self.exportTgtList.append('BG')
            self.bgList = ['DCT_CtubeA', 'DCT_CtubeB', 'DCT_Cbunki', 'DCT_CNml',
                            'DCT_CtubeC017', 'DCT_Cescape', 'DCT_CtubeWideA', 'DCT_CtubeWideB']
        elif self.mode == 'CORA':
            self.exportTgtList = ['LXM', 'saki',
                                    'LgtSetCORin', 'LgtSetAddCoreA']
            self.exportTgtList.append('BG')
            self.bgList = ['ZGRCORin']

        self.exportTgtList.append('Cam')
        self.exportTgtList.append('all')

        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(self.exportTgtList)

        print self.mode

    def debug_checkBox_changed(self):
        currentState = self.ui.debug_checkBox.isChecked()
        print currentState
        self.testRun = currentState

    def overrideValue_LineEdit_stateChange(self):
        currentState = self.ui.cameraScaleOverride_CheckBox.isChecked()
        self.ui.overrideValue_LineEdit.setEnabled(currentState)

    def stepValue_LineEdit_stateChange(self):
        currentState = self.ui.stepValue_CheckBox.isChecked()
        self.ui.stepValue_LineEdit.setEnabled(currentState)

    def yeti_checker(self):
        self.yeti = self.ui.yeti_CheckBox.isChecked()
        print self.yeti

    def execExport(self, charaName, inputpath):

        print self.testRun
        opc = util.outputPathConf(inputpath, test=testRun)
        opc.createOutputDir(charaName)

        abcOutput = opc.publishfullabcpath + '/' + charaName + '.abc'
        hairOutput = opc.publishfullpath + '/' + 'hair.abc'
        charaOutput = opc.publishfullpath + '/' + charaName + '.abc'

        charaSetup = import_module('./setting.'+charaName+'Setup',package=None)
        batch.abcExport(charaSetup.nsChara, charaSetup.abcSet,
                        abcOutput, inputpath, self.yeti, self.stepValue)

        abcFiles = os.listdir(opc.publishfullabcpath)
        if len(abcFiles) == 0:
            opc.removeDir()
            return
        print abcFiles
        allOutput = []
        for abc in abcFiles:
            ns = abc.replace(charaName+'_', '').replace('.abc', '')
            hairOutput = opc.publishfullpath + '/' + 'hair_' + ns + '.ma'
            if '___' in ns:
                ns = ns.replace('___', ':')
            if charaSetup.assetHair != '':
                batch.hairExport(charaSetup.assetHair, ns, ns +
                                    ':'+charaSetup.topNode, hairOutput, inputpath)

            abcOutput = opc.publishfullabcpath + '/' + abc
            charaOutput = opc.publishfullpath + '/' + abc.replace('abc', 'ma')
            batch.abcAttach(charaSetup.assetChara, ns, ns+':' +
                            charaSetup.topNode, abcOutput, charaOutput)
            allOutput.append([abc.replace('abc', 'ma'), abc])
        opc.makeCurrentDir()

        for output in allOutput:
            print '#' * 20
            print output
            charaOutput = opc.publishcurrentpath + '/' + output[0]
            abcOutput = opc.publishcurrentpath + '/abc/' + output[1]
            batch.repABC(charaOutput, abcOutput)

    def execExportAnim(self, charaName, inputpath):
        opc = util.outputPathConf(inputpath, True, test=testRun)
        opc.createOutputDir(charaName)

        output = opc.publishfullanimpath
        charaSetup = import_module('setting.'+charaName+'Setup',package=None)
        # regex = ["*_Cntrl","*_Cntrl_01","*_Cntrl_02","*_Cntrl_03","*_Cntrl_04","*Attr_CntrlShape","*Wire","*All_Grp","*_ctrl"]
        regex = charaSetup.regex
        regex = ','.join(regex)
        batch.animExport(output, 'anim', charaSetup.nsChara, regex, inputpath, self.yeti)

        animFiles = os.listdir(opc.publishfullanimpath)
        if len(animFiles) == 0:
            opc.removeDir()
            return
        for animFile in animFiles:
            ns = animFile.replace('anim_', '').replace('.ma', '')
            animOutput = opc.publishfullanimpath + '/' + animFile
            charaOutput = opc.publishfullpath + '/' + ns + '.ma'
            batch.animAttach(charaSetup.assetChara, ns,
                                animOutput, charaOutput)
        opc.makeCurrentDir()

        for animFile in animFiles:
            if animFile[:5] != 'anim_':
                continue
            if animFile[-3:] != '.ma':
                continue
            ns = animFile.replace('anim_', '').replace('.ma', '')
            batch.animReplace(ns, opc.publishcurrentpath+'/anim/' +
                                animFile, opc.publishcurrentpath+'/'+ns+'.ma')

    def execExportCam(self, inputpath, camScale):
        opc = util.outputPathConf(inputpath, test=testRun)
        opc.createCamOutputDir()

        batch.camExport(opc.publishfullpath, opc.sequence +
                        opc.shot+'_cam', camScale, inputpath)
        camFiles = os.listdir(opc.publishfullpath)
        for camFile in camFiles:
            srcFile = os.path.join(opc.publishfullpath, camFile)
            dstDir = os.path.join(opc.publishfullpath, '..')
            try:
                shutil.copy(srcFile, dstDir)
            except:
                pass


def run(*argv):
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
    run(sys.argv[:])
