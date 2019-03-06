import traceback
import time


RED="\033[1;31m"
INFO_COLOR="\033[1m"
BLUE="\033[1;34m"
SUCCESS_COLOR="\033[1;32m"
YELLOW="\033[1;33m"
DEFAULT_COLOR="\033[0m"

m_logfile=""
m_teeLog=""


def Init(logFile="SysLog.log", teeLog="y"):
    global m_logfile,m_teeLog
    m_logfile = logFile
    m_teeLog  = teeLog
    

def print_error(log_class, msg):      
    f='x'
     
    try: 
        str_callStack=traceback.format_exc()
        
        if m_teeLog=='y':
            print("%sThere is a error(%s->%s)\033[0m\a"	% (SUCCESS_COLOR, log_class, msg)) 
            if len(str_callStack) != 0 and not str_callStack is None:
                print("-------------call stack ---------------->>>")
                print(str_callStack)
                print("-------------call stack ----------------<<<")  
            
        with open(m_logfile, 'a') as  f:
            f.write('ERROR:' + time.strftime('%Y%m%d-%H:%M:%S',time.localtime()) + ',' + log_class + ','  + msg + ',' + str_callStack + '\n')
       
    except Exception as e:
        print("Warning: Can't write log. (%s)" % e)
    finally:
        pass;
      

def print_info(type, msg):
    f='x'
     
    try:        
        if m_teeLog=='y':
            print("Info(%s->%s)"	% (type, msg))

        with open(m_logfile, 'a') as ff:
            ff.write('INFO:' + time.strftime('%Y%m%d-%H:%M:%S', time.localtime()) + ',' + type + ',' + msg + '\n')

    except Exception as e:
        print("Warning: Can't write log. (%s)" % e)
    finally:
        pass;

Init()        