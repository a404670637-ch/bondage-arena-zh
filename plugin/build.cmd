@echo off
REM Build the optional BepInEx plugin. Pass the game folder as the first argument.
setlocal
set GAME=%~1
if "%GAME%"=="" set GAME=..\..
set CSC=%WINDIR%\Microsoft.NET\Framework64\v4.0.30319\csc.exe
if not exist "%CSC%" (
  echo Cannot find csc.exe at %CSC%
  exit /b 1
)
set MANAGED=%GAME%\Bondage Arena_Data\Managed
set BEP=%GAME%\BepInEx\core\BepInEx.dll
if not exist "%BEP%" (
  echo BepInEx.dll not found. Install BepInEx 5 (x64) into the game folder first.
  exit /b 1
)
"%CSC%" /nologo /target:library /out:BA_ZH.dll ^
  /reference:"%MANAGED%\netstandard.dll" ^
  /reference:"%MANAGED%\UnityEngine.dll" ^
  /reference:"%MANAGED%\UnityEngine.CoreModule.dll" ^
  /reference:"%MANAGED%\UnityEngine.UI.dll" ^
  /reference:"%MANAGED%\Unity.TextMeshPro.dll" ^
  /reference:"%BEP%" ^
  BA_ZH.cs
if errorlevel 1 exit /b 1
echo Built BA_ZH.dll
