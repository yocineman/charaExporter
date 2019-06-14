# -*- coding: utf-8 -*-

import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import re

import os


def newScene ():
    mc.file(new=True)

def saveAs (outputPath):
    ext = os.path.splitext(outputPath)[1]
    mc.file(rn=outputPath)
    if ext == '.ma':
        mc.file(f=True, s=True, type='mayaAscii')
    else:
        mc.file(f=True, s=True, type='mayaBinary')

def save ():
    print 'save!!!'*10
    mc.file(s=True, f=True)

def replaceAsset (assetPath, namespace):
    mc.warning( 'replace start ')
    refs = mc.ls(type='reference')
    try:
        print refs
        refs.remove('sharedReferenceNode')
    except:
        pass
    tgtRN = ''
    for r in refs:
        ns = mel.eval('referenceQuery -ns ' + r)[1:]
        if namespace == ns:
            tgtRN = r
            break
    else:
        mc.error('can not replace')

    # print assetPath, tgtRN
    try:
        mc.file(assetPath, loadReference=tgtRN)
    except:
        pass
    mc.warning('replace end')

def camreplaceAsset (assetPath, namespace):
    mc.warning( 'replace start ')
    # refs = mc.ls(type='reference')
    # try:
    #     print refs
    #     # refs.remove('sharedReferenceNode')
    # except:
    #     pass
    # tgtRN = ''
    # for r in refs:
    #     ns = mel.eval('referenceQuery -ns ' + r)[1:]
    #     if namespace == ns:
    #         tgtRN = r
    #         break
    # else:
    #     mc.error('can not replace')

    # # print assetPath, tgtRN
    # try:
    #     mc.file(assetPath, loadReference=tgtRN)
    # except:
    #     pass
    mc.warning('replace end')


def exportFile (outputPath, topNode):
    mc.warning('export start')
    mc.select(topNode)
    mc.file(outputPath, typ='mayaAscii', f=True, es=True, pr=True)
    mc.warning('export end')

def loadAsset (assetPath, namespace):
    mc.file(assetPath, r=True, namespace=namespace, mergeNamespacesOnClash=False, ignoreVersion=True)

def importAsset (animPath, namespace):
    with open(os.path.dirname(os.path.dirname(animPath))+'/cal_grb.txt') as f:
        a = f.readline().strip()
        b = f.readline().strip()
        camtype = f.readline().strip()
    print camtype
    print os.path.dirname(os.path.dirname(animPath))

    if camtype == 'aim':
        print 'camtype is "aim_camera"'
        # camPath_neo = 'E:/users/ueda/camTestaim.ma'
        camPath_neo = r'P:\proj\TMST\elm\_cam\cam\rig\Aim\maya\master\camAim.cur.del_mtoa.ma'
        # camPath_neo = r'P:\proj\TMST\elm\_cam\cam\rig\3D\maya\master\cam.cur.ma'
    elif camtype == '2D':
        print 'camtype is "2D_camera"'
        camPath_neo = r'P:\proj\TMST\elm\_cam\cam\rig\2D\maya\master\cam2D_del_mtoa.cur.ma'
        # camPath_neo = 'E:/users/ueda/camTest2D.ma'
        # camPath_neo = r'P:\proj\TMST\elm\_cam\cam\rig\2D\maya\master\cam.cur.ma'
    elif camtype == '3D':
        print 'camtype is "3D_camera"'
        camPath_neo = r'P:\proj\TMST\elm\_cam\cam\rig\3D\maya\master\cam.cur.del_mtoa.ma'

        # camPath_neo = 'E:/users/ueda/camTest.ma'
        # camPath_neo = 'E:/users/ueda/camTest.ma'

        # camPath_neo = r'P:\proj\TMST\elm\_cam\cam\rig\Aim\maya\master\camAim.cur.ma'
    else:
        print 'camtype cant unload....'

    mc.file(camPath_neo,i=True, ignoreVersion=True, preserveReferences=True,mergeNamespacesOnClash=False, importFrameRate=True, importTimeRange='override')

    # ---outputPath----
    # E:/Project/b/shots/d/e/NBB062/publish/test_charSet/cameraA/v062/anim/BG.ma
    # ----camPath----
    # P:/proj/TMST/elm/_cam/cam/rig/3D/maya/master/cam.cur.ma
    # print 'import Asset end'

def renameAsset(namespace, animPath):
    mc.select('cloCamera_grp',hi=True)
    x=pm.ls(sl=True,)
    if not namespace:
        for i in x:
            i.rename(re.sub('^',namespace,i.name()))
    else:
        for i in x:
            i.rename(re.sub('^',namespace+'_',i.name()))

    print os.path.dirname(os.path.dirname(animPath))+'/cal_grb.txt'

    with open(os.path.dirname(os.path.dirname(animPath))+'/cal_grb.txt') as f:
        a = f.readline().strip()
        b = f.readline().strip()

    x = pm.ls('NAX000')
    x[0].rename(a)
    y = pm.ls('frame_1_120')
    y[0].rename(b)

def attachABC (abcPath, hierarchyList):
    if not mc.pluginInfo('AbcImport', q=True, l=True):
        mc.loadPlugin('AbcImport')
    hierarchy = ' '.join(hierarchyList)
    mel.eval('AbcImport -mode import -fitTimeRange -debug -connect ' + '\"' + hierarchy + '\" ' + '\"' + abcPath + '\"')

def replaceABCPath (repAbcPath):
    abcNodes = mc.ls(type='AlembicNode')
    if len(abcNodes) != 0:
        mc.setAttr(abcNodes[0]+'.abc_File', repAbcPath, type='string')
    print 'x' * 20

def delUnknownNode ():
    unknownNodes = mc.ls(type='unknown')
    if len(unknownNodes) != 0:
        mc.delete(unknownNodes)

def setEnv ():
    os.environ['VRAY_FOR_MAYA2015_MAIN_X64'] = 'Y:\\users\\env\\vray\\maya2015_vray_adv_36004\\maya_vray'
    os.environ['VRAY_TOOLS_MAYA2015_X64'] = 'Y:\\users\\env\\vray\\maya2015_vray_adv_36004\\vray\\bin'
    os.environ['MAYA_PLUG_IN_PATH'] = 'Y:/users/env/vray/maya2015_vray_adv_36004/maya_vray/plug-ins;'+os.environ['MAYA_PLUG_IN_PATH']
    os.environ['VRAYPATH'] = 'Y:\\users\\env\\vray\\maya2015_vray_adv_36004'
    os.environ['VRAY_FOR_MAYA2015_PLUGINS_X64'] = 'Y:/users/env/vray/maya2015_vray_adv_36004/maya_vray/vrayplugins'
    os.environ['MAYA_SCRIPT_PATH'] = 'Y:/users/env/vray/maya2015_vray_adv_36004/maya_vray/scripts;'+os.environ['MAYA_SCRIPT_PATH']
    os.environ['VRAY_VER'] = '36004'
    os.environ['VRAY_AUTH_CLIENT_FILE_PATH'] = 'Y:\\users\\env\\maya\\lic'
    os.environ['VRAY_OSL_PATH_MAYA2015_X64'] = 'Y:\\users\\env\\vray\\maya2015_vray_adv_36004\\vray\\opensl'

    for k,v in os.environ.items():
        print k, v


# def bakeKeys (topNode):
#     sframe = mc.playbackOptions(q=True, min=True)
#     eframe = mc.playbackOptions(q=True, max=True
#     mc.bakeResults(topNode, simulation=True, t=(sframe, eframe), hierarchy='below', sampleBy=1, dic=True, pok=True, sac=False, ral=False, bol=False, mr=True, cp=False, shape=True)

#     constraints = []
#     constraints += mc.ls(topNode, dag=True, type='parentConstraint')
#     constraints += mc.ls(topNode, dag=True, type='pointConstraint')
#     constraints += mc.ls(topNode, dag=True, type='orientConstraint')
#     constraints += mc.ls(topNode, dag=True, type='scaleConstraint')
#     for constraint in constraints:
#         if mc.referenceQuery(constraint, inr=True): continue
#         mc.delete(constraint)


if __name__ == '__main__':
    namespace = 'DDNinaNml'
    assetPath = 'P:/Project/mem2/assets/chara/DDNina/DDNinaNml/publish/model/RenderHigh/maya/current/DDNinaNml_mdlRH.mb'
    topNode = 'DDNinaNml'
    abcPath = 'P:/Project/mem2/shots/roll04/s116D/c009D/publish/animGeo/s116Dc009D_anm_v004.ma/s116Dc009D_animGeoCache_DDNinaNml.abc'

    loadAsset(assetPath, namespace)

    selHierarchy = mc.ls(namespace+':'+topNode, dag=True)
    attachABC(abcPath, selHierarchy)