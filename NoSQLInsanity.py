"""NoSQLInsanity: Tool for Security Assesment NSQL"""
# This research for final year project

__author__      = "Roby Firnando Yusuf aka greycat"
__copyright__   = "Copyright 2022"

# import requests
# import string
# import urllib
# import json
from json.tool import main
import urllib3
import argparse
import nsimongo
from _helper import *
from termcolor import colored

urllib3.disable_warnings()

class NoSQLInsanity(object):
    def __init__(self, url, platform):
      self.url = url
      self.platform = platform
      self.reqMethod = ""
      self.alg = ""
      self.attackType = ""
      self.arrAttackTypes = ["DB Attacks (Exfiltrate)"]
      self.typeParam = ""
      self.params = list('')
      self.param = ""
      self.successIdentifier = ""

    def banner(self):
      print('''
                _                        
               \`*-.                    
                )  _`-.                 
               .  : `. .                
               : _   '  \               
               ; *` _.   `*-._          
               `-.-'          `-.       
                 ;       `       `.     
                 :.       .        \    
                 . \  .   :   .-'   .   
                 '  `+.;  ;  '      :   
                 :  '  |    ;       ;-. 
                 ; '   : :`-:     _.`* ;
[NoSQLInsanity] .*' /  .*' ; .*`- +'  `*' 
              `*-*   `*-*  `*-*' [By: greycat - 0x3a3a3a@gmail.com]
      ''')

    def mainMenu(self):
      print(self.info())
      print(colored(f"\n=================\n[Attack type]\n\n1) DB Attacks (Exfiltrate)\n", "yellow"))
      self.attackType = input("Choose Attack Type >>")
      return self.attackType

    def methodMenu(self):
      print(self.info())
      print(colored(f"\n=================\n[Method]\n\n1) Send Request as GET\n2) Send Request as POST\n", "yellow"))
      self.reqMethod = input("Choose Request Method >>")
      return self.reqMethod
    
    def info(self):
      attackType = ""
      if self.attackType != "":
        attackType = "Attack Type : " + self.arrAttackTypes[int(self.attackType) - 1]
        
      banner = """\n================\nTarget      : %s\nPlatform    : %s\n%s """ % (self.url, self.platform, attackType)
      return banner

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='NoSQLInsanity: Tool for Security Assesment NSQL')
  parser.add_argument('--url', type=str, required=True)
  parser.add_argument('--platform', type=str, required=True)
  args = parser.parse_args()
  url = args.url
  platform = args.platform

  nsi = NoSQLInsanity(url, platform)
  nsi.banner()
  
  if platform == 'mongodb':
    
    mainMenu = nsi.mainMenu()
    # choosedMenu = nsi.chooseMainMenu(mainMenu)
    with Switch(mainMenu) as case:
      while case('1'):
        choosedParam = nsimongo.paramMenu(nsi)
        # print('ok' + '\n'.join(map(str, nsi.params)))
        httpMethod = nsimongo.typeReqPayload(nsi)
        alg = nsimongo.algMenu(nsi)
        nsimongo.checkWeb(url)
        resArr = nsimongo.vulnTest(nsi=nsi)
        
        for item in resArr:
            if True in item.values():
              # print("True exists in the array" + str(item))
              print("Injecting .. ")
              break
        else:
          print("Not vulnerable !")
          exit(0)
        
        if (alg == '1'):
          # if (httpMethod == '1') :#GET
          #   nsimongo.slinearGet(nsi)
          # else:
            nsimongo.slinear(nsi)
        else:
          nsimongo.sbin(nsi)
        # params = nsimongo.requestBuilder(nsi=nsi, isExploiting=True)
        break
      while case('2'):
        print('foo')
        break
      while case.default:
        print('Choosen number invalid !')
        break

# !TODO: Menu "Configuration param" supposed to be: 
# 1. Dump rows by param
# 2. Dump by known value
#refs: 
# https://github.com/eversinc33/Papaya/blob/875a1585f8f0776963c8b004597e7290b530b11c/papaya.py#L121
# https://github.com/Hex27/mongomap/tree/d16cee2e0b2b2af3c3a34e4f1a21f66cc7dacafe/tests