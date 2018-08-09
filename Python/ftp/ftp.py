#coding:utf-8

#--------------------------------------
# Imports
#--------------------------------------

from modules.Connector import Connector
from modules.Parser import Parser

#--------------------------------------
# Default dev settings
#--------------------------------------

debug = True

#--------------------------------------
# Connector
#--------------------------------------

con = Connector()
con.debug = debug
con.attempt()

#--------------------------------------
# Interpreter
# --------------------------------------

prs = Parser(con.ftp, con.address, con.user)
prs.debug = debug
prs.watch()
