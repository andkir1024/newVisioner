import codecs
import copy
import sys
import xml.etree.ElementTree as ET
import re
from xml.etree.ElementTree import Element
from changeSvgUtils import *

def doPathSvg(parent, child, doTwo, morf, globalSize, sizeSvg):
    path = str(child.attrib)
    path = path.replace('Z', 'z')

    child.attrib.pop("class", None)
    m = re.search('d\':(.+?)z', path)
    if m:
        newChild = copy.deepcopy(child)
        found = m.group(1)

        svgPath = svgSinglePath(found)
        newPath = svgPath.doPath(found, morf, globalSize, sizeSvg)
                    
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
# кординаты лекала
minX = minY = 10000000
maxX = maxY =-10000000 

def getSizePathSvg(parent, child, doTwo, morf):
    global  minX, maxX, minY, maxY
    path = str(child.attrib)
    path = path.replace('Z', 'z')

    child.attrib.pop("class", None)
    m1 = re.search('d=\':(.+?)z', path)
    m = re.search('d\':(.+?)z', path)
    
    s = 'STARTabcdENDefSTARTghiEND'
    a = 'START'
    b = 'END'
    out = re.findall(a+'(.+?)'+b, s)
    out1 = re.findall('d\''+'(.+?)'+'z', path)
    
    if m:
        found = m.group(1)
        svgPath = svgSinglePath(found)
        minX, minY, maxX, maxY = svgPath.getGlobalMinMax(minX, minY, maxX, maxY)
        pass
    return

def doChangeSvg(morfDst, nameSrc, nameDst):
    tree = ET.parse(nameSrc)
    root = tree.getroot()

    doTwo = True
    doTwo = svgSinglePath.decodeIsTwo(morfDst)
    # doTwo = False
    # удаление ненужных ветвей 
    for child in root:
        index = child.tag.find('}') 
        if index > 0:
            tstSt = child.tag[index+1:]
            if tstSt in 'namedview':
                root.remove(child)

    # расчет размеров
    for ii in range(len(root)):
        child = root[ii]
        index = child.tag.find('}') 
        if index > 0:
            tstSt = child.tag[index+1:]
            if tstSt in 'g':
                for iiG in range(len(child)):
                    childG = child[iiG]
                    tstStG = childG.tag[index+1:]
                    if tstStG in 'path':
                        getSizePathSvg(child, childG, doTwo, morfDst)
                    pass
            if tstSt in 'path':
                getSizePathSvg(root, child, doTwo, morfDst)
                
    globalSize = [minX, minY, maxX, maxY]            

    # обработка всех Path
    viewBox = root.attrib['viewBox']
    width = root.attrib['width']
    height = root.attrib['height']
    sizeSvg = [width, height, viewBox]

    for ii in range(len(root)):
        child = root[ii]
        index = child.tag.find('}') 
        if index > 0:
            tstSt = child.tag[index+1:]
            if tstSt in 'g':
                for iiG in range(len(child)):
                    childG = child[iiG]
                    tstStG = childG.tag[index+1:]
                    if tstStG in 'path':
                        doPathSvg(child, childG, doTwo, morfDst, globalSize, sizeSvg)
                    pass
            if tstSt in 'path':
                doPathSvg(root, child, doTwo, morfDst, globalSize, sizeSvg)


    ET.register_namespace("", "http://www.w3.org/2001")
    tree.write(nameDst) 

    # удаление служебных ненужных символов
    with open(nameDst, "r") as f:
        lines = f.readlines()
    with codecs.open(nameDst, "w","utf-8") as f:
    # with open(nameDst, "w", "utf-8") as f:
        for line in lines:
            line = line.replace('ns0:', '')
            line = line.replace(':ns0', '')
            f.write(line)
    print('finOk')
    
morfDst = sys.argv[1]
nameSrc = sys.argv[2]
nameDst = sys.argv[3]
doChangeSvg(morfDst, nameSrc, nameDst)
    