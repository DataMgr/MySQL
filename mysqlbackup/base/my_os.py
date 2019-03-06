import subprocess
import os
import sys
import common
import time
import log_manager as logger
import exception   as ex
import my_cfg      as cfg

       
def file2List(i_fileName):
    with open(i_fileName, 'r') as file:
        whole=[]
        mystr=''
        for oneLine in file:
            contend = oneLine.rstrip('\n').rstrip().split('\t')
            whole.append(''.join(contend))

    return whole
    
def run_linux_cmd2(cmd):
    subp=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    retMsg=""
    c=subp.stdout.readline()
    while c:
        retMsg = retMsg + c.decode()
        c=subp.stdout.readline()
    return retMsg

def run_linux_cmd_quiet(i_cmd, i_result=None, i_nohup='0'):
    l_func_name=__name__+ '.' + sys._getframe().f_code.co_name
    
    if i_result is None:
        l_curTime=time.strftime('%Y%m%d_%H%M%S',time.localtime())
        l_result=l_curTime+str(os.getpid())+'.log'
        inFileFlag='0'
    else:
        l_result=i_result
        inFileFlag='1'
        
    if i_nohup == '1':
        l_cmd="nohup {cmd} > {result} 2>&1 &".format(cmd=i_cmd, result=l_result)
    else:
        l_cmd="{cmd} > {result} 2>&1".format(cmd=i_cmd, result=l_result)
        
    if cfg.TRACE_FLAG == 'y': 
        logger.print_info(l_func_name, common.concatString(l_cmd, '...'))
    val = os.system(l_cmd) 
    msg=file2List(l_result)
    if 0 != val:
        #logger.print_error(l_func_name,common.concatString(l_cmd, 'failed.\n   retCode:',val))
        pass
    else:
        if '0' == inFileFlag:
            os.system('rm -f ' + l_result)
        if cfg.TRACE_FLAG == 'y':
            pass
            #logger.print_info(l_func_name, common.concatString(l_cmd, 'ok.\n   retCode:',val))
    
    return (val,msg)

         
def run_linux_cmd_return_msg(cmd):
    l_func_name=__name__+ '.' + sys._getframe().f_code.co_name
    
    if cfg.TRACE_FLAG == 'y':
        logger.print_info(l_func_name, cmd)
       
    try:
        val = os.popen(cmd).read() 
        if (val == ''):
          raise  ex.ProcessError(cmd, -1) 
        else:
          return (True, val)
    except ex.ProcessError as e:
        logger.print_error(l_func_name, e.getMsg())
        return (False,'Failed')
 
def run_os_cmd(cmd):
    sysstr=platform.system()
    if(sysstr =="Windows"):     
        return 0
    elif(sysstr == "Linux"):        
        return 1        
    


    