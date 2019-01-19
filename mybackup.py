#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('backup')
sys.path.append('base') 
sys.path.append('cfg') 

import time
import getopt 
import mysql_backup as mysqlbk
import my_cfg  as cfg
import common

def Usage():
    print("""
    backupMgr.py
    Usage:
        backupMgr.py -i 
        backupMgr.py -f 
    Options:
        -h --help
            show the usage
        -v --version
            show the version of backupMgr.py
        -u --user=<user> 
            login database by the user
        -p --password=<password>
            the user's password
        -r --repository=<directory>
            backup to the dir
        -d --database=dbname
            the database name of backup
        -e --expired=<days>
            delete the expired backupset
        -m --mode=(full|inc)
            backup database with increment/mode mode 
    """)

def my_program(i_args):
    l_myArgs = i_args

    # parse the argments
    l_exclude=""
    l_mysqlCNF=""
    
    l_init=""
    l_zip=""
    l_user=""
    l_pwd=""
    l_database=""
    l_repository=""
    l_expired=""
    l_mode=""
    
    opts,args = getopt.getopt(l_myArgs,
                              '-i-h-t-v-z-u:-p:-d:-r:-e:-m:',
                              ['init', 'help','trace','version','zip=','user=','password=','directory=','repository=','expired=', 'mode='])
    
    try:
        for opt_name,opt_value in opts:

            if opt_name in ('-i', '--zip'):
                l_init = 'yes'
                continue
            if opt_name in ('-h','--help'):
                Usage()
                exit(0)
            if opt_name in ('-t','--trace'):   
                print('-t')
                import pdb
                pdb.set_trace()
                continue            
            if opt_name in ('-v','--version'):
                print("Version is 0.01 ")
                exit(0)
            if opt_name in ('-z', '--zip'):
                l_zip = opt_value
                continue
            if opt_name in ('-u','--user'):
                l_user = opt_value
                continue 
            if opt_name in ('-p','--password'):
                l_pwd = opt_value
                continue 
            if opt_name in ('-d', '--database'):
                l_database = opt_value
                continue
            if opt_name in ('-r', '--repository'):
                l_repository = opt_value
                continue
            if opt_name in ('-e', '--expired'):
                l_expired = opt_value
                continue
            if opt_name in ('-m', '--mode'):
                l_mode = opt_value
                continue
           
    except GetoptError as opt:
        print('unsupported parameter')
    except Exception as e:
        print("unknowned error (%s)" % e)  
    
    l_init=common.nvl(l_init,'n')   
    l_zip=common.nvl(l_zip,cfg.ZIP_BACKUP)    
    l_user=common.nvl(l_user,cfg.USER_BACKUP)
    l_pwd=common.nvl(l_pwd,cfg.PWD_BACKUP)
    l_database=common.nvl(l_database,cfg.DATABASE_BACKUP)
    l_repository=common.nvl(l_repository,cfg.REPOSITORY_BACKUP)
    l_expired=common.nvl(l_expired,cfg.EXPIRED_BACKUP)
    l_mode=common.nvl(l_mode,cfg.MODE_BACKUP)
    
    l_mysqlCNF=common.nvl(l_mysqlCNF,cfg.MYSQL_CNF)
    l_exclude=common.nvl(l_exclude, cfg.EXCLUDE_BACKUP)
    l_user_admin=cfg.USER_ADMIN
    l_pwd_admin=cfg.PWD_ADMIN
    l_port=cfg.PORT_BACKUP
    
    modes=['inc', 'full']
    if l_mode in modes: 
        mysqlbk.execute_backup(l_database,l_port, l_mysqlCNF,l_user,l_pwd,l_exclude,l_repository, l_mode, l_zip) 

    if(len(l_expired) != 0):
        mysqlbk.del_expired_backupset(l_repository, l_expired)    
    
    if 'n' != l_init:   
        mysqlbk.Init_backup_env(l_user_admin, l_pwd_admin, l_user,l_pwd, l_port)

if __name__ == '__main__':
    l_args=sys.argv[1:]
    #l_args=['-u', 'togogo', '-p', 'donet', '-m' ,'inc']
    sys.exit(my_program(l_args))