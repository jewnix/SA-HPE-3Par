#!/usr/bin/python
from hp3parclient import client, exceptions
import json

SERVERS = ['3par1','3par2']
USERNAME = 'user'
PASSWORD = 'password'
COMMAND = 'statport'
CMD_WITH_ARGS = [COMMAND, '-iter', '1', '-ni', '-rw', '-host']

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
    CMD_RETURN.pop()
    CMD_RETURN.pop()
    CMD_RETURN.pop()

    DATE_RAW = CMD_RETURN[0].split(',')[0]
    DATE = DATE_RAW.split(' ')[1] + ' ' + DATE_RAW.split(' ')[0]

    CMD_RETURN.pop(0)
    CMD_RETURN.pop(0)

    DATA = []
    DATA_READ = []
    DATA_WRITE = []
    DICT_READ = []
    DICT_WRITE = []

    for LINE in CMD_RETURN:
        LINE_LIST = LINE.split(',')
        LINE_LIST_CURS = [LINE_LIST[0], LINE_LIST[2], LINE_LIST[3], LINE_LIST[6], LINE_LIST[9]]
        if LINE_LIST_CURS[0] != 'admin':
            if LINE_LIST_CURS[0] != '.srdata':
                if LINE_LIST_CURS[1] == 'r':
                    LINE_LIST_CURS.pop(1)
                    DATA_READ.append(LINE_LIST_CURS)
                if LINE_LIST_CURS[1] == 'w':
                    LINE_LIST_CURS.pop(1)
                    DATA_WRITE.append(LINE_LIST_CURS)
    
    HEADERS_READ = ['Device', 'rReq_PS', 'rKB_PS', 'rSvt']
    HEADERS_WRITE = ['Device', 'wReq_PS', 'wKB_PS', 'wSvt']

    for list in DATA_READ:
        DICTIONARY_READ = dict(zip(HEADERS_READ, list))
        DICT_READ.append(DICTIONARY_READ)

    for list in DATA_WRITE:
        DICTIONARY_WRITE = dict(zip(HEADERS_WRITE, list))
        DICT_WRITE.append(DICTIONARY_WRITE)

    for dict_w in DICT_WRITE:
        for dict_r in DICT_READ:
            if dict_w['Device'] == dict_r['Device']:
                DATA.append(dict_w)
                DATA[-1].update(dict_r)

    for line  in DATA:
        line['date'] = DATE
        line['array'] = SERVER

        out = json.dumps(line)
        #out = json.dumps(line, indent = 4)
        print out
