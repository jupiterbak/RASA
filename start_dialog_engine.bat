@echo off
:: This a simple program to start the environment of FAPS NLU

echo Refresh environment variables
call refreshenv
:: 'call docker run --restart=always -d -p 8000:8000 -it rasa/duckling:latest --name faps_duckling
echo Start the container
call docker container ls --all
call docker restart faps_duckling
echo Start RASA engine\n
call cd DialogEngineService
call "C:\ProgramData\Anaconda3\Scripts\activate.bat"
call conda activate RASA
start rasa run actions
start rasa run
pause
echo Start FAPS NLU


