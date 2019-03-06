import re
import time
import datetime
import log_manager as logger
import my_os       as myos
import common 
import sys
import socket
import os

def backup_pre():
    #check mysql
    #check  innobackupex
    #    
    return myos.run_linux_cmd_return_msg('which xtrabackup') 
    
def get_full_backup_dir(i_backup_repository):
    (retVal, retMsg) = myos.run_linux_cmd_return_msg('grep full ' + i_backup_repository + '/result.log | tail -n1')
    if retVal == True:
        retMsg = retMsg.replace("\n", "");
        return retMsg
    else:
        return '' 
        
def gen_backup_cmd(i_cnf,i_user,i_pwd,i_exclude,i_last_full_backup, i_dst, i_mode): 
    l_func_name=__name__+ '.' + sys._getframe().f_code.co_name  
    
    l_backupCMD='innobackupex'
    l_cnf=i_cnf
    l_user=i_user
    l_pwd=i_pwd
    l_exclude=i_exclude
    l_full_backup_dir=i_last_full_backup
    l_dst=i_dst
    l_mode=i_mode
    
    if i_mode == 'inc':
        l_fullCMD="{xtrabackup} --defaults-file={cnf} --user={user} --password={pwd}\
                   --no-timestamp --slave-info --rsync --databases-exclude=\'{exclude}\'\
                   --incremental --incremental-basedir={full_backup_dir} {dst}".format(xtrabackup=l_backupCMD
                   ,cnf=l_cnf,user=l_user,pwd=l_pwd,exclude=l_exclude,full_backup_dir=l_full_backup_dir
                   ,dst=l_dst)
    else:
        l_fullCMD="{xtrabackup} --defaults-file={cnf} --user={user} --password={pwd}\
               --no-timestamp --slave-info --rsync --databases-exclude=\'{exclude}\' {dst}".format(xtrabackup=l_backupCMD
               ,cnf=l_cnf,user=l_user,pwd=l_pwd,exclude=l_exclude
               ,dst=l_dst)
    return l_fullCMD  
    
def backup_post(i_backupResult):    
    if 0 == myos.run_linux_cmd_quiet("grep 'completed OK!$' " + i_backupResult):
        return True
    else:
        return False
        
def insert_backup_result(i_user, i_pwd, i_port,i_startTime, i_mode, i_backup_dir, i_status):
    l_hostname = socket.gethostname()  
    l_curTime=time.strftime('%Y%m%d_%H%M%S',time.localtime())
    l_sql = """insert into {dbname}.t_backup(hostname,backup_Type,start_time,end_time,backup_dir,status)
                                 values('{hostname}','{backup_Type}','{start_time}','{end_time}','{backup_dir}','{status}')
     """.format(dbname=i_user, hostname=l_hostname,backup_dir=i_backup_dir, backup_Type=i_mode
                ,start_time=i_startTime,end_time=l_curTime,status=i_status)
    run_mysql_sql_quient(i_user, i_pwd, i_user, i_port, l_sql) 
    
def execute_backup(i_dbName, i_port,i_cnf,i_user,i_pwd,i_exclude,i_backup_repository, i_mode, i_zip): 
    modes=['inc', 'full']
    if not i_mode in modes:
        return False;
    
    l_func_name=__name__+ '.' + sys._getframe().f_code.co_name
    #0 record input args
    logger.print_info(l_func_name, common.concatArgs(i_cnf,i_user,i_pwd,i_exclude,i_backup_repository, i_zip))
    
    #step 1 check
    (retVal,retMsg)=backup_pre()
    if retVal == True:
        logger.print_info(l_func_name, '###step1 passed');
    else:
        logger.print_error(l_func_name,'###step1 failed');
        return retVal
    
    #step 2 do  
    
    l_curTime=time.strftime('%Y%m%d_%H%M%S',time.localtime())
    l_last_full_backup=i_backup_repository 
    retVal = os.path.exists(l_last_full_backup)
    if i_mode == 'inc':
        l_last_full_backup=get_full_backup_dir(i_backup_repository)
        if len(l_last_full_backup) == 0 or True != retVal:
            logger.print_error(l_func_name,"###step2 failed, there isn't a valid backup");
            return False        
    l_dst = i_backup_repository + '/' + l_curTime + '_' + i_mode + '_' + i_dbName
    
    l_cmd=gen_backup_cmd(i_cnf,i_user,i_pwd,i_exclude,l_last_full_backup,l_dst, i_mode)
    l_backupResult="{repository}/{curTime}_{mode}_result.log".format(repository=i_backup_repository,
                                                     mode=i_mode,curTime=l_curTime)
    (retVal, retMsg) = myos.run_linux_cmd_quiet(l_cmd, l_backupResult)
    if retVal == 0:
        insert_backup_result(i_user,i_pwd, i_port,l_curTime,  i_mode,l_dst, 'ok')
        logger.print_info(l_func_name, 'execute backup cmd(xtrabackup) successed.' + l_backupResult)
        l_result='{repository}/result.log'.format(repository=i_backup_repository)
        common.writeLine2File(l_result,l_dst)
        #myos.run_linux_cmd_quiet('echo {dst} >> {repository}/result.log '.format(dst=l_dst, repository=i_backup_repository))        
        logger.print_info(l_func_name,'###step2 ok.');
    else:        
        insert_backup_result(i_user,i_pwd, i_port,l_curTime,  i_mode,l_dst, 'failed')
        logger.print_error(l_func_name,'###step2 failed, execute backup cmd(xtrabackup) failed');
        return False
    
    #step3 post check
    if i_zip == 'y':
        myos.run_linux_cmd_quiet('tar -czvf {repository}/{curTime}_{mode}_{dbname}.tgz {dst}'.format(
                                    repository=i_backup_repository, curTime=l_curTime, mode=i_mode,dbname=i_dbName, dst=l_dst))
                                    
    return backup_post(l_backupResult)
    
 
    
def del_expired_backupset(i_dir, i_ndays):
    if len(i_dir) == 0:
        return 1;
        
    now = datetime.datetime.now()
    expired_day = now + datetime.timedelta(days=-common.toNum(i_ndays))
    strTime = expired_day.strftime("%Y%m%d")

    l_dstDir = 'rm -rf '+ i_dir + '/' + strTime + '*'
    myos.run_linux_cmd_quiet(l_dstDir)

    return 0;
    
        
def up_load_backupset(i_user, i_pwd, i_dstDir):
    print(__name__, i_user, i_pwd, i_dstDir, 'call the internal upload funcion') 
 
def run_mysql_return_msg(i_user, i_pwd, i_port, i_sql):
    mysql_cmd="mysql -u{user} -p{pwd} -P{port} -Bse \"{sql}\"".format(
                        user=i_user, pwd=i_pwd, port=i_port, sql=i_sql)
    return myos.run_linux_cmd_return_msg(mysql_cmd)

def run_mysql_sql_quient(i_user, i_pwd, i_dbName, i_port, i_sql):
    mysql_cmd="mysql -u{user} -p{pwd} -P{port} -Bse \"{sql}\" {dbname}".format(
                        user=i_user, pwd=i_pwd, port=i_port, sql=i_sql, dbname=i_dbName)
    return myos.run_linux_cmd_quiet(mysql_cmd)
                        
def run_ddl_forMySQL(i_user, i_pwd, i_port, i_sql):
    mysql_cmd="mysql -u{user} -p{pwd} -P{port} -Bse \"{sql}\"".format(
                        user=i_user, pwd=i_pwd, port=i_port, sql=i_sql)
    return myos.run_linux_cmd_quiet(mysql_cmd)
    
def Init_backup_env(i_user_admin, i_pwd_admin, i_user_backup, i_pwd_backup, i_port):
    l_func_name=__name__+ '.' + sys._getframe().f_code.co_name
    
    l_sql="select count(*) from information_schema.tables where table_schema='{user}' and table_name='t_backup'".format(user=i_user_backup.lower())
    (retval,retmsg)=run_mysql_return_msg(i_user_admin, i_pwd_admin, i_port, l_sql) 
    retmsg=retmsg.replace('\n', '')
    if retmsg == '0':
        logger.print_info(l_func_name, "ready to init database for backup")
        l_sql="""
        CREATE SCHEMA IF NOT EXISTS {user};
        CREATE USER '{user}'@'localhost' IDENTIFIED BY '{pwd}'; 
        GRANT  PROCESS,RELOAD,LOCK TABLES,REPLICATION CLIENT ON *.* TO '{user}'@'localhost';
        GRANT ALL ON {user}.* to '{user}'@'localhost';
        flush privileges;
        CREATE TABLE IF NOT EXISTS {user}.t_backup 
        (
            id          bigint       NOT NULL auto_increment,
            hostname    varchar(100) DEFAULT NULL,
            backup_Type varchar(100) DEFAULT NULL,
            start_time  varchar(100) NULL DEFAULT NULL,
            end_time    varchar(100) NULL DEFAULT NULL,
            backup_dir  varchar(255) DEFAULT NULL, 
            status      varchar(25)  DEFAULT NULL ,
            PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
        """.format(user=i_user_backup.lower(), pwd=i_pwd_backup.lower())
        run_ddl_forMySQL(i_user_admin, i_pwd_admin, i_port, l_sql) 
    else:
        logger.print_info(l_func_name, "The database has been inited.") 