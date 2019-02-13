# -*- coding: utf-8 -*-

import maya.cmds as mc
import maya.mel as mel

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

def replaceAsset (assetPath, namespace):
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

    mc.file(assetPath, loadReference=tgtRN)


def exportFile (outputPath, topNode):
    mc.select(topNode)
    mc.file(outputPath, typ='mayaAscii', f=True, es=True, pr=True)

def loadAsset (assetPath, namespace):
    mc.file(assetPath, r=True, namespace=namespace, mergeNamespacesOnClash=False, ignoreVersion=True)

def attachABC (abcPath, hierarchyList):
    hierarchy = ' '.join(hierarchyList)
    mel.eval('AbcImport -mode import -fitTimeRange -debug -connect ' + '\"' + hierarchy + '\" ' + '\"' + abcPath + '\"')

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


def bakeKeys (topNode):
    sframe = mc.playbackOptions(q=True, min=True)
    eframe = mc.playbackOptions(q=True, max=True
    mc.bakeResults(topNode, simulation=True, t=(sframe, eframe), hierarchy='below', sampleBy=1, dic=True, pok=True, sac=False, ral=False, bol=False, mr=True, cp=False, shape=True)

    constraints = []
    constraints += mc.ls(topNode, dag=True, type='parentConstraint')
    constraints += mc.ls(topNode, dag=True, type='pointConstraint')
    constraints += mc.ls(topNode, dag=True, type='orientConstraint')
    constraints += mc.ls(topNode, dag=True, type='scaleConstraint')
    for constraint in constraints:
        if mc.referenceQuery(constraint, inr=True): continue
        mc.delete(constraint)


if __name__ == '__main__':
    namespace = 'DDNinaNml'
    assetPath = 'P:/Project/mem2/assets/chara/DDNina/DDNinaNml/publish/model/RenderHigh/maya/current/DDNinaNml_mdlRH.mb'
    topNode = 'DDNinaNml'
    abcPath = 'P:/Project/mem2/shots/roll04/s116D/c009D/publish/animGeo/s116Dc009D_anm_v004.ma/s116Dc009D_animGeoCache_DDNinaNml.abc'

    loadAsset(assetPath, namespace)

    selHierarchy = mc.ls(namespace+':'+topNode, dag=True)
    attachABC(abcPath, selHierarchy)