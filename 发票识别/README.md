# 通过发票<<(小写)¥>>来识别发票的金额，并根据金额对发票进行重命名
# 以后还会根据情况对抬头或者发票编号进行识别

### 需要安装cv2，不同操作系统不一样
### macos需要安装的东西(我这次只装了这么多，根据情况而定)
```
pip3 install opencv-python
pip3 install pytesseract
brew install tesseract
```
```
t_image 是模板文件，通过该模板文件进行匹配
d_image 是需要识别的发票的jpg文件的存放位置，注意格式必须是.jpg或者.JPG
main.py 程序主文件，直接运行即可
python3 main.py 此脚本运行在python3环境下
```
###如有问题，请联系微信 82128679，备注：github
