#!/usr/bin/env python
import sys
from time import sleep
import paramiko
import os
import datetime

USER="user"
PASSWD="password"

f = open('switches')
for line in f:
# Trim from 'switches'
  ip=line[:11]
  hostname=line[13:16]
  print "Connecting to " + (ip)
  HOST = ip.strip()
# Create an ssh connection
  conn = paramiko.SSHClient()
  conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  conn.connect(HOST, username=USER, password=PASSWD)
  switch_conn = conn.invoke_shell()
  print('Successfully connected to %s' % hostname)
# Send the command and backup to tftp server file saved as config.txt
  switch_conn.send("copy running-config tftp://192.168.X.X/config.txt\n")
  switch_conn.send('\n')
  sleep(1)
  switch_conn.send('\n')
  sleep(3)
#config.txt renamed to SwitchName with present date
  current_date = datetime.datetime.today().strftime ('%b-%d-%Y')
  os.rename(r'/tftpboot/config.txt',r'/tftpboot/'+ str(hostname)+'-'+ str(current_date) + '.cfg')
  print('Backup completed for %s' % hostname)
conn.close

