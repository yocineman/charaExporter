# -*- coding: utf-8 -*-

import os
import re
import shutil
import distutils.dir_util

# publishpath = shotpath + 'publish' + 'charSet' + char
# publishfullpath = publishpath + currentVer
# publishfullabcpath = publishfullpath + 'abc'


class outputPathConf (object):

    def __init__ (self, inputPath, isAnim=False, test=False, overlap=0):
        self.inputPath = inputPath.replace('\\', '/')
        self.isAnim = isAnim
        self.outputRootDir = 'charSet'
        self.outputCamRootDir = 'Cam'
        self.overlap = overlap
        if test:
            self.outputRootDir = 'test_charSet'
            self.outputCamRootDir = 'test_Cam'
        print self.inputPath
        match = re.match('(P:/Project/[a-zA-Z0-9_]+)/([a-zA-Z0-9_]+)/([a-zA-Z0-9_]+)/([a-zA-Z0-9_]+)/([a-zA-Z0-9_]+)', self.inputPath)
        if match is None:
            raise ValueError('directory structure is not n-design format')

        self._project  = match.group(1)
        self._roll     = match.group(3)
        self._sequence = match.group(4)
        self._shot     = match.group(5)
        self._shotpath = os.path.join(self._project, 'shots', self._roll, self._sequence, self._shot)

    def createOutputDir (self, char):
        self._publishpath = os.path.join(self._shotpath, 'publish', self.outputRootDir, char)
        if os.path.exists(self._publishpath):
            self.verInc()
        else:
            try:
                os.makedirs(self._publishpath)
                self.verInc()
            except:
                pass

    def createCamOutputDir (self):
        self._publishpath = os.path.join(self._shotpath, 'publish', self.outputCamRootDir, os.path.basename(self.inputPath))
        self._publishfullpath = self._publishpath
        if not os.path.exists(self._publishpath):
            try:
                os.makedirs(self._publishpath)
            except:
                pass

    def verInc (self):
        vers = os.listdir(self._publishpath)
        if len(vers) == 0:
            self._currentVer = 'v001'
        else:
            vers.sort()
            currentVer = vers[-1]
            currentVerNum = int(currentVer[1:])
            nextVerNum = currentVerNum + 1
            if self.overlap == 1:
                nextVer = 'v'+str(currentVerNum).zfill(3)
            else:
                nextVer = 'v' + str(nextVerNum).zfill(3)
            self._currentVer = nextVer
        self._publishfullpath = os.path.join(self._publishpath, self._currentVer)
        self._publishfullabcpath = os.path.join(self._publishfullpath, 'abc')
        self._publishfullanimpath = os.path.join(self._publishfullpath, 'anim')
        print self._publishfullpath
        if os.path.exists(self._publishfullpath):
            pass
        else:
            os.mkdir(self._publishfullpath)
            print 'mkdir' + self._publishfullpath
        try:
            if self.isAnim:
                os.mkdir(self._publishfullanimpath)
            else:
                os.mkdir(self._publishfullabcpath)
        except:
            pass

    def makeCurrentDir (self):
        currentDir = os.path.join(self.publishpath, 'current')
        self._publishcurrentpath = currentDir
        # if os.path.exists(currentDir):
        #     shutil.rmtree(currentDir)
        # shutil.copytree(self._publishfullpath, currentDir)
        distutils.dir_util.copy_tree(self._publishfullpath, currentDir)

    def removeDir (self):
        if os.path.exists(self._publishpath+'/current'):
            files = os.listdir(self._publishpath+'/current')
            for f in files:
                if '.ma' in f:
                    return
        shutil.rmtree(self._publishpath)

    def setChar (self, char):
        if char == 'Cam':
            self._publishpath = os.path.join(self._shotpath, 'publish', self.outputCamRootDir, os.path.basename(self.inputPath)).replace(os.path.sep, '/')
            self._publishfullpath = self._publishpath
            self._currentVer = 'Cam'
        else:
            self._publishpath = os.path.join(self._shotpath, 'publish', self.outputRootDir, char).replace(os.path.sep, '/')
            vers = []
            try:
                vers = os.listdir(self._publishpath)
            except WindowsError:
                raise ValueError
            if len(vers) == 0:
                raise ValueError
            vers.sort()
            self._currentVer = vers[-1]
            if vers[0] > vers[-1]:
                self._currentVer = vers[0]
            self._publishfullpath = os.path.join(self._publishpath, self._currentVer)
            self._publishfullabcpath = os.path.join(self._publishfullpath, 'abc')
            self._publishfullanimpath = os.path.join(self._publishfullpath, 'anim')
            self._publishcurrentpath = self._publishpath+'/current'

    @property
    def sequence (self):
        return self._sequence

    @property
    def shot (self):
        return self._shot

    @property
    def publishpath (self):
        return self._publishpath.replace(os.path.sep, '/')

    @property
    def publishfullpath (self):
        return self._publishfullpath.replace(os.path.sep, '/')

    @property
    def publishfullabcpath (self):
        return self._publishfullabcpath.replace(os.path.sep, '/')

    @property
    def publishfullanimpath (self):
        return self._publishfullanimpath.replace(os.path.sep, '/')

    @property
    def publishcurrentpath (self):
        return self._publishcurrentpath.replace(os.path.sep, '/')

    @property
    def currentVer (self):
        return self._currentVer


def addTimeLog (char, inputpath, test):
    from datetime import datetime
    opc = outputPathConf(inputpath, True, test)
    try:
        opc.setChar(char)
    except ValueError:
        return

    print opc.publishfullpath

    with open(os.path.join(opc.publishpath, 'timelog.txt').replace(os.path.sep, '/'), 'a') as f:
        f.write(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        f.write(' ' + opc.currentVer)
        f.write(' ' + inputpath)
        f.write(' ' + os.environ['USERNAME'])
        f.write('\n')
