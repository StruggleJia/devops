# 把图片根据某个靶图做区域热点

### 需要安装cv2，不通操作系统不一样
### mac安装(不一定能成功)
```
pip3 install opencv-python
```
###安装之后就可以运行ImageToHtmlArea.py这个脚本了
11.png是原图
22.png是靶图，可以通过图片编辑软件裁出来


###注意：不通的图片转出来的二值可能不一样，所以程序可能需要做适当调整


###网页代码
```
<html>
<img src="11.png" alt="" usemap="#Map" />
<map name="Map" id="Map">
    打印出来的东西贴在这里
</map>
</html>
```
