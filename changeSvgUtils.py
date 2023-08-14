import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import re
import math

class svgSinglePath:
    minX = minY = 10000000
    maxX = maxY =-10000000
    centerX = centerY = 0
    propLekalo = 1
    pathString = ""
    currentX = currentY = 0
    def __init__(self, path):
        self.pathString = path
        # нахождение положения path
        self.calkPathCoord(path)
        
    def getGlobalMinMax(self, minX, minY, maxX, maxY):
        minX = min(self.minX, minX)
        minY = min(self.minY, minY)

        maxX = max(self.maxX, maxX)
        maxY = max(self.maxY, maxY)
        return minX, minY, maxX, maxY
    def getMinMax(self, px, py):
        self.minX = min(self.minX, px)
        self.minY = min(self.minY, py)

        self.maxX = max(self.maxX, px)
        self.maxY = max(self.maxY, py)
        return
    def is_number(s):
        try:
            res = float(s)
            return res
        except ValueError:
            return None
    def getCoords(digits):
        params = re.split(",| ", digits)    
        result = []
        for dg in params:
            val = svgSinglePath.is_number(dg)
            if val is not None:
                result.append(val)
        if len(result)==0:
            return None
        return result
    def doDispAndScale(self, rs, index, dx, dy, scaleX, scaleY):
        isX = True if (index%2)==0 else False
        if scaleY < 0:
            if scaleX>= 1:
                scaleX = scaleX - int(scaleX)
            else:
                scaleX = -(1 - scaleX)
            if isX:
                pp = ((rs - self.centerX) * (1 + scaleX)) + self.centerX + dx
            else:
                pp = ((rs - self.centerY) * (1 + (scaleX*self.propLekalo))) + self.centerY + dy
        else:
            if isX:
                pp = ((rs) * ((scaleX))) +  dx
            else:
                pp = ((rs) * ((scaleY))) +  dy
        # pp = int(pp)
        return pp
    def doDigits(self, marker, digits, dx, dy, scaleX, scaleY):
        params = re.split(",| ", digits)    
        result = []
        for dg in params:
            val = svgSinglePath.is_number(dg)
            if val is not None:
                result.append(val)
        if len(result)==0:
            return None
        out = marker 
        for index, rs in enumerate(result):
            pp = self.doDispAndScale(rs, index, dx, dy, scaleX, scaleY)
            if index < len(result)-1:
                out = out + str(pp) + ','
            else:
                out = out + str(pp) + ''
                
        return out
    def doDigitsRelToAbs(self, marker, digits, dx, dy, scaleX, scaleY):
        if digits is None:
            return None
        out = marker 
        for index, rs in enumerate(digits):
            pp = self.doDispAndScale(rs, index, dx, dy, scaleX, scaleY)
            if index < len(digits)-1:
                out = out + str(pp) + ','
            else:
                out = out + str(pp) + ''
                
        return out
    def getDigits(self, digits):
        params = re.split(",| ", digits)    
        result = []
        for dg in params:
            val = svgSinglePath.is_number(dg)
            if val is not None:
                result.append(val)
        if len(result)==0:
            return None
        return result
    def calkPathCoord(self, path):
        self.minX =self.minY = 10000000
        self.maxX =self.maxY =-10000000
        self.propLekalo = 1
        params =svgSinglePath.splitPath( path)
        for index, item in enumerate(params):
            res = None
            # абсолютные координаты
            if item == 'M' or item == 'm':
                res = svgSinglePath.getCoords(params[ index + 1])
                self.currentX = res[0]
                self.currentY = res[1]
                self.getMinMax(res[0], res[1])
            if item == 'L':
                res = svgSinglePath.getCoords(params[ index + 1])
                self.currentX = res[0]
                self.currentY = res[1]
                self.getMinMax(res[0], res[1])
            if item == 'H':
                tmp = params[ index + 1] + " , 0"
                res = svgSinglePath.getCoords(tmp)
                self.currentX = res[0]
                self.getMinMax(self.currentX, self.currentY )
            if item == 'V':
                tmp = " 0, " + params[ index + 1]
                res = svgSinglePath.getCoords(tmp)
                self.currentY = res[1]
                self.getMinMax(self.currentX, self.currentY )
            if item == 'C':
                res = svgSinglePath.getCoords(params[ index + 1])
                self.getMinMax(res[4], res[5])
            # относительные координаты
            if item == 'l':
                res = svgSinglePath.getCoords(params[ index + 1])
                self.currentX += res[0]
                self.currentY += res[1]
                self.getMinMax(self.currentX, self.currentY)
            if item == 'c':
                res = svgSinglePath.getCoords(params[ index + 1])
                self.currentX += res[4]
                self.currentY += res[5]
                self.getMinMax(self.currentX, self.currentY)
            if item == 'v':
                tmp = " 0, " + params[ index + 1]
                res = svgSinglePath.getCoords(tmp)
                self.currentX += res[0]
                self.currentY += res[1]
                self.getMinMax(self.currentX, self.currentY)
            if item == 'h':
                tmp = params[ index + 1] + " , 0"
                res = svgSinglePath.getCoords(tmp)
                self.currentX += res[0]
                self.currentY += res[1]
                self.getMinMax(self.currentX, self.currentY)
            pass
        self.centerX = self.minX + (self.maxX - self.minX)/2
        self.centerY = self.minY + (self.maxY - self.minY)/2
        self.propLekalo = (self.maxX - self.minX)/(self.maxY - self.minY)
        return None
    def decodeIsTwo(morf):
        params = morf.split('_')
        for pp in params:
            vals = pp.split('=')
            if vals[0] == 'src':
                return True
        return False
    def decodeMorph(morf):
        dx = dy = 0
        sx = sy = 1
        cx = cy = 1
        a = 0
        m = -1
        params = morf.split('_')
        for pp in params:
            vals = pp.split('=')
            if vals[0] == 'dx':
                dx = float(vals[1])
            if vals[0] == 'dy':
                dy = float(vals[1])
            if vals[0] == 'sx':
                sx = float(vals[1])
            if vals[0] == 'sy':
                sy = float(vals[1])
            if vals[0] == 'cx':
                cx = float(vals[1])
            if vals[0] == 'cy':
                cy = float(vals[1])
            if vals[0] == 'a':
                a = float(vals[1])
            if vals[0] == 'm':
                m = int(vals[1])
            pass
        return dx, dy, sx, sy, cx, cy, a, m

    def rotate(origin, point, angle):
        """
        Rotate a point counterclockwise by a given angle around a given origin.
        The angle should be given in radians.
        """
        angle = math.radians(angle)
        ox, oy = origin
        px, py = point
        qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
        qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
        return qx, qy
    def rotateDigits(cx, cy, digits, angle):
        origin = cx, cy
        for index in range(0, len(digits), 2):
            point = digits[index], digits[index + 1]
            rotated = svgSinglePath.rotate(origin, point, angle)
            digits[index] = rotated[0]
            digits[index + 1] = rotated[1]
            pass
        return    
    def splitPath( path):
        path = path[2:]
        pathPure = path.replace(' ', '_') 
        pathPure = path.replace('_', '') 
        
        params =re.split('([M|L|C|V|H|m|l|c|v|h])',pathPure)
        return params
    
    ''' размеры
em     The default font size - usually the height of a character.
ex     The height of the character x
px     Pixels
pt     Points (1 / 72 of an inch)
pc     Picas (1 / 6 of an inch)
cm     Centimeters
mm     Millimeters
in     Inches
%       percentages
    '''
    def calkScaleMode1(self, sx, sy, globalSize, sizeSvg):
        return sx, sy
    def doPath(self, path, morf, globalSize, sizeSvg):
        dx, dy, sx, sy, cx, cy, a, m = svgSinglePath.decodeMorph(morf)
        if m == 0:
            dx = -globalSize[0]
            dy = -globalSize[1]
        if m == 1:
            sx, sy = self.calkScaleMode1(sx, sy, globalSize, sizeSvg)
        params =svgSinglePath.splitPath( path)
        newD = ''
        curX = curY = None
        for index, item in enumerate(params):
            res = None
            # абсолютный путь
            if item == 'M' or item == 'm':
                curX, curY, digits = self.convertRelToAbs(curX, curY, params[ index + 1])
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('M', digits, dx, dy, sx, sy)
            if item == 'L':
                res = self.doDigits('L', params[ index + 1], dx, dy, sx, sy)
            if item == 'C':
                res = self.doDigits('C', params[ index + 1], dx, dy, sx, sy)
            if item == 'V':
                tmp = " 0, " + params[ index + 1]
                # curX, curY, digits = self.convertRelToAbs(None, None, tmp)
                curX, curY, digits = self.convertVH(curX, curY, tmp, True)
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('L', digits, dx, dy, sx, sy)
            if item == 'H':
                tmp = params[ index + 1] + " , 0"
                # curX, curY, digits = self.convertRelToAbs(curX, curY, tmp)
                curX, curY, digits = self.convertVH(curX, curY, tmp, False)
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('L', digits, dx, dy, sx, sy)
            # относительный путь
            if item == 'l':
                curX, curY, digits = self.convertRelToAbs(curX, curY, params[ index + 1])
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('L', digits, dx, dy, sx, sy)
                pass
            if item == 'h':
                tmp = params[ index + 1] + " , 0"
                curX, curY, digits = self.convertRelToAbs(curX, curY, tmp)
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('L', digits, dx, dy, sx, sy)
            if item == 'v':
                tmp = " 0, " + params[ index + 1]
                curX, curY, digits = self.convertRelToAbs(curX, curY, tmp)
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('L', digits, dx, dy, sx, sy)
            if item == 'c':
                curX, curY, digits = self.convertRelToAbs(curX, curY, params[ index + 1])
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('C', digits, dx, dy, sx, sy)
                pass
            if res is not None:
                if newD == '':
                    newD = res
                else:
                    newD = newD + ' ' + res
        newD = newD + 'Z'
        return newD
    def convertVH(self, curX, curY, params, isV):
        digits = self.getDigits(params)
        if digits is not None:
            if isV:
                curY = digits[1]
                digits[0] = curX
            else:
                curX = digits[0]
                digits[1] = curY
            return curX, curY, digits
        return None, None, None
    def convertRelToAbs(self, curX, curY, params):
        digits = self.getDigits(params)
        if digits is not None:
            all = int(len(digits)/2)
            for index in range(all):
                iX = index * 2
                iY = (index * 2) + 1
                if curX is None:
                    curX = digits[iX]
                    curY = digits[iY]
                elif all == 1: 
                    dX = curX + digits[iX]
                    dY = curY + digits[iY]
                    digits[iX] = int(dX)
                    digits[iY] = int(dY)
                    curX = dX
                    curY = dY
                else:
                    dX = curX + digits[iX]
                    dY = curY + digits[iY]
                    digits[iX] = int(dX)
                    digits[iY] = int(dY)
                    partThree = (index+1) % 3
                    if partThree == 0:
                        curX = dX
                        curY = dY
                    pass
            return curX, curY, digits
        return None, None, None
