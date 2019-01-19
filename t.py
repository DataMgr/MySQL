#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.path.append('backup')
sys.path.append('base') 
sys.path.append('cfg') 


import getopt 
import mysql_backup as mysqlbk 
import my_os as myos
 

ret=''
ret=myos.run_linux_cmd_quiet('cat /tmp/a.log')
print(ret)