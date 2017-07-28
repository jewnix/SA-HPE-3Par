#!/usr/bin/python
from hp3parclient import client, exceptions
import json

SERVERS = ['3par1','3par1']
USERNAME = 'user'
PASSWORD = 'password'
COMMAND = 'statcpu'
CMD_WITH_ARGS = [COMMAND, '-iter', '1']

def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

def string_to_quoteless_list(string):
    quoteless = string.replace('"','')
    list = quoteless.split(",")
    return list

def stats_to_dictionary(HEAD_LIST):
    CPU = string_to_quoteless_list(HEAD_LIST)
    CPU_STATS = dict(zip(HEADERS, CPU))
    return CPU_STATS

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
    
    DATE = CMD_RETURN.pop(0)
    QUOTED_HEADERS = CMD_RETURN.pop(0)
    HEADERS = string_to_quoteless_list(QUOTED_HEADERS)
    
    CMD_RETURN.pop(9)
    CMD_RETURN.pop()
    CMD_RETURN.pop()
    
    DICTIONARY = {'date':DATE,'server':SERVER}
    
    HEAD_0, HEAD_1 = split_list(CMD_RETURN)
    
    for quoted_string in HEAD_0:
        HEAD_DICT = stats_to_dictionary(quoted_string)
        HEAD_DICT['date'] = DATE
        HEAD_DICT['array'] = SERVER

        out = json.dumps(HEAD_DICT)
        print out
        DICTIONARY = {'date':DATE,'server':SERVER}
    
    for quoted_string in HEAD_1:
        HEAD_DICT = stats_to_dictionary(quoted_string)
        HEAD_DICT['date'] = DATE
        HEAD_DICT['array'] = SERVER
        out = json.dumps(HEAD_DICT)
        print out
        DICTIONARY = {'date':DATE,'server':SERVER}
        
    ssh_client.close()
