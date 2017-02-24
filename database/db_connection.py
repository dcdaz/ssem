#!/usr/bin/python3
# File to connect with sqlite3 database
# (c) Daniel Córdova A. <danesc87@gmail.com>, GPL v2

import sqlite3

class DataBaseConnector(object):
    '''Class that allows connection to sqlite3 database and do inserts, show all scripts, select some script by id
    and delete some script by id'''
    def __init__(self):
        self.connection_to_database = sqlite3.connect('ssemDB')
        self.connector_cursor = self.connection_to_database.cursor()

    def close_connection_to_database(self):
        self.connector_cursor.close()
        self.connection_to_database.close()

    def insert_on_database(self, script_itself, script_description):
        script_id = None
        script_id = self.connector_cursor.execute('SELECT MAX(ID) FROM SCRIPTS_TABLE')
        script_id = int(script_id.fetchone()[0]) + 1
        insert_on_database = self.connector_cursor.execute('INSERT INTO SCRIPTS_TABLE (ID, DESCRIPTION, SCRIPT) VALUES (?,?,?)', (int(script_id), script_description, script_itself))
        self.connection_to_database.commit()
        self.close_connection_to_database()

    def show_all_scripts(self):
        select_from_database = self.connector_cursor.execute('SELECT * FROM SCRIPTS_TABLE')
        select_from_database = select_from_database.fetchall()
        self.close_connection_to_database()
        return select_from_database

    def select_script(self, script_id):
        select_from_database = self.connector_cursor.execute('SELECT SCRIPT FROM SCRIPTS_TABLE WHERE ID=?', (int(script_id),))
        select_from_database = select_from_database.fetchall()
        self.close_connection_to_database()
        return select_from_database

    def delete_from_database(self, script_id):
        delete_from_database = self.connector_cursor.execute('DELETE FROM SCRIPTS_TABLE WHERE ID=?', (int(script_id),))
        self.connection_to_database.commit()
        self.close_connection_to_database()

