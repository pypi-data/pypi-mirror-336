@echo off
setlocal EnableExtensions DisableDelayedExpansion
pushd .

:: see posix version for details

set myRoot=%~dp0..
:build
cd /d %myRoot%
poetry run python ci\_setup.py bdist_msi
set result=%errorlevel%
if NOT %result% == 0 (
	goto :failed
)
echo ** SUCCEEDED **
goto :passed

:failed
echo ** FAILED **
:passed
popd
exit /b %result%
