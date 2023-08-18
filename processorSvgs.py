import os
import shutil

dirWork = '/home/andy/Works/andyWork/lekalo/svgAll'
dirDst  = '/home/andy/Works/andyWork/lekalo/svgAllDst'

def getFiles(filesDir):
    if os.path.isdir(filesDir) == True:
        files = []
        for f in os.scandir(filesDir):
            if f.is_file() and f.path.split('.')[-1].lower() == 'svg':
                files.append(f.path)
        return files
    return None

listFiles = getFiles(dirWork)
for file in listFiles:
    pass
