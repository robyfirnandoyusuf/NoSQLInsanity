import requests
import urllib3

urllib3.disable_warnings()

def scanMongoInj():
  print('scan mongo inj')
  
def typeReqPayload(nsi):
  print(nsi.info())
  print('''\n=================\n[Request Method]\n\n1) Send Request as GET\n2) Send Request as POST\n''')
  nsi.reqMethod = input("Choose Request Method >>")
  return nsi.reqMethod
  
def paramMenu(nsi):
  print(nsi.info())
  print('''\n=================\n[Configuration Parameter]\n\n1) Default Payload\n2) Custom Payload\n''')
  nsi.typeParam = input("Choose One >>")
  nsi.params = input("Input Param >>")
  return nsi.typeParam