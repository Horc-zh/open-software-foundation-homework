@echo off
setlocal enabledelayedexpansion

:: 设置仓库路径
set REPO_PATH="D:\Code\VSCode\other\opensoftware-foundation\auto_commit.bat"
set FILE_PATH="%REPO_PATH%\file.txt"

:: 进入仓库目录
cd /d %REPO_PATH%

:: 无限循环
:loop
    :: 生成随机的时间间隔（比如在5到10分钟之间）
    set /a "randomWaitTime=(5+random*5)"

    :: 等待随机时间
    echo Waiting for %randomWaitTime% seconds...
    timeout /t %randomWaitTime% >nul

    :: 生成新的文件内容
    echo %random% >> %FILE_PATH%

    :: 添加更改到 Git
    git add %FILE_PATH%

    :: 提交更改
    git commit -m "Auto commit at %date% %time%"

    :: 推送到 GitHub
    git push origin main

    :: 返回循环
    goto loop
