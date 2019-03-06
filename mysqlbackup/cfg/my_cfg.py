#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import  os 
WORK_DIR=os.path.abspath('./')

#基础变量
DB_IP='172.24.121.61'
DBName='Trade'
Password='Oracle'

UseKey='N'
USER_MYSQL='mysql'
PWD_MYSQL='mysql'

Tee_log='N'

USER_ROOT='ROOT'
PWD_ROOT='futures123456'

USER_ADMIN="root"
PWD_ADMIN="mysql"
USER_BACKUP="backupmgr"
PWD_BACKUP="backupmgr"
REPOSITORY_BACKUP="/data/backup"
DATABASE_BACKUP="tbdb"
PORT_BACKUP="3306"
EXPIRED_BACKUP="30"
MODE_BACKUP=""
ZIP_BACKUP="y"
EXCLUDE_BACKUP="readonlyDB1 readonlyDB2"
MYSQL_CNF="/etc/my.cnf" 

TRACE_FLAG='y'

#推导变量
DIR_LOG=WORK_DIR+'/log'
DIR_LIB=WORK_DIR+'/lib'
TMP_DIR=WORK_DIR+'/tmp'
CFG_DIR=WORK_DIR+'/conf'

logFile=DIR_LOG + '/syslog.log'

#完善
isExists=os.path.exists(DIR_LOG)
if not isExists:
    os.makedirs(DIR_LOG)

isExists=os.path.exists(TMP_DIR)
if not isExists:
    os.makedirs(TMP_DIR)    