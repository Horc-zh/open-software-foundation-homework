@echo off
setlocal enabledelayedexpansion

:: 设置GitHub仓库的URL
set "REPO_URL=https://github.com/yourusername/yourrepository.git"
:: 设置本地仓库路径
set "REPO_PATH=C:\path\to\your\repo"

:: 进入仓库目录
cd /d %REPO_PATH%

:: 循环开始
:loop
:: 生成随机时间（单位：秒），范围1到60秒
set /a "randtime=!random! %% 60 + 1"
echo Waiting for !randtime! seconds...
timeout /t !randtime!

:: 生成新文件名
set "newfile=commit_!random!.txt"

:: 创建新文件并写入内容
echo This is commit number: !random! > !newfile!

:: 添加文件到git
git add !newfile!

:: 提交更改
git commit -m "Automated commit with new file !newfile!"

:: 推送到GitHub
git push origin main

:: 循环回到开始
goto loop

:: 随机数生成器
:random
set /a "i=!random! * !random!"
goto :eof