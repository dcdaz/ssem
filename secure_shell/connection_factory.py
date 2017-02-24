#!/usr/bin/python3
# File for create and open connection to server
# (c) Daniel Cordova A. <danesc87@gmail.com>, GPL v2
import os, pwd
import time
import paramiko
import getpass

class ConnectionFactory(object):
    '''Factory Class that returns an opened connection'''
    @staticmethod
    def create_connection(chosen_host):
        selected_host = ServerHost(chosen_host)
        connection_created = Connection(selected_host)
        return connection_created

class ServerHost(ConnectionFactory):
    '''Class that get all parameter for connection'''
    def __init__(self, chosen_host):
        self.this_host = chosen_host
        self.hostname = None
        config_file = os.path.join(os.getenv('HOME'), '.ssh/config')
        self.ssh_config = paramiko.SSHConfig()
        self.ssh_config.parse(open(config_file, 'r'))
        self.parameters_for_host(chosen_host)
        self.host_ip = self.hostname.get('hostname', 'localhost')
        self.port = self.hostname.get('port', 22)
        self.user = self.hostname.get('user', pwd.getpwuid(os.getuid()))

    def parameters_for_host(self, chosen_host):
        self.hostname = self.ssh_config.lookup(chosen_host)
        if self.hostname['hostname'].find('@') > 0:
            self.no_config_file_host(self.hostname)

    def no_config_file_host(self, hostname):
        no_config_file_host = {'user':'','hostname':''}
        no_config_file_host['user'] = self.hostname['hostname'].split('@', 1)[0]
        no_config_file_host['hostname'] = self.hostname['hostname'].split('@', 1)[1]
        self.hostname = no_config_file_host

class Connection(ConnectionFactory):
    '''Class that opens some connection to server'''
    def __init__(self, host):
        self.host = host
        self.connection_time = 1
        self.ssh_connection = None
        self._create_ssh_connection()
        self.connecting_to_server()
        self.open_channel()

    def _create_ssh_connection(self):
        self.ssh_connection = paramiko.SSHClient()
        self.ssh_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connecting_to_server(self):
        print('Conectando al servidor ' + self.host.this_host)
        try:
            try:
                self.ssh_connection.connect(self.host.host_ip, port=self.host.port, username=self.host.user)
            except:
                print('No se encuentra tu llave en el servidor ' + self.host.this_host)
                serverPassword = getpass.getpass('Ingrese contraseña del servidor ')
                try:
                    self.ssh_connection.connect(self.host.host_ip, port=self.host.port,
                                                      username=self.host.user, password=serverPassword)
                except paramiko.AuthenticationException as e:
                    print(e)
                    # continue
        except:
            print('No se puede conectar al servidor ' + self.host.this_host + ' esperando para reconectar')
            self.connection_time += 1
            time.sleep(2)
        if self.connection_time == 30:
            print('Imposible conectar al servidor ' + self.host.this_host)
            self.exit_app()
    def open_channel(self):
        self.transport = self.ssh_connection.get_transport()
        self.channel = self.transport.open_session()
        self.channel.get_pty()
        self.channel = self.ssh_connection.invoke_shell()

    def exit_app(self):
        os.system('stty echo')
        exit()