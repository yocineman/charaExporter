# -*- coding: utf-8 -*-

import os
import re
import shutil
import distutils.dir_util

# publishpath = shotpath + 'publish' + 'charSet' + char
# publishfullpath = publishpath + currentVer
# publishfullabcpath = publishfullpath + 'abc'

class outputPathConf (object):

    def __init__ (self, inputPath, isAnim=False):
        self.inputPath = inputPath.replace('\\', '/')
        self.isAnim = isAnim
        print self.inputPath
        match = re.match('(P:/Project/[a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)', self.inputPath)
        if match is None:
            raise ValueError('directory structure is not n-design format')

        self._project  = match.group(1)
        self._roll     = match.group(3)
        self._sequence = match.group(4)
        self._shot     = match.group(5)
        self._shotpath = os.path.join(self._project, 'shots', self._roll, self._sequence, self._shot)

    def createOutputDir (self, char):
        self._publishpath = os.path.join(self._shotpath, 'publish', 'charSet', char)
        if os.path.exists(self._publishpath):
            self.verInc()
        else:
            try:
                os.makedirs(self._publishpath)
                self.verInc()
            except:
                pass

    def createCamOutputDir (self):
        self._publishpath = os.path.join(self._shotpath, 'publish', 'Cam', os.path.basename(self.inputPath))
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
            nextVer = 'v' + str(nextVerNum).zfill(3)
            self._currentVer = nextVer
        self._publishfullpath = os.path.join(self._publishpath, self._currentVer)
        self._publishfullabcpath = os.path.join(self._publishfullpath, 'abc')
        self._publishfullanimpath = os.path.join(self._publishfullpath, 'anim')
        try:
            os.mkdir(self._publishfullpath)
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
