#!/usr/bin/python3
# File that send command to execute on remote server with an opened connection
# (c) Daniel Cordova A. <danesc87@gmail.com>, GPL v2

import os
import paramiko
from secure_shell import time_file

class ExecutorOnServer(object):
    '''Class that send some comand to remote server'''
    def __init__(self, opened_connection):
        self.connection_factory = opened_connection

    def send_command(self, script_to_execute, exec_time):
        newline = '\r'
        line_buffer = ''
        channel_buffer = ''
        timeout = int(time_file)
        if exec_time != 0:
            timeout = int(exec_time)
        self.connection_factory.channel.settimeout(timeout)
        try:
            while True:
                try:
                    self.connection_factory.channel.send('clear' + newline)
                    self.connection_factory.channel.send(script_to_execute + newline)
                    while True:
                        channel_buffer = self.connection_factory.channel.recv(1).decode('UTF-8','replace')
                        if len(channel_buffer) == 0:
                            break
                        channel_buffer  = channel_buffer.replace('\r', '')
                        if channel_buffer != '\n':
                            line_buffer += channel_buffer
                        else:
                            print (line_buffer)
                            line_buffer   = ''
                except paramiko.SSHException as e:
                    print ('Error en ejecución remota', str(e))
                    self.exit_app()
                    break
                retcode = self.connection_factory.channel.recv_exit_status()
                buf = ''
                while self.connection_factory.channel.recv_ready():
                    buf+= self.connection_factory.channel.recv(9999).decode('UTF-8','replace')
                    print (buf, retcode)
                    break
        except:
            self.connection_factory.channel.close()
            self.exit_app()
        finally:
            self.connection_factory.channel.close()

    def exit_app(self):
        os.system('stty echo')
        exit()
