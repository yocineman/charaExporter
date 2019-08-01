# -*- coding: utf-8 -*-
import sys
import os
import subprocess

# import psutil
# mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2015\\bin\\mayabatch.exe'
mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2017\\bin\\mayabatch.exe'
pythonBatch = 'C:\\Program Files\\Shotgun\\Python\\python.exe'

def abcExport (namespace, exportSet, outputPath, scene, yeti, step_value):
    if yeti:
        print "load yeti"
        env_load()
    nw_cmd = []
    nw_cmd.append(mayaBatch)
    nw_cmd.append('-command')
    nw_cmd.append('''python(\"import sys;sys.path.append('P:/Project/mem2/Library/Tool/maya/scripts/python/charaExporter');from ndPyLibExportAbc import ndPyLibExportAbc2;ndPyLibExportAbc2(''' + str(namespace) + ''', ''' + str(exportSet) + ''',''' + "\'" + outputPath + "\'" + ''',''' + "\'" + str(step_value) + "\'" + ''')\")''')
    nw_cmd.append('-file')
    nw_cmd.append(scene)

    x = subprocess.call(nw_cmd)

def hairExport (assetPath, namespace, topNode, outputPath, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"import sys;sys.path.append('P:/Project/mem2/Library/Tool/maya/scripts/python/charaExporter');from mayaBasic import *;replaceAsset(''' + "\'" + assetPath + "\'" + ',' + "\'" + namespace + "\'" + ''');exportFile(''' + "\'" + outputPath + "\'" + ',' + "\'" + topNode + "\'" + ''')\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd
    ret = subprocess.call(cmd)

def abcAttach (assetPath, namespace,topNode, abcPath, outputPath):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"import sys;sys.path.append('P:/Project/mem2/Library/Tool/maya/scripts/python/charaExporter');from mayaBasic import *;import maya.cmds as mc;saveAs(''' + "\'" + outputPath + "\'" + ''');loadAsset(''' + "\'" + assetPath + "\'" + "," + "\'" + namespace + "\'"''');selHierarchy=mc.ls(''' + "\'" + topNode + "\'" + ''', dag=True);attachABC(''' + "\'" + abcPath + "\'" + ","+"\'"+namespace+"\'"+''',selHierarchy);saveAs(''' + "\'" + outputPath + "\'" + ''')\")''')
    print cmd
    ret = subprocess.call(cmd)

def animExport (outputPath, oFilename, namespace, regex, scene, yeti):
    if yeti:
        print "loading yeti"
        env_load()
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"import sys; sys.path.append('P:/Project/mem2/Library/Tool/maya/scripts/python/charaExporter');from ndPyLibExportAnim import ndPyLibExportAnim2;ndPyLibExportAnim2(''' + "\'" + outputPath + "\'" + "," + "\'" + oFilename + "\'" + "," + str(namespace) + "," + "\'" + regex + "\'"  + ''', 0);\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd
    subprocess.call(cmd)

def animAttach (assetPath, namespace, animPath, outputPath):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"import sys;sys.path.append('P:/Project/mem2/Library/Tool/maya/scripts/python/charaExporter');from mayaBasic import *;import maya.cmds as mc;saveAs(''' + "\'" + outputPath + "\'" + ''');loadAsset(''' + "\'" + assetPath + "\'" + "," + "\'" + namespace + "\'"''');loadAsset(''' + "\'" + animPath + "\'" + "," + "\'" + namespace+'_anim' + "\'" + ''');saveAs(''' + "\'" + outputPath + "\'" + ''');\")''')
    print cmd
    ret = subprocess.call(cmd)

def animReplace (namespace, animPath, scene):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"import sys;sys.path.append('P:/Project/mem2/Library/Tool/maya/scripts/python/charaExporter');from mayaBasic import *;replaceAsset(''' + "\'" + animPath + "\'" + "," + "\'" + namespace+'_anim' + "\'" + ''');save();\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd
    subprocess.call(cmd)

def camExport (outputPath, oFilename, camScale, scene):
    env_load()
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"import sys;sys.path.append('P:/Project/mem2/Library/Tool/maya/scripts/python/charaExporter');from ndPyLibExportCam import ndPyLibExportCam2;ndPyLibExportCam2(''' + "\'" + outputPath + "\'" + "," + "\'" + oFilename + "\'" + "," + str(camScale) + ''');\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd
    subprocess.call(cmd)

def repABC (scenePath, repAbcPath):
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"import sys;sys.path.append('P:/Project/mem2/Library/Tool/maya/scripts/python/charaExporter');from mayaBasic import *;replaceABCPath(''' + "\'" + repAbcPath + "\'" + ''');save();\")''')
    cmd.append('-file')
    cmd.append(scenePath)
    print cmd
    subprocess.call(cmd)

def env_load():
    os.environ["_TMP_VRAY_VER"]='36004'
    ND_TOOL_PATH_default = "Y:/tool/ND_Tools/python"

    env_key = "ND_TOOL_PATH_PYTHON"
    ND_TOOL_PATH = os.environ.get(env_key, ND_TOOL_PATH_default)
    for path in ND_TOOL_PATH.split(';'):
        path = path.replace('\\', '/')
        if path in sys.path: continue
        sys.path.append(path)
    import env_loader
    env_loader.run(sys.argv[:], fork=True)
