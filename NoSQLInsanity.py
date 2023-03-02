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

urllib3.disable_warnings()

class NoSQLInsanity(object):
    def __init__(self, url, platform):
      self.url = url
      self.platform = platform
      self.reqMethod = ""
      self.attackType = ""
      self.arrAttackTypes = ["DB Attacks (Exfiltrate)"]
      self.typeParam = ""
      self.params = list('')
      self.param = ""

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
      print('''\n=================\n[Attack type]\n\n1) DB Attacks (Exfiltrate)\n''')
      self.attackType = input("Choose Attack Type >>")
      return self.attackType

    def methodMenu(self):
      print(self.info())
      print('''\n=================\n[Method]\n\n1) Send Request as GET\n2) Send Request as POST\n''')
      self.reqMethod = input("Choose Request Method >>")
      return self.reqMethod
    
    def info(self):
      attackType = ""
      if self.attackType != "":
        attackType = "Attack Type : " + self.arrAttackTypes[int(self.attackType) - 1]
        
      banner = """\n================\nTarget      : %s\nPlatform    : %s\n%s """ % (self.url, self.platform, attackType)
      return banner

    # def request(self):
    #   payload='{"username": {"$eq": "%s"}, "password": {"$regex": "^%s" }}' % (username, password + c)
    #   # payload = '{"username": {"$eq": "admin"}, "password": {"$regex": "^2" }})'
    #   headers = {
    #     'Content-Type': 'application/json'
    #   }
    #   r = requests.request("POST", url, headers=headers, data=payload, verify = False)

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
        nsimongo.typeReqPayload(nsi)
        nsimongo.pwnGet(url)
        break
      while case('2'):
        print('foo')
        break
      while case.default:
        print('Choosen number invalid !')
        break
    # nsi.chooseMethodMenu(choosedMenu)
    # nsi.chooseMethodMenu()


  # nsi.request()