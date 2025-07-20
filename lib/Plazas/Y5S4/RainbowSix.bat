@echo off
chcp 65001
echo 游戏正在启动中，请稍等... 
start "" RainbowSix.exe /belaunch
echo 此窗口按任意键可退出游戏，清理残余R6进程 (解决r6s退游戏残留进程bug)！
pause
echo 游戏正在关闭...
TASKKILL.EXE /IM RainbowSix.exe /F
pause
echo...