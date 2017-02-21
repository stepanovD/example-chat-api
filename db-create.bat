del /f /q database.db
rd /s /q db_repository

C:\Python27\python.exe db_create.py
C:\Python27\python.exe db_init_data.py

@echo off
::create demo data for test
if "%~1"=="--demo" Goto :Demo

Goto :eof

:Demo
@echo on
C:\Python27\python.exe db_init_test_data.py