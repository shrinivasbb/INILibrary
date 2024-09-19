*** Settings ***
Library    ../src/inilibrary/INILibrary.py

*** Test Cases ***
Read And Write INI File
    INILibrary.Load Ini File    ini/example.ini
    ${value}    Get INI Value    demo    env
    ${value}    Get INI Value    demo    env1
    Set INI Value    Database    Port    5432
    Set INI Value    Database    URL    http://localhost:5432
    Save INI File    ini/example.ini
    ${sec_exists}    Section Exists    Database
    Should be True    ${sec_exists}
    Remove Ini Key    Database    Port
    Remove Ini Key    Database    URL
    Remove Section    Database
    Save INI File    ini/example.ini
    ${sec_exists}    Section Exists    Database
    Should Not be True    ${sec_exists}
    
