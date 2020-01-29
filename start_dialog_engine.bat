@echo off
:: This a simple program to start the environment of FAPS NLU

echo Refresh environment variables
call refreshenv
:: 'call docker run --restart=always -d -p 8000:8000 -it --name faps_duckling rasa/duckling:latest
echo Pull dockling service
call docker pull rasa/duckling
echo Start the container
call docker container ls --all
call docker run --restart=always -d -p 8000:8000 -it --name faps_duckling rasa/duckling:latest
echo Start RASA engine\n
call cd DialogEngineService
call "C:\ProgramData\Anaconda3\Scripts\activate.bat"
call conda activate RASA
start rasa run actions
start rasa run
pause
echo Start FAPS NLU

