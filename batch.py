# -*- coding: utf-8 -*-

import subprocess

# mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2015\\bin\\mayabatch.exe' 
mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2017\\bin\\mayabatch.exe' 


def abcExport (namespace, outputPath, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from ndPyLibExportAbc import ndPyLibExportAbc2;ndPyLibExportAbc2(''' + str(namespace) +''', ['abcExport_Sets'],''' + "\'" + outputPath + "\'" + ''')\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd
    subprocess.call(cmd)

def hairExport (assetPath, namespace, topNode, outputPath, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from mayaBasic import *;replaceAsset(''' + "\'" + assetPath + "\'" + ',' + "\'" + namespace + "\'" + ''');exportFile(''' + "\'" + outputPath + "\'" + ',' + "\'" + topNode + "\'" + ''')\")''')
    # cmd.append('''python(\"import sys;sys.path.append(\'P:/Project/mem2/Library/Tool/maya/scripts/python/charaExporter\');from mayaBasic import *\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd
    ret = subprocess.call(cmd)

def abcAttach (assetPath, namespace,topNode, abcPath, outputPath):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from mayaBasic import *;import maya.cmds as mc;saveAs(''' + "\'" + outputPath + "\'" + ''');loadAsset(''' + "\'" + assetPath + "\'" + "," + "\'" + namespace + "\'"''');selHierarchy=mc.ls(''' + "\'" + topNode + "\'" + ''', dag=True);attachABC(''' + "\'" + abcPath + "\'" + ''',selHierarchy);''' + '''saveAs(''' + "\'" + outputPath + "\'" + ''');\")''')
    print cmd
    ret = subprocess.call(cmd)

def animExport (outputPath, oFilename, regex, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from ndPyLibExportAnim import ndPyLibExportAnim2;ndPyLibExportAnim2(''' + "\'" + outputPath + "\'" + "," + "\'" + oFilename + "\'" + "," + "\'" + regex + "\'"  + ''', 0);\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd
    subprocess.call(cmd)