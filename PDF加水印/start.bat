@echo off
set current_dir=%cd%
echo %current_dir%
cd /d "%current_dir%"\PDF-WaterMarker
echo ���ˮӡͼƬpng����watermarkerĿ¼�£��ļ�����logo.png
echo �����Ҫ��ˮӡ��ͼƬ���ӷ���inputĿ¼��

pause
"%current_dir%"\python-3.7\python.exe watermarker.py

echo ת����ɣ�ת������ļ���ouputĿ¼��

pause
