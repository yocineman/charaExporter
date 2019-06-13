# -*- coding: utf-8 -*-
import os
import subprocess
import shutil

# mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2015\\bin\\mayabatch.exe'
mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2017\\bin\\mayabatch.exe'


def abcExport (namespace, exportSet, outputPath, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from ndPyLibExportAbc import ndPyLibExportAbc2;ndPyLibExportAbc2(''' + str(namespace) +''', ''' + str(exportSet) + ''',''' + "\'" + outputPath + "\'" + ''')\")''')
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

def animExport (outputPath, oFilename, namespace, regex, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from ndPyLibExportAnim import ndPyLibExportAnim2;ndPyLibExportAnim2(''' + "\'" + outputPath + "\'" + "," + "\'" + oFilename + "\'" + "," + str(namespace) + "," + "\'" + regex + "\'"  + ''', 0);\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd
    subprocess.call(cmd)

def camExport (outputPath, oFilename, scene, camScale):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from ndPyLibExportCam3 import ndPyLibExportCam2;ndPyLibExportCam2(''' + "\'" + outputPath + "\'" + "," + "\'" + oFilename + "\'" + "," + str(camScale) + ''', 0);\")''')

    cmd.append('-file')
    cmd.append(scene)
    print '=========='*10
    print cmd
    subprocess.call(cmd)

def animAttach (assetPath, namespace, animPath, outputPath):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from mayaBasic import *;import maya.cmds as mc;saveAs(''' + "\'" + outputPath + "\'" + ''');loadAsset(''' + "\'" + assetPath + "\'" + "," + "\'" + namespace + "\'"''');loadAsset(''' + "\'" + animPath + "\'" + "," + "\'" + namespace+'_anim' + "\'" + ''');saveAs(''' + "\'" + outputPath + "\'" + ''');\")''')
    print cmd
    ret = subprocess.call(cmd)

def camAttach (assetPath, namespace, animPath, outputPath):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from mayaBasic import *;import maya.cmds as mc;saveAs(''' + "\'" + outputPath + "\'" + ''');importAsset(''' + "\'" + animPath + "\'"+ "," + "\'" + namespace + "\'" + ''');renameAsset('''+ "\'" + namespace + "\'"+ "," + "\'" + animPath + "\'"+ ''');loadAsset(''' + "\'" + animPath + "\'" + "," + "\'" + namespace+'_anim' + "\'" + ''');saveAs(''' + "\'" + outputPath + "\'" + ''');\")''')
    print cmd

    ret = subprocess.call(cmd)

def animReplace (namespace, animPath, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from mayaBasic import *;replaceAsset(''' + "\'" + animPath + "\'" + "," + "\'" + namespace+'_anim' + "\'" + ''');save();\")''')
    cmd.append('-file')
    cmd.append(scene)

    subprocess.call(cmd)

def camReplace (namespace, animPath, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from mayaBasic import *;camreplaceAsset(''' + "\'" + animPath + "\'" + "," + "\'" +namespace+'_anim' + "\'" + ''');save();\")''')
    cmd.append('-file')
    cmd.append(scene)
    subprocess.call(cmd)

def repABC (scenePath, repAbcPath):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from mayaBasic import *;replaceABCPath(''' + "\'" + repAbcPath + "\'" + ''');save();\")''')
    cmd.append('-file')
    cmd.append(scenePath)
    print cmd
    subprocess.call(cmd)
