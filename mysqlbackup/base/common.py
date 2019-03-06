import subprocess
import os
import sys

import log_manager as logger
import exception   as ex

def writeLine2File(i_fileName,i_content):
    with open(i_fileName, 'a') as file:
         file.writelines('\n'+i_content)
  
  

def ask_yesno(question):
    yes = set(['yes', 'y'])
    no = set(['no', 'n'])

    done = False
    print(question)
    while not done:
        choice = input().lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond by yes or no.")


def is_in(obj, l):
    """
    Checks whether an object is one of the item in the list.
    This is different from ``in`` because ``in`` uses __cmp__ when
    present. Here we change based on the object itself
    """
    for item in l:
        if item is obj:
            return True
    return False

    
def toNum(i_para):
    if type(i_para) == str:
        return int(i_para)
    else:
        return i_para

def toStr(i_para):
    if type(i_para) == str:
        return i_para
    else:
        return str(i_para)
        
def nvl(i_p1, i_p2):
    if i_p1 is None or (type(i_p1) == str and i_p1.strip()==''):
        return i_p2
    else:
        return i_p1
        
        
def concatArgs(*pArgs):
    logMsg = '('
    for p in pArgs:
        if type(p) == str:
            if len(logMsg) == 1:
                logMsg = logMsg + '\'' + p + '\''
            else:
                logMsg = logMsg + ',\'' + p + '\''
        else:
            if len(logMsg) == 1:
                logMsg = logMsg + str(p)
            else:
                logMsg = logMsg + ','+ str(p)        
    return logMsg+')'
    
def concatString(*pArgs):
    logMsg = ''
    for p in pArgs:
        if type(p) == str:
            if len(logMsg) == 0:
                logMsg = logMsg + '\'' + p + '\''
            else:
                logMsg = logMsg + ',\'' + p + '\''
        else:
            if len(logMsg) == 0:
                logMsg = logMsg + str(p)
            else:
                logMsg = logMsg + ','+ str(p)        
    return logMsg
    

    