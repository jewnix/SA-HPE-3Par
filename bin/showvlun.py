#!/usr/bin/python

from hp3parclient import client, exceptions
import json
 
SERVERS = ['3par1','3par2']
USERNAME = 'user'
PASSWORD = 'password'
COMMAND = 'showvlun'
CMD_WITH_ARGS = [COMMAND,'-a','-showcols', 'Lun,VVName,HostName,VV_WWN,Port,Host_WWN']
 
for SERVER in SERVERS:
    SERVER_NAME = SERVER + '.example.com'
    ssh_client = client.ssh.HP3PARSSHClient(SERVER_NAME, USERNAME, PASSWORD, port=22)
 
    #logging in
    try:
        ssh_client.open()
    except:
        print 'login failed on SERVER: ' + SERVER
 
    #run the command
    CMD_RETURN = ssh_client.run(CMD_WITH_ARGS)
 
    #logging out
    ssh_client.close()
   
    CMD_RETURN.pop()
    CMD_RETURN.pop()
 
    HEADERS = CMD_RETURN.pop(0)
    HEADERS = HEADERS.split(',')
 
    for LINE in CMD_RETURN:
        LINE_LIST = LINE.split(',')
        DICTIONARY = dict(zip(HEADERS, LINE_LIST))
        DICTIONARY['array'] = SERVER
        DICTIONARY['Lun_id'] = DICTIONARY['Lun']
        DICTIONARY.pop('Lun')
        out = json.dumps(DICTIONARY)
        print out
