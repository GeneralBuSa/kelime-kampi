@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo.
echo  Kelime Kampi baslatiliyor: http://localhost:8765
echo  Tarayici birazdan acilacak. Kapatmak icin bu pencereyi kapat.
echo.
start "" cmd /c "timeout /t 2 >nul & start http://localhost:8765"
where python >nul 2>nul
if %errorlevel%==0 (
  python -m http.server 8765 --bind 127.0.0.1
  goto :eof
)
where py >nul 2>nul
if %errorlevel%==0 (
  py -m http.server 8765 --bind 127.0.0.1
  goto :eof
)
echo  Python bulunamadi. Sorun degil: index.html dosyasini cift tiklayarak da acabilirsin.
start "" "%~dp0index.html"
pause
