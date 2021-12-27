@echo off
TITLE Creating some files.............
@echo Creating some files
echo.>Enter_some_guess_passwords.txt
type nul > Enter_some_guess_passwords.txt
@echo Created Files
@echo ............................................................................
TITLE Installing required python libraries...........
@echo ____________________________________________________________________________
@echo                    Installing required python libraries
@echo                 ___________________________________________
pip install -r requirements.txt
