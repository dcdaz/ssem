#!/usr/bin/python3
# Clase para el conector remoto
# (c) Daniel Cordova A. <danesc87@gmail.com>, GPL v2
import os
import sys
import time
import select
import paramiko
import codecs
import getpass

def connectionToServer(chosenHost, script_to_execute, execTime):
	config_file = os.path.join(os.getenv('HOME'), '.ssh/config')
	config = paramiko.SSHConfig()
	config.parse(open(config_file, 'r'))
	allHosts = config.get_hostnames()
	hostNoFile = {'user':'','hostname':''}
	host = config.lookup(chosenHost)
	if host['hostname'].find('@') > 0:
		hostNoFile['user'] = host['hostname'].split('@',1)[0]
		hostNoFile['hostname'] = host['hostname'].split('@',1)[1]
		host = hostNoFile
	connectorService(host, chosenHost, script_to_execute, execTime)

def connectorService(host, chosenHost, script_to_execute, execTime):
	i = 1
	try:
		while True:
			print ('Conectando al servidor ' + chosenHost)
			try:
				sshConnection = paramiko.SSHClient()
				sshConnection.load_system_host_keys()
				sshConnection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
				try:
					connectionPort = int(host['port'])
				except:
					connectionPort = 22
				try:
					sshConnection.connect(host['hostname'], port=connectionPort, username=host['user'])
				except:
					print ('No se encuentra tu llave en el servidor ' + chosenHost)
					# serverPassword = input ('Ingrese contraseña del servidor ')
					serverPassword = getpass.getpass('Ingrese contraseña del servidor ')
					try:
						sshConnection.connect(host['hostname'], port=connectionPort, username=host['user'], password=serverPassword)
					except paramiko.AuthenticationException as error:
						print(error)
						break
			except:
				print ('No se puede conectar al servidor ' + chosenHost + ' esperando para reconectar')
				i += 1
				time.sleep(2)
			if i == 30:
				print ('Imposible conectar al servidor ' + chosenHost)
				sys.exit(1)
			transport = sshConnection.get_transport()
			channel = transport.open_session()
			channel.get_pty()
			try:
				channel = sshConnection.invoke_shell()
				if execTime == None or execTime == 0:
					timeout = 5
				else:
					timeout = int(execTime)
				channel.settimeout(timeout)
				newline        = '\r'
				line_buffer    = ''
				channel_buffer = ''
				channel.send('clear' + newline)
				channel.send(script_to_execute + newline)
				while True:
					channel_buffer = channel.recv(1).decode('UTF-8','replace')
					if len(channel_buffer) == 0:
						break
					channel_buffer  = channel_buffer.replace('\r', '')
					if channel_buffer != '\n':
						line_buffer += channel_buffer
					else:
						print (line_buffer)
						line_buffer   = ''
			# except socket.timeout:
			# 	# print(str(c))
			# 	print ("Se acbo el tiempoooooooooooo!!!!!!!!!!!!!!!!!")
			# 	break
			# 	exitFunction()
			except paramiko.SSHException as e:
				print ('Errooooooorrrrrrrr!!!!!',str(e))
				exitFunction()
				break
			retcode = channel.recv_exit_status()
			buf = ''
			while channel.recv_ready():
				buf+= channel.recv(9999).decode('UTF-8','replace')
				print (buf, retcode)
				break
	except:
		exitFunction()
	finally:
		sshConnection.close()

def exitFunction():
	# os.system('clear')
	os.system('stty echo')
	exit()
