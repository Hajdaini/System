#coding:utf-8

import shlex

s = input("Command: ")
s = shlex.split(s)
print(s)
