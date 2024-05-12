@echo off
chcp 65001
echo 游戏正在启动中，请稍等... 
start "" RainbowSix.exe /belaunch
echo 此窗口按任意键可中止启动，立刻退出游戏，清理残余R6进程！
pause
echo 游戏正在关闭...
TASKKILL.EXE /IM RainbowSix.exe /F
pause
echo...