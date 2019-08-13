# -*- coding: utf-8 -*-

from ndPyLibAnimGetAnimNodeAndAttr import *
import maya.cmds as mc
import os

def ndPyLibAnimIOExportContain (isFilterCurve, inPfxInfo, inDirPath, inFileName, inForNodes, isCheckAnimCurve, isCheckConstraint, frameRange, bakeAnim):
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
            buf = retNodes[i*2+1].split(':')
            if len(buf) == 2:
                rn = mc.rename(retNodes[i*2+1], buf[1])
                retNodes[i*2+1] = rn
            mc.select(retNodes[i*2+1], add=True)

    # print '*'*30
    # print 'bakeTest'
    # print retNodes
    if bakeAnim:
        animNodes = retNodes[1:len(retNodes):2]
        bakeList = []
        for animNode in animNodes:
            bakeList += mc.listConnections(animNode+'.output', s=False, d=True, p=True)
        ### bakeResult cannot bake 'scene time warp' animation
        for t in range(int(frameRange[0]),int(frameRange[1]+1)):
            mc.currentTime(t)
            currentTime = mc.currentTime(q=True)
            print currentTime
            for bake in bakeList:
                obj, attr = bake.split('.')
                mc.setKeyframe(obj, t=currentTime, at=attr)
    
    if isFilterCurve:
        mc.filterCurve()
    else:
        print '[nd] Not use filterCurve\n'

    fileName = inFileName + '.ma'
    filePathName = inDirPath + '/' + fileName
    mc.file(filePathName, f=True, es=True, typ='mayaAscii', ch=0, chn=0, exp=0, con=0, sh=0)

    inc = 0
    # print retNodes
    for i in range(len(retNodes)/2):
        print retNodes[i*2+1], inPfxInfo, NS[pfxSw], retNodes[i*2]
        node = retNodes[i*2].split('|')[-1]
        # cmd = 'connectAttr \"' + retNodes[i*2+1] + '.output\" \":' + inPfxInfo[1] + NS[pfxSw] + retNodes[i*2] + '\";\n'
        cmd = 'connectAttr \"' + retNodes[i*2+1] + '.output\" \":' + inPfxInfo[1] + NS[pfxSw] + node + '\";\n'
        addCmd.append(cmd)

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
    os.rename(tmp, org)

    ###