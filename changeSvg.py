import copy
import sys
import xml.etree.ElementTree as ET
import re
from xml.etree.ElementTree import Element
from changeSvgUtils import *

def doPathSvg(parent, child, doTwo, morf):
    path = str(child.attrib)
    path = path.replace('Z', 'z')

    child.attrib.pop("class", None)
    m = re.search('d\':(.+?)z', path)
    if m:
        newChild = copy.deepcopy(child)
        found = m.group(1)

        svgPath = svgSinglePath(found)
        newPath = svgPath.doPath(found, morf)
                    
        add = True
        width = '10'
        child.attrib['stroke']='blue'
        child.attrib['stroke-width']=width
        child.attrib['fill']='none'
        if doTwo == False:
            child.attrib['d']=newPath
        else:
            newChild.attrib['d']=newPath
            newChild.attrib['stroke']='red'
            newChild.attrib['stroke-width']=width
            newChild.attrib['fill']='none'
            parent.append(newChild)
    return

morfDst = sys.argv[1]
nameSrc = sys.argv[2]
nameDst = sys.argv[3]
tree = ET.parse(nameSrc)
root = tree.getroot()

add = None
doTwo = True
doTwo = False
for child in root:
    index = child.tag.find('}') 
    if index > 0:
        tstSt = child.tag[index+1:]
        if tstSt in 'namedview':
            root.remove(child)

for ii in range(len(root)):
    child = root[ii]
    index = child.tag.find('}') 
    if index > 0:
        tstSt = child.tag[index+1:]
        # if tstSt in 'namedview':
            # root.remove(child)
            # xx = False
            # xx = root.attrib.pop(child.tag, None)
            # xx = child.attrib.pop(child.tag, None)
        if tstSt in 'g':
            for iiG in range(len(child)):
                childG = child[iiG]
                tstStG = childG.tag[index+1:]
                if tstStG in 'path':
                    doPathSvg(child, childG, doTwo, morfDst)
                pass
        if tstSt in 'path':
            doPathSvg(root, child, doTwo, morfDst)


ET.register_namespace("", "http://www.w3.org/2001")
tree.write(nameDst)        
with open(nameDst, "r") as f:
    lines = f.readlines()
with open(nameDst, "w") as f:
    for line in lines:
        line = line.replace('ns0:', '')
        line = line.replace(':ns0', '')
        f.write(line)
print('finOk')