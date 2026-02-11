@echo off
REM Makefile for Sphinx documentation

setlocal enabledelayedexpansion

set SPHINXBUILD=sphinx-build
set SOURCEDIR=source
set BUILDDIR=build

if "%1"=="" goto help

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.can add a directory to the PATH environment variable so that it
	echo.contains the Sphinx 'sphinx-build' executable.
	echo.If you don't have Sphinx installed, grab it from
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %*
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %*

:end
endlocal
