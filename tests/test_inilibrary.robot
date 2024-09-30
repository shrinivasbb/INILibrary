*** Settings ***
Library    INILibrary

*** Test Cases ***
load non existent file
    INILibrary.Load Ini File    ini/abc.ini

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
    
Negative scenarios Get INI Value
    INILibrary.Load Ini File    ini/example.ini
    ${value}    Get INI Value    demo    env1

Negative Scenarios Set INI Value
    INILibrary.Load Ini File    ini/example.ini
    Set INI Value    demo2    key1    value1
    Save INI File    ini/example.ini

remove non existent section
    INILibrary.Load Ini File    ini/example.ini
    Remove Ini Key    demo2    value123

get All key vals
    Load INI File    ini/example.ini
    ${dict}    Get All Keys And Values    demo3
    Log    ${dict}

get values list
    Load INI File    ini/example.ini
    ${list}    Get Values List    demo3    abc
    Log    ${list}
    ${state}    Key Exists    demo3    twtwtw