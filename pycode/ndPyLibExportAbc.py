# -*- coding: utf-8 -*-

import os
import re

import maya.cmds as mc
import maya.mel as mel


def norefresh(func):
    def _norefresh(*args):
        try:
            mc.refresh(suspend=True)
            return func(*args)
        finally:
            mc.refresh(suspend=False)
    return _norefresh


def _getNamespace():
    namespaces = mc.namespaceInfo(lon=True, r=True)
    namespaces.remove('UI')
    namespaces.remove('shared')
    return namespaces


def _getAllNodes(outputPath, namespace, regexArgs):
    namespace = namespace.rstrip('$')##お試し

    if len(regexArgs) == 0:
        regexArgs = ['*']

    nodes = []
    for regex in regexArgs:
        regexN = ''
        if namespace != '':
            regexN += namespace + ':'
        regexN = regexN + regex
        objs = mc.ls(regexN, type='transform')
        try:
            objSets = mc.sets(regexN, q=True)
            if len(objs) != 0:
                nodes += objs
            if len(objSets) != 0:
                nodes += objSets
            yetiobjs = mc.ls(namespace+':yetiSet')
            if len(yetiobjs) != 0:
            #     nodes += yetiobjs
            #     nodes += mc.sets(namespace+':yetiSet',q=True)
                dirname = os.path.dirname(outputPath)
                dirname = os.path.dirname(dirname)
                inyeticasch = mc.getAttr(namespace+":pgYetiMaya"+namespace+"Shape.cacheFileName")
                outyeticasch = mc.getAttr(namespace+":pgYetiMaya"+namespace+"Shape.outputCacheFileName")
                outputFile = os.path.join(dirname,'yetimem.txt')
                try:
                    with open(outputFile, 'w') as fp:
                        fp.write(inyeticasch)
                        fp.write('\n')
                        fp.write(outyeticasch)
                except:
                    pass
        except:
            pass


    return nodes

@norefresh
def _exportAbc (publishpath, oFilename, namespaceList, regexArgs):
    allNamespaces = []
    if len(namespaceList) == 0:
        allNamespaces = _getNamespace()
    else:
        allNamespaces = namespaceList

    allNodes = {}
    for ns in allNamespaces:
        allNodes[ns] = _getAllNodes(publishpath, ns, regexArgs)

    if not mc.pluginInfo('AbcExport', q=True, l=True):
        mc.loadPlugin('AbcExport')

    frameHandle = 5

    outputfiles = []
    for ns in allNamespaces:
        pickNodes = []
        pickNodes = allNodes[ns]
        print pickNodes
        if len(pickNodes) == 0: continue
        outputfile = os.path.join(publishpath, oFilename+'_'+ns+'.abc')
        outputfile = outputfile.replace(os.path.sep, '/')
        outputfiles.append(outputfile)

        strAbc = ''
        strAbc = strAbc + '-frameRange '
        strAbc = strAbc + str(sframe) + ' '
        strAbc = strAbc + str(eframe) + ' '
        strAbc = strAbc + '-uvWrite '
        strAbc = strAbc + '-worldSpace '
        strAbc = strAbc + '-writeVisibility '
        strAbc = strAbc + '-eulerFilter '
        strAbc = strAbc + '-dataFormat ogawa '
        for pn in pickNodes:
            strAbc = strAbc + '-root '
            strAbc = strAbc + pn + ' '
        strAbc = strAbc + '-file '
        strAbc = strAbc + outputfile

        print 'AbcExport -j ' + strAbc
        #mel.eval('AbcExport -j ' + '"' + strAbc + '"')

    return outputfiles


def ndPyLibExportAbc (namespaceList, regexArgs, outputFile=None, isLatest=1):
    if mc.file(q=True, modified=True):
        mc.warning('please save scene file...')
        return

    filepath = mc.file(q=True, sceneName=True)
    filename = os.path.basename(filepath)

    match = re.match('(P:/Project/[a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)', filepath)
    if match is None:
        mc.warning('aaaaaa')
        mc.warning('directory structure is not n-design format')
        return

    project  = match.group(1)
    roll     = match.group(3)
    sequence = match.group(4)
    shot     = match.group(5)

    shotpath = os.path.join(project, 'shots', roll, sequence, shot)

    abcOutDir = 'animGeo'
    publishpath = os.path.join(shotpath, 'publish', abcOutDir, filename)

    oFilename = sequence + shot + '_animGeoCache'

    if not os.path.exists(shotpath):
        mc.warning('no exist folder...')
        return

    if not os.path.exists(publishpath):
        publishpath = os.path.normpath(publishpath)
        os.makedirs(publishpath)

    outputfiles = _exportAbc(publishpath, oFilename, namespaceList, regexArgs)

    for o in outputfiles:
        print 'output file : ' + o

    if outputFile is not None:
        print outputFile
        with open(outputFile, 'w') as fp:
            for o in outputfiles:
                fp.write(o)

    return outputfiles

    # if isLatest:
    #     for o in outputfiles:


def _exportAbc2 (outputPath, namespaceList, regexArgs, step_value, framerange_output=False):
    sframe = mc.playbackOptions(q=True, min=True)
    eframe = mc.playbackOptions(q=True, max=True)

    ###
    sframe -= 10
    eframe += 10
    if framerange_output == 'True':
        with open(os.path.join(publishpath, '..', 'sceneConf.txt').replace('\\', '/'), 'w') as f:
            f.write(str(sframe)+'\n')
            f.write(str(eframe)+'\n')

    allNamespaces = []
    if len(namespaceList) == 0:
        allNamespaces = _getNamespace()

    else:
        print namespaceList
        print '>>>>>>>>>>>>>'
        # for x in namespaceList:
        #     allNamespaces.append(x)

        tmpNS = _getNamespace()
        print tmpNS

        for _nsList in namespaceList:
            for _ns in tmpNS:
                match = re.match(_nsList, _ns)
                print _nsList + ' ' + _ns
                if match != None:
                    allNamespaces.append(_ns)

        print allNamespaces

    allNodes = {}
    for ns in allNamespaces:
        allNodes[ns] = _getAllNodes(outputPath, ns, regexArgs)

    if not mc.pluginInfo('AbcExport', q=True, l=True):
        mc.loadPlugin('AbcExport')

    for ns in allNamespaces:
        pickNodes = []
        pickNodes = allNodes[ns]
        if len(pickNodes) == 0: continue

        print pickNodes

        if ':' in ns:
            ns = ns.replace(':', '___')
        outputPath_ns = outputPath.replace('.abc', '_'+ns+'.abc')

        print sframe
        print eframe

        strAbc = ''
        strAbc = strAbc + '-frameRange '
        strAbc = strAbc + str(sframe) + ' '
        strAbc = strAbc + str(eframe) + ' '

        strAbc = strAbc + '-uvWrite '
        # strAbc = strAbc + '-worldSpace '
        strAbc = strAbc + '-writeVisibility '
        strAbc = strAbc + '-eulerFilter '
        strAbc = strAbc + '-dataFormat ogawa '
        strAbc = strAbc + '-step '
        strAbc = strAbc + step_value + ' '
        for pn in pickNodes:
            strAbc = strAbc + '-root '
            strAbc = strAbc + pn + ' '
        strAbc = strAbc + '-file '
        strAbc = strAbc + outputPath_ns

        print 'AbcExport -j ' + strAbc
        mel.eval('AbcExport -verbose -j ' + '"' + strAbc + '"')

def ndPyLibExportAbc2 (namespaceList, regexArgs, outputPath, step_value, framerange_output=False):
    print 'x'*20
    print regexArgs
    print namespaceList
    print outputPath
    print step_value
    _exportAbc2(outputPath, namespaceList, regexArgs, step_value, framerange_output)
