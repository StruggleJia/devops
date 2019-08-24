#!/usr/bin/env python
#coding:utf-8
#code by struggle
import cv2 #这个包需要安装 pip3 install opencv-python
import numpy as np

def findline(image, Target, info):
    uniq = []
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target,0)
    w, h = template.shape[::-1]
    for pt in info:
        #print(pt)
        zs = pt
        yx = (pt[0] + w, pt[1] + h)
        #print(zs,yx)
        l, u, r, d = left, up, right, down = zs[0], zs[1], yx[0], yx[1]
        while l > 0:
            if img_gray[up, l] == 0 or img_gray[up, l] != 255:
                #print(l)
                break
            l = l - 1
        while u > 0:
            if img_gray[u, left] == 0 or img_gray[u, left] !=255 :
                #print(u)
                break
            u = u - 1
        while r > 0:
            if img_gray[down, r] == 0 or img_gray[down, r] != 255:
                #print(r)
                break
            r = r + 1
        while d > 0:
            if img_gray[d, right] == 0 or img_gray[d, right] != 255:
                #print(d)
                break
            d = d + 1
        maplist = ",".join([str(l),str(u),str(l),str(d),str(r),str(d),str(r),str(u)])
        if maplist not in uniq:
            uniq.append(maplist)
    return uniq

def mathc_img(image, Target, value):
    allarea = []
    img_rgb = cv2.imread(image)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    template = cv2.imread(Target,0)
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
    threshold = value
    loc = np.where( res >= threshold)
    return zip(*loc[::-1])
    #for pt in zip(*loc[::-1]):
    #    print(pt)
    #    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (7,249,151), 2)
    #cv2.imshow('Detected',img_gray)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

if __name__ == "__main__":
    image=("11.png") #原图 
    Target=('22.png') #图形里的靶点
    value=0.9 #匹配精确度
    arealist = mathc_img(image,Target,value)
    area = findline(image, Target, arealist)
    for i in area:
        print('<area alt="" title="" href="#" shape="poly" coords="' + i + '" />') # 直接打印html里的area标签



"""
<html>
<img src="11.png" alt="" usemap="#Map" />
<map name="Map" id="Map">
    打印出来的东西贴在这里
</map>
</html>
"""