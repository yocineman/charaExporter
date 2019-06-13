# -*- coding: utf-8 -*-

#------------------------------
__version__ = '0.6.7 mst'
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
    def __init__ (self, parent=None, mode='ZGR'):
        print mode
        super(self.__class__, self).__init__(parent)
        self.ui_path = '.\\gui.ui'
        self.mode = mode

        self.ui = QUiLoader().load(self.ui_path)
        self.setCentralWidget(self.ui)

        debug = ''
        if testRun:
            debug = '__debug__'
        self.setWindowTitle('%s %s %s' % (self.WINDOW, __version__, debug))
        self.setGeometry(400, 400, 400, 300)
        # if mode == 'ZGR':
        if True:
            self.charaList = ['kesedoA', 'opekoA', 'pandoraA', 'noahA', 'handyCameraA', 'PRcarA', 'adaptorFlowerA', 'adaptorBigbugA']
            self.exportTgtList = self.charaList[:]
            self.exportTgtList.append('BG')
        self.exportTgtList.append('Cam')
        self.exportTgtList.append('all')
        self.bgList = ['debrisA', 'ghosttownOutdoorsA', 'skyA', 'seaFloorA']
        self.ui.comboBox.addItems(self.exportTgtList)
        self.ui.groupBox.installEventFilter(self)

        self.ui.overrideValue_LineEdit.setEnabled(False)
        self.ui.cameraScaleOverride_CheckBox.stateChanged.connect(self.overrideValue_LineEdit_stateChange)

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

                    chara = self.ui.comboBox.currentText()
                    print chara

                    camScale = -1
                    if self.ui.cameraScaleOverride_CheckBox.isChecked():
                        camScale = float(self.ui.overrideValue_LineEdit.text())
                    else:
                        camScale = -1

                    if chara != 'all':
                        print self.charaList
                        if chara in self.charaList:
                            self.execExportAnim(chara, inputpath)
                        elif chara == 'BG':
                            for bg in self.bgList:
                                self.execExportAnim(bg, inputpath)
                        elif chara == 'Cam':
                            self.execExportCam(chara, inputpath, camScale)
                        else:
                            self.execExport(chara, inputpath)
                        util.addTimeLog(chara, inputpath)

                    else:
                        charaList = self.exportTgtList
                        charaList.remove('all')
                        for chara in charaList:
                            if chara in self.charaList:
                                self.execExportAnim(chara, inputpath)
                            elif chara == 'BG':
                                for bg in self.bgList:
                                    self.execExportAnim(bg, inputpath)
                                pass
                            elif chara == 'Cam':
                                self.execExportCam(chara, inputpath, camScale)
                            else:
                                self.execExport(chara, inputpath)

                            util.addTimeLog(char, inputpath)

                # QMessageBox.information()
                print '******************* end *********************'

    def overrideValue_LineEdit_stateChange (self):
        currentState = self.ui.cameraScaleOverride_CheckBox.isChecked()
        self.ui.overrideValue_LineEdit.setEnabled(currentState)

    def execExport (self, charaName, inputpath):
        opc = util.outputPathConf(inputpath, test=testRun)
        opc.createOutputDir(charaName)

        abcOutput = opc.publishfullabcpath + '/' + charaName + '.abc'
        hairOutput = opc.publishfullpath + '/' + 'hair.abc'
        charaOutput = opc.publishfullpath + '/' + charaName + '.abc'
        cameraOutput = opc.publishfullpath + '/' + 'camera.abc'

        charaSetup = import_module('setting.'+charaName+'Setup')
        batch.abcExport(charaSetup.nsChara, charaSetup.abcSet, abcOutput, inputpath)

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
                batch.hairExport(charaSetup.assetHair, ns, ns+':'+charaSetup.topNode, hairOutput, inputpath)

            abcOutput = opc.publishfullabcpath + '/' + abc
            charaOutput = opc.publishfullpath + '/' + abc.replace('abc', 'ma')
            batch.abcAttach(charaSetup.assetChara, ns, ns+':'+charaSetup.topNode, abcOutput, charaOutput)
            allOutput.append([abc.replace('abc', 'ma'), abc])
        opc.makeCurrentDir()

        for output in allOutput:
            charaOutput = opc.publishcurrentpath + '/' + output[0]
            abcOutput = opc.publishcurrentpath + '/abc/' + output[1]
            batch.repABC(charaOutput, abcOutput)

    def execExportAnim (self, charaName, inputpath):
        opc = util.outputPathConf(inputpath, True, test=testRun)
        opc.createOutputDir(charaName)

        output = opc.publishfullanimpath
        charaSetup = import_module('setting.'+charaName+'Setup')
        # regex = ["*_Cntrl","*_Cntrl_01","*_Cntrl_02","*_Cntrl_03","*_Cntrl_04","*Attr_CntrlShape","*Wire","*All_Grp","*_ctrl"]
        regex = charaSetup.regex
        regex = ','.join(regex)
        batch.animExport(output, 'anim', charaSetup.nsChara, regex, inputpath)

        animFiles = os.listdir(opc.publishfullanimpath)
        if len(animFiles) == 0:
            opc.removeDir()
            return
        for animFile in animFiles:
            ns = animFile.replace('anim_', '').replace('.ma', '')
            animOutput = opc.publishfullanimpath + '/' + animFile
            charaOutput = opc.publishfullpath + '/' + ns + '.ma'
            batch.animAttach(charaSetup.assetChara, ns, animOutput, charaOutput)
        opc.makeCurrentDir()

        for animFile in animFiles:
            batch.animReplace(ns, opc.publishcurrentpath+'/anim/'+animFile, opc.publishcurrentpath+'/'+ns+'.ma')

    def execExportCam (self, cameraName, inputpath, camScale):#CameraName=CameraA
        cameraSetup = import_module('setting.cameraAsetup')
        ns = cameraSetup.nsCamera
        ns = ','.join(ns)
        ns = ns.split(',')
        print ns
        print ns[0]
        print ns[1]
        print ns[2]

        opc = util.outputPathConf(inputpath, True, test=testRun)
        opc.createOutputDir(cameraName)
        nsCamera = []
        output = opc.publishfullcampath
        batch.camExport(output, 'camera', inputpath, camScale)

        camFiles = os.listdir(opc.publishfullcampath)

        for camFile in camFiles:
            srcFile = os.path.join(opc.publishfullpath, camFile)
            dstDir = os.path.join(opc.publishfullpath, '..')
            try:
                shutil.copy(srcFile, dstDir)
            except:
                pass

        count = 0

        for camFile in camFiles:
            camanimOutput = opc.publishfullcampath + '/' + camFile

            camOutput = opc.publishfullpath + '/' + ns[count] +'_cloCamera1.ma'
            batch.camAttach(cameraSetup.assetCamera, ns[count], camanimOutput, camOutput)
            opc.makeCurrentDir()

            count= count + 1
        opc.makeCurrentDir()

        # count = 0
        # for camFile in camFiles:
        #     if ns[count] != 'empty':
        #         batch.camReplace(ns[count], opc.publishcurrentpath+'/anim/'+camFile, opc.publishcurrentpath+'/'+ns[count]+'_cloCamera1.ma')
        #     else:
        #         batch.camReplace(ns[count], opc.publishcurrentpath+'/anim/'+camFile, opc.publishcurrentpath+'/cloCamera1.ma')
        #     count = count + 1



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