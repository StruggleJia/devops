#!/usr/bin/env python
#coding:utf-8
#code by struggle

import cv2
import numpy as np
import pytesseract
from PIL import Image
import sys

class ImageToHtmlArea(object):
    def __init__(self, image, target_image, value):
        self.image = image
        self.img_rgb = cv2.imread(image)
        self.img_gray = cv2.cvtColor(self.img_rgb, cv2.COLOR_BGR2GRAY)
        self.template = cv2.imread(target_image,0)
        self.w, self.h = self.template.shape[::-1]
        self.threshold = value
        self.dictinfo = {}

    def __getstr(self,info):
            if info:
                tmp_image = self.img_gray[info[1]:info[1]+ self.h, info[0]:info[0] + self.w + self.w]
                cv2.imwrite("tmp.png",tmp_image)
                tmp_image = cv2.imread("tmp.png")
                text = pytesseract.image_to_string(tmp_image, config='--psm 7')
                return text

    def __getzoneinfo(self,info):
            l, u, r, d = left, up, right, down = info[0], info[1], info[0] + self.w, info[1] + self.h
            while l > 0:
                if self.img_gray[up, l] == 0 or self.img_gray[up, l] != 255:
                    #print(l)
                    break
                l = l - 1
            while u > 0:
                if self.img_gray[u, left] == 0 or self.img_gray[u, left] !=255 :
                    #print(u)
                    break
                u = u - 1
            while r > 0:
                if self.img_gray[down, r] == 0 or self.img_gray[down, r] != 255:
                    #print(r)
                    break
                r = r + 1
            while d > 0:
                if self.img_gray[d, right] == 0 or self.img_gray[d, right] != 255:
                    #print(d)
                    break
                d = d + 1
            maplist = ",".join([str(l),str(u),str(l),str(d),str(r),str(d),str(r),str(u)])
            return maplist
            

    def match_img(self):
        #zb = (434, 539)
        #print(self.__getstr(zb))
        res = cv2.matchTemplate(self.img_gray,self.template,cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= self.threshold)
        for pt in zip(*loc[::-1]):
            getstrinfo = self.__getstr(pt)
            if getstrinfo[0:4] not in self.dictinfo: # and getstrinfo[2].isdigit():
                self.dictinfo[getstrinfo[0:4]] = pt
        #print(self.dictinfo)
    
    def gethotarea(self):
        for k, v in self.dictinfo.items():
            #print(k + " " + self.__getzoneinfo(v))
            print('<area alt="" title="%s" href="#" shape="poly" coords="%s" />' % (k, self.__getzoneinfo(v)))


if __name__ == "__main__":
    a = ImageToHtmlArea("11.png", "22.png", 0.9)
    a.match_img()
    a.gethotarea()



"""
<html>
<img src="11.png" alt="" usemap="#Map" />
<map name="Map" id="Map">
    打印出来的东西贴这里
</map>
</html>
"""






