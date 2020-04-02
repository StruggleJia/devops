#!/usr/bin/env python
#coding:utf-8
#code by struggle

import os
import sys
import cv2
import numpy as np
import pytesseract
from PIL import Image

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
                tmp_image = self.img_gray[info[1]:info[1]+ self.h, info[0] + self.w:info[0] + 3*self.w]
                cv2.imwrite("tmp.png", tmp_image)
                tmp_image = cv2.imread("tmp.png")
                text = pytesseract.image_to_string(tmp_image, config='--psm 7')
                return text

    def match_img(self):
        getstrinfo = ""
        res = cv2.matchTemplate(self.img_gray, self.template,cv2.TM_CCOEFF_NORMED)
        loc = np.where( res >= self.threshold)
        for pt in zip(*loc[::-1]):
            getstrinfo = self.__getstr(pt)
        return getstrinfo

def walk_files(path):
    for root,dirs,files in os.walk(path):
        pass
    return files

if __name__ == "__main__":
    mypath = os.getcwd()
    allfile = walk_files(mypath + "/d_image")
    t_file = ['t.png', 't2.png', 't3.png', 't4.png', 't5.png', 't6.png', 't7.png', 't8.png', 't9.png']
    f = {}
    print(allfile)
    for i in allfile:
        try:
            if i.endswith(".jpg") or i.endswith(".JPG"):
                for t in t_file:
                    a = ImageToHtmlArea(mypath + "/d_image/"+ i, mypath + "/t_image/" + t, 0.9)
                    p = a.match_img()
                    if p:
                        print(i + "识别成功，金额： " + str(p.replace('|','').replace(' ','')))
                        break
                if p:
                    if p not in f:
                        f[p] = 0
                        os.rename(mypath + "/d_image/"+ i, mypath + "/d_image/" + str(p.replace('|','').replace(' ','')) + ".jpg")
                    else:
                        f[p] = f[p] + 1
                        os.rename(mypath + "/d_image/"+ i, mypath + "/d_image/" + str(p.replace('|','').replace(' ','')) + "(" + str(f[p] + 1) +")" + ".jpg")
        except:
            print("error")