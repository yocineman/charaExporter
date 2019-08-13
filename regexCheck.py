import maya.cmds as cmds
import re
import charaExporter.setting.noahASetup
reload(charaExporter.setting.noahASetup)

allCtrl = []
for s in cmds.sets('BGghosttownOutdoorsA:all_anmSet', q=True):
    allCtrl += cmds.sets(s, q=True)

newCtrl = []
for c in allCtrl:
    name = c.split('_')[1:]
    newName = ''
    for n in name:
        newName = newName + '_'
        newName = newName + n
    newCtrl.append(str(newName))

charSet = set(newCtrl)
regex = set([r.replace('*', '') for r in charaExporter.setting.noahASetup.regex])
print charSet - regex
