#!/usr/bin/python3
# Archivo para conector con la base de datos sqlite3
# (c) Daniel Córdova A. <danesc87@gmail.com>, GPL v2

import argparse
import DBConnection
import ConnectorService

script_to_execute = None
scriptID = None
execTime = None
args = None

def argumentsForParse():
    parser = argparse.ArgumentParser(description='Arguments for SSEM')
    parser.add_argument('--remotehost','-r', nargs='*', help='Connetion to remote host')
    parser.add_argument('--remoteexecute','-x',nargs='*', help='Execute command on remote host')
    parser.add_argument('--addscript','-a',nargs=2, help='Add script to data base')
    parser.add_argument('--deletescript','-d', help='Delete script to data base')
    return parser.parse_args()

def executionTime(argsObject, parameterNumber):
    timeForExecution = None
    if len(argsObject) < parameterNumber:
        timeForExecution = 0
    else:
        timeForExecution = argsObject[parameterNumber-1]
    return int(timeForExecution)

def printListOfScripts(scriptList):
    for i in scriptList:
        print(i)

args = argumentsForParse()
if args.remotehost:
    # print(list(DBConnection.show_all_scripts()))
    printListOfScripts(DBConnection.show_all_scripts())
    execTime = executionTime(args.remotehost, 2)
    scriptID = input('Seleccione el ID del script a ejecutar: ')
    script_to_execute = DBConnection.select_script(scriptID)[0][0]
    ConnectorService.connectionToServer(args.remotehost[0], script_to_execute, execTime)
elif args.remoteexecute:
    execTime = executionTime(args.remoteexecute, 3)
    ConnectorService.connectionToServer(args.remoteexecute[0], args.remoteexecute[1], execTime)
elif args.addscript:
    DBConnection.insert_on_DB(args.addscript[0], args.addscript[1])
elif args.deletescript:
    DBConnection.delete_from_DB(args.deletescript)
