@echo off
cmd /k "cd /d .. & py -m venv venv & cd /d .\venv\Scripts & activate & cd /d ..\.. & py -m pip install -U pip & pip install -r requirements.txt & del "requirements.txt" & exit"