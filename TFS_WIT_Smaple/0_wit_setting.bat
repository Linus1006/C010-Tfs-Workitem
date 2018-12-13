@REM 設定專案名稱
@set /p prj_name="請輸入您要修改的專案名稱:"
ECHO 專案名稱: %prj_name%

@REM 設定目錄
@REM @set witadmin_dir="C:\Program Files (x86)\Microsoft Visual Studio\2017\Professional\Common7\IDE\CommonExtensions\Microsoft\TeamFoundation\Team Explorer"
@set witadmin_dir="C:\Program Files (x86)\Microsoft Visual Studio 14.0\Common7\IDE"

C:
@cd %witadmin_dir%

@REM 執行 witadmin
witadmin importwitd /collection:https://tfsa0w0p02:8080/tfs/C004 /f:D:\TFS_WIT_Smaple\myworkitems.xml /p:%prj_name%
witadmin importwitd /collection:https://tfsa0w0p02:8080/tfs/C004 /f:D:\TFS_WIT_Smaple\myrequest.xml /p:%prj_name%
PAUSE
