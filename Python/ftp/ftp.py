#coding:utf-8

#--------------------------------------
# Imports
#--------------------------------------

from modules.Connector import Connector
from modules.Parser import Parser
from modules.Config import Config

#--------------------------------------
# Default dev settings
#--------------------------------------

debug = True

#--------------------------------------
# Connector
#--------------------------------------

con = Connector()
con.debug = False
con.attempt()

#--------------------------------------
# Interpreter
# --------------------------------------

prs = Parser(con.ftp)
prs.debug = debug
prs.watch()

