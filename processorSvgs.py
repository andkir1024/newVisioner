import os
import shutil
import pathlib
from changeSvg import *

dirWork = '/home/andy/Works/andyWork/lekalo/svgAll/out/'
dirDst  = '/home/andy/Works/andyWork/lekalo/svgAllDst/'

def getFiles(filesDir):
    if os.path.isdir(filesDir) == True:
        files = []
        for f in os.scandir(filesDir):
            if f.is_file() and f.path.split('.')[-1].lower() == 'svg':
                files.append(f.path)
        return files
    return None

listFiles = getFiles(dirWork)
morfDst = 'src=0_sx=1.01_sy=1.005'
allOk =0
allBad =0
for file in listFiles:
    nameSrc = file
    name = pathlib.Path(file).stem
    nameDst = dirDst + name + '.svg'
    try:
        doChangeSvg(morfDst, nameSrc, nameDst)
    except Exception:
        allBad +=1
        print('Bad' + str(allBad))
    allOk +=1
print('OK ' + str(allOk))
print('Bad ' + str(allBad))
