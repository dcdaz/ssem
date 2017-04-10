#!/usr/bin/python3
#Common configs for SSEM
# (c) Daniel Córdova A. <danesc87@gmail.com>, GPL v2
import os
import configparser

CONFIGDIR = os.path.expanduser('~/.config/ssem/')
GENERALCONFIGDIR = os.path.abspath('/etc/')
CONFIGFILE = 'ssem.conf'

if not os.path.exists(CONFIGDIR):
    try:
        os.makedirs(CONFIGDIR)
    except OSError:
        pass

config_reader = configparser.RawConfigParser()
ssem_config_file = os.path.join(CONFIGDIR, CONFIGFILE)
if not os.path.exists(ssem_config_file):
    ssem_config_file = os.path.join(GENERALCONFIGDIR, CONFIGFILE)
config_reader.read(ssem_config_file)