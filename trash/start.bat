setlocal enabledelayedexpansion
chcp 65001 &
wsl ./tesseract.sh &
for /F "usebackq delims=" %%A in (`type modified_res.txt`) do set voice=!voice!%%A &
C:\Users\oogar\application\BouyomiChan\RemoteTalk\RemoteTalk.exe /Talk "%voice%" &
exit &