#coding:utf-8

#--------------------------------------
# Imports
#--------------------------------------

import os
from modules.Connector import Connector
from modules.Parser import Parser
from modules.Config import Config

#--------------------------------------
# Default dev settings
#--------------------------------------

debug = False

#--------------------------------------
# Connector
#--------------------------------------

con = Connector()
con.debug = False
con.attempt()

con.ftp.chome = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
con.ftp.debug = debug

#--------------------------------------
# Interpreter
# --------------------------------------

prs = Parser(con.ftp)
prs.debug = debug
prs.watch()

