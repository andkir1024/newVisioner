import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
import re
import math

class svgSinglePath:
    minX = maxX = minY = maxY = 0
    centerX = centerY = 0
    propLekalo = 1
    pathString = ""
    currentX = currentY = 0
    def __init__(self, path):
        self.pathString = path
        # нахождение положения path
        self.calkPathCoord(path)
        
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
    def doDigits(self, marker, digits, dx, dy, scale):
        params = re.split(",| ", digits)    
        result = []
        for dg in params:
            val = svgSinglePath.is_number(dg)
            if val is not None:
                result.append(val)
        if len(result)==0:
            return None
        out = marker 
        scale = scale - int(scale)
        for index, rs in enumerate(result):
            isX = True if (index%2)==0 else False
            if isX:
                pp = ((rs - self.centerX) * (1 + scale)) + self.centerX + dx
            else:
                pp = ((rs - self.centerY) * (1 + (scale*self.propLekalo))) + self.centerY + dy
            # pp = int(pp)
            if index < len(result)-1:
                out = out + str(pp) + ','
            else:
                out = out + str(pp) + ''
                
        return out
    def doDigitsRelToAbs(self, marker, digits, dx, dy, scale):
        if digits is None:
            return None
        out = marker 
        if scale>= 1:
            scale = scale - int(scale)
        else:
            scale = -(1 - scale)
        for index, rs in enumerate(digits):
            isX = True if (index%2)==0 else False
            if isX:
                pp = ((rs - self.centerX) * (1 + scale)) + self.centerX + dx
            else:
                pp = ((rs - self.centerY) * (1 + (scale*self.propLekalo))) + self.centerY + dy
            pp = int(pp)
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
        self.minX =self.minY = 100000
        self.maxX =self.maxY = 0
        self.propLekalo = 1
        params =svgSinglePath.splitPath( path)
        for index, item in enumerate(params):
            res = None
            if item == 'M' or item == 'm':
                res = svgSinglePath.getCoords(params[ index + 1])
                self.currentX = res[0]
                self.currentY = res[1]
                self.getMinMax(res[0], res[1])
            if item == 'L':
                res = svgSinglePath.getCoords(params[ index + 1])
                self.getMinMax(res[0], res[1])
            if item == 'l':
                res = svgSinglePath.getCoords(params[ index + 1])
                self.currentX += res[0]
                self.currentY += res[1]
                self.getMinMax(self.currentX, self.currentY)
            if item == 'C':
                res = svgSinglePath.getCoords(params[ index + 1])
                self.getMinMax(res[4], res[5])
            if item == 'c':
                res = svgSinglePath.getCoords(params[ index + 1])
                self.currentX += res[4]
                self.currentY += res[5]
                self.getMinMax(self.currentX, self.currentY)
            pass
        self.centerX = self.minX + (self.maxX - self.minX)/2
        self.centerY = self.minY + (self.maxY - self.minY)/2
        self.propLekalo = (self.maxX - self.minX)/(self.maxY - self.minY)
        return None
    def decodeMorph(morf):
        dx = dy = 0
        sx = sy = 1
        cx = cy = 1
        a = 0
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
            pass
        return dx, dy, sx, sy, cx, cy, a

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
    def doPath(self, path, morf):
        dx, dy, sx, sy, cx, cy, a = svgSinglePath.decodeMorph(morf)
        params =svgSinglePath.splitPath( path)
        newD = ''
        curX = curY = None
        for index, item in enumerate(params):
            res = None
            # абсолютный путь
            if item == 'M' or item == 'm':
                curX, curY, digits = self.convertRelToAbs(curX, curY, params[ index + 1])
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('M', digits, dx, dy, sx)
            if item == 'L':
                res = self.doDigits('L', params[ index + 1], dx, dy, sx)
            if item == 'C':
                res = self.doDigits('C', params[ index + 1], dx, dy, sx)
            if item == 'V':
                tmp = " 0, " + params[ index + 1]
                # curX, curY, digits = self.convertRelToAbs(None, None, tmp)
                curX, curY, digits = self.convertVH(curX, curY, tmp, True)
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('L', digits, dx, dy, sx)
            if item == 'H':
                tmp = params[ index + 1] + " , 0"
                # curX, curY, digits = self.convertRelToAbs(curX, curY, tmp)
                curX, curY, digits = self.convertVH(curX, curY, tmp, False)
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('L', digits, dx, dy, sx)
            # относительный путь
            if item == 'l':
                curX, curY, digits = self.convertRelToAbs(curX, curY, params[ index + 1])
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('L', digits, dx, dy, sx)
                pass
            if item == 'h':
                tmp = params[ index + 1] + " , 0"
                curX, curY, digits = self.convertRelToAbs(curX, curY, tmp)
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('L', digits, dx, dy, sx)
            if item == 'v':
                tmp = " 0, " + params[ index + 1]
                curX, curY, digits = self.convertRelToAbs(curX, curY, tmp)
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('L', digits, dx, dy, sx)
            if item == 'c':
                curX, curY, digits = self.convertRelToAbs(curX, curY, params[ index + 1])
                svgSinglePath.rotateDigits(cx, cy, digits, a)
                res = self.doDigitsRelToAbs('C', digits, dx, dy, sx)
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