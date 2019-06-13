# -*- coding: utf-8 -*-

import os
import re, glob

import maya.cmds as mc
import maya.mel as mel

from importlib import import_module

from ndPyLibCamIOExportContain import *

def _getNamespace ():
    #no using
    return namespaces


def _getAllNodes ():
    cameraSetup = import_module('setting.cameraAsetup')
    nodeShort = cameraSetup.keyNode
    nodeShort = ','.join(nodeShort)
    nodeShort = nodeShort.split(',')
    return nodeShort

def _getConstraintAttributes (nodes):
    attrs = []
    print nodes
    for n in nodes:
        const = mc.listConnections(n, s=True, d=False, p=False, c=True, t='constraint')
        if const is None: continue
        for i in range(0, len(const), 2):
            attrs.append(const[i])
    return attrs

def _getPairBlendAttributes (nodes):
    attrs = []
    for n in nodes:
        pairblend = mc.listConnections(n, s=True, d=False, p=False, c=True, t='pairBlend')
        if pairblend is None: continue
        for i in range(0, len(pairblend), 2):
            attrs.append(pairblend[i])
    return attrs

def _getNoKeyAttributes (nodes):
    attrs = []
    for n in nodes:
        gAttrs = mc.listAttr(n, keyable=True)
        if gAttrs is None: continue
        for attr in gAttrs:
            if '.' not in attr:
                if mc.listConnections(n+'.'+attr, s=True, d=False) is None:
                    attrs.append(n+'.'+attr)
                    print 'find no key attribute : ' + n + '.' + attr

    return attrs


def _exportCam (publishpath, oFilename, CameraScale, isFilter):
    outputfiles = []
    sframe = mc.playbackOptions(q=True, min=True)
    eframe = mc.playbackOptions(q=True, max=True)
    namespaces = []

    ###
    sframe -= 10
    eframe += 10

    # namespaces = _getNamespace()
    namespaces = []
    namespaces.append('BG')
    namespaces.append('chara')
    namespaces.append('empty')

    # print namespaces1
    # for oDialogloop in namespaces1:
    #     namespaces.append((oDialogloop).encode('utf-8'))
    # print namespaces
    tmpallNodes = []
    allNodes = []
    tmpallNodes += _getAllNodes() #強引に4つに

    print tmpallNodes
    characterSet = mc.ls(type='character')

    if len(characterSet) == 0:
        mc.delete(characterSet)

    checkNodes = []

    for selectNode in tmpallNodes:
        print selectNode
        try:
            mc.select(selectNode,hi=True,add=True)##NotSelected
            allNodes.append(selectNode)
            checkNodes.append(0)
        except:
            checkNodes.append(1)
            # pass
    print allNodes
    i = 0
    mc.select(allNodes)

    baseAnimationLayer = mc.animLayer(q=True, r=True)

    if baseAnimationLayer!=None:
        animLayers = mc.ls(type='animLayer')
        for al in animLayers:
            mc.animLayer(al, e=True, sel=False)
        mc.animLayer(baseAnimationLayer, e=True, sel=True)
        mc.bakeResults(t=(sframe, eframe), sb=True, ral=True)
        print 'merge animation layers'

    mc.select(cl=True)

    attrs = _getNoKeyAttributes(allNodes)
    if len(attrs) != 0:
        mc.setKeyframe(attrs, t=sframe, insertBlend=False)

    if CameraScale != -1:
        mc.setKeyframe(attrs, t=sframe, v=CameraScale, at='.cs')

    attrs = _getConstraintAttributes(allNodes)
    attrs += _getPairBlendAttributes(allNodes)
    if len(attrs)!=0:
        mc.bakeResults(attrs, t=(sframe, eframe), sb=True)

    x = 0

    for ns in namespaces:
        if checkNodes[x]== 0:
            pickNodes = []
            for n in allNodes:
                pickNodes.append(n)
            if len(pickNodes) != 0:
                outputfiles.append(publishpath+oFilename+'_'+ns+'_cloCamera1.ma')
                ndPyLibAnimIOExportContain(isFilter, ['3', ''],publishpath, 'anim_'+ns+'_cloCamera1', pickNodes, 0, 0,ns)

            x = x+2
        else:
            x = x+2

    return outputfiles



def ndPyLibExportCam (isFilter):
    if mc.file(q=True, modified=True):
        mc.warning('please save scene file...')
    return

    filepath = mc.file(q=True, sceneName=True)
    filename = os.path.basename(filepath)

    match = re.match('(P:/Project/[a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)', filepath)
    if match is None:
        mc.warning('directory structure is not n-design format')
        return

    project  = match.group(1)
    roll     = match.group(3)
    sequence = match.group(4)
    shot     = match.group(5)

    shotpath = os.path.join(project, 'shots', roll, sequence, shot)

    camOutDir = 'Anim'
    publishpath = os.path.join(shotpath, 'publish', camOutDir, filename)

    oFilename = sequence + shot + '_anim'

    if not os.path.exists(shotpath):
        mc.warning('no exist folder...')
        return

    if not os.path.exists(publishpath):
        publishpath = os.path.normpath(publishpath)
        os.makedirs(publishpath)

def ndPyLibExportCam2 (publishpath, oFilename, camScale,isFilter):
    _exportCam(publishpath, oFilename, camScale, isFilter)