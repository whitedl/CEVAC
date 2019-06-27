REM emergency_report_startup.bat
REM launches python autotiling script and chrome app mode
REM to make this a startup program, follow this guide https://www.computerhope.com/issues/ch000322.htm

cd "C:\Users\cevac\Local Settings\Application Data\Programs\Python\Python37\"
start python.exe "C:\path\to\autotiling.py"

cd "C:\Program Files (x86)\Google\Chrome\Application\"
start chrome.exe --app=http://google.com
