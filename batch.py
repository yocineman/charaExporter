# -*- coding: utf-8 -*-

import subprocess

mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2015\\bin\\mayabatch.exe' 


def abcExport (namespace, outputPath, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from ndPyLibExportAbc import ndPyLibExportAbc2;ndPyLibExportAbc2(['''+"\'" + namespace + "\'"+'''], ['abcExport_Sets'],''' + "\'" + outputPath + "\'" + ''')\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd
    subprocess.call(cmd)

def hairExport (assetPath, namespace, topNode, outputPath, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from mayaBasic import *;replaceAsset(''' + "\'" + assetPath + "\'" + ',' + "\'" + namespace + "\'" + ''');exportFile(''' + "\'" + outputPath + "\'" + ',' + "\'" + topNode + "\'" + ''')\")''')
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