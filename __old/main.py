# -*- coding: utf-8 -*-

import os
import subprocess
import tempfile


# def makeTmpFile ():
#     # with tempfile.NamedTemporaryFile(delete=False) as fp:
#         filename = fp.name
#     return filename


def run ():

    fp = tempfile.NamedTemporaryFile(delete=False)
    tmp = fp.name
    tmp = tmp.replace('\\', '/')
    fp.close()


    mayaBatch = 'C:\\Program Files\\Autodesk\\Maya2015\\bin\\mayabatch.exe' 
    scene = 'P:\\Project\\mem2\\shots\\roll04\\s116D\\c009D\\work\\okano\\s116Dc009D_anm_v004.ma'

    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from ndPyLibExportAbc import ndPyLibExportAbc;ndPyLibExportAbc(['DDNinaNml'], ['abcExport_Sets'],''' + "\'" + tmp + "\'" + ''')\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd

    # ret = subprocess.call(cmd)
    # p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # stdout, stderr = p.communicate()
    print '*' * 30
    # print stdout
    # print stderr

    # with open(tmp, 'r') as fp:
    #     print fp.read()

    ############################
    namespace = 'DDNinaNml'
    assetPath = 'P:/Project/mem2/assets/chara/DDNina/DDNinaNml/publish/setup/RenderHighHair/maya/current/DDNinaNml_rigRHhair.mb'
    outputPath = 'P:/Project/mem2/shots/roll04/s116D/c009D/publish/animGeo/s116Dc009D_anm_v004.ma/hair.ma'
    topNode = namespace + ':' + 'DDNinaNml'
    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    cmd.append('''python(\"from ninaSetup import *;replaceAsset(''' + "\'" + assetPath + "\'" + ',' + "\'" + namespace + "\'" + ''');exportFile(''' + "\'" + outputPath + "\'" + ',' + "\'" + topNode + "\'" + ''')\")''')
    cmd.append('-file')
    cmd.append(scene)
    print cmd
    # ret = subprocess.call(cmd)

    assetHair = outputPath
    nsHair = 'DDNinaNmlHair'
    assetNina = 'P:/Project/mem2/assets/chara/DDNina/DDNinaNml/publish/model/RenderHigh/maya/current/DDNinaNml_mdlRH.mb'
    nsNina = namespace
    abcPath = 'P:/Project/mem2/shots/roll04/s116D/c009D/publish/animGeo/s116Dc009D_anm_v004.ma/s116Dc009D_animGeoCache_DDNinaNml.abc'
    outputPath = 'P:/Project/mem2/shots/roll04/s116D/c009D/publish/animGeo/s116Dc009D_anm_v004.ma/nina.ma'

    cmd = []
    cmd.append(mayaBatch)
    cmd.append('-command')
    # cmd.append('''python(\"from ninaSetup import *;import maya.cmds as mc;newScene();loadAsset(''' + "\'" + assetNina + "\'" + "," + "\'" + nsNina + "\'"''');selHierarchy=mc.ls(''' + "\'" + topNode + "\'" + ''', dag=True);attachABC(''' + "\'" + abcPath + "\'" + ''',selHierarchy);loadAsset(''' + "\'" + assetHair + "\'" + ''', ''' + "\'" + nsHair + "\'" + ''');\")''')
    # cmd.append('''python(\"from ninaSetup import *;import maya.cmds as mc;newScene();loadAsset(''' + "\'" + assetNina + "\'" + "," + "\'" + nsNina + "\'"''');selHierarchy=mc.ls(''' + "\'" + topNode + "\'" + ''', dag=True);attachABC(''' + "\'" + abcPath + "\'" + ''',selHierarchy);''' + '''saveAs(''' + "\'" + outputPath + "\'" + ''');\")''')
    cmd.append('''python(\"from ninaSetup import *;import maya.cmds as mc;setEnv();loadAsset(''' + "\'" + assetNina + "\'" + "," + "\'" + nsNina + "\'"''');selHierarchy=mc.ls(''' + "\'" + topNode + "\'" + ''', dag=True);attachABC(''' + "\'" + abcPath + "\'" + ''',selHierarchy);''' + '''saveAs(''' + "\'" + outputPath + "\'" + ''');\")''')
    # cmd.append('''python(\"from ninaSetup import *;setEnv();\")''')
    print cmd
    ret = subprocess.call(cmd)



if __name__ == '__main__':
    run()