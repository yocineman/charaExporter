# -*- coding: utf-8 -*-

import os
import re

# publishpath = shotpath + 'publish' + 'charSet' + char
# publishfullpath = publishpath + currentVer
# publishfullabcpath = publishfullpath + 'abc'

class outputPathConf (object):

    def __init__ (self, inputPath):
        self.inputPath = inputPath
        match = re.match('(P:/Project/[a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)/([a-zA-Z0-9]+)', inputPath)
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
        try:
            os.mkdir(self._publishfullpath)
            os.mkdir(self._publishfullabcpath)
        except:
            pass

    @property
    def publishpath (self):
        return self._publishpath.replace(os.path.sep, '/')

    @property
    def publishfullpath (self):
        return self._publishfullpath.replace(os.path.sep, '/')

    @property
    def publishfullabcpath (self):
        return self._publishfullabcpath.replace(os.path.sep, '/')

