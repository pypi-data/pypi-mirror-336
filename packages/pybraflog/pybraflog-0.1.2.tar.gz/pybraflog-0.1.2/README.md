# pybraflog Readme 📜
Brainstorming package to manage logs in txt file

# Installation ⚡
Opérating system :  Windows, MacOS & Linux :

# Available function/class 📑
### to create => FileUtils(afilename, adeffolder)
    adeffolder : folder to write file. if not exist or empty error.
    afilename  : the file name to write.
### to open log => openlog
    Open the log file.
### to write info in log => writeLog(alog, anbrident)
    alog : a line to add in file log. wothout add \n at the end to CRLF.
    anbrident : to define indentation, number of space to add before alog, by default 0.
### to clear log => clearoldlog(aretentionday)
    to erase all log old than aretentionday, by default 15 days(optional).
    You need to do when the filelog is open.
### to close log => closelog()
    Close the log file.
### class log, this class is use to transfert txt log for function to parant function
    value : for log in one line.
    valuelst : for log in more lines.

# Howto use 📰
    import os
    import pybraflog
    import pybrafile

    flog = pybraflog.FileLog('testlog.txt', '')
    if flog.iserror:
        print(flog.error)

    flog = pybraflog.FileLog('testlog.txt', os.getcwd())    
    flog.openlog()

    flog.writeLog('first line')
    flog.writeLog('first line indent', 10)
    flog.writeLog('two line')
    
    flog.closelog()
    
    file = pybrafile.FileUtils('testlog.txt')
    file.openfile('r')
    txt = file.readfile()
    file.close()

    print(txt)
    print(pybraflog.version())

## Meta 💬
Brainstorming – Support.erp@brainstorming.eu

Distributed under the MIT license. See ``LICENSE`` for more information.