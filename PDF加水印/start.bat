@echo off
set current_dir=%cd%
echo %current_dir%
cd /d "%current_dir%"\PDF-WaterMarker
echo 请把水印图片png放在watermarker目录下，文件名是logo.png
echo 请把需要加水印的图片房子放在input目录下

pause
"%current_dir%"\python-3.7\python.exe watermarker.py

echo 转换完成，转换后的文件在ouput目录下

pause
