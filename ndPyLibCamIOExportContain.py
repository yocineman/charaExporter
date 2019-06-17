# -*- coding: utf-8 -*-

from ndPyLibCamGetAnimNodeAndAttr import *
import pymel.core as pc
import maya.cmds as mc
import os

def ndPyLibAnimIOExportContain (isFilterCurve, inPfxInfo, inDirPath, inFileName, inForNodes, isCheckAnimCurve, isCheckConstraint, ns):
    retNodes = []
    addCmd = []

    pfxSw = int(inPfxInfo[0])
    NS = ['', '_', ':', '']

    tmpFile = 'ndExportAnimCurveTmp.ma'

    if pfxSw<3:
        retNodes = ndPyLibAnimGetAnimNodeAndAttr(inForNodes, 2, isCheckAnimCurve, isCheckConstraint)
    else:
        retNodes = ndPyLibAnimGetAnimNodeAndAttr(inForNodes, 0, isCheckAnimCurve, isCheckConstraint)

    if len(retNodes) <= 0:
        message = 'No Animation Nodes!\n' + 'Do you want to continue ?\n'
        resultStr = mc.confirmDialog(title='Confirm', message=message,
            button=['Yes', 'No'], defaultButton='Yes', cancelButton='No', dismissString='No')
        if resultStr == 'No':
            mc.confirmDialog(title='Abort', message='Stop export.')
            return

    mc.select(cl=True)
    count = 0
    for i in range(len(retNodes)/2):
        if mc.objExists(retNodes[i*2+1]) == 1:

            mc.select(retNodes[i*2+1], add=True)


    if isFilterCurve:
        mc.filterCurve()
    else:
        print '[nd] Not use filterCurve\n'

    fileName = inFileName + '.ma'
    filePathName = inDirPath + '/' + fileName
    mc.file(filePathName, f=True, es=True, typ='mayaAscii', ch=0, chn=0, exp=0, con=0, sh=0)

    print inDirPath
    print 'inDirPath'

    x = pc.ls('NBB???',type='transform')
    y = pc.listRelatives(x, ad=True)

    if ns != 'empty':
        check2D = pc.ls(ns+'_anim2D')
        checkaim = pc.ls(ns+'_cloCamera_1_aim')
    else:
        check2D = pc.ls('anim2D')
        checkaim = pc.ls('cloCamera_1_aim')

    if checkaim != []:
        camtype = 'aim'
    elif check2D != []:
        camtype = '2D'
    else:
        camtype = '3D'

    if ns == 'empty':
        cameraScale = pc.getAttr('cloCamera_1_animCam.cameraScale')
    else:
        if ns == 'ch':
            ns = 'chara'
        cameraScale = mc.getAttr(ns+'_cloCamera_1_animCam.cameraScale')
    if ns == 'empty':
        f = open(os.path.dirname(inDirPath)+'/' + 'cal_grb.txt', mode = 'w')
    else:
        f = open(os.path.dirname(inDirPath)+'/' + ns + '_cal_grb.txt', mode = 'w')

    f.write(x[0] + '\n')
    f.write(y[0] + '\n')
    f.write(camtype + '\n')

    f.write(str(cameraScale) + '\n')


    f.close()

    inc = 0
    # print retNodes
    for i in range(len(retNodes)/2):
        cmd = 'connectAttr \"' + retNodes[i*2+1] + '.output\" \" :' + inPfxInfo[1] + NS[pfxSw] + retNodes[i*2] + '\";\n'

        addCmd.append(cmd)
        print cmd

    try:
        readFileID = open(inDirPath+'/'+fileName, 'r')
        writeFileID = open(inDirPath+'/'+tmpFile, 'w')

        line = readFileID.readline()

        while line:
            if line == '// End of ' + fileName + '\n':
                for c in addCmd:
                    writeFileID.write(c)
                writeFileID.write('// End of '+fileName+'\n')
            else:
                writeFileID.write(line)
            line = readFileID.readline()
    except:
        pass
    finally:
        readFileID.close()
        writeFileID.close()

    org = inDirPath + '/' + fileName
    tmp = inDirPath + '/' + tmpFile
    os.remove(org)
    os.rename(tmp, inDirPath+ '/' + inFileName + '.ma')

    ###