# import json
# from urllib import request  
# url = 'https://api-server-name.com/methodname_post'  
# param_dict = {'param': 'data'}  
# response = request.post(url, data=json.dumps(param_dict))

import os
import shutil
import pathlib
from changeSvg import *

# dirWork = '/home/andy/Works/andyWork/lekalo/svgAll/out/'
# dirDst  = '/home/andy/Works/andyWork/lekalo/svgAllDst1/'
dirWork = '/home/andy/Works/andyWork/lekalo/svgAll/'
dirDst  = '/home/andy/Works/andyWork/lekalo/svgTemp/'

def getFiles(filesDir):
    if os.path.isdir(filesDir) == True:
        files = []
        for f in os.scandir(filesDir):
            if f.is_file() and f.path.split('.')[-1].lower() == 'svg':
                files.append(f.path)
        return files
    return None

listFiles = getFiles(dirWork)
allOk =0
allBad =0
for file in listFiles:
    nameSrc = file
    name = pathlib.Path(file).stem
    # morfDst = 'src=0_sx=1.01_sy=1.005'
    # morfDst = 'src=0_a=1'
    morfDst = 'a=1'
    nameDst = dirDst + name + '.svg'
    doChangeSvg(morfDst, nameSrc, nameDst)

    # for angle in range(-15,15,1):
    #     morfDst = 'src=0_a='+str(angle)
    #     nameDst = dirDst + name + '_' + str(angle) +'.svg'
    #     try:
    #         doChangeSvg(morfDst, nameSrc, nameDst)
    #     except Exception:
    #         allBad +=1
    #         print('Bad' + str(allBad))
    #     allOk +=1
print('OK ' + str(allOk))
print('Bad ' + str(allBad))
