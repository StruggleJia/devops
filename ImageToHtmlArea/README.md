# 通过靶图分析靶向区域文字，确定唯一的靶向区域坐标，并通过坐标做热点坐标

### 需要安装cv2，不同操作系统不一样
### macos需要安装的东西(我这次只装了这么多，根据情况而定)
```
pip3 install opencv-python
pip3 install pytesseract
brew install tesseract
```
### 安装之后就可以运行或者引用NewImageToHtmlArea.py这个脚本了
11.png是原图
22.png是靶图，可以通过图片编辑软件裁出来


### 注意：不同的图片转出来的二值可能不一样，所以程序可能需要做适当调整


### 网页代码 title和coords都是代码自动生成出来的
```
<html>
<img src="11.png" alt="" usemap="#Map" />
<map name="Map" id="Map">
	<area alt="" title="BDO2" href="#" shape="poly" coords="409,11,409,332,584,332,584,11" />
	<area alt="" title="BDO1" href="#" shape="poly" coords="12,11,12,332,405,332,405,11" />
	<area alt="" title="BDO3" href="#" shape="poly" coords="588,11,588,332,981,332,981,11" />
	<area alt="" title="BDO4" href="#" shape="poly" coords="12,336,12,605,981,605,981,336" />
	<area alt="" title="BDO5" href="#" shape="poly" coords="12,609,12,916,798,916,798,609" />
	<area alt="" title="BDO6" href="#" shape="poly" coords="802,609,802,916,981,916,981,609" />
</map>
</html>

```
