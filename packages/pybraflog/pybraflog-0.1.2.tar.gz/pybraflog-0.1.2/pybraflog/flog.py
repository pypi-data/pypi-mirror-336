import os
import datetime
import pybrafile

class FileLog:
    """ Manage log file
    """
    def __init__(self, afilename:str, adeffolder:str):
        """__init__ Open or create log file

        Parameters
        ----------
        afilename : str
            the file name of the logfile
        adeffolder : str
            The directory to save the log file
        """        
        self._filename = afilename
        self._folder = adeffolder
        self._errortxt = ''
        self._iserror = True
        if (self._filename == ''):
            self._errortxt = 'Le nom du fichier log ne peux être vide'
            return
        
        if (self._folder == ''):
            self._errortxt = 'Le nom du réperoire log ne peux être vide'
            return
        
        self._logfile = pybrafile.FileUtils(self._filename, self._folder)

        if self._logfile.iserror:
            #FOLDERFOUND
            if (self._logfile.errorcode == pybrafile.TFileError.FOLDERNFOUND):
                if (self._logfile.createdir() == False):
                    self._errortxt = self._logfile.error
                    return

        #create file                    
        if ((self._logfile.errorcode == pybrafile.TFileError.FILENFOUND) and 
            (self._logfile.createfile() == False)):
            self._errortxt = self._logfile.error
            return
            
        self._iserror = False

    def openlog(self):        
        """openlog Open log file for append text
        """
        self._logfile.openfile('a')

    def closelog(self):
        self._logfile.close()
    
    def clearoldlog(self, aretentionday = 15):
        """clearoldlog Clear all log in the file when date is <= curedate - aretentionday

        Parameters
        ----------
        aretentionday : int, optional
            nbr of retention days, by default 15
        """
        #Calc datelogstr
        datelog = datetime.datetime.now() - datetime.timedelta(days=aretentionday)
        datelogstr = datelog.strftime('%Y-%m-%d')

        #Save logfile in backfile
        os.rename(self._logfile.filename, self._logfile.filename+'.bak')
        #open all file back and log
        backfile = pybrafile.FileUtils(os.path.basename(self._logfile.filename+'.bak'), os.path.dirname(self._logfile.filename+'.bak'))
        try:
            backfile.openfile('r')
            self._logfile.openfile('w')

            lines = backfile.readlns()
            for line in lines:
                if line[:10] >= datelogstr:
                    self._logfile.writeln(line)
        finally:
            backfile.close()
            self._logfile.close()
            #delete backup file
            os.remove(backfile.filename)

    def writeLog(self, alog : str, anbrident : int = 0)->str:
        """formatLog Add date time to the log string and indent if necesseray

        Parameters
        ----------
        alog : str
            the log to format
        anbrident : int, optional
            add ident in the log, by default 0 no indent

        Returns
        -------
        str
            The log formatied with the date time log and indent
        """
        datelog = datetime.datetime.now()
        datelogstr = datelog.strftime('%Y-%m-%d %H:%M:%S')
        nlog = datelogstr
        if (anbrident == 0):
            nlog = ''.join([nlog, ' - ', alog, '\n'])
        else:
            nlog = ''.join([nlog, ' - ']) 
            for x in range(anbrident):
                nlog = ''.join([nlog, '  '])
            nlog = ''.join([nlog, alog, '\n'])

        self._logfile.writeln(nlog)

        return nlog

    #property function
    def _get_iserror(self)->bool:
        """__get_iserror test if issues during init component 

        Returns
        -------
        bool
            False = error and get the error for description, True non error 
        """
        return self._iserror
    
    def _get_error(self)->str:
        """__get_error get the definition of error code

        Returns
        -------
        str
            the error in texte
        """        
        return self._errortxt

    # Set property() to use get_name, set_name and del_name methods
    iserror = property(_get_iserror)
    error   = property(_get_error)

class log:
    """ To Manage log string and log list
    """
    def __init__(self):
        """__init__ Open or create log string
        """
        self._LogStr = ''
        self._LogLst = list() 

    def clear(self):
        """clear clear log list and log str
        """
        self._LogStr = ''
        self._LogLst.clear()
    
    def count(self)->int:
        """return the number of element on Valuelst
        """
        return len(self._LogLst)
    
    def tostring(self, achars : str = '\r\n')->str:
        """return the Valuelst in string separated by aChar (default '\n\r')
        """
        return achars + achars.join(self._LogLst)
    
    def getlogtag(self, asep : str = '')->str:
        """Get log tag

        Parameters
        ----------
        asep : str
            the end text separetor

        Returns
        -------
        str
            the date and tile of the log
        """
        datelog = datetime.datetime.now()
        datelogstr = datelog.strftime('%Y-%m-%d %H:%M:%S')
        return datelogstr + asep

    #property function
    def __get_value(self)->str:
        return self._LogStr
    
    def __set_value(self, aLog : str):
        self._LogStr = aLog

    def __get_lst(self)->list: 
        return self._LogLst
    
    def __set_lst(self, aLog : str):
        self._LogLst.append(aLog)

    ## Set property() to use get_name, set_name and del_name methods
    value = property(__get_value, __set_value)
    Valuelst = property(__get_lst, __set_lst)