@echo off

set CHROME_EXE=c:\Program Files (x86)\Google\Chrome\Application\chrome.exe
set CHROME_SETTINGS=%CHROME_SETTINGS% --app="data:text/html,<html><body><script>window.moveTo(0,0);window.resizeTo(1920,1080);window.location='http://wfic-cevac1/cevac_web/map';</script></body></html>"
start "" "%CHROME_EXE%" %CHROME_SETTINGS%

set CHROME_EXE=c:\Program Files (x86)\Google\Chrome\Application\chrome.exe
set CHROME_SETTINGS=%CHROME_SETTINGS% --app="data:text/html,<html><body><script>window.moveTo(1920,0);window.resizeTo(1920,1080);window.location='https://sas.clemson.edu:8343/SASVisualAnalytics/report?location=/Shared Data/CEVAC/Watt Dive&type=Report.BI&section=vi30059';</script></body></html>"
start "" "%CHROME_EXE%" %CHROME_SETTINGS%

TIMEOUT 45

set CHROME_EXE=c:\Program Files (x86)\Google\Chrome\Application\chrome.exe
set CHROME_SETTINGS=%CHROME_SETTINGS% --app="data:text/html,<html><body><script>window.moveTo(3840,0);window.resizeTo(1920,1080);window.location='https://sas.clemson.edu:8343/SASVisualAnalytics/report?location=/Shared Data/CEVAC/ASC Dive&type=Report.BI&section=vi452326';</script></body></html>"
start "" "%CHROME_EXE%" %CHROME_SETTINGS%

TIMEOUT 15

set CHROME_EXE=c:\Program Files (x86)\Google\Chrome\Application\chrome.exe
set CHROME_SETTINGS=%CHROME_SETTINGS% --app="data:text/html,<html><body><script>window.moveTo(5760,0);window.resizeTo(1920,1080);window.location='https://sas.clemson.edu:8343/SASVisualAnalytics/report?location=/Shared Data/CEVAC/Cooper Dive&type=Report.BI&section=vi450631';</script></body></html>"
start "" "%CHROME_EXE%" %CHROME_SETTINGS%

TIMEOUT 15

set CHROME_EXE=c:\Program Files (x86)\Google\Chrome\Application\chrome.exe
set CHROME_SETTINGS=%CHROME_SETTINGS% --app="data:text/html,<html><body><script>window.moveTo(0,1080);window.resizeTo(1920,1080);window.location='https://sas.clemson.edu:8343/SASVisualAnalytics/report?location=/Shared Data/CEVAC/Campus Overview&type=Report.BI&section=vi42';</script></body></html>"
start "" "%CHROME_EXE%" %CHROME_SETTINGS%

TIMEOUT 15

set CHROME_EXE=c:\Program Files (x86)\Google\Chrome\Application\chrome.exe
set CHROME_SETTINGS=%CHROME_SETTINGS% --app="data:text/html,<html><body><script>window.moveTo(1920,1080);window.resizeTo(1920,1080);window.location='https://sas.clemson.edu:8343/SASVisualAnalytics/report?location=/Shared Data/CEVAC/Fluor Dive&type=Report.BI&section=vi447203';</script></body></html>"
start "" "%CHROME_EXE%" %CHROME_SETTINGS%

TIMEOUT 15

set CHROME_EXE=c:\Program Files (x86)\Google\Chrome\Application\chrome.exe
set CHROME_SETTINGS=%CHROME_SETTINGS% --app="data:text/html,<html><body><script>window.moveTo(3840,1080);window.resizeTo(1920,1080);window.location='https://sas.clemson.edu:8343/SASVisualAnalytics/report?location=/Shared Data/CEVAC/Holmes Dive&type=Report.BI&section=vi36488';</script></body></html>"
start "" "%CHROME_EXE%" %CHROME_SETTINGS%

TIMEOUT 15

set CHROME_EXE=c:\Program Files (x86)\Google\Chrome\Application\chrome.exe
set CHROME_SETTINGS=%CHROME_SETTINGS% --app="data:text/html,<html><body><script>window.moveTo(5760,1080);window.resizeTo(1920,1080);window.location='https://sas.clemson.edu:8343/SASVisualAnalytics/report?location=/Shared Data/CEVAC/LeeIII Dive&type=Report.BI&section=vi446309';</script></body></html>"
start "" "%CHROME_EXE%" %CHROME_SETTINGS%

TIMEOUT 15

set CHROME_EXE=c:\Program Files (x86)\Google\Chrome\Application\chrome.exe
set CHROME_SETTINGS=%CHROME_SETTINGS% --app="data:text/html,<html><body><script>window.moveTo(1920,0);window.resizeTo(1920,1080);window.location='https://sas.clemson.edu:8343/SASVisualAnalytics/report?location=/Shared Data/CEVAC/Fike Dive&type=Report.BI&section=vi473253';</script></body></html>"
start "" "%CHROME_EXE%" %CHROME_SETTINGS%
