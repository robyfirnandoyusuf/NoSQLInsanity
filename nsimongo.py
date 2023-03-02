import requests
import urllib3
import urllib
from _helper import *

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
  while nsi.param != 'd':
    print('press "d" for submit the param')
    nsi.param = input("Input Param >>")
    
    if (nsi.param != 'd'):
      nsi.params.append(nsi.param)
  return nsi.typeParam

def getResponseBodyHandlingErrors(req):
    try:
        responseBody = urllib3.urlopen(req).read()
    except urllib3.HTTPError as err:
        responseBody = err.read()
    
    return responseBody

def pwnGet(url):
  print("Checking to see if site at " +str(url).strip() + " is up...")
  tester = WebAppTester(url)
  if tester.is_up():
      print("Web application is up. Starting injection test !")
  else:
      print("Web application is down")
  return 0