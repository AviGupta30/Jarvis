@echo off
REM ============================================================
REM  Jarvis MySQL Setup Helper — Run as Administrator
REM  This creates the jarvis_memory DB and a dedicated user.
REM ============================================================

echo.
echo  ====================================================
echo  Jarvis MySQL Setup — Running as Administrator
echo  ====================================================
echo.

set /p MYSQL_ROOT_PASS=Enter your MySQL root password: 
echo.

set MYSQL_BIN=C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe

REM Create database and user
echo Creating jarvis_memory database and jarvis user...
"%MYSQL_BIN%" -u root -p%MYSQL_ROOT_PASS% -e "CREATE DATABASE IF NOT EXISTS jarvis_memory CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci; CREATE USER IF NOT EXISTS 'jarvis'@'localhost' IDENTIFIED BY 'jarvis123'; GRANT ALL PRIVILEGES ON jarvis_memory.* TO 'jarvis'@'localhost'; FLUSH PRIVILEGES;"

if %errorlevel% neq 0 (
    echo.
    echo [FAIL] Could not connect. Check your root password and try again.
    pause
    exit /b 1
)

echo.
echo [OK] Database 'jarvis_memory' created.
echo [OK] User 'jarvis'@'localhost' created with password 'jarvis123'.
echo.
echo Now add this line to your Jarvis .env file:
echo   MYSQL_URL=mysql+aiomysql://jarvis:jarvis123@localhost/jarvis_memory
echo.
echo Then run: python scripts/init_rag_memory.py
echo.
pause
