#!/usr/bin/python3
# Archivo para conectar con la base de datos sqlite3
# (c) Daniel Córdova A. <danesc87@gmail.com>, GPL v2

import sqlite3

def insert_on_DB(scriptForTable, description):
	connectionDB = sqlite3.connect('ssemDB')
	connectorToDB = connectionDB.cursor()
	idNumber = None
	idNumber = connectorToDB.execute('SELECT MAX(ID) FROM SCRIPTS_TABLE')
	idNumber = int(idNumber.fetchone()[0]) + 1
	inserOnTable = connectorToDB.execute('INSERT INTO SCRIPTS_TABLE (ID, DESCRIPTION, SCRIPT) VALUES (?,?,?)', (int(idNumber), description, scriptForTable))
	connectionDB.commit()
	connectorToDB.close()
	connectionDB.close()

def show_all_scripts():
	connectionDB = sqlite3.connect('ssemDB')
	connectorToDB = connectionDB.cursor()
	selectFromDB = connectorToDB.execute('SELECT * FROM SCRIPTS_TABLE')
	selectFromDB = selectFromDB.fetchall()
	connectorToDB.close()
	connectionDB.close()
	return selectFromDB

def select_script(idNumber):
	connectionDB = sqlite3.connect('ssemDB')
	connectorToDB = connectionDB.cursor()
	selectFromDB = connectorToDB.execute('SELECT SCRIPT FROM SCRIPTS_TABLE WHERE ID=?',(int(idNumber),))
	selectFromDB = selectFromDB.fetchall()
	connectorToDB.close()
	connectionDB.close()
	return selectFromDB

def delete_from_DB(idNumber):
	connectionDB = sqlite3.connect('ssemDB')
	connectorToDB = connectionDB.cursor()
	delete_from_DB = connectorToDB.execute('DELETE FROM SCRIPTS_TABLE WHERE ID=?',(int(idNumber),))
	connectionDB.commit()
	connectorToDB.close()
	connectionDB.close()
